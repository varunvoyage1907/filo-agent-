"""
Demonstration of the Marketing Agent Memory System
Shows how the agent remembers campaigns, decisions, and learnings.
"""
from marketing_agent import MarketingAgent
from datetime import datetime
import json

def demo_campaign_launch():
    """Demonstrate campaign launch with memory tracking."""
    
    print("🚀 DEMO: Campaign Launch with Memory")
    print("="*50)
    
    agent = MarketingAgent()
    
    # Create a sample campaign brief
    campaign_brief = {
        "name": "Voyage Summer Collection 2024",
        "brand": "Voyage",
        "objective": "conversions",
        "target_audience": {
            "age_range": "25-45",
            "interests": ["fashion", "eyewear", "lifestyle"],
            "location": "India"
        },
        "budget": {
            "daily_budget": 2000,  # INR
            "total_budget": 60000   # INR
        },
        "expected_outcome": "Increase summer collection sales by 25%"
    }
    
    # Launch campaign
    result = agent.launch_campaign(campaign_brief)
    
    print(f"\n📊 Campaign Launch Result:")
    print(f"Status: {result['status']}")
    print(f"Campaign ID: {result['campaign_data']['id']}")
    print(f"Recommendations: {len(result['strategic_brief'].get('recommendations', []))}")
    
    return result['campaign_data']['id']

def demo_performance_analysis(campaign_id):
    """Demonstrate performance analysis with memory context."""
    
    print(f"\n📊 DEMO: Performance Analysis with Memory")
    print("="*50)
    
    agent = MarketingAgent()
    
    # Simulate performance data
    simulated_performance = {
        "impressions": "15000",
        "clicks": "450",
        "spend": "1800.50",
        "ctr": "3.0",
        "cpc": "4.00",
        "conversions": "25",
        "cost_per_conversion": "72.02"
    }
    
    # Update performance in memory
    agent.campaign_tracker.update_performance(campaign_id, simulated_performance)
    
    # Analyze performance
    analysis = agent.analyze_performance(campaign_id=campaign_id)
    
    print(f"\n📈 Performance Analysis:")
    print(f"Campaign ID: {analysis.get('campaign_id', 'Unknown')}")
    print(f"Current CTR: {simulated_performance['ctr']}%")
    print(f"Current CPC: ₹{simulated_performance['cpc']}")
    print(f"Recommendations: {len(analysis.get('recommendations', []))}")
    
    return analysis

def demo_optimization(campaign_id):
    """Demonstrate campaign optimization with memory."""
    
    print(f"\n🔧 DEMO: Campaign Optimization with Memory")
    print("="*50)
    
    agent = MarketingAgent()
    
    # Optimize campaign
    optimization_params = {
        "audience_expansion": True,
        "budget_increase": 500,  # INR
        "creative_refresh": True,
        "expected_impact": "15% CTR improvement"
    }
    
    result = agent.optimize_campaign(
        campaign_id=campaign_id,
        optimization_type="audience",
        parameters=optimization_params
    )
    
    print(f"\n⚡ Optimization Result:")
    print(f"Status: {result['status']}")
    print(f"Type: {result['optimization_type']}")
    print(f"Expected Impact: {result['expected_impact']}")
    
    return result

def demo_memory_persistence():
    """Demonstrate how memory persists across sessions."""
    
    print(f"\n💾 DEMO: Memory Persistence")
    print("="*50)
    
    # Create new agent instance (simulating new session)
    agent = MarketingAgent()
    
    # Generate comprehensive report
    report = agent.generate_session_report()
    print(report)
    
    # Show memory files created
    import os
    memory_files = []
    for file in os.listdir('.'):
        if file.endswith('.json'):
            memory_files.append(file)
    
    print(f"\n📁 Memory Files Created:")
    for file in memory_files:
        size = os.path.getsize(file)
        print(f"  📄 {file} ({size} bytes)")

def demo_brand_analysis():
    """Demonstrate brand-level analysis with memory."""
    
    print(f"\n🏷️ DEMO: Brand Analysis with Memory")
    print("="*50)
    
    agent = MarketingAgent()
    
    # Add some sample learnings
    agent.strategic_memory.log_campaign_learning(
        brand="Voyage",
        campaign_id="demo_campaign_001",
        learning_type="audience_insight",
        insight="25-35 age group shows 40% higher engagement with lifestyle-focused creatives",
        data={"engagement_rate": 4.2, "age_group": "25-35", "creative_type": "lifestyle"}
    )
    
    agent.strategic_memory.log_campaign_learning(
        brand="Voyage",
        campaign_id="demo_campaign_002", 
        learning_type="creative_insight",
        insight="Video ads outperform image ads by 60% for summer collection",
        data={"video_ctr": 3.2, "image_ctr": 2.0, "collection": "summer"}
    )
    
    # Analyze brand
    analysis = agent.analyze_performance(brand="Voyage")
    
    print(f"\n📊 Brand Analysis:")
    print(f"Brand: {analysis.get('brand', 'Unknown')}")
    print(f"Total Campaigns: {analysis.get('total_campaigns', 0)}")
    print(f"Active Campaigns: {analysis.get('active_campaigns', 0)}")
    print(f"Key Learnings: {len(analysis.get('brand_context', {}).get('key_learnings', []))}")

def main():
    """Run complete memory system demonstration."""
    
    print("🤖 FACEBOOK MARKETING AGENT MEMORY SYSTEM DEMO")
    print("="*60)
    print("This demo shows how the agent remembers everything:")
    print("• Campaign launches and strategies")
    print("• Performance data and trends") 
    print("• Optimizations and their outcomes")
    print("• Strategic decisions and reasoning")
    print("• Brand learnings and insights")
    print("="*60)
    
    # Demo 1: Campaign Launch
    campaign_id = demo_campaign_launch()
    
    # Demo 2: Performance Analysis  
    analysis = demo_performance_analysis(campaign_id)
    
    # Demo 3: Optimization
    optimization = demo_optimization(campaign_id)
    
    # Demo 4: Brand Analysis
    demo_brand_analysis()
    
    # Demo 5: Memory Persistence
    demo_memory_persistence()
    
    print(f"\n🎉 DEMO COMPLETE!")
    print("="*60)
    print("✅ Campaign launched and tracked")
    print("✅ Performance analyzed with context")
    print("✅ Optimization applied and logged")
    print("✅ Brand insights captured")
    print("✅ Memory persisted to files")
    print("\n💡 Key Benefits:")
    print("• Every action is remembered")
    print("• Context is maintained across sessions")
    print("• Decisions are based on historical data")
    print("• Learnings compound over time")
    print("• Strategic insights improve with experience")

if __name__ == "__main__":
    main()
