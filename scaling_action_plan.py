"""
Facebook Ads Scaling Action Plan
Step-by-step guide for scaling campaigns with ROAS 5.29
"""

def generate_scaling_plan():
    """Generate comprehensive scaling action plan."""
    
    print("🚀 FACEBOOK ADS SCALING ACTION PLAN")
    print("Current ROAS: 5.29 (Excellent!) - Ready for Aggressive Scaling")
    print("="*70)
    
    print("\n📋 IMMEDIATE ACTIONS (Next 24 Hours)")
    print("="*50)
    
    immediate_actions = [
        {
            "priority": "🔴 CRITICAL",
            "action": "Increase Budgets on Top Performers",
            "details": [
                "Go to Facebook Ads Manager",
                "Find your best performing campaigns from yesterday",
                "Increase daily budgets by 30-40%",
                "Example: ₹1000 → ₹1300-1400"
            ],
            "expected_result": "20-30% more revenue within 2-3 days"
        },
        {
            "priority": "🟠 HIGH",
            "action": "Monitor Spend Pacing",
            "details": [
                "Check every 4 hours for first 48 hours",
                "Ensure campaigns are spending the increased budget",
                "Watch for delivery issues or audience saturation",
                "Adjust if spend is too fast or too slow"
            ],
            "expected_result": "Smooth budget scaling without performance drops"
        },
        {
            "priority": "🟡 MEDIUM",
            "action": "Duplicate Best Campaign",
            "details": [
                "Find your highest ROAS campaign",
                "Duplicate it with same settings",
                "Change campaign name (add 'v2' or 'Scale')",
                "Start with 50% of original budget"
            ],
            "expected_result": "Additional revenue stream with proven performance"
        }
    ]
    
    for action in immediate_actions:
        print(f"\n{action['priority']}: {action['action']}")
        print("Steps:")
        for i, step in enumerate(action['details'], 1):
            print(f"  {i}. {step}")
        print(f"Expected Result: {action['expected_result']}")
    
    print("\n📊 THIS WEEK ACTIONS (Days 2-7)")
    print("="*50)
    
    weekly_actions = [
        {
            "day": "Day 2-3",
            "action": "Audience Expansion",
            "steps": [
                "Create lookalike audiences from recent purchasers",
                "Test 1% and 2% lookalikes",
                "Expand age ranges (e.g., 25-45 → 22-55)",
                "Add related interests to existing campaigns"
            ]
        },
        {
            "day": "Day 4-5", 
            "action": "Creative Testing",
            "steps": [
                "Create 3-5 new ad variations",
                "Test different headlines and descriptions",
                "Try new image/video formats",
                "A/B test call-to-action buttons"
            ]
        },
        {
            "day": "Day 6-7",
            "action": "Budget Optimization",
            "steps": [
                "Analyze which campaigns scaled best",
                "Reallocate budget from poor performers",
                "Increase budgets again on winners (20-30%)",
                "Pause any campaigns with ROAS < 3.0"
            ]
        }
    ]
    
    for action in weekly_actions:
        print(f"\n📅 {action['day']}: {action['action']}")
        for i, step in enumerate(action['steps'], 1):
            print(f"  {i}. {step}")
    
    print("\n🎯 SPECIFIC BUDGET SCALING STRATEGY")
    print("="*50)
    
    scaling_strategy = {
        "Week 1": {
            "increase": "30-40%",
            "rationale": "Conservative scaling to test performance",
            "example": "₹1000 → ₹1300-1400",
            "monitor": "Daily performance checks"
        },
        "Week 2": {
            "increase": "25-30%", 
            "rationale": "If Week 1 maintains ROAS > 4.0",
            "example": "₹1400 → ₹1750-1820",
            "monitor": "Every 2 days"
        },
        "Week 3": {
            "increase": "20-25%",
            "rationale": "Continued scaling if ROAS > 3.5",
            "example": "₹1800 → ₹2160-2250",
            "monitor": "Weekly reviews"
        },
        "Week 4": {
            "increase": "15-20%",
            "rationale": "Mature scaling phase",
            "example": "₹2200 → ₹2530-2640",
            "monitor": "Bi-weekly optimization"
        }
    }
    
    for week, strategy in scaling_strategy.items():
        print(f"\n📈 {week}:")
        print(f"  • Increase: {strategy['increase']}")
        print(f"  • Rationale: {strategy['rationale']}")
        print(f"  • Example: {strategy['example']}")
        print(f"  • Monitor: {strategy['monitor']}")
    
    print("\n⚠️ SCALING SAFETY RULES")
    print("="*50)
    
    safety_rules = [
        "Never increase budget by more than 50% in one day",
        "If ROAS drops below 4.0, pause scaling for 2 days",
        "If ROAS drops below 3.0, reduce budgets by 20%",
        "If ROAS drops below 2.0, pause campaign immediately",
        "Monitor frequency - if > 3.0, expand audiences",
        "Check CPC trends - if increases > 50%, optimize targeting"
    ]
    
    for i, rule in enumerate(safety_rules, 1):
        print(f"  {i}. {rule}")
    
    print("\n🎨 CREATIVE REFRESH SCHEDULE")
    print("="*50)
    
    creative_schedule = {
        "Week 1": "Test 2-3 new ad variations",
        "Week 2": "Refresh underperforming creatives", 
        "Week 3": "Test new formats (video if using images)",
        "Week 4": "Seasonal/trending creative updates",
        "Monthly": "Complete creative audit and refresh"
    }
    
    for period, task in creative_schedule.items():
        print(f"  📅 {period}: {task}")
    
    print("\n📊 PERFORMANCE MONITORING CHECKLIST")
    print("="*50)
    
    monitoring_checklist = {
        "Daily (First Week)": [
            "Check total spend vs budget",
            "Monitor overall ROAS",
            "Watch for delivery issues",
            "Check frequency levels"
        ],
        "Every 2 Days": [
            "Analyze campaign-level ROAS",
            "Review CTR trends",
            "Check CPC changes",
            "Monitor conversion rates"
        ],
        "Weekly": [
            "Complete performance review",
            "Budget reallocation decisions",
            "Creative performance analysis",
            "Audience expansion planning"
        ]
    }
    
    for frequency, tasks in monitoring_checklist.items():
        print(f"\n⏰ {frequency}:")
        for task in tasks:
            print(f"  ✅ {task}")
    
    print("\n💰 EXPECTED RESULTS")
    print("="*50)
    
    print("If you follow this plan with ROAS 5.29:")
    print("• Week 1: 20-30% revenue increase")
    print("• Week 2: 40-60% revenue increase (cumulative)")
    print("• Week 3: 60-90% revenue increase (cumulative)")
    print("• Month 1: 80-120% revenue increase")
    print()
    print("Conservative Estimate:")
    print("• Current daily revenue: ~₹46,000 (with ₹8,731 spend)")
    print("• After scaling: ~₹80,000-100,000 daily revenue")
    print("• Monthly increase: +₹1,000,000-1,500,000")
    
    print("\n🚨 RED FLAGS - STOP SCALING IF:")
    print("="*50)
    
    red_flags = [
        "ROAS drops below 3.0 for 2+ days",
        "CPC increases by more than 100%",
        "CTR drops below 0.5%",
        "Frequency exceeds 4.0",
        "Conversion rate drops by 50%+",
        "Quality score drops below 6.0"
    ]
    
    for flag in red_flags:
        print(f"  🚨 {flag}")
    
    print("\n✅ SUCCESS INDICATORS - CONTINUE SCALING:")
    print("="*50)
    
    success_indicators = [
        "ROAS maintains above 4.0",
        "CPC remains stable or decreases",
        "CTR stays above 1.0%",
        "Frequency below 3.0",
        "Consistent daily conversions",
        "Smooth budget delivery"
    ]
    
    for indicator in success_indicators:
        print(f"  ✅ {indicator}")

def generate_facebook_ads_manager_guide():
    """Step-by-step guide for Facebook Ads Manager."""
    
    print("\n\n🖥️ FACEBOOK ADS MANAGER - STEP BY STEP GUIDE")
    print("="*70)
    
    print("\n📱 HOW TO INCREASE BUDGETS:")
    print("="*40)
    
    budget_steps = [
        "1. Go to business.facebook.com",
        "2. Select your GoEye3.0 ad account",
        "3. Click on 'Campaigns' tab",
        "4. Find your best performing campaign",
        "5. Click the campaign name to select it",
        "6. Click 'Edit' button at the top",
        "7. Find 'Budget & Schedule' section",
        "8. Increase daily budget by 30-40%",
        "9. Click 'Publish' to save changes",
        "10. Repeat for other high-performing campaigns"
    ]
    
    for step in budget_steps:
        print(f"   {step}")
    
    print("\n🔄 HOW TO DUPLICATE CAMPAIGNS:")
    print("="*40)
    
    duplicate_steps = [
        "1. In Campaigns tab, select your best campaign",
        "2. Click 'Duplicate' button at the top",
        "3. Choose 'Duplicate campaign'",
        "4. Rename it (add 'v2' or 'Scale')",
        "5. Set budget to 50% of original",
        "6. Keep all other settings the same",
        "7. Click 'Publish' to create",
        "8. Monitor both campaigns separately"
    ]
    
    for step in duplicate_steps:
        print(f"   {step}")
    
    print("\n👥 HOW TO CREATE LOOKALIKE AUDIENCES:")
    print("="*40)
    
    lookalike_steps = [
        "1. Go to Audiences section in Ads Manager",
        "2. Click 'Create Audience' → 'Lookalike Audience'",
        "3. Choose source: 'Website Custom Audience' or 'Pixel'",
        "4. Select 'Purchase' events from last 30 days",
        "5. Choose location: India",
        "6. Set audience size: 1% (most similar)",
        "7. Click 'Create Audience'",
        "8. Use this audience in new ad sets"
    ]
    
    for step in lookalike_steps:
        print(f"   {step}")

if __name__ == "__main__":
    generate_scaling_plan()
    generate_facebook_ads_manager_guide()
