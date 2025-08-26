"""
Active Campaigns Analyzer
Comprehensive analysis of all active Facebook campaigns with strategic recommendations.
"""
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from facebook_ads_client import FacebookAdsClient
from financial_risk_manager import FinancialRiskManager
from strategic_memory import StrategicMemory

class ActiveCampaignsAnalyzer:
    """Analyze all active campaigns and provide strategic recommendations."""
    
    def __init__(self):
        self.client = FacebookAdsClient()
        self.risk_manager = FinancialRiskManager()
        self.strategic_memory = StrategicMemory()
        
        # Performance benchmarks for eyewear industry
        self.benchmarks = {
            "excellent_roas": 4.0,
            "good_roas": 2.5,
            "minimum_roas": 2.0,
            "excellent_ctr": 2.0,
            "good_ctr": 1.2,
            "minimum_ctr": 0.8,
            "max_cpc": 50.0,  # INR
            "max_frequency": 3.0,
            "min_quality_score": 7.0
        }
    
    def analyze_all_active_campaigns(self) -> Dict[str, Any]:
        """Comprehensive analysis of all active campaigns."""
        
        print("🔍 ANALYZING ALL ACTIVE FACEBOOK CAMPAIGNS")
        print("="*60)
        
        try:
            # Get all campaigns
            all_campaigns = self.client.get_campaigns(limit=100)
            active_campaigns = [c for c in all_campaigns if c.get('status') == 'ACTIVE']
            
            print(f"📊 Campaign Overview:")
            print(f"   • Total Campaigns: {len(all_campaigns)}")
            print(f"   • Active Campaigns: {len(active_campaigns)}")
            print(f"   • Paused/Completed: {len(all_campaigns) - len(active_campaigns)}")
            
            if not active_campaigns:
                return self._handle_no_active_campaigns()
            
            # Analyze each active campaign
            campaign_analyses = []
            total_spend = 0
            total_revenue = 0
            
            print(f"\n🎯 DETAILED CAMPAIGN ANALYSIS:")
            print("-" * 60)
            
            for i, campaign in enumerate(active_campaigns, 1):
                analysis = self._analyze_single_campaign(campaign, i)
                campaign_analyses.append(analysis)
                
                # Aggregate totals
                total_spend += analysis.get('financial_metrics', {}).get('spend', 0)
                total_revenue += analysis.get('financial_metrics', {}).get('revenue', 0)
            
            # Overall analysis
            overall_analysis = self._generate_overall_analysis(
                campaign_analyses, total_spend, total_revenue
            )
            
            # Strategic recommendations
            recommendations = self._generate_strategic_recommendations(campaign_analyses)
            
            # Priority actions
            priority_actions = self._identify_priority_actions(campaign_analyses)
            
            return {
                "summary": {
                    "total_campaigns": len(all_campaigns),
                    "active_campaigns": len(active_campaigns),
                    "total_spend": total_spend,
                    "total_revenue": total_revenue,
                    "overall_roas": total_revenue / total_spend if total_spend > 0 else 0,
                    "analysis_timestamp": datetime.now().isoformat()
                },
                "campaign_analyses": campaign_analyses,
                "overall_analysis": overall_analysis,
                "strategic_recommendations": recommendations,
                "priority_actions": priority_actions,
                "next_steps": self._generate_next_steps(campaign_analyses)
            }
            
        except Exception as e:
            print(f"❌ Error analyzing campaigns: {e}")
            return self._handle_api_error(str(e))
    
    def _analyze_single_campaign(self, campaign: Dict[str, Any], index: int) -> Dict[str, Any]:
        """Analyze a single campaign in detail."""
        
        campaign_id = campaign.get('id')
        campaign_name = campaign.get('name', 'Unnamed Campaign')
        
        print(f"\n{index}. 📈 {campaign_name}")
        print(f"   ID: {campaign_id}")
        print(f"   Objective: {campaign.get('objective', 'Unknown')}")
        print(f"   Created: {campaign.get('created_time', 'Unknown')[:10]}")
        
        try:
            # Get performance insights
            insights = self.client.get_campaign_insights(campaign_id)
            
            if insights and 'error' not in insights:
                financial_metrics = self._extract_financial_metrics(insights)
                performance_metrics = self._extract_performance_metrics(insights)
                
                # Display key metrics
                print(f"   💰 Spend: ₹{financial_metrics['spend']:,.2f}")
                print(f"   📈 Revenue: ₹{financial_metrics['revenue']:,.2f}")
                print(f"   🎯 ROAS: {financial_metrics['roas']:.2f}")
                print(f"   📊 CTR: {performance_metrics['ctr']:.2f}%")
                print(f"   💸 CPC: ₹{performance_metrics['cpc']:.2f}")
                
                # Performance assessment
                assessment = self._assess_campaign_performance(financial_metrics, performance_metrics)
                print(f"   📋 Status: {assessment['status_emoji']} {assessment['status']}")
                
                if assessment['alerts']:
                    for alert in assessment['alerts']:
                        print(f"   ⚠️  {alert}")
                
                if assessment['opportunities']:
                    for opp in assessment['opportunities']:
                        print(f"   🚀 {opp}")
                
                return {
                    "campaign_id": campaign_id,
                    "campaign_name": campaign_name,
                    "campaign_info": campaign,
                    "financial_metrics": financial_metrics,
                    "performance_metrics": performance_metrics,
                    "assessment": assessment,
                    "insights_data": insights
                }
            else:
                print(f"   ⚠️  No performance data available")
                return {
                    "campaign_id": campaign_id,
                    "campaign_name": campaign_name,
                    "campaign_info": campaign,
                    "error": "No insights data available"
                }
                
        except Exception as e:
            print(f"   ❌ Error getting insights: {str(e)[:50]}...")
            return {
                "campaign_id": campaign_id,
                "campaign_name": campaign_name,
                "campaign_info": campaign,
                "error": str(e)
            }
    
    def _extract_financial_metrics(self, insights: Dict[str, Any]) -> Dict[str, float]:
        """Extract financial metrics from insights."""
        
        spend = float(insights.get('spend', 0))
        purchase_roas = float(insights.get('purchase_roas', 0))
        revenue = spend * purchase_roas if purchase_roas > 0 else 0
        
        return {
            "spend": spend,
            "revenue": revenue,
            "roas": purchase_roas,
            "cost_per_purchase": float(insights.get('cost_per_purchase', 0)),
            "purchase_value": float(insights.get('purchase_value', 0))
        }
    
    def _extract_performance_metrics(self, insights: Dict[str, Any]) -> Dict[str, float]:
        """Extract performance metrics from insights."""
        
        return {
            "impressions": int(insights.get('impressions', 0)),
            "clicks": int(insights.get('clicks', 0)),
            "ctr": float(insights.get('ctr', 0)),
            "cpc": float(insights.get('cpc', 0)),
            "cpm": float(insights.get('cpm', 0)),
            "reach": int(insights.get('reach', 0)),
            "frequency": float(insights.get('frequency', 0))
        }
    
    def _assess_campaign_performance(self, financial: Dict[str, float], performance: Dict[str, float]) -> Dict[str, Any]:
        """Assess campaign performance against benchmarks."""
        
        roas = financial['roas']
        ctr = performance['ctr']
        cpc = performance['cpc']
        frequency = performance['frequency']
        
        alerts = []
        opportunities = []
        
        # ROAS Assessment
        if roas >= self.benchmarks["excellent_roas"]:
            status = "EXCELLENT"
            status_emoji = "🟢"
            opportunities.append(f"Scale opportunity - ROAS {roas:.2f} is excellent")
        elif roas >= self.benchmarks["good_roas"]:
            status = "GOOD"
            status_emoji = "🟡"
        elif roas >= self.benchmarks["minimum_roas"]:
            status = "ACCEPTABLE"
            status_emoji = "🟠"
            alerts.append(f"ROAS {roas:.2f} needs improvement")
        else:
            status = "CRITICAL"
            status_emoji = "🔴"
            alerts.append(f"LOW ROAS {roas:.2f} - Immediate action required")
        
        # CTR Assessment
        if ctr < self.benchmarks["minimum_ctr"]:
            alerts.append(f"Low CTR {ctr:.2f}% - Creative refresh needed")
        elif ctr >= self.benchmarks["excellent_ctr"]:
            opportunities.append(f"Excellent CTR {ctr:.2f}% - Creative performing well")
        
        # CPC Assessment
        if cpc > self.benchmarks["max_cpc"]:
            alerts.append(f"High CPC ₹{cpc:.2f} - Optimize targeting")
        
        # Frequency Assessment
        if frequency > self.benchmarks["max_frequency"]:
            alerts.append(f"High frequency {frequency:.2f} - Audience fatigue risk")
        
        return {
            "status": status,
            "status_emoji": status_emoji,
            "alerts": alerts,
            "opportunities": opportunities,
            "performance_score": self._calculate_performance_score(roas, ctr, cpc, frequency)
        }
    
    def _calculate_performance_score(self, roas: float, ctr: float, cpc: float, frequency: float) -> float:
        """Calculate overall performance score (0-100)."""
        
        score = 0
        
        # ROAS score (40% weight)
        if roas >= self.benchmarks["excellent_roas"]:
            score += 40
        elif roas >= self.benchmarks["good_roas"]:
            score += 30
        elif roas >= self.benchmarks["minimum_roas"]:
            score += 20
        else:
            score += 10
        
        # CTR score (30% weight)
        if ctr >= self.benchmarks["excellent_ctr"]:
            score += 30
        elif ctr >= self.benchmarks["good_ctr"]:
            score += 20
        elif ctr >= self.benchmarks["minimum_ctr"]:
            score += 15
        else:
            score += 5
        
        # CPC score (20% weight)
        if cpc <= self.benchmarks["max_cpc"] * 0.7:  # 30% below max
            score += 20
        elif cpc <= self.benchmarks["max_cpc"]:
            score += 15
        else:
            score += 5
        
        # Frequency score (10% weight)
        if frequency <= 2.0:
            score += 10
        elif frequency <= self.benchmarks["max_frequency"]:
            score += 7
        else:
            score += 3
        
        return min(score, 100)
    
    def _generate_overall_analysis(self, campaign_analyses: List[Dict], total_spend: float, total_revenue: float) -> Dict[str, Any]:
        """Generate overall account analysis."""
        
        valid_campaigns = [c for c in campaign_analyses if 'error' not in c]
        
        if not valid_campaigns:
            return {"error": "No valid campaign data available"}
        
        # Calculate averages
        avg_roas = sum(c['financial_metrics']['roas'] for c in valid_campaigns) / len(valid_campaigns)
        avg_ctr = sum(c['performance_metrics']['ctr'] for c in valid_campaigns) / len(valid_campaigns)
        avg_cpc = sum(c['performance_metrics']['cpc'] for c in valid_campaigns) / len(valid_campaigns)
        
        # Count performance categories
        excellent_campaigns = len([c for c in valid_campaigns if c['assessment']['status'] == 'EXCELLENT'])
        good_campaigns = len([c for c in valid_campaigns if c['assessment']['status'] == 'GOOD'])
        critical_campaigns = len([c for c in valid_campaigns if c['assessment']['status'] == 'CRITICAL'])
        
        return {
            "overall_roas": total_revenue / total_spend if total_spend > 0 else 0,
            "average_roas": avg_roas,
            "average_ctr": avg_ctr,
            "average_cpc": avg_cpc,
            "performance_distribution": {
                "excellent": excellent_campaigns,
                "good": good_campaigns,
                "critical": critical_campaigns
            },
            "total_spend": total_spend,
            "total_revenue": total_revenue,
            "net_profit": total_revenue - total_spend
        }
    
    def _generate_strategic_recommendations(self, campaign_analyses: List[Dict]) -> List[Dict[str, Any]]:
        """Generate strategic recommendations based on campaign analysis."""
        
        recommendations = []
        valid_campaigns = [c for c in campaign_analyses if 'error' not in c]
        
        if not valid_campaigns:
            return [{"type": "error", "message": "No campaign data available for recommendations"}]
        
        # Find top performers
        top_performers = sorted(valid_campaigns, 
                              key=lambda x: x['assessment']['performance_score'], 
                              reverse=True)[:3]
        
        # Find underperformers
        underperformers = [c for c in valid_campaigns if c['assessment']['status'] == 'CRITICAL']
        
        # Scaling opportunities
        scaling_candidates = [c for c in valid_campaigns if c['assessment']['status'] == 'EXCELLENT']
        
        if scaling_candidates:
            recommendations.append({
                "type": "scaling",
                "priority": "high",
                "title": "Scale Top Performing Campaigns",
                "description": f"You have {len(scaling_candidates)} excellent campaigns ready for scaling",
                "campaigns": [c['campaign_name'] for c in scaling_candidates],
                "action": "Increase budgets by 20-30% for top performers",
                "expected_impact": "25-40% revenue increase"
            })
        
        # Optimization opportunities
        if underperformers:
            recommendations.append({
                "type": "optimization",
                "priority": "critical",
                "title": "Fix Underperforming Campaigns",
                "description": f"{len(underperformers)} campaigns need immediate attention",
                "campaigns": [c['campaign_name'] for c in underperformers],
                "action": "Pause or optimize campaigns with ROAS < 2.0",
                "expected_impact": "Prevent further losses"
            })
        
        # Creative refresh opportunities
        creative_refresh_needed = [c for c in valid_campaigns 
                                 if c['performance_metrics']['ctr'] < self.benchmarks['minimum_ctr']]
        
        if creative_refresh_needed:
            recommendations.append({
                "type": "creative",
                "priority": "medium",
                "title": "Creative Refresh Required",
                "description": f"{len(creative_refresh_needed)} campaigns have low CTR",
                "campaigns": [c['campaign_name'] for c in creative_refresh_needed],
                "action": "Test new creative formats and messaging",
                "expected_impact": "15-30% CTR improvement"
            })
        
        return recommendations
    
    def _identify_priority_actions(self, campaign_analyses: List[Dict]) -> List[Dict[str, Any]]:
        """Identify immediate priority actions."""
        
        actions = []
        valid_campaigns = [c for c in campaign_analyses if 'error' not in c]
        
        # Critical actions
        for campaign in valid_campaigns:
            if campaign['assessment']['status'] == 'CRITICAL':
                actions.append({
                    "priority": "IMMEDIATE",
                    "action": "PAUSE OR OPTIMIZE",
                    "campaign": campaign['campaign_name'],
                    "reason": f"ROAS {campaign['financial_metrics']['roas']:.2f} below minimum threshold",
                    "financial_impact": f"Losing ₹{campaign['financial_metrics']['spend'] - campaign['financial_metrics']['revenue']:,.2f}"
                })
        
        # Scaling actions
        for campaign in valid_campaigns:
            if campaign['assessment']['status'] == 'EXCELLENT':
                actions.append({
                    "priority": "HIGH",
                    "action": "SCALE BUDGET",
                    "campaign": campaign['campaign_name'],
                    "reason": f"Excellent ROAS {campaign['financial_metrics']['roas']:.2f}",
                    "financial_impact": f"Potential ₹{campaign['financial_metrics']['revenue'] * 0.3:,.2f} additional revenue"
                })
        
        return actions
    
    def _generate_next_steps(self, campaign_analyses: List[Dict]) -> List[str]:
        """Generate specific next steps."""
        
        steps = [
            "1. 🔴 IMMEDIATE: Address any critical ROAS issues",
            "2. 🟡 TODAY: Review and optimize underperforming campaigns", 
            "3. 🟢 THIS WEEK: Scale top performing campaigns",
            "4. 📊 ONGOING: Monitor performance daily",
            "5. 🎨 WEEKLY: Test new creative variations"
        ]
        
        return steps
    
    def _handle_no_active_campaigns(self) -> Dict[str, Any]:
        """Handle case when no active campaigns found."""
        
        return {
            "summary": {
                "total_campaigns": 0,
                "active_campaigns": 0,
                "message": "No active campaigns found"
            },
            "recommendations": [
                {
                    "type": "launch",
                    "priority": "high",
                    "title": "Launch New Campaigns",
                    "description": "No active campaigns detected",
                    "action": "Create new campaigns for your eyewear brands",
                    "suggested_budgets": {
                        "Voyage": "₹2,000-5,000 daily",
                        "GoEye": "₹1,500-3,000 daily",
                        "Eyejack": "₹1,000-2,500 daily"
                    }
                }
            ],
            "next_steps": [
                "1. Create campaign strategy for each brand",
                "2. Set up conversion tracking",
                "3. Launch with conservative budgets",
                "4. Monitor and optimize based on performance"
            ]
        }
    
    def _handle_api_error(self, error_message: str) -> Dict[str, Any]:
        """Handle API errors gracefully."""
        
        if "expired" in error_message.lower():
            return {
                "error": "access_token_expired",
                "message": "Facebook access token has expired",
                "solution": "Please refresh your Facebook access token",
                "next_steps": [
                    "1. Go to Facebook Developer Console",
                    "2. Generate new access token",
                    "3. Update your .env file",
                    "4. Re-run the analysis"
                ]
            }
        else:
            return {
                "error": "api_error",
                "message": error_message,
                "solution": "Check Facebook API connection and permissions"
            }

def main():
    """Run active campaigns analysis."""
    
    analyzer = ActiveCampaignsAnalyzer()
    results = analyzer.analyze_all_active_campaigns()
    
    # Display results
    if "error" in results:
        print(f"\n❌ ERROR: {results['message']}")
        if "next_steps" in results:
            print(f"\n🔧 SOLUTION:")
            for step in results["next_steps"]:
                print(f"   {step}")
    else:
        print(f"\n📊 ANALYSIS COMPLETE!")
        print(f"✅ {results['summary']['active_campaigns']} active campaigns analyzed")
        print(f"💰 Total Spend: ₹{results['summary']['total_spend']:,.2f}")
        print(f"📈 Total Revenue: ₹{results['summary']['total_revenue']:,.2f}")
        print(f"🎯 Overall ROAS: {results['summary']['overall_roas']:.2f}")
        
        if results.get('strategic_recommendations'):
            print(f"\n💡 TOP RECOMMENDATIONS:")
            for rec in results['strategic_recommendations'][:3]:
                print(f"   • {rec['title']}: {rec['description']}")
        
        if results.get('priority_actions'):
            print(f"\n🚨 PRIORITY ACTIONS:")
            for action in results['priority_actions'][:3]:
                print(f"   • {action['priority']}: {action['action']} - {action['campaign']}")

if __name__ == "__main__":
    main()
