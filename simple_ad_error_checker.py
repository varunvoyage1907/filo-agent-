"""
Simple Facebook Ads Error Checker
Checks for ad errors in ad sets using direct API calls.
"""
import json
import logging
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from facebook_ads_api import FacebookAdsAPI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_ad_errors():
    """Check for ad errors in all ad sets."""
    
    print("\n" + "="*80)
    print("FACEBOOK ADS ERROR CHECKER")
    print("="*80)
    
    try:
        # Initialize API client
        from config import FacebookConfig
        config = FacebookConfig()
        api = FacebookAdsAPI(config)
        
        print(f"Checking ad account: {config.ad_account_id}")
        print(f"API Version: {config.api_version}")
        print()
        
        # Test connection first
        print("Testing API connection...")
        connection_test = api.test_connection()
        
        if connection_test.get('status') == 'error':
            print(f"❌ API Connection Failed: {connection_test.get('error')}")
            print("\nPossible solutions:")
            print("1. Check your Facebook access token")
            print("2. Verify your .env file has correct credentials")
            print("3. Ensure your token has proper permissions")
            return
        
        print("✅ API Connection Successful")
        if 'user_info' in connection_test:
            user_info = connection_test['user_info']
            print(f"   Connected as: {user_info.get('name', 'Unknown')} ({user_info.get('id', 'Unknown')})")
        
        if 'ad_account_info' in connection_test:
            account_info = connection_test['ad_account_info']
            print(f"   Ad Account: {account_info.get('name', 'Unknown')} ({account_info.get('status', 'Unknown')})")
        print()
        
        # Get campaigns
        print("Fetching campaigns...")
        campaigns = api.get_campaigns()
        print(f"Found {len(campaigns)} campaigns")
        
        total_issues = 0
        
        for campaign in campaigns:
            print(f"\n📊 Campaign: {campaign['name']} (ID: {campaign['id']})")
            print(f"   Status: {campaign['status']}")
            
            campaign_issues = []
            
            # Check campaign status
            if campaign['status'] == 'PAUSED':
                campaign_issues.append("⚠️  Campaign is paused")
            elif campaign['status'] != 'ACTIVE':
                campaign_issues.append(f"❌ Campaign status is {campaign['status']}")
            
            # Get ad sets for this campaign
            try:
                adsets = api.get_ad_sets(campaign['id'])
                print(f"   Ad Sets: {len(adsets)}")
                
                if not adsets:
                    campaign_issues.append("❌ No ad sets in campaign")
                
                for adset in adsets:
                    adset_issues = check_adset_errors(api, adset)
                    if adset_issues:
                        print(f"\n   🔍 Ad Set: {adset['name']} (ID: {adset['id']})")
                        for issue in adset_issues:
                            print(f"      {issue}")
                        total_issues += len(adset_issues)
                
            except Exception as e:
                campaign_issues.append(f"❌ Error fetching ad sets: {str(e)}")
            
            # Print campaign issues
            if campaign_issues:
                for issue in campaign_issues:
                    print(f"   {issue}")
                total_issues += len(campaign_issues)
        
        print(f"\n" + "="*80)
        print(f"SUMMARY: Found {total_issues} total issues")
        
        if total_issues == 0:
            print("✅ No critical issues found in your ad account!")
        else:
            print("🔧 Review the issues above and take appropriate action.")
        
        print("="*80)
        
    except Exception as e:
        print(f"❌ Error running ad error checker: {e}")
        logger.error(f"Error in check_ad_errors: {e}")

def check_adset_errors(api: FacebookAdsAPI, adset: Dict[str, Any]) -> List[str]:
    """Check for errors in a specific ad set."""
    issues = []
    
    # Check ad set status
    if adset['status'] == 'PAUSED':
        issues.append("⚠️  Ad set is paused")
    elif adset['status'] != 'ACTIVE':
        issues.append(f"❌ Ad set status is {adset['status']}")
    
    # Check budget
    daily_budget = adset.get('daily_budget')
    lifetime_budget = adset.get('lifetime_budget')
    
    if not daily_budget and not lifetime_budget:
        issues.append("❌ No budget set (neither daily nor lifetime)")
    elif daily_budget and float(daily_budget) < 100:  # Less than $1 USD equivalent
        issues.append(f"⚠️  Very low daily budget: ${float(daily_budget)/100:.2f}")
    
    # Check for ads in the ad set
    try:
        ads = api.get_ads(adset['id'])
        if not ads:
            issues.append("❌ No ads in ad set")
        else:
            active_ads = [ad for ad in ads if ad.get('status') == 'ACTIVE']
            if not active_ads:
                issues.append("❌ No active ads in ad set")
            
            # Check for disapproved ads
            for ad in ads:
                if ad.get('status') == 'DISAPPROVED':
                    issues.append(f"❌ Ad '{ad['name']}' is disapproved")
                elif ad.get('status') == 'PAUSED':
                    issues.append(f"⚠️  Ad '{ad['name']}' is paused")
    
    except Exception as e:
        issues.append(f"❌ Error checking ads: {str(e)}")
    
    return issues

def check_specific_adset(adset_id: str):
    """Check a specific ad set for detailed errors."""
    
    print(f"\n🔍 DETAILED AD SET ANALYSIS")
    print(f"Ad Set ID: {adset_id}")
    print("="*50)
    
    try:
        from config import FacebookConfig
        config = FacebookConfig()
        api = FacebookAdsAPI(config)
        
        # Get detailed ad set information
        adset_data = api._make_request('GET', adset_id, {
            'fields': 'id,name,status,effective_status,daily_budget,lifetime_budget,start_time,end_time,targeting,optimization_goal,bid_strategy'
        })
        
        if 'error' in adset_data:
            print(f"❌ Error fetching ad set: {adset_data['error'].get('message', 'Unknown error')}")
            return
        
        print(f"Name: {adset_data.get('name', 'Unknown')}")
        print(f"Status: {adset_data.get('status', 'Unknown')}")
        print(f"Effective Status: {adset_data.get('effective_status', 'Unknown')}")
        print(f"Daily Budget: ${float(adset_data.get('daily_budget', 0))/100:.2f}" if adset_data.get('daily_budget') else "No daily budget")
        print(f"Lifetime Budget: ${float(adset_data.get('lifetime_budget', 0))/100:.2f}" if adset_data.get('lifetime_budget') else "No lifetime budget")
        print()
        
        # Check for issues
        issues = []
        
        if adset_data.get('status') == 'PAUSED':
            issues.append("⚠️  Ad set is manually paused")
        
        effective_status = adset_data.get('effective_status')
        if effective_status and effective_status != 'ACTIVE':
            issues.append(f"❌ Effective status is {effective_status} (not ACTIVE)")
        
        # Check ads
        ads_data = api._make_request('GET', f'{adset_id}/ads', {
            'fields': 'id,name,status,effective_status'
        })
        
        if 'error' not in ads_data:
            ads = ads_data.get('data', [])
            print(f"Ads in ad set: {len(ads)}")
            
            if not ads:
                issues.append("❌ No ads in ad set")
            else:
                for ad in ads:
                    print(f"  - {ad.get('name', 'Unknown')}: {ad.get('status', 'Unknown')}")
                    if ad.get('status') == 'DISAPPROVED':
                        issues.append(f"❌ Ad '{ad.get('name')}' is disapproved")
        
        # Check recent performance
        insights_data = api._make_request('GET', f'{adset_id}/insights', {
            'fields': 'spend,impressions,clicks,reach',
            'date_preset': 'yesterday'
        })
        
        if 'error' not in insights_data:
            insights = insights_data.get('data', [])
            if insights:
                insight = insights[0]
                spend = float(insight.get('spend', 0))
                impressions = int(insight.get('impressions', 0))
                print(f"\nYesterday's Performance:")
                print(f"  Spend: ${spend:.2f}")
                print(f"  Impressions: {impressions:,}")
                
                if spend == 0 and impressions == 0:
                    issues.append("❌ No delivery yesterday (0 spend, 0 impressions)")
            else:
                print("\nNo performance data available for yesterday")
        
        print(f"\n{'='*50}")
        if issues:
            print("ISSUES FOUND:")
            for issue in issues:
                print(f"  {issue}")
        else:
            print("✅ No issues found with this ad set!")
        
    except Exception as e:
        print(f"❌ Error analyzing ad set: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Check specific ad set
        adset_id = sys.argv[1]
        check_specific_adset(adset_id)
    else:
        # Check all ad sets
        check_ad_errors()