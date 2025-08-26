"""
Financial Risk Management System for Facebook Advertising
Critical financial controls and risk assessment for real money decisions.
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import logging
from dataclasses import dataclass
from enum import Enum

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertType(Enum):
    BUDGET_OVERRUN = "budget_overrun"
    LOW_ROAS = "low_roas"
    HIGH_CPC = "high_cpc"
    AUDIENCE_FATIGUE = "audience_fatigue"
    CREATIVE_FATIGUE = "creative_fatigue"
    ACCOUNT_SPENDING_ANOMALY = "account_spending_anomaly"
    CONVERSION_DROP = "conversion_drop"
    QUALITY_SCORE_DROP = "quality_score_drop"

@dataclass
class FinancialMetrics:
    """Comprehensive financial metrics for a campaign."""
    spend: float
    revenue: float
    roas: float
    roi: float
    net_profit: float
    profit_margin: float
    cost_per_acquisition: float
    lifetime_value: float
    payback_period: float
    budget_utilization: float
    daily_budget: float
    remaining_budget: float

@dataclass
class RiskAssessment:
    """Risk assessment for a campaign or account."""
    overall_risk_level: RiskLevel
    risk_score: float  # 0-100
    financial_risk: float
    performance_risk: float
    operational_risk: float
    market_risk: float
    risk_factors: List[str]
    mitigation_strategies: List[str]

class FinancialRiskManager:
    """Comprehensive financial risk management for Facebook advertising."""
    
    def __init__(self, data_file: str = "financial_risk_data.json"):
        self.data_file = data_file
        self.memory = self._load_memory()
        
        # Critical financial thresholds (customizable per business)
        self.thresholds = {
            # Financial thresholds
            "min_roas": 2.0,  # Minimum acceptable ROAS
            "target_roas": 4.0,  # Target ROAS
            "max_cpa": 500.0,  # Maximum cost per acquisition (INR)
            "min_profit_margin": 0.20,  # Minimum 20% profit margin
            "max_daily_spend": 10000.0,  # Maximum daily spend (INR)
            "budget_utilization_warning": 80.0,  # Warn at 80% budget utilization
            "budget_utilization_critical": 95.0,  # Critical at 95% budget utilization
            
            # Performance thresholds
            "min_ctr": 0.8,  # Minimum CTR %
            "max_cpc": 100.0,  # Maximum CPC (INR)
            "max_frequency": 3.0,  # Maximum frequency before fatigue
            "min_quality_score": 6.0,  # Minimum quality score
            "min_conversion_rate": 1.0,  # Minimum conversion rate %
            
            # Risk thresholds
            "high_risk_score": 70.0,  # High risk threshold
            "critical_risk_score": 85.0,  # Critical risk threshold
            
            # Anomaly detection thresholds
            "spend_anomaly_threshold": 50.0,  # % increase that triggers anomaly alert
            "performance_drop_threshold": 30.0,  # % drop that triggers alert
        }
        
        # Business-specific settings
        self.business_settings = {
            "average_order_value": 2500.0,  # INR
            "customer_lifetime_value": 7500.0,  # INR
            "gross_margin": 0.40,  # 40% gross margin
            "acceptable_payback_period": 30,  # days
            "currency": "INR",
            "business_hours": {"start": 9, "end": 18},  # IST
            "weekend_multiplier": 0.7  # Weekend performance typically 70% of weekdays
        }
    
    def _load_memory(self) -> Dict[str, Any]:
        """Load financial risk memory."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading financial risk memory: {e}")
                return self._create_financial_memory()
        return self._create_financial_memory()
    
    def _create_financial_memory(self) -> Dict[str, Any]:
        """Create comprehensive financial risk memory structure."""
        return {
            "financial_overview": {
                "total_spend": 0.0,
                "total_revenue": 0.0,
                "total_profit": 0.0,
                "overall_roas": 0.0,
                "overall_roi": 0.0,
                "monthly_spend_limit": 100000.0,  # INR
                "current_month_spend": 0.0,
                "daily_spend_average": 0.0,
                "spend_trend": "stable"
            },
            "campaign_financials": {},
            "account_financials": {},
            "brand_financials": {},
            "risk_assessments": {},
            "active_alerts": [],
            "alert_history": [],
            "budget_controls": {
                "auto_pause_enabled": True,
                "auto_pause_threshold": 1.0,  # Pause if ROAS < 1.0
                "daily_spend_limits": {},
                "campaign_spend_limits": {},
                "emergency_stop_triggers": []
            },
            "performance_benchmarks": {
                "historical_roas": [],
                "historical_cpc": [],
                "historical_ctr": [],
                "seasonal_adjustments": {}
            },
            "financial_forecasts": {
                "projected_monthly_spend": 0.0,
                "projected_monthly_revenue": 0.0,
                "projected_roas": 0.0,
                "confidence_level": 0.0
            },
            "compliance_tracking": {
                "budget_approvals": [],
                "spend_authorizations": [],
                "audit_trail": []
            },
            "last_updated": None
        }
    
    def save_memory(self):
        """Save financial risk memory with audit trail."""
        self.memory["last_updated"] = datetime.now().isoformat()
        
        # Create audit entry
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "memory_save",
            "user": "system",
            "changes": "Financial data updated"
        }
        self.memory["compliance_tracking"]["audit_trail"].append(audit_entry)
        
        # Keep only last 1000 audit entries
        if len(self.memory["compliance_tracking"]["audit_trail"]) > 1000:
            self.memory["compliance_tracking"]["audit_trail"] = self.memory["compliance_tracking"]["audit_trail"][-1000:]
        
        try:
            # Create backup
            if os.path.exists(self.data_file):
                backup_file = f"{self.data_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                os.rename(self.data_file, backup_file)
            
            with open(self.data_file, 'w') as f:
                json.dump(self.memory, f, indent=2, default=str)
            logger.info(f"✅ Financial risk memory saved to {self.data_file}")
        except Exception as e:
            logger.error(f"❌ Error saving financial risk memory: {e}")
    
    def calculate_financial_metrics(self, campaign_data: Dict[str, Any]) -> FinancialMetrics:
        """Calculate comprehensive financial metrics."""
        
        spend = float(campaign_data.get('spend', 0))
        revenue = float(campaign_data.get('revenue', 0))
        conversions = int(campaign_data.get('conversions', 0))
        daily_budget = float(campaign_data.get('daily_budget', 0))
        
        # Calculate basic metrics
        roas = revenue / spend if spend > 0 else 0
        roi = ((revenue - spend) / spend * 100) if spend > 0 else 0
        net_profit = revenue - spend
        profit_margin = net_profit / revenue if revenue > 0 else 0
        cost_per_acquisition = spend / conversions if conversions > 0 else 0
        
        # Calculate advanced metrics
        lifetime_value = self.business_settings["customer_lifetime_value"]
        payback_period = cost_per_acquisition / (lifetime_value * self.business_settings["gross_margin"]) * 30 if lifetime_value > 0 else 0
        budget_utilization = (spend / daily_budget * 100) if daily_budget > 0 else 0
        remaining_budget = daily_budget - spend if daily_budget > spend else 0
        
        return FinancialMetrics(
            spend=spend,
            revenue=revenue,
            roas=roas,
            roi=roi,
            net_profit=net_profit,
            profit_margin=profit_margin,
            cost_per_acquisition=cost_per_acquisition,
            lifetime_value=lifetime_value,
            payback_period=payback_period,
            budget_utilization=budget_utilization,
            daily_budget=daily_budget,
            remaining_budget=remaining_budget
        )
    
    def assess_campaign_risk(self, campaign_data: Dict[str, Any], financial_metrics: FinancialMetrics) -> RiskAssessment:
        """Comprehensive risk assessment for a campaign."""
        
        risk_factors = []
        mitigation_strategies = []
        
        # Financial Risk Assessment (40% weight)
        financial_risk = 0
        
        if financial_metrics.roas < self.thresholds["min_roas"]:
            financial_risk += 30
            risk_factors.append(f"Low ROAS: {financial_metrics.roas:.2f} (Target: {self.thresholds['target_roas']:.2f})")
            mitigation_strategies.append("Optimize audience targeting and creative performance")
        
        if financial_metrics.cost_per_acquisition > self.thresholds["max_cpa"]:
            financial_risk += 25
            risk_factors.append(f"High CPA: ₹{financial_metrics.cost_per_acquisition:.2f}")
            mitigation_strategies.append("Improve conversion rate through landing page optimization")
        
        if financial_metrics.profit_margin < self.thresholds["min_profit_margin"]:
            financial_risk += 20
            risk_factors.append(f"Low profit margin: {financial_metrics.profit_margin*100:.1f}%")
            mitigation_strategies.append("Review pricing strategy or reduce acquisition costs")
        
        if financial_metrics.budget_utilization > self.thresholds["budget_utilization_critical"]:
            financial_risk += 15
            risk_factors.append(f"Critical budget utilization: {financial_metrics.budget_utilization:.1f}%")
            mitigation_strategies.append("Implement budget pacing controls")
        
        if financial_metrics.payback_period > self.business_settings["acceptable_payback_period"]:
            financial_risk += 10
            risk_factors.append(f"Long payback period: {financial_metrics.payback_period:.0f} days")
            mitigation_strategies.append("Focus on higher-value customer segments")
        
        # Performance Risk Assessment (30% weight)
        performance_risk = 0
        
        ctr = float(campaign_data.get('ctr', 0))
        cpc = float(campaign_data.get('cpc', 0))
        frequency = float(campaign_data.get('frequency', 0))
        quality_score = float(campaign_data.get('quality_score', 10))
        
        if ctr < self.thresholds["min_ctr"]:
            performance_risk += 25
            risk_factors.append(f"Low CTR: {ctr:.2f}%")
            mitigation_strategies.append("Refresh creative assets and test new formats")
        
        if cpc > self.thresholds["max_cpc"]:
            performance_risk += 20
            risk_factors.append(f"High CPC: ₹{cpc:.2f}")
            mitigation_strategies.append("Optimize bidding strategy and audience targeting")
        
        if frequency > self.thresholds["max_frequency"]:
            performance_risk += 20
            risk_factors.append(f"High frequency: {frequency:.2f}")
            mitigation_strategies.append("Expand audience or implement frequency capping")
        
        if quality_score < self.thresholds["min_quality_score"]:
            performance_risk += 15
            risk_factors.append(f"Low quality score: {quality_score:.1f}")
            mitigation_strategies.append("Improve ad relevance and landing page experience")
        
        # Operational Risk Assessment (20% weight)
        operational_risk = 0
        
        campaign_age = self._calculate_campaign_age(campaign_data.get('created_time'))
        if campaign_age > 30:  # Campaign running for more than 30 days
            operational_risk += 15
            risk_factors.append("Long-running campaign may have creative fatigue")
            mitigation_strategies.append("Schedule regular creative refreshes")
        
        if not campaign_data.get('optimization_history'):
            operational_risk += 10
            risk_factors.append("No recent optimizations detected")
            mitigation_strategies.append("Implement regular optimization schedule")
        
        # Market Risk Assessment (10% weight)
        market_risk = 0
        
        current_hour = datetime.now().hour
        if current_hour < self.business_settings["business_hours"]["start"] or current_hour > self.business_settings["business_hours"]["end"]:
            market_risk += 5
            risk_factors.append("Running outside business hours")
            mitigation_strategies.append("Consider dayparting optimization")
        
        # Calculate overall risk score
        overall_risk_score = (
            financial_risk * 0.4 +
            performance_risk * 0.3 +
            operational_risk * 0.2 +
            market_risk * 0.1
        )
        
        # Determine risk level
        if overall_risk_score >= self.thresholds["critical_risk_score"]:
            risk_level = RiskLevel.CRITICAL
        elif overall_risk_score >= self.thresholds["high_risk_score"]:
            risk_level = RiskLevel.HIGH
        elif overall_risk_score >= 40:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW
        
        return RiskAssessment(
            overall_risk_level=risk_level,
            risk_score=overall_risk_score,
            financial_risk=financial_risk,
            performance_risk=performance_risk,
            operational_risk=operational_risk,
            market_risk=market_risk,
            risk_factors=risk_factors,
            mitigation_strategies=mitigation_strategies
        )
    
    def _calculate_campaign_age(self, created_time: str) -> int:
        """Calculate campaign age in days."""
        if not created_time:
            return 0
        
        try:
            created = datetime.fromisoformat(created_time.replace('Z', '+00:00'))
            age = (datetime.now() - created).days
            return age
        except:
            return 0
    
    def generate_alerts(self, campaign_id: str, campaign_data: Dict[str, Any], financial_metrics: FinancialMetrics, risk_assessment: RiskAssessment) -> List[Dict[str, Any]]:
        """Generate critical alerts based on financial and performance data."""
        
        alerts = []
        
        # Critical ROAS Alert
        if financial_metrics.roas < 1.0:
            alerts.append({
                "id": f"roas_critical_{campaign_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "type": AlertType.LOW_ROAS.value,
                "severity": "critical",
                "campaign_id": campaign_id,
                "title": "CRITICAL: Campaign Losing Money",
                "message": f"ROAS of {financial_metrics.roas:.2f} means you're losing ₹{abs(financial_metrics.net_profit):.2f}",
                "recommended_action": "PAUSE CAMPAIGN IMMEDIATELY or optimize urgently",
                "financial_impact": abs(financial_metrics.net_profit),
                "timestamp": datetime.now().isoformat(),
                "auto_action": "pause_if_enabled"
            })
        
        # Budget Overrun Alert
        if financial_metrics.budget_utilization > self.thresholds["budget_utilization_critical"]:
            alerts.append({
                "id": f"budget_overrun_{campaign_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "type": AlertType.BUDGET_OVERRUN.value,
                "severity": "high",
                "campaign_id": campaign_id,
                "title": "Budget Overrun Alert",
                "message": f"Campaign has used {financial_metrics.budget_utilization:.1f}% of daily budget",
                "recommended_action": "Review budget pacing and adjust if necessary",
                "financial_impact": financial_metrics.spend - financial_metrics.daily_budget,
                "timestamp": datetime.now().isoformat()
            })
        
        # High CPC Alert
        cpc = float(campaign_data.get('cpc', 0))
        if cpc > self.thresholds["max_cpc"]:
            alerts.append({
                "id": f"high_cpc_{campaign_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "type": AlertType.HIGH_CPC.value,
                "severity": "medium",
                "campaign_id": campaign_id,
                "title": "High CPC Alert",
                "message": f"CPC of ₹{cpc:.2f} is above threshold of ₹{self.thresholds['max_cpc']:.2f}",
                "recommended_action": "Optimize audience targeting or bidding strategy",
                "financial_impact": (cpc - self.thresholds["max_cpc"]) * int(campaign_data.get('clicks', 0)),
                "timestamp": datetime.now().isoformat()
            })
        
        # Audience Fatigue Alert
        frequency = float(campaign_data.get('frequency', 0))
        if frequency > self.thresholds["max_frequency"]:
            alerts.append({
                "id": f"audience_fatigue_{campaign_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "type": AlertType.AUDIENCE_FATIGUE.value,
                "severity": "medium",
                "campaign_id": campaign_id,
                "title": "Audience Fatigue Detected",
                "message": f"Frequency of {frequency:.2f} indicates potential audience fatigue",
                "recommended_action": "Expand audience or refresh creative",
                "financial_impact": 0,  # Indirect impact
                "timestamp": datetime.now().isoformat()
            })
        
        # Quality Score Drop Alert
        quality_score = float(campaign_data.get('quality_score', 10))
        if quality_score < self.thresholds["min_quality_score"]:
            alerts.append({
                "id": f"quality_drop_{campaign_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "type": AlertType.QUALITY_SCORE_DROP.value,
                "severity": "medium",
                "campaign_id": campaign_id,
                "title": "Quality Score Below Threshold",
                "message": f"Quality score of {quality_score:.1f} may increase costs",
                "recommended_action": "Improve ad relevance and landing page experience",
                "financial_impact": 0,  # Indirect impact
                "timestamp": datetime.now().isoformat()
            })
        
        # Store alerts in memory
        for alert in alerts:
            self.memory["active_alerts"].append(alert)
            self.memory["alert_history"].append(alert)
        
        # Keep only last 100 active alerts
        if len(self.memory["active_alerts"]) > 100:
            self.memory["active_alerts"] = self.memory["active_alerts"][-100:]
        
        return alerts
    
    def execute_auto_actions(self, alerts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute automatic actions based on alerts."""
        
        actions_taken = []
        
        if not self.memory["budget_controls"]["auto_pause_enabled"]:
            return actions_taken
        
        for alert in alerts:
            if alert.get("auto_action") == "pause_if_enabled" and alert["severity"] == "critical":
                # In a real implementation, this would pause the campaign via Facebook API
                action = {
                    "timestamp": datetime.now().isoformat(),
                    "action": "auto_pause",
                    "campaign_id": alert["campaign_id"],
                    "reason": alert["message"],
                    "alert_id": alert["id"],
                    "financial_protection": alert["financial_impact"]
                }
                actions_taken.append(action)
                
                # Log the action
                logger.warning(f"AUTO-PAUSE: Campaign {alert['campaign_id']} paused due to critical ROAS")
        
        return actions_taken
    
    def get_financial_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive financial dashboard."""
        
        overview = self.memory["financial_overview"]
        active_alerts = [alert for alert in self.memory["active_alerts"] if alert["severity"] in ["critical", "high"]]
        
        dashboard = {
            "financial_summary": {
                "total_spend": overview["total_spend"],
                "total_revenue": overview["total_revenue"],
                "total_profit": overview["total_profit"],
                "overall_roas": overview["overall_roas"],
                "overall_roi": overview["overall_roi"],
                "monthly_spend_remaining": overview["monthly_spend_limit"] - overview["current_month_spend"],
                "daily_average_spend": overview["daily_spend_average"]
            },
            "risk_summary": {
                "total_active_alerts": len(self.memory["active_alerts"]),
                "critical_alerts": len([a for a in active_alerts if a["severity"] == "critical"]),
                "high_risk_alerts": len([a for a in active_alerts if a["severity"] == "high"]),
                "total_financial_impact": sum(alert.get("financial_impact", 0) for alert in active_alerts)
            },
            "recent_alerts": active_alerts[:10],
            "budget_status": {
                "monthly_limit": overview["monthly_spend_limit"],
                "current_spend": overview["current_month_spend"],
                "utilization_percentage": (overview["current_month_spend"] / overview["monthly_spend_limit"]) * 100,
                "projected_month_end": self._project_month_end_spend()
            },
            "performance_trends": {
                "roas_trend": self._calculate_roas_trend(),
                "spend_trend": overview["spend_trend"],
                "efficiency_trend": self._calculate_efficiency_trend()
            },
            "recommendations": self._generate_dashboard_recommendations()
        }
        
        return dashboard
    
    def _project_month_end_spend(self) -> float:
        """Project month-end spend based on current trends."""
        current_day = datetime.now().day
        days_in_month = 30  # Simplified
        daily_average = self.memory["financial_overview"]["daily_spend_average"]
        
        if daily_average > 0:
            remaining_days = days_in_month - current_day
            projected_additional_spend = daily_average * remaining_days
            return self.memory["financial_overview"]["current_month_spend"] + projected_additional_spend
        
        return self.memory["financial_overview"]["current_month_spend"]
    
    def _calculate_roas_trend(self) -> str:
        """Calculate ROAS trend based on historical data."""
        historical_roas = self.memory["performance_benchmarks"]["historical_roas"]
        
        if len(historical_roas) < 2:
            return "insufficient_data"
        
        recent_avg = sum(historical_roas[-7:]) / len(historical_roas[-7:])
        previous_avg = sum(historical_roas[-14:-7]) / len(historical_roas[-14:-7]) if len(historical_roas) >= 14 else recent_avg
        
        if recent_avg > previous_avg * 1.1:
            return "improving"
        elif recent_avg < previous_avg * 0.9:
            return "declining"
        else:
            return "stable"
    
    def _calculate_efficiency_trend(self) -> str:
        """Calculate overall efficiency trend."""
        # This would analyze multiple efficiency metrics
        return "stable"
    
    def _generate_dashboard_recommendations(self) -> List[Dict[str, Any]]:
        """Generate dashboard-level recommendations."""
        
        recommendations = []
        overview = self.memory["financial_overview"]
        
        # ROAS Recommendation
        if overview["overall_roas"] < self.thresholds["target_roas"]:
            recommendations.append({
                "type": "financial",
                "priority": "high",
                "title": "Improve Overall ROAS",
                "description": f"Current ROAS of {overview['overall_roas']:.2f} is below target of {self.thresholds['target_roas']:.2f}",
                "action": "Focus optimization efforts on underperforming campaigns",
                "potential_impact": f"Could save ₹{(overview['total_spend'] * 0.2):.0f} monthly"
            })
        
        # Budget Utilization Recommendation
        monthly_utilization = (overview["current_month_spend"] / overview["monthly_spend_limit"]) * 100
        if monthly_utilization > 80:
            recommendations.append({
                "type": "budget",
                "priority": "medium",
                "title": "Monitor Monthly Budget",
                "description": f"Used {monthly_utilization:.1f}% of monthly budget",
                "action": "Review remaining campaigns and adjust spend allocation",
                "potential_impact": "Prevent budget overruns"
            })
        
        # Alert Management Recommendation
        critical_alerts = len([a for a in self.memory["active_alerts"] if a["severity"] == "critical"])
        if critical_alerts > 0:
            recommendations.append({
                "type": "operational",
                "priority": "critical",
                "title": "Address Critical Alerts",
                "description": f"{critical_alerts} critical alerts require immediate attention",
                "action": "Review and resolve critical performance issues",
                "potential_impact": "Prevent further financial losses"
            })
        
        return recommendations
    
    def update_campaign_financials(self, campaign_id: str, campaign_data: Dict[str, Any]):
        """Update comprehensive financial tracking for a campaign."""
        
        # Calculate financial metrics
        financial_metrics = self.calculate_financial_metrics(campaign_data)
        
        # Assess risk
        risk_assessment = self.assess_campaign_risk(campaign_data, financial_metrics)
        
        # Generate alerts
        alerts = self.generate_alerts(campaign_id, campaign_data, financial_metrics, risk_assessment)
        
        # Execute auto actions if needed
        auto_actions = self.execute_auto_actions(alerts)
        
        # Update memory
        self.memory["campaign_financials"][campaign_id] = {
            "timestamp": datetime.now().isoformat(),
            "financial_metrics": financial_metrics.__dict__,
            "risk_assessment": {
                "overall_risk_level": risk_assessment.overall_risk_level.value,
                "risk_score": risk_assessment.risk_score,
                "financial_risk": risk_assessment.financial_risk,
                "performance_risk": risk_assessment.performance_risk,
                "operational_risk": risk_assessment.operational_risk,
                "market_risk": risk_assessment.market_risk,
                "risk_factors": risk_assessment.risk_factors,
                "mitigation_strategies": risk_assessment.mitigation_strategies
            },
            "alerts_generated": len(alerts),
            "auto_actions_taken": len(auto_actions)
        }
        
        # Update overall financials
        self._update_overall_financials(financial_metrics)
        
        # Save memory
        self.save_memory()
        
        return {
            "financial_metrics": financial_metrics,
            "risk_assessment": risk_assessment,
            "alerts": alerts,
            "auto_actions": auto_actions
        }
    
    def _update_overall_financials(self, financial_metrics: FinancialMetrics):
        """Update overall financial tracking."""
        
        overview = self.memory["financial_overview"]
        
        # Update totals (this would be more sophisticated in real implementation)
        overview["total_spend"] += financial_metrics.spend
        overview["total_revenue"] += financial_metrics.revenue
        overview["total_profit"] += financial_metrics.net_profit
        
        # Update ROAS
        if overview["total_spend"] > 0:
            overview["overall_roas"] = overview["total_revenue"] / overview["total_spend"]
            overview["overall_roi"] = ((overview["total_revenue"] - overview["total_spend"]) / overview["total_spend"]) * 100
        
        # Update monthly tracking
        current_month = datetime.now().strftime("%Y-%m")
        overview["current_month_spend"] += financial_metrics.spend
        
        # Update benchmarks
        self.memory["performance_benchmarks"]["historical_roas"].append(financial_metrics.roas)
        if len(self.memory["performance_benchmarks"]["historical_roas"]) > 90:  # Keep 90 days
            self.memory["performance_benchmarks"]["historical_roas"] = self.memory["performance_benchmarks"]["historical_roas"][-90:]

if __name__ == "__main__":
    # Example usage
    risk_manager = FinancialRiskManager()
    
    # Example campaign data
    sample_campaign = {
        "spend": 2500.0,
        "revenue": 8000.0,
        "conversions": 15,
        "daily_budget": 3000.0,
        "ctr": 1.8,
        "cpc": 45.0,
        "frequency": 2.1,
        "quality_score": 7.5,
        "created_time": "2024-01-15T10:00:00Z"
    }
    
    # Update campaign financials
    result = risk_manager.update_campaign_financials("test_campaign_001", sample_campaign)
    
    print("✅ Financial Risk Assessment Complete")
    print(f"💰 ROAS: {result['financial_metrics'].roas:.2f}")
    print(f"📊 Risk Level: {result['risk_assessment'].overall_risk_level.value}")
    print(f"🚨 Alerts Generated: {len(result['alerts'])}")
    print(f"🤖 Auto Actions: {len(result['auto_actions'])}")
    
    # Get dashboard
    dashboard = risk_manager.get_financial_dashboard()
    print(f"\n📈 Dashboard Summary:")
    print(f"Total Spend: ₹{dashboard['financial_summary']['total_spend']:.2f}")
    print(f"Total Revenue: ₹{dashboard['financial_summary']['total_revenue']:.2f}")
    print(f"Overall ROAS: {dashboard['financial_summary']['overall_roas']:.2f}")
    print(f"Active Alerts: {dashboard['risk_summary']['total_active_alerts']}")
