"""
Comprehensive Facebook Campaign Tracker for Real Money Decisions
Every critical attribute needed for serious advertising decisions.
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from facebook_ads_client import FacebookAdsClient
from config import FacebookConfig
import logging

# Set up logging for critical operations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComprehensiveCampaignTracker:
    """
    Complete campaign tracking system for real money Facebook advertising.
    Tracks every critical metric needed for business decisions.
    """
    
    def __init__(self, data_file: str = "comprehensive_campaign_data.json"):
        self.data_file = data_file
        self.memory = self._load_memory()
        self.client = FacebookAdsClient()
        
        # Critical thresholds for alerts
        self.critical_thresholds = {
            "max_daily_spend": 5000,  # INR
            "min_roas": 2.0,
            "max_cpc": 100,  # INR
            "min_ctr": 0.5,  # %
            "max_frequency": 3.0,
            "min_quality_score": 6.0
        }
    
    def _load_memory(self) -> Dict[str, Any]:
        """Load comprehensive campaign memory."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading memory: {e}")
                return self._create_comprehensive_memory()
        return self._create_comprehensive_memory()
    
    def _create_comprehensive_memory(self) -> Dict[str, Any]:
        """Create comprehensive memory structure with all critical attributes."""
        return {
            "campaigns": {},
            "ad_accounts": {},
            "financial_tracking": {
                "total_spend": 0.0,
                "total_revenue": 0.0,
                "overall_roas": 0.0,
                "monthly_budgets": {},
                "spend_by_brand": {},
                "profit_margins": {}
            },
            "performance_benchmarks": {
                "industry_averages": {
                    "ctr": 1.2,
                    "cpc": 45,  # INR
                    "cpm": 350,  # INR
                    "roas": 4.0,
                    "conversion_rate": 2.5
                },
                "account_benchmarks": {},
                "brand_benchmarks": {}
            },
            "risk_management": {
                "budget_alerts": [],
                "performance_alerts": [],
                "account_issues": [],
                "spending_anomalies": []
            },
            "attribution_data": {
                "conversion_paths": {},
                "attribution_models": {},
                "cross_device_data": {},
                "assisted_conversions": {}
            },
            "audience_intelligence": {
                "demographic_performance": {},
                "interest_performance": {},
                "behavior_performance": {},
                "custom_audience_performance": {},
                "lookalike_performance": {}
            },
            "creative_intelligence": {
                "format_performance": {},
                "message_performance": {},
                "visual_performance": {},
                "cta_performance": {},
                "creative_fatigue_patterns": {}
            },
            "competitive_intelligence": {
                "competitor_analysis": {},
                "market_share_data": {},
                "pricing_intelligence": {},
                "seasonal_trends": {}
            },
            "last_updated": None
        }
    
    def save_memory(self):
        """Save comprehensive memory with backup."""
        self.memory["last_updated"] = datetime.now().isoformat()
        
        # Create backup before saving
        if os.path.exists(self.data_file):
            backup_file = f"{self.data_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.rename(self.data_file, backup_file)
        
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.memory, f, indent=2, default=str)
            logger.info(f"✅ Comprehensive memory saved to {self.data_file}")
        except Exception as e:
            logger.error(f"❌ Error saving memory: {e}")
    
    def track_campaign_comprehensive(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Track campaign with all critical attributes."""
        
        campaign_id = campaign_data.get('id')
        if not campaign_id:
            raise ValueError("Campaign ID is required")
        
        # Get comprehensive campaign data from Facebook
        try:
            # Basic campaign info
            campaign_info = self.client.get_campaigns(limit=1)  # This would be modified to get specific campaign
            
            # Detailed insights with all metrics
            insights = self._get_comprehensive_insights(campaign_id)
            
            # Ad set level data
            ad_sets = self._get_ad_set_data(campaign_id)
            
            # Ad level data
            ads = self._get_ad_data(campaign_id)
            
            # Audience insights
            audience_data = self._get_audience_insights(campaign_id)
            
            # Creative performance
            creative_data = self._get_creative_performance(campaign_id)
            
            # Attribution data
            attribution_data = self._get_attribution_data(campaign_id)
            
        except Exception as e:
            logger.error(f"Error getting comprehensive data: {e}")
            # Use provided data if API fails
            insights = campaign_data.get('insights', {})
            ad_sets = campaign_data.get('ad_sets', [])
            ads = campaign_data.get('ads', [])
            audience_data = campaign_data.get('audience_data', {})
            creative_data = campaign_data.get('creative_data', {})
            attribution_data = campaign_data.get('attribution_data', {})
        
        # Create comprehensive campaign record
        comprehensive_record = {
            "campaign_id": campaign_id,
            "timestamp": datetime.now().isoformat(),
            
            # Basic Campaign Info
            "basic_info": {
                "name": campaign_data.get('name'),
                "objective": campaign_data.get('objective'),
                "status": campaign_data.get('status'),
                "created_time": campaign_data.get('created_time'),
                "start_time": campaign_data.get('start_time'),
                "stop_time": campaign_data.get('stop_time'),
                "updated_time": campaign_data.get('updated_time')
            },
            
            # Financial Metrics (CRITICAL for real money decisions)
            "financial_metrics": {
                "spend": float(insights.get('spend', 0)),
                "revenue": float(insights.get('purchase_roas', 0)) * float(insights.get('spend', 0)),
                "roas": float(insights.get('purchase_roas', 0)),
                "roi": (float(insights.get('purchase_roas', 0)) - 1) * 100,
                "cost_per_purchase": float(insights.get('cost_per_purchase', 0)),
                "purchase_value": float(insights.get('purchase_value', 0)),
                "profit_margin": campaign_data.get('profit_margin', 0),
                "net_profit": 0,  # Calculated below
                "budget_utilization": 0,  # Calculated below
                "daily_budget": float(campaign_data.get('daily_budget', 0)),
                "lifetime_budget": float(campaign_data.get('lifetime_budget', 0))
            },
            
            # Performance Metrics
            "performance_metrics": {
                "impressions": int(insights.get('impressions', 0)),
                "reach": int(insights.get('reach', 0)),
                "frequency": float(insights.get('frequency', 0)),
                "clicks": int(insights.get('clicks', 0)),
                "ctr": float(insights.get('ctr', 0)),
                "cpc": float(insights.get('cpc', 0)),
                "cpm": float(insights.get('cpm', 0)),
                "cpp": float(insights.get('cpp', 0)),  # Cost per 1000 people reached
                "unique_clicks": int(insights.get('unique_clicks', 0)),
                "unique_ctr": float(insights.get('unique_ctr', 0)),
                "cost_per_unique_click": float(insights.get('cost_per_unique_click', 0))
            },
            
            # Conversion Metrics
            "conversion_metrics": {
                "conversions": int(insights.get('conversions', 0)),
                "conversion_rate": float(insights.get('conversion_rate', 0)),
                "cost_per_conversion": float(insights.get('cost_per_conversion', 0)),
                "purchases": int(insights.get('purchases', 0)),
                "purchase_conversion_value": float(insights.get('purchase_conversion_value', 0)),
                "add_to_cart": int(insights.get('add_to_cart', 0)),
                "initiate_checkout": int(insights.get('initiate_checkout', 0)),
                "view_content": int(insights.get('view_content', 0)),
                "lead": int(insights.get('lead', 0)),
                "complete_registration": int(insights.get('complete_registration', 0))
            },
            
            # Engagement Metrics
            "engagement_metrics": {
                "post_engagement": int(insights.get('post_engagement', 0)),
                "page_engagement": int(insights.get('page_engagement', 0)),
                "likes": int(insights.get('likes', 0)),
                "comments": int(insights.get('comments', 0)),
                "shares": int(insights.get('shares', 0)),
                "video_views": int(insights.get('video_views', 0)),
                "video_view_rate": float(insights.get('video_view_rate', 0)),
                "video_avg_time_watched": float(insights.get('video_avg_time_watched', 0)),
                "video_p25_watched": int(insights.get('video_p25_watched', 0)),
                "video_p50_watched": int(insights.get('video_p50_watched', 0)),
                "video_p75_watched": int(insights.get('video_p75_watched', 0)),
                "video_p100_watched": int(insights.get('video_p100_watched', 0))
            },
            
            # Quality Metrics
            "quality_metrics": {
                "quality_score": float(insights.get('quality_score', 0)),
                "engagement_rate_ranking": insights.get('engagement_rate_ranking', 'unknown'),
                "quality_ranking": insights.get('quality_ranking', 'unknown'),
                "conversion_rate_ranking": insights.get('conversion_rate_ranking', 'unknown'),
                "relevance_score": float(insights.get('relevance_score', 0))
            },
            
            # Audience Data
            "audience_data": audience_data,
            
            # Creative Performance
            "creative_data": creative_data,
            
            # Attribution Data
            "attribution_data": attribution_data,
            
            # Ad Set Performance
            "ad_sets": ad_sets,
            
            # Individual Ad Performance
            "ads": ads,
            
            # Risk Indicators
            "risk_indicators": self._calculate_risk_indicators(insights, campaign_data),
            
            # Performance Analysis
            "performance_analysis": self._analyze_comprehensive_performance(insights, campaign_data),
            
            # Recommendations
            "recommendations": self._generate_comprehensive_recommendations(insights, campaign_data)
        }
        
        # Calculate derived metrics
        comprehensive_record = self._calculate_derived_metrics(comprehensive_record)
        
        # Store in memory
        if campaign_id not in self.memory["campaigns"]:
            self.memory["campaigns"][campaign_id] = {
                "creation_date": datetime.now().isoformat(),
                "performance_history": [],
                "optimization_history": [],
                "spend_history": [],
                "alerts_history": []
            }
        
        self.memory["campaigns"][campaign_id]["performance_history"].append(comprehensive_record)
        
        # Update financial tracking
        self._update_financial_tracking(comprehensive_record)
        
        # Check for alerts
        alerts = self._check_critical_alerts(comprehensive_record)
        if alerts:
            self.memory["campaigns"][campaign_id]["alerts_history"].extend(alerts)
            self.memory["risk_management"]["performance_alerts"].extend(alerts)
        
        # Save memory
        self.save_memory()
        
        return comprehensive_record
    
    def _get_comprehensive_insights(self, campaign_id: str) -> Dict[str, Any]:
        """Get comprehensive insights with all available metrics."""
        try:
            # This would be expanded to get all possible metrics
            insights = self.client.get_campaign_insights(campaign_id)
            return insights
        except Exception as e:
            logger.error(f"Error getting insights: {e}")
            return {}
    
    def _get_ad_set_data(self, campaign_id: str) -> List[Dict[str, Any]]:
        """Get detailed ad set performance data."""
        # This would get ad set level data
        return []
    
    def _get_ad_data(self, campaign_id: str) -> List[Dict[str, Any]]:
        """Get individual ad performance data."""
        # This would get individual ad data
        return []
    
    def _get_audience_insights(self, campaign_id: str) -> Dict[str, Any]:
        """Get detailed audience performance data."""
        return {
            "age_breakdown": {},
            "gender_breakdown": {},
            "location_breakdown": {},
            "interest_breakdown": {},
            "behavior_breakdown": {},
            "device_breakdown": {},
            "placement_breakdown": {}
        }
    
    def _get_creative_performance(self, campaign_id: str) -> Dict[str, Any]:
        """Get creative performance breakdown."""
        return {
            "format_performance": {},
            "message_performance": {},
            "visual_performance": {},
            "cta_performance": {}
        }
    
    def _get_attribution_data(self, campaign_id: str) -> Dict[str, Any]:
        """Get attribution and conversion path data."""
        return {
            "attribution_model": "last_click",
            "conversion_paths": [],
            "assisted_conversions": 0,
            "cross_device_conversions": 0
        }
    
    def _calculate_derived_metrics(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate derived financial and performance metrics."""
        
        financial = record["financial_metrics"]
        performance = record["performance_metrics"]
        conversions = record["conversion_metrics"]
        
        # Calculate net profit
        revenue = financial["revenue"]
        spend = financial["spend"]
        profit_margin = financial["profit_margin"] / 100 if financial["profit_margin"] > 1 else financial["profit_margin"]
        
        financial["net_profit"] = (revenue * profit_margin) - spend
        
        # Calculate budget utilization
        daily_budget = financial["daily_budget"]
        if daily_budget > 0:
            financial["budget_utilization"] = (spend / daily_budget) * 100
        
        # Calculate efficiency metrics
        record["efficiency_metrics"] = {
            "cost_per_thousand_impressions": financial["spend"] / (performance["impressions"] / 1000) if performance["impressions"] > 0 else 0,
            "revenue_per_impression": revenue / performance["impressions"] if performance["impressions"] > 0 else 0,
            "profit_per_click": financial["net_profit"] / performance["clicks"] if performance["clicks"] > 0 else 0,
            "conversion_efficiency": conversions["conversions"] / performance["clicks"] * 100 if performance["clicks"] > 0 else 0
        }
        
        return record
    
    def _calculate_risk_indicators(self, insights: Dict[str, Any], campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate risk indicators for the campaign."""
        
        spend = float(insights.get('spend', 0))
        roas = float(insights.get('purchase_roas', 0))
        cpc = float(insights.get('cpc', 0))
        ctr = float(insights.get('ctr', 0))
        frequency = float(insights.get('frequency', 0))
        
        risk_indicators = {
            "high_spend_risk": spend > self.critical_thresholds["max_daily_spend"],
            "low_roas_risk": roas < self.critical_thresholds["min_roas"],
            "high_cpc_risk": cpc > self.critical_thresholds["max_cpc"],
            "low_ctr_risk": ctr < self.critical_thresholds["min_ctr"],
            "high_frequency_risk": frequency > self.critical_thresholds["max_frequency"],
            "budget_burn_risk": False,  # Would calculate based on budget pacing
            "audience_fatigue_risk": frequency > 2.5,
            "creative_fatigue_risk": False,  # Would calculate based on performance decline
            "overall_risk_score": 0  # Calculated below
        }
        
        # Calculate overall risk score (0-100)
        risk_score = 0
        if risk_indicators["high_spend_risk"]: risk_score += 20
        if risk_indicators["low_roas_risk"]: risk_score += 25
        if risk_indicators["high_cpc_risk"]: risk_score += 15
        if risk_indicators["low_ctr_risk"]: risk_score += 15
        if risk_indicators["high_frequency_risk"]: risk_score += 15
        if risk_indicators["audience_fatigue_risk"]: risk_score += 10
        
        risk_indicators["overall_risk_score"] = min(risk_score, 100)
        
        return risk_indicators
    
    def _analyze_comprehensive_performance(self, insights: Dict[str, Any], campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive performance analysis."""
        
        roas = float(insights.get('purchase_roas', 0))
        ctr = float(insights.get('ctr', 0))
        cpc = float(insights.get('cpc', 0))
        frequency = float(insights.get('frequency', 0))
        
        analysis = {
            "overall_status": "unknown",
            "financial_health": "unknown",
            "performance_health": "unknown",
            "audience_health": "unknown",
            "creative_health": "unknown",
            "scaling_potential": "unknown",
            "optimization_priority": "unknown",
            "key_insights": [],
            "critical_issues": [],
            "opportunities": []
        }
        
        # Financial Health Analysis
        if roas >= 4.0:
            analysis["financial_health"] = "excellent"
            analysis["key_insights"].append(f"Strong ROAS of {roas:.2f} indicates profitable campaign")
        elif roas >= 2.0:
            analysis["financial_health"] = "good"
        elif roas >= 1.0:
            analysis["financial_health"] = "break_even"
            analysis["critical_issues"].append("Campaign at break-even, needs optimization")
        else:
            analysis["financial_health"] = "poor"
            analysis["critical_issues"].append(f"Losing money with ROAS of {roas:.2f}")
        
        # Performance Health Analysis
        if ctr >= 2.0:
            analysis["performance_health"] = "excellent"
            analysis["key_insights"].append(f"High CTR of {ctr:.2f}% shows strong creative performance")
        elif ctr >= 1.0:
            analysis["performance_health"] = "good"
        else:
            analysis["performance_health"] = "poor"
            analysis["critical_issues"].append(f"Low CTR of {ctr:.2f}% needs creative optimization")
        
        # Audience Health Analysis
        if frequency <= 2.0:
            analysis["audience_health"] = "excellent"
        elif frequency <= 3.0:
            analysis["audience_health"] = "good"
        else:
            analysis["audience_health"] = "poor"
            analysis["critical_issues"].append(f"High frequency of {frequency:.2f} indicates audience fatigue")
        
        # Overall Status
        if analysis["financial_health"] == "excellent" and analysis["performance_health"] in ["excellent", "good"]:
            analysis["overall_status"] = "excellent"
            analysis["scaling_potential"] = "high"
        elif analysis["financial_health"] in ["good", "excellent"]:
            analysis["overall_status"] = "good"
            analysis["scaling_potential"] = "medium"
        else:
            analysis["overall_status"] = "needs_attention"
            analysis["scaling_potential"] = "low"
        
        return analysis
    
    def _generate_comprehensive_recommendations(self, insights: Dict[str, Any], campaign_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate comprehensive, actionable recommendations."""
        
        recommendations = []
        
        roas = float(insights.get('purchase_roas', 0))
        ctr = float(insights.get('ctr', 0))
        cpc = float(insights.get('cpc', 0))
        frequency = float(insights.get('frequency', 0))
        spend = float(insights.get('spend', 0))
        
        # Financial Recommendations
        if roas < 2.0:
            recommendations.append({
                "type": "critical",
                "category": "financial",
                "action": "pause_or_optimize",
                "title": "Low ROAS Alert",
                "description": f"ROAS of {roas:.2f} is below profitable threshold",
                "specific_actions": [
                    "Pause campaign immediately if ROAS < 1.0",
                    "Optimize audience targeting",
                    "Test new creative variations",
                    "Adjust bidding strategy"
                ],
                "expected_impact": "Improve ROAS by 50-100%",
                "timeline": "Immediate action required"
            })
        
        # Performance Recommendations
        if ctr < 1.0:
            recommendations.append({
                "type": "high",
                "category": "creative",
                "action": "creative_refresh",
                "title": "Low CTR Optimization",
                "description": f"CTR of {ctr:.2f}% is below benchmark",
                "specific_actions": [
                    "Test new creative formats (video vs image)",
                    "Update ad copy and headlines",
                    "Test different call-to-action buttons",
                    "A/B test visual elements"
                ],
                "expected_impact": "Increase CTR by 30-50%",
                "timeline": "Within 3-5 days"
            })
        
        # Audience Recommendations
        if frequency > 3.0:
            recommendations.append({
                "type": "high",
                "category": "audience",
                "action": "audience_expansion",
                "title": "Audience Fatigue Mitigation",
                "description": f"Frequency of {frequency:.2f} indicates audience fatigue",
                "specific_actions": [
                    "Expand audience size by 20-30%",
                    "Create lookalike audiences",
                    "Test new interest categories",
                    "Implement frequency capping"
                ],
                "expected_impact": "Reduce frequency by 20-30%",
                "timeline": "Within 2-3 days"
            })
        
        # Budget Recommendations
        if roas > 4.0 and ctr > 2.0:
            recommendations.append({
                "type": "opportunity",
                "category": "scaling",
                "action": "increase_budget",
                "title": "Scaling Opportunity",
                "description": "Strong performance indicates scaling potential",
                "specific_actions": [
                    "Increase daily budget by 20-30%",
                    "Create similar campaigns",
                    "Expand to new audiences",
                    "Test additional placements"
                ],
                "expected_impact": "Increase revenue by 25-40%",
                "timeline": "Within 1-2 days"
            })
        
        return recommendations
    
    def _update_financial_tracking(self, record: Dict[str, Any]):
        """Update overall financial tracking."""
        
        financial = record["financial_metrics"]
        brand = record["basic_info"].get("name", "unknown").lower()
        
        # Update totals
        self.memory["financial_tracking"]["total_spend"] += financial["spend"]
        self.memory["financial_tracking"]["total_revenue"] += financial["revenue"]
        
        # Update brand tracking
        if brand not in self.memory["financial_tracking"]["spend_by_brand"]:
            self.memory["financial_tracking"]["spend_by_brand"][brand] = 0
        self.memory["financial_tracking"]["spend_by_brand"][brand] += financial["spend"]
        
        # Update overall ROAS
        total_spend = self.memory["financial_tracking"]["total_spend"]
        total_revenue = self.memory["financial_tracking"]["total_revenue"]
        if total_spend > 0:
            self.memory["financial_tracking"]["overall_roas"] = total_revenue / total_spend
    
    def _check_critical_alerts(self, record: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for critical performance alerts."""
        
        alerts = []
        risk_indicators = record["risk_indicators"]
        financial = record["financial_metrics"]
        
        # Critical spend alert
        if risk_indicators["high_spend_risk"]:
            alerts.append({
                "type": "critical",
                "category": "budget",
                "message": f"High daily spend alert: ₹{financial['spend']:.2f}",
                "action_required": "Review budget allocation immediately",
                "timestamp": datetime.now().isoformat()
            })
        
        # Low ROAS alert
        if risk_indicators["low_roas_risk"]:
            alerts.append({
                "type": "critical",
                "category": "performance",
                "message": f"Low ROAS alert: {financial['roas']:.2f}",
                "action_required": "Optimize or pause campaign",
                "timestamp": datetime.now().isoformat()
            })
        
        # Audience fatigue alert
        if risk_indicators["audience_fatigue_risk"]:
            alerts.append({
                "type": "warning",
                "category": "audience",
                "message": "Audience fatigue detected",
                "action_required": "Expand audience or refresh creative",
                "timestamp": datetime.now().isoformat()
            })
        
        return alerts
    
    def get_financial_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive financial dashboard."""
        
        financial = self.memory["financial_tracking"]
        
        dashboard = {
            "overview": {
                "total_spend": financial["total_spend"],
                "total_revenue": financial["total_revenue"],
                "overall_roas": financial["overall_roas"],
                "net_profit": financial["total_revenue"] - financial["total_spend"],
                "profit_margin": ((financial["total_revenue"] - financial["total_spend"]) / financial["total_revenue"] * 100) if financial["total_revenue"] > 0 else 0
            },
            "spend_by_brand": financial["spend_by_brand"],
            "performance_summary": self._get_performance_summary(),
            "risk_summary": self._get_risk_summary(),
            "recommendations": self._get_dashboard_recommendations()
        }
        
        return dashboard
    
    def _get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary across all campaigns."""
        
        total_campaigns = len(self.memory["campaigns"])
        active_campaigns = 0
        total_conversions = 0
        average_roas = 0
        
        for campaign_id, campaign in self.memory["campaigns"].items():
            if campaign["performance_history"]:
                latest = campaign["performance_history"][-1]
                if latest["basic_info"]["status"] == "ACTIVE":
                    active_campaigns += 1
                total_conversions += latest["conversion_metrics"]["conversions"]
                average_roas += latest["financial_metrics"]["roas"]
        
        if total_campaigns > 0:
            average_roas = average_roas / total_campaigns
        
        return {
            "total_campaigns": total_campaigns,
            "active_campaigns": active_campaigns,
            "total_conversions": total_conversions,
            "average_roas": average_roas
        }
    
    def _get_risk_summary(self) -> Dict[str, Any]:
        """Get risk summary across all campaigns."""
        
        high_risk_campaigns = 0
        total_alerts = len(self.memory["risk_management"]["performance_alerts"])
        
        for campaign_id, campaign in self.memory["campaigns"].items():
            if campaign["performance_history"]:
                latest = campaign["performance_history"][-1]
                if latest["risk_indicators"]["overall_risk_score"] > 50:
                    high_risk_campaigns += 1
        
        return {
            "high_risk_campaigns": high_risk_campaigns,
            "total_alerts": total_alerts,
            "recent_alerts": self.memory["risk_management"]["performance_alerts"][-5:]
        }
    
    def _get_dashboard_recommendations(self) -> List[Dict[str, Any]]:
        """Get dashboard-level recommendations."""
        
        recommendations = []
        financial = self.memory["financial_tracking"]
        
        # Overall ROAS recommendation
        if financial["overall_roas"] < 3.0:
            recommendations.append({
                "type": "critical",
                "title": "Improve Overall ROAS",
                "description": f"Account ROAS of {financial['overall_roas']:.2f} needs improvement",
                "action": "Focus on optimizing underperforming campaigns"
            })
        
        # Budget allocation recommendation
        spend_by_brand = financial["spend_by_brand"]
        if spend_by_brand:
            top_brand = max(spend_by_brand.items(), key=lambda x: x[1])
            recommendations.append({
                "type": "insight",
                "title": "Budget Allocation Insight",
                "description": f"{top_brand[0]} accounts for highest spend: ₹{top_brand[1]:.2f}",
                "action": "Analyze if allocation matches performance"
            })
        
        return recommendations

if __name__ == "__main__":
    # Example usage
    tracker = ComprehensiveCampaignTracker()
    
    # Example campaign data
    sample_campaign = {
        "id": "test_comprehensive_001",
        "name": "Voyage Premium Collection",
        "objective": "conversions",
        "status": "ACTIVE",
        "daily_budget": 2000,
        "profit_margin": 40,  # 40% profit margin
        "insights": {
            "spend": "1500.00",
            "purchase_roas": "4.5",
            "ctr": "2.1",
            "cpc": "35.00",
            "impressions": "25000",
            "clicks": "525",
            "conversions": "45",
            "frequency": "1.8"
        }
    }
    
    # Track comprehensive campaign
    result = tracker.track_campaign_comprehensive(sample_campaign)
    
    print("✅ Comprehensive Campaign Tracking Complete")
    print(f"📊 Overall Risk Score: {result['risk_indicators']['overall_risk_score']}")
    print(f"💰 Net Profit: ₹{result['financial_metrics']['net_profit']:.2f}")
    print(f"📈 Performance Status: {result['performance_analysis']['overall_status']}")
    print(f"🎯 Recommendations: {len(result['recommendations'])}")
