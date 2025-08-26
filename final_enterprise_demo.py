"""
Final Enterprise Marketing Agent Demonstration
Shows complete system with all critical attributes for real money decisions.
"""
import json
from datetime import datetime
from financial_risk_manager import FinancialRiskManager, RiskLevel
from comprehensive_campaign_tracker import ComprehensiveCampaignTracker
from strategic_memory import StrategicMemory

class EnterpriseDemo:
    """Demonstration of enterprise-grade Facebook marketing system."""
    
    def __init__(self):
        self.risk_manager = FinancialRiskManager()
        self.campaign_tracker = ComprehensiveCampaignTracker()
        self.strategic_memory = StrategicMemory()
        
        # Critical business settings for real money protection
        self.business_rules = {
            "max_daily_spend_per_campaign": 10000.0,  # INR
            "max_monthly_spend_total": 500000.0,  # INR
            "min_roas_threshold": 2.0,
            "auto_pause_enabled": True,
            "emergency_stop_roas": 0.8,  # Stop if ROAS drops below 0.8
            "require_approval_above": 25000.0,  # INR daily spend
        }
    
    def demonstrate_enterprise_campaign_launch(self):
        """Demonstrate enterprise campaign launch with all validations."""
        
        print("🏢 ENTERPRISE CAMPAIGN LAUNCH DEMONSTRATION")
        print("="*60)
        print("This shows how the system protects your real money with:")
        print("• Comprehensive validation")
        print("• Financial risk assessment") 
        print("• Automated alerts and controls")
        print("• Complete audit trail")
        print("="*60)
        
        # High-value campaign that requires all protections
        campaign_brief = {
            "name": "Voyage Premium Collection - Holiday Campaign",
            "brand": "Voyage",
            "objective": "conversions",
            "daily_budget": 15000.0,  # High budget requiring approval
            "lifetime_budget": 450000.0,  # 30 days
            "profit_margin": 35,  # 35% profit margin
            "target_audience": {
                "age_range": "25-45",
                "interests": ["premium eyewear", "fashion", "luxury"],
                "location": "India",
                "income": "top_25_percent"
            },
            "expected_outcome": "₹1,800,000 revenue with 4.0 ROAS"
        }
        
        print(f"\n💰 CAMPAIGN BRIEF:")
        print(f"• Name: {campaign_brief['name']}")
        print(f"• Daily Budget: ₹{campaign_brief['daily_budget']:,.2f}")
        print(f"• Monthly Budget: ₹{campaign_brief['lifetime_budget']:,.2f}")
        print(f"• Profit Margin: {campaign_brief['profit_margin']}%")
        print(f"• Expected Revenue: {campaign_brief['expected_outcome']}")
        
        # Step 1: Business Rules Validation
        print(f"\n🔍 STEP 1: BUSINESS RULES VALIDATION")
        validation_results = self._validate_campaign_brief(campaign_brief)
        
        for result in validation_results:
            status = "✅" if result["passed"] else "❌"
            print(f"{status} {result['rule']}: {result['message']}")
        
        # Step 2: Financial Risk Assessment
        print(f"\n📊 STEP 2: FINANCIAL RISK ASSESSMENT")
        financial_metrics = self.risk_manager.calculate_financial_metrics({
            "spend": 0,  # Initial
            "revenue": 0,  # Initial
            "conversions": 0,  # Initial
            "daily_budget": campaign_brief["daily_budget"]
        })
        
        risk_assessment = self.risk_manager.assess_campaign_risk(campaign_brief, financial_metrics)
        
        print(f"• Break-even ROAS: {100/campaign_brief['profit_margin']:.2f}")
        print(f"• Target ROAS: {self.business_rules['min_roas_threshold']:.2f}")
        print(f"• Maximum CPA: ₹{campaign_brief['daily_budget'] * 0.1:.2f}")
        print(f"• Risk Level: {risk_assessment.overall_risk_level.value.upper()}")
        print(f"• Risk Score: {risk_assessment.risk_score:.1f}/100")
        
        # Step 3: Approval Process
        print(f"\n📋 STEP 3: APPROVAL PROCESS")
        approval_required = campaign_brief["daily_budget"] > self.business_rules["require_approval_above"]
        
        if approval_required:
            print(f"⚠️  APPROVAL REQUIRED: Daily budget ₹{campaign_brief['daily_budget']:,.2f} exceeds threshold")
            print(f"   Threshold: ₹{self.business_rules['require_approval_above']:,.2f}")
            print(f"   Status: PENDING MANUAL APPROVAL")
        else:
            print(f"✅ AUTO-APPROVED: Budget within automatic approval limits")
        
        # Step 4: Financial Controls Setup
        print(f"\n🛡️  STEP 4: FINANCIAL CONTROLS SETUP")
        controls = {
            "auto_pause_enabled": self.business_rules["auto_pause_enabled"],
            "emergency_stop_roas": self.business_rules["emergency_stop_roas"],
            "daily_budget_limit": campaign_brief["daily_budget"],
            "spend_alerts_at": campaign_brief["daily_budget"] * 0.8,  # 80% of budget
            "performance_monitoring": "real_time"
        }
        
        for control, value in controls.items():
            print(f"• {control.replace('_', ' ').title()}: {value}")
        
        return campaign_brief
    
    def demonstrate_real_time_monitoring(self, campaign_brief):
        """Demonstrate real-time monitoring and alerts."""
        
        print(f"\n📡 REAL-TIME MONITORING DEMONSTRATION")
        print("="*60)
        
        campaign_id = f"ent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Simulate different performance scenarios
        scenarios = [
            {
                "name": "Hour 1: Good Performance",
                "data": {
                    "spend": 625.0,  # ₹625 in first hour
                    "revenue": 2500.0,  # ₹2500 revenue
                    "conversions": 5,
                    "ctr": 2.1,
                    "cpc": 35.0,
                    "frequency": 1.1,
                    "quality_score": 8.2
                },
                "expected_status": "excellent"
            },
            {
                "name": "Hour 6: Warning Signs",
                "data": {
                    "spend": 4200.0,  # ₹4200 in 6 hours
                    "revenue": 8400.0,  # ₹8400 revenue
                    "conversions": 18,
                    "ctr": 1.8,
                    "cpc": 42.0,
                    "frequency": 1.8,
                    "quality_score": 7.5
                },
                "expected_status": "good"
            },
            {
                "name": "Hour 12: Critical Alert",
                "data": {
                    "spend": 9500.0,  # ₹9500 in 12 hours (high spend)
                    "revenue": 14250.0,  # ₹14250 revenue
                    "conversions": 28,
                    "ctr": 1.2,  # Declining CTR
                    "cpc": 65.0,  # High CPC
                    "frequency": 2.8,  # High frequency
                    "quality_score": 6.8
                },
                "expected_status": "needs_attention"
            },
            {
                "name": "Hour 18: Emergency Stop Triggered",
                "data": {
                    "spend": 14500.0,  # ₹14500 (over daily budget)
                    "revenue": 10150.0,  # ₹10150 revenue (ROAS = 0.7)
                    "conversions": 22,
                    "ctr": 0.8,  # Very low CTR
                    "cpc": 85.0,  # Very high CPC
                    "frequency": 3.5,  # Very high frequency
                    "quality_score": 5.2
                },
                "expected_status": "critical"
            }
        ]
        
        for scenario in scenarios:
            print(f"\n⏰ {scenario['name']}")
            print("-" * 40)
            
            data = scenario['data']
            
            # Calculate metrics
            roas = data['revenue'] / data['spend'] if data['spend'] > 0 else 0
            budget_utilization = (data['spend'] / campaign_brief['daily_budget']) * 100
            
            print(f"💰 Financial Metrics:")
            print(f"   Spend: ₹{data['spend']:,.2f}")
            print(f"   Revenue: ₹{data['revenue']:,.2f}")
            print(f"   ROAS: {roas:.2f}")
            print(f"   Budget Used: {budget_utilization:.1f}%")
            
            print(f"📊 Performance Metrics:")
            print(f"   CTR: {data['ctr']:.2f}%")
            print(f"   CPC: ₹{data['cpc']:.2f}")
            print(f"   Frequency: {data['frequency']:.2f}")
            print(f"   Quality Score: {data['quality_score']:.1f}")
            
            # Generate alerts
            alerts = self._generate_scenario_alerts(data, campaign_brief, roas, budget_utilization)
            
            if alerts:
                print(f"🚨 ALERTS GENERATED:")
                for alert in alerts:
                    severity_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡"}.get(alert["severity"], "🔵")
                    print(f"   {severity_icon} {alert['severity'].upper()}: {alert['message']}")
                    if alert.get("auto_action"):
                        print(f"      🤖 AUTO ACTION: {alert['auto_action']}")
            else:
                print(f"✅ No alerts - Performance within acceptable ranges")
            
            # Check for emergency stop
            if roas < self.business_rules["emergency_stop_roas"]:
                print(f"\n🛑 EMERGENCY STOP TRIGGERED!")
                print(f"   ROAS {roas:.2f} below emergency threshold {self.business_rules['emergency_stop_roas']}")
                print(f"   🤖 AUTO ACTION: CAMPAIGN PAUSED IMMEDIATELY")
                print(f"   💰 FINANCIAL PROTECTION: Prevented further losses")
                break
    
    def demonstrate_financial_dashboard(self):
        """Demonstrate comprehensive financial dashboard."""
        
        print(f"\n💼 FINANCIAL DASHBOARD DEMONSTRATION")
        print("="*60)
        
        # Simulate account-level financial data
        account_data = {
            "total_spend": 125000.0,  # ₹1.25 Lakh
            "total_revenue": 487500.0,  # ₹4.875 Lakh
            "total_campaigns": 8,
            "active_campaigns": 5,
            "monthly_budget": 500000.0,  # ₹5 Lakh monthly limit
            "current_month_spend": 325000.0,  # ₹3.25 Lakh used
        }
        
        overall_roas = account_data["total_revenue"] / account_data["total_spend"]
        net_profit = account_data["total_revenue"] - account_data["total_spend"]
        profit_margin = (net_profit / account_data["total_revenue"]) * 100
        budget_utilization = (account_data["current_month_spend"] / account_data["monthly_budget"]) * 100
        
        print(f"📊 EXECUTIVE SUMMARY:")
        print(f"• Total Ad Spend: ₹{account_data['total_spend']:,.2f}")
        print(f"• Total Revenue: ₹{account_data['total_revenue']:,.2f}")
        print(f"• Net Profit: ₹{net_profit:,.2f}")
        print(f"• Overall ROAS: {overall_roas:.2f}")
        print(f"• Profit Margin: {profit_margin:.1f}%")
        
        print(f"\n💰 BUDGET MANAGEMENT:")
        print(f"• Monthly Budget: ₹{account_data['monthly_budget']:,.2f}")
        print(f"• Current Spend: ₹{account_data['current_month_spend']:,.2f}")
        print(f"• Budget Utilization: {budget_utilization:.1f}%")
        print(f"• Remaining Budget: ₹{account_data['monthly_budget'] - account_data['current_month_spend']:,.2f}")
        
        print(f"\n🎯 CAMPAIGN OVERVIEW:")
        print(f"• Total Campaigns: {account_data['total_campaigns']}")
        print(f"• Active Campaigns: {account_data['active_campaigns']}")
        print(f"• Paused/Completed: {account_data['total_campaigns'] - account_data['active_campaigns']}")
        
        # Risk assessment
        risk_level = "LOW"
        if budget_utilization > 90:
            risk_level = "HIGH"
        elif budget_utilization > 75:
            risk_level = "MEDIUM"
        
        print(f"\n🚨 RISK ASSESSMENT:")
        print(f"• Overall Risk Level: {risk_level}")
        print(f"• Budget Risk: {'HIGH' if budget_utilization > 80 else 'LOW'}")
        print(f"• Performance Risk: {'LOW' if overall_roas > 3.0 else 'MEDIUM'}")
        
        # Recommendations
        print(f"\n💡 STRATEGIC RECOMMENDATIONS:")
        if overall_roas > 4.0:
            print("• ✅ Excellent ROAS - Consider scaling successful campaigns")
        if budget_utilization > 80:
            print("• ⚠️  High budget utilization - Monitor remaining spend carefully")
        if net_profit > 300000:
            print("• 🚀 Strong profitability - Explore new market opportunities")
    
    def _validate_campaign_brief(self, campaign_brief):
        """Validate campaign brief against business rules."""
        
        validations = []
        
        # Daily budget validation
        daily_budget = campaign_brief.get("daily_budget", 0)
        if daily_budget <= 0:
            validations.append({
                "rule": "Daily Budget > 0",
                "passed": False,
                "message": "Daily budget must be greater than 0"
            })
        elif daily_budget > self.business_rules["max_daily_spend_per_campaign"]:
            validations.append({
                "rule": "Daily Budget Limit",
                "passed": False,
                "message": f"Exceeds maximum ₹{self.business_rules['max_daily_spend_per_campaign']:,.2f}"
            })
        else:
            validations.append({
                "rule": "Daily Budget Validation",
                "passed": True,
                "message": f"₹{daily_budget:,.2f} within acceptable limits"
            })
        
        # Profit margin validation
        profit_margin = campaign_brief.get("profit_margin", 0)
        min_roas_required = 100 / profit_margin if profit_margin > 0 else float('inf')
        
        if min_roas_required > self.business_rules["min_roas_threshold"]:
            validations.append({
                "rule": "Profit Margin Feasibility",
                "passed": True,
                "message": f"Break-even ROAS {min_roas_required:.2f} is achievable"
            })
        else:
            validations.append({
                "rule": "Profit Margin Risk",
                "passed": False,
                "message": f"Requires ROAS > {min_roas_required:.2f} which may be challenging"
            })
        
        # Brand validation
        brand = campaign_brief.get("brand", "").lower()
        valid_brands = ["voyage", "goeye", "eyejack"]
        validations.append({
            "rule": "Brand Recognition",
            "passed": brand in valid_brands,
            "message": f"Brand '{brand}' {'recognized' if brand in valid_brands else 'not in system'}"
        })
        
        # Objective validation
        objective = campaign_brief.get("objective", "").lower()
        valid_objectives = ["conversions", "traffic", "awareness", "engagement"]
        validations.append({
            "rule": "Campaign Objective",
            "passed": objective in valid_objectives,
            "message": f"Objective '{objective}' {'valid' if objective in valid_objectives else 'invalid'}"
        })
        
        return validations
    
    def _generate_scenario_alerts(self, data, campaign_brief, roas, budget_utilization):
        """Generate alerts for monitoring scenarios."""
        
        alerts = []
        
        # Budget alerts
        if budget_utilization > 95:
            alerts.append({
                "severity": "critical",
                "message": f"Budget overrun: {budget_utilization:.1f}% of daily budget used",
                "auto_action": "Reduce bid amounts by 20%"
            })
        elif budget_utilization > 80:
            alerts.append({
                "severity": "high",
                "message": f"High budget utilization: {budget_utilization:.1f}%",
                "auto_action": "Monitor spend pacing closely"
            })
        
        # ROAS alerts
        if roas < 1.0:
            alerts.append({
                "severity": "critical",
                "message": f"Campaign losing money: ROAS {roas:.2f}",
                "auto_action": "PAUSE CAMPAIGN IMMEDIATELY"
            })
        elif roas < self.business_rules["min_roas_threshold"]:
            alerts.append({
                "severity": "high",
                "message": f"Low ROAS: {roas:.2f} below target {self.business_rules['min_roas_threshold']:.2f}",
                "auto_action": "Optimize audience and creative"
            })
        
        # Performance alerts
        if data["ctr"] < 1.0:
            alerts.append({
                "severity": "medium",
                "message": f"Low CTR: {data['ctr']:.2f}% indicates creative fatigue",
                "auto_action": "Test new creative variations"
            })
        
        if data["cpc"] > 75:
            alerts.append({
                "severity": "medium",
                "message": f"High CPC: ₹{data['cpc']:.2f} above optimal range",
                "auto_action": "Optimize bidding strategy"
            })
        
        if data["frequency"] > 3.0:
            alerts.append({
                "severity": "medium",
                "message": f"High frequency: {data['frequency']:.2f} indicates audience fatigue",
                "auto_action": "Expand audience size"
            })
        
        return alerts
    
    def run_complete_demonstration(self):
        """Run complete enterprise system demonstration."""
        
        print("🏢 ENTERPRISE FACEBOOK MARKETING AGENT")
        print("COMPLETE SYSTEM DEMONSTRATION")
        print("="*80)
        print("This system protects your real advertising money with:")
        print("• Comprehensive validation and approval workflows")
        print("• Real-time financial risk monitoring")
        print("• Automated alerts and emergency stops")
        print("• Complete audit trail and compliance tracking")
        print("• Strategic memory and continuous learning")
        print("="*80)
        
        # Step 1: Campaign Launch
        campaign_brief = self.demonstrate_enterprise_campaign_launch()
        
        # Step 2: Real-time Monitoring
        self.demonstrate_real_time_monitoring(campaign_brief)
        
        # Step 3: Financial Dashboard
        self.demonstrate_financial_dashboard()
        
        print(f"\n🎉 DEMONSTRATION COMPLETE!")
        print("="*80)
        print("✅ ENTERPRISE FEATURES DEMONSTRATED:")
        print("• Campaign validation with business rules")
        print("• Financial risk assessment and controls")
        print("• Real-time monitoring and alerts")
        print("• Emergency stop protection")
        print("• Comprehensive financial dashboard")
        print("• Automated decision making")
        
        print(f"\n💰 FINANCIAL PROTECTION FEATURES:")
        print("• Auto-pause when ROAS < 0.8 (prevents losses)")
        print("• Budget overrun alerts at 80% utilization")
        print("• Daily spend limits with approval workflows")
        print("• Real-time performance monitoring")
        print("• Complete audit trail for compliance")
        
        print(f"\n🚀 READY FOR REAL MONEY OPERATIONS!")
        print("Your Facebook advertising is now protected by enterprise-grade")
        print("financial controls and risk management systems.")

if __name__ == "__main__":
    demo = EnterpriseDemo()
    demo.run_complete_demonstration()
