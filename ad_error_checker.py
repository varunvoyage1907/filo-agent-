"""
Facebook Ads Error Checker
Comprehensive tool to check for ad errors in ad sets and provide solutions.
"""
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from facebook_ads_api import FacebookAdsAPI
from config import FacebookConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdErrorChecker:
    """Comprehensive ad error checker for Facebook Ads."""
    
    def __init__(self, config: Optional[FacebookConfig] = None):
        """Initialize the ad error checker."""
        self.config = config or FacebookConfig()
        self.api = FacebookAdsAPI(self.config)
        
    def check_all_ad_errors(self, ad_account_id: str = None) -> Dict[str, Any]:
        """
        Check for errors across all campaigns, ad sets, and ads.
        
        Args:
            ad_account_id: Ad account ID to check. Uses config default if None.
            
        Returns:
            Comprehensive error report with solutions.
        """
        account_id = ad_account_id or self.config.ad_account_id
        if not account_id:
            raise ValueError("No ad account ID provided")
            
        logger.info(f"Starting comprehensive ad error check for account {account_id}")
        
        error_report = {
            'account_id': account_id,
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_campaigns': 0,
                'total_adsets': 0,
                'total_ads': 0,
                'campaigns_with_errors': 0,
                'adsets_with_errors': 0,
                'ads_with_errors': 0,
                'critical_issues': 0,
                'warnings': 0
            },
            'campaigns': [],
            'critical_issues': [],
            'warnings': [],
            'recommendations': []
        }
        
        try:
            # First, test API connection
            connection_test = self.api.test_connection()
            if connection_test.get('status') == 'error':
                error_report['critical_issues'].append({
                    'type': 'API_CONNECTION_ERROR',
                    'message': f"Cannot connect to Facebook API: {connection_test.get('error')}",
                    'solution': "Check your access token and API credentials"
                })
                return error_report
            
            # Get all campaigns
            campaigns = self.api.get_campaigns(account_id)
            error_report['summary']['total_campaigns'] = len(campaigns)
            
            for campaign in campaigns:
                campaign_report = self._check_campaign_errors(campaign)
                error_report['campaigns'].append(campaign_report)
                
                if campaign_report['has_errors']:
                    error_report['summary']['campaigns_with_errors'] += 1
                
                # Check ad sets in this campaign
                adsets = self.api.get_ad_sets(campaign['id'])
                error_report['summary']['total_adsets'] += len(adsets)
                
                for adset in adsets:
                    adset_report = self._check_adset_errors(adset, campaign)
                    campaign_report['adsets'].append(adset_report)
                    
                    if adset_report['has_errors']:
                        error_report['summary']['adsets_with_errors'] += 1
                    
                    # Check ads in this ad set
                    ads = self.api.get_ads(adset['id'])
                    error_report['summary']['total_ads'] += len(ads)
                    
                    for ad in ads:
                        ad_report = self._check_ad_errors(ad, adset, campaign)
                        adset_report['ads'].append(ad_report)
                        
                        if ad_report['has_errors']:
                            error_report['summary']['ads_with_errors'] += 1
            
            # Compile critical issues and warnings
            self._compile_issues(error_report)
            
            # Generate recommendations
            self._generate_recommendations(error_report)
            
            logger.info("Ad error check completed successfully")
            return error_report
            
        except Exception as e:
            logger.error(f"Error during ad error check: {e}")
            error_report['critical_issues'].append({
                'type': 'SYSTEM_ERROR',
                'message': f"System error during check: {str(e)}",
                'solution': "Contact support or check system logs"
            })
            return error_report
    
    def _check_campaign_errors(self, campaign: Dict[str, Any]) -> Dict[str, Any]:
        """Check for errors in a specific campaign."""
        campaign_report = {
            'id': campaign['id'],
            'name': campaign['name'],
            'status': campaign['status'],
            'has_errors': False,
            'errors': [],
            'warnings': [],
            'adsets': []
        }
        
        # Check campaign status issues
        if campaign['status'] == 'PAUSED':
            campaign_report['warnings'].append({
                'type': 'CAMPAIGN_PAUSED',
                'message': f"Campaign '{campaign['name']}' is paused",
                'solution': "Review and activate campaign if needed"
            })
            campaign_report['has_errors'] = True
        
        # Check for missing objectives or other issues
        if not campaign.get('objective'):
            campaign_report['errors'].append({
                'type': 'MISSING_OBJECTIVE',
                'message': "Campaign has no objective set",
                'solution': "Set a clear campaign objective"
            })
            campaign_report['has_errors'] = True
        
        return campaign_report
    
    def _check_adset_errors(self, adset: Dict[str, Any], campaign: Dict[str, Any]) -> Dict[str, Any]:
        """Check for errors in a specific ad set."""
        adset_report = {
            'id': adset['id'],
            'name': adset['name'],
            'status': adset['status'],
            'has_errors': False,
            'errors': [],
            'warnings': [],
            'ads': []
        }
        
        # Check ad set status
        if adset['status'] == 'PAUSED':
            adset_report['warnings'].append({
                'type': 'ADSET_PAUSED',
                'message': f"Ad set '{adset['name']}' is paused",
                'solution': "Review and activate ad set if needed"
            })
            adset_report['has_errors'] = True
        
        # Check budget issues
        daily_budget = adset.get('daily_budget')
        if daily_budget and float(daily_budget) < 100:  # Less than $1 USD equivalent
            adset_report['warnings'].append({
                'type': 'LOW_BUDGET',
                'message': f"Ad set has very low daily budget: {daily_budget}",
                'solution': "Consider increasing budget for better delivery"
            })
            adset_report['has_errors'] = True
        
        # Check for missing budget
        if not daily_budget and not adset.get('lifetime_budget'):
            adset_report['errors'].append({
                'type': 'NO_BUDGET',
                'message': "Ad set has no budget set",
                'solution': "Set either daily or lifetime budget"
            })
            adset_report['has_errors'] = True
        
        return adset_report
    
    def _check_ad_errors(self, ad: Dict[str, Any], adset: Dict[str, Any], campaign: Dict[str, Any]) -> Dict[str, Any]:
        """Check for errors in a specific ad."""
        ad_report = {
            'id': ad['id'],
            'name': ad['name'],
            'status': ad['status'],
            'has_errors': False,
            'errors': [],
            'warnings': []
        }
        
        # Check ad status
        if ad['status'] == 'PAUSED':
            ad_report['warnings'].append({
                'type': 'AD_PAUSED',
                'message': f"Ad '{ad['name']}' is paused",
                'solution': "Review and activate ad if needed"
            })
            ad_report['has_errors'] = True
        elif ad['status'] == 'DISAPPROVED':
            ad_report['errors'].append({
                'type': 'AD_DISAPPROVED',
                'message': f"Ad '{ad['name']}' has been disapproved",
                'solution': "Review ad content and Facebook policies, then resubmit"
            })
            ad_report['has_errors'] = True
        
        return ad_report
    
    def _compile_issues(self, error_report: Dict[str, Any]):
        """Compile all critical issues and warnings from the report."""
        for campaign in error_report['campaigns']:
            for error in campaign['errors']:
                error_report['critical_issues'].append({
                    'campaign': campaign['name'],
                    'type': error['type'],
                    'message': error['message'],
                    'solution': error['solution']
                })
            
            for warning in campaign['warnings']:
                error_report['warnings'].append({
                    'campaign': campaign['name'],
                    'type': warning['type'],
                    'message': warning['message'],
                    'solution': warning['solution']
                })
            
            for adset in campaign['adsets']:
                for error in adset['errors']:
                    error_report['critical_issues'].append({
                        'campaign': campaign['name'],
                        'adset': adset['name'],
                        'type': error['type'],
                        'message': error['message'],
                        'solution': error['solution']
                    })
                
                for warning in adset['warnings']:
                    error_report['warnings'].append({
                        'campaign': campaign['name'],
                        'adset': adset['name'],
                        'type': warning['type'],
                        'message': warning['message'],
                        'solution': warning['solution']
                    })
                
                for ad in adset['ads']:
                    for error in ad['errors']:
                        error_report['critical_issues'].append({
                            'campaign': campaign['name'],
                            'adset': adset['name'],
                            'ad': ad['name'],
                            'type': error['type'],
                            'message': error['message'],
                            'solution': error['solution']
                        })
                    
                    for warning in ad['warnings']:
                        error_report['warnings'].append({
                            'campaign': campaign['name'],
                            'adset': adset['name'],
                            'ad': ad['name'],
                            'type': warning['type'],
                            'message': warning['message'],
                            'solution': warning['solution']
                        })
        
        error_report['summary']['critical_issues'] = len(error_report['critical_issues'])
        error_report['summary']['warnings'] = len(error_report['warnings'])
    
    def _generate_recommendations(self, error_report: Dict[str, Any]):
        """Generate actionable recommendations based on found issues."""
        recommendations = []
        
        # API connection issues
        if any(issue['type'] == 'API_CONNECTION_ERROR' for issue in error_report['critical_issues']):
            recommendations.append({
                'priority': 'CRITICAL',
                'action': 'Fix API Connection',
                'description': 'Resolve Facebook API connection issues before proceeding',
                'steps': [
                    '1. Check your Facebook access token',
                    '2. Verify API credentials in config',
                    '3. Ensure proper permissions are granted',
                    '4. Test connection using test_connection() method'
                ]
            })
        
        # Budget issues
        budget_issues = [issue for issue in error_report['critical_issues'] + error_report['warnings'] 
                        if issue['type'] in ['NO_BUDGET', 'LOW_BUDGET']]
        if budget_issues:
            recommendations.append({
                'priority': 'HIGH',
                'action': 'Review Budget Settings',
                'description': f'Found {len(budget_issues)} budget-related issues',
                'steps': [
                    '1. Review ad sets with missing or low budgets',
                    '2. Set appropriate daily or lifetime budgets',
                    '3. Consider account spending limits',
                    '4. Monitor budget utilization'
                ]
            })
        
        # Status issues
        paused_items = [issue for issue in error_report['warnings'] 
                       if issue['type'] in ['CAMPAIGN_PAUSED', 'ADSET_PAUSED', 'AD_PAUSED']]
        if paused_items:
            recommendations.append({
                'priority': 'MEDIUM',
                'action': 'Review Paused Items',
                'description': f'Found {len(paused_items)} paused campaigns/ad sets/ads',
                'steps': [
                    '1. Review why items were paused',
                    '2. Activate high-performing items',
                    '3. Optimize underperforming items before reactivating',
                    '4. Set up monitoring for future issues'
                ]
            })
        
        # Disapproved ads
        disapproved_ads = [issue for issue in error_report['critical_issues'] 
                          if issue['type'] == 'AD_DISAPPROVED']
        if disapproved_ads:
            recommendations.append({
                'priority': 'HIGH',
                'action': 'Fix Disapproved Ads',
                'description': f'Found {len(disapproved_ads)} disapproved ads',
                'steps': [
                    '1. Review Facebook ad policies',
                    '2. Modify ad content to comply with policies',
                    '3. Resubmit ads for review',
                    '4. Monitor approval status'
                ]
            })
        
        error_report['recommendations'] = recommendations
    
    def check_specific_adset(self, adset_id: str) -> Dict[str, Any]:
        """
        Perform detailed error check on a specific ad set.
        
        Args:
            adset_id: The ad set ID to check
            
        Returns:
            Detailed error report for the ad set
        """
        logger.info(f"Checking specific ad set: {adset_id}")
        
        try:
            # Get ad set details with extended fields
            adset_data = self.api._make_request('GET', adset_id, {
                'fields': 'id,name,status,effective_status,configured_status,daily_budget,lifetime_budget,start_time,end_time,targeting,optimization_goal,bid_strategy,issues_info,delivery_info'
            })
            
            if 'error' in adset_data:
                return {
                    'adset_id': adset_id,
                    'error': adset_data['error'],
                    'status': 'API_ERROR'
                }
            
            # Get ads in this ad set
            ads_data = self.api._make_request('GET', f'{adset_id}/ads', {
                'fields': 'id,name,status,effective_status,configured_status,issues_info,delivery_info'
            })
            
            # Get recent insights
            insights_data = self.api._make_request('GET', f'{adset_id}/insights', {
                'fields': 'spend,impressions,clicks,reach,frequency',
                'date_preset': 'yesterday'
            })
            
            report = {
                'adset_id': adset_id,
                'adset_details': adset_data,
                'ads': ads_data.get('data', []) if 'error' not in ads_data else [],
                'insights': insights_data.get('data', []) if 'error' not in insights_data else [],
                'diagnosis': self._diagnose_adset_issues(adset_data, ads_data, insights_data),
                'timestamp': datetime.now().isoformat()
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error checking ad set {adset_id}: {e}")
            return {
                'adset_id': adset_id,
                'error': str(e),
                'status': 'SYSTEM_ERROR'
            }
    
    def _diagnose_adset_issues(self, adset_data: Dict, ads_data: Dict, insights_data: Dict) -> Dict[str, Any]:
        """Diagnose specific issues with an ad set."""
        diagnosis = {
            'status': 'OK',
            'issues': [],
            'recommendations': []
        }
        
        # Check if API calls failed
        if 'error' in adset_data:
            diagnosis['issues'].append({
                'type': 'API_ERROR',
                'severity': 'CRITICAL',
                'message': f"Cannot fetch ad set data: {adset_data['error'].get('message', 'Unknown error')}",
                'solution': 'Check API permissions and ad set ID'
            })
            diagnosis['status'] = 'ERROR'
            return diagnosis
        
        # Check ad set status
        status = adset_data.get('status')
        effective_status = adset_data.get('effective_status')
        
        if status == 'PAUSED':
            diagnosis['issues'].append({
                'type': 'ADSET_PAUSED',
                'severity': 'HIGH',
                'message': 'Ad set is manually paused',
                'solution': 'Activate the ad set if you want it to run'
            })
        
        if effective_status and effective_status != 'ACTIVE':
            diagnosis['issues'].append({
                'type': 'DELIVERY_ISSUE',
                'severity': 'HIGH',
                'message': f'Ad set effective status is {effective_status}',
                'solution': 'Check for policy violations, budget issues, or targeting problems'
            })
        
        # Check for ads
        if 'error' not in ads_data:
            ads = ads_data.get('data', [])
            if not ads:
                diagnosis['issues'].append({
                    'type': 'NO_ADS',
                    'severity': 'CRITICAL',
                    'message': 'Ad set has no ads',
                    'solution': 'Create ads in this ad set to start delivery'
                })
            else:
                # Check ad statuses
                active_ads = [ad for ad in ads if ad.get('status') == 'ACTIVE']
                if not active_ads:
                    diagnosis['issues'].append({
                        'type': 'NO_ACTIVE_ADS',
                        'severity': 'HIGH',
                        'message': 'Ad set has no active ads',
                        'solution': 'Activate at least one ad in this ad set'
                    })
        
        # Check budget
        daily_budget = adset_data.get('daily_budget')
        lifetime_budget = adset_data.get('lifetime_budget')
        
        if not daily_budget and not lifetime_budget:
            diagnosis['issues'].append({
                'type': 'NO_BUDGET',
                'severity': 'CRITICAL',
                'message': 'Ad set has no budget configured',
                'solution': 'Set either daily or lifetime budget'
            })
        elif daily_budget and float(daily_budget) < 100:  # Less than $1 USD equivalent
            diagnosis['issues'].append({
                'type': 'LOW_BUDGET',
                'severity': 'MEDIUM',
                'message': f'Daily budget is very low: {daily_budget}',
                'solution': 'Consider increasing budget for better delivery'
            })
        
        # Check insights for delivery
        if 'error' not in insights_data:
            insights = insights_data.get('data', [])
            if insights:
                insight = insights[0]
                spend = float(insight.get('spend', 0))
                impressions = int(insight.get('impressions', 0))
                
                if spend == 0 and impressions == 0:
                    diagnosis['issues'].append({
                        'type': 'NO_DELIVERY',
                        'severity': 'HIGH',
                        'message': 'Ad set had no delivery yesterday',
                        'solution': 'Check targeting, budget, and ad approval status'
                    })
        
        # Set overall status
        if any(issue['severity'] == 'CRITICAL' for issue in diagnosis['issues']):
            diagnosis['status'] = 'CRITICAL'
        elif any(issue['severity'] == 'HIGH' for issue in diagnosis['issues']):
            diagnosis['status'] = 'WARNING'
        elif diagnosis['issues']:
            diagnosis['status'] = 'MINOR_ISSUES'
        
        return diagnosis
    
    def print_error_report(self, error_report: Dict[str, Any]):
        """Print a formatted error report."""
        print("\n" + "="*80)
        print("FACEBOOK ADS ERROR REPORT")
        print("="*80)
        print(f"Account ID: {error_report['account_id']}")
        print(f"Timestamp: {error_report['timestamp']}")
        print()
        
        # Summary
        summary = error_report['summary']
        print("SUMMARY:")
        print(f"  Total Campaigns: {summary['total_campaigns']}")
        print(f"  Total Ad Sets: {summary['total_adsets']}")
        print(f"  Total Ads: {summary['total_ads']}")
        print(f"  Campaigns with Errors: {summary['campaigns_with_errors']}")
        print(f"  Ad Sets with Errors: {summary['adsets_with_errors']}")
        print(f"  Ads with Errors: {summary['ads_with_errors']}")
        print(f"  Critical Issues: {summary['critical_issues']}")
        print(f"  Warnings: {summary['warnings']}")
        print()
        
        # Critical Issues
        if error_report['critical_issues']:
            print("CRITICAL ISSUES:")
            for i, issue in enumerate(error_report['critical_issues'], 1):
                print(f"  {i}. {issue['type']}")
                print(f"     Message: {issue['message']}")
                print(f"     Solution: {issue['solution']}")
                if 'campaign' in issue:
                    print(f"     Campaign: {issue['campaign']}")
                if 'adset' in issue:
                    print(f"     Ad Set: {issue['adset']}")
                if 'ad' in issue:
                    print(f"     Ad: {issue['ad']}")
                print()
        
        # Recommendations
        if error_report['recommendations']:
            print("RECOMMENDATIONS:")
            for i, rec in enumerate(error_report['recommendations'], 1):
                print(f"  {i}. {rec['action']} (Priority: {rec['priority']})")
                print(f"     {rec['description']}")
                for step in rec['steps']:
                    print(f"     {step}")
                print()


def main():
    """Run ad error checker."""
    try:
        checker = AdErrorChecker()
        
        # Check all ads for errors
        print("Starting comprehensive ad error check...")
        error_report = checker.check_all_ad_errors()
        
        # Print the report
        checker.print_error_report(error_report)
        
        # Save report to file
        with open('ad_error_report.json', 'w') as f:
            json.dump(error_report, f, indent=2)
        print("Detailed report saved to 'ad_error_report.json'")
        
    except Exception as e:
        print(f"Error running ad error checker: {e}")
        logger.error(f"Error in main: {e}")


if __name__ == "__main__":
    main()