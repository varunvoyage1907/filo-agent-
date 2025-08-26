"""
Facebook Campaign Tracker & Memory System
Comprehensive tracking for all campaign activities, performance, and insights.
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from facebook_ads_client import FacebookAdsClient
from config import FacebookConfig

class CampaignTracker:
    """Tracks all campaign activities, performance, and strategic decisions."""
    
    def __init__(self, data_file: str = "campaign_memory.json"):
        self.data_file = data_file
        self.memory = self._load_memory()
        self.client = FacebookAdsClient()
    
    def _load_memory(self) -> Dict[str, Any]:
        """Load existing campaign memory from file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading memory: {e}")
                return self._create_empty_memory()
        return self._create_empty_memory()
    
    def _create_empty_memory(self) -> Dict[str, Any]:
        """Create empty memory structure."""
        return {
            "campaigns": {},
            "strategies": {},
            "performance_history": {},
            "insights": {},
            "decisions": {},
            "brand_profiles": {},
            "audience_insights": {},
            "creative_performance": {},
            "budget_allocations": {},
            "seasonal_patterns": {},
            "last_updated": None
        }
    
    def save_memory(self):
        """Save current memory to file."""
        self.memory["last_updated"] = datetime.now().isoformat()
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.memory, f, indent=2, default=str)
            print(f"✅ Memory saved to {self.data_file}")
        except Exception as e:
            print(f"❌ Error saving memory: {e}")
    
    def log_campaign_launch(self, campaign_data: Dict[str, Any], strategy: str, reasoning: str):
        """Log a new campaign launch with full context."""
        campaign_id = campaign_data.get('id')
        timestamp = datetime.now().isoformat()
        
        self.memory["campaigns"][campaign_id] = {
            "launch_date": timestamp,
            "campaign_data": campaign_data,
            "strategy": strategy,
            "reasoning": reasoning,
            "status": "active",
            "performance_snapshots": [],
            "optimizations": [],
            "insights": []
        }
        
        # Log the strategic decision
        self.memory["decisions"][timestamp] = {
            "type": "campaign_launch",
            "campaign_id": campaign_id,
            "strategy": strategy,
            "reasoning": reasoning,
            "expected_outcome": campaign_data.get('expected_outcome', 'Not specified')
        }
        
        self.save_memory()
        print(f"📝 Logged campaign launch: {campaign_data.get('name', campaign_id)}")
    
    def update_performance(self, campaign_id: str, performance_data: Dict[str, Any]):
        """Update campaign performance data."""
        if campaign_id not in self.memory["campaigns"]:
            print(f"⚠️ Campaign {campaign_id} not found in memory")
            return
        
        timestamp = datetime.now().isoformat()
        snapshot = {
            "timestamp": timestamp,
            "performance": performance_data,
            "analysis": self._analyze_performance(performance_data)
        }
        
        self.memory["campaigns"][campaign_id]["performance_snapshots"].append(snapshot)
        
        # Update performance history
        if campaign_id not in self.memory["performance_history"]:
            self.memory["performance_history"][campaign_id] = []
        
        self.memory["performance_history"][campaign_id].append(snapshot)
        self.save_memory()
    
    def _analyze_performance(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance data and provide insights."""
        analysis = {
            "status": "unknown",
            "trends": [],
            "recommendations": [],
            "alerts": []
        }
        
        # Basic performance analysis
        ctr = float(performance_data.get('ctr', 0))
        cpc = float(performance_data.get('cpc', 0))
        spend = float(performance_data.get('spend', 0))
        
        # CTR Analysis
        if ctr > 2.0:
            analysis["status"] = "excellent"
            analysis["trends"].append("High CTR indicates strong creative performance")
        elif ctr > 1.0:
            analysis["status"] = "good"
        elif ctr < 0.5:
            analysis["status"] = "poor"
            analysis["alerts"].append("Low CTR - creative needs optimization")
            analysis["recommendations"].append("Test new creative variations")
        
        # CPC Analysis
        if cpc > 50:  # Assuming INR
            analysis["alerts"].append("High CPC - audience or creative optimization needed")
            analysis["recommendations"].append("Refine audience targeting")
        
        return analysis
    
    def log_optimization(self, campaign_id: str, optimization_type: str, changes: Dict[str, Any], reasoning: str):
        """Log campaign optimizations."""
        if campaign_id not in self.memory["campaigns"]:
            print(f"⚠️ Campaign {campaign_id} not found in memory")
            return
        
        timestamp = datetime.now().isoformat()
        optimization = {
            "timestamp": timestamp,
            "type": optimization_type,
            "changes": changes,
            "reasoning": reasoning,
            "expected_impact": changes.get('expected_impact', 'Not specified')
        }
        
        self.memory["campaigns"][campaign_id]["optimizations"].append(optimization)
        
        # Log as decision
        self.memory["decisions"][timestamp] = {
            "type": "optimization",
            "campaign_id": campaign_id,
            "optimization_type": optimization_type,
            "reasoning": reasoning,
            "changes": changes
        }
        
        self.save_memory()
        print(f"🔧 Logged optimization for campaign {campaign_id}")
    
    def get_campaign_summary(self, campaign_id: str) -> Dict[str, Any]:
        """Get comprehensive campaign summary."""
        if campaign_id not in self.memory["campaigns"]:
            return {"error": "Campaign not found in memory"}
        
        campaign = self.memory["campaigns"][campaign_id]
        
        # Get latest performance
        latest_performance = None
        if campaign["performance_snapshots"]:
            latest_performance = campaign["performance_snapshots"][-1]
        
        return {
            "campaign_id": campaign_id,
            "launch_date": campaign["launch_date"],
            "strategy": campaign["strategy"],
            "status": campaign["status"],
            "total_optimizations": len(campaign["optimizations"]),
            "performance_snapshots": len(campaign["performance_snapshots"]),
            "latest_performance": latest_performance,
            "recent_optimizations": campaign["optimizations"][-3:] if campaign["optimizations"] else []
        }
    
    def get_brand_overview(self, brand_name: str = None) -> Dict[str, Any]:
        """Get overview of all campaigns for a brand or all brands."""
        overview = {
            "total_campaigns": len(self.memory["campaigns"]),
            "active_campaigns": 0,
            "total_optimizations": 0,
            "recent_decisions": [],
            "performance_trends": {}
        }
        
        # Count active campaigns and optimizations
        for campaign_id, campaign in self.memory["campaigns"].items():
            if campaign["status"] == "active":
                overview["active_campaigns"] += 1
            overview["total_optimizations"] += len(campaign["optimizations"])
        
        # Get recent decisions (last 10)
        recent_decisions = sorted(
            self.memory["decisions"].items(),
            key=lambda x: x[0],
            reverse=True
        )[:10]
        
        overview["recent_decisions"] = [
            {
                "timestamp": timestamp,
                "type": decision["type"],
                "campaign_id": decision.get("campaign_id"),
                "reasoning": decision["reasoning"][:100] + "..." if len(decision["reasoning"]) > 100 else decision["reasoning"]
            }
            for timestamp, decision in recent_decisions
        ]
        
        return overview
    
    def sync_with_facebook(self):
        """Sync memory with current Facebook campaign data."""
        print("🔄 Syncing with Facebook Ads API...")
        
        try:
            # Get current campaigns
            campaigns = self.client.get_campaigns(limit=50)
            
            for campaign in campaigns:
                campaign_id = campaign['id']
                
                # Update campaign status if it exists in memory
                if campaign_id in self.memory["campaigns"]:
                    self.memory["campaigns"][campaign_id]["current_fb_status"] = campaign['status']
                    
                    # Get and update performance
                    try:
                        insights = self.client.get_campaign_insights(campaign_id)
                        if insights and 'error' not in insights:
                            self.update_performance(campaign_id, insights)
                    except Exception as e:
                        print(f"⚠️ Could not get insights for {campaign_id}: {e}")
            
            print("✅ Sync completed")
            
        except Exception as e:
            print(f"❌ Sync failed: {e}")
    
    def generate_report(self) -> str:
        """Generate comprehensive campaign report."""
        overview = self.get_brand_overview()
        
        report = f"""
📊 CAMPAIGN MEMORY REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*50}

📈 OVERVIEW:
• Total Campaigns Tracked: {overview['total_campaigns']}
• Active Campaigns: {overview['active_campaigns']}
• Total Optimizations Made: {overview['total_optimizations']}

🎯 RECENT STRATEGIC DECISIONS:
"""
        
        for decision in overview['recent_decisions'][:5]:
            report += f"""
• {decision['timestamp'][:10]} - {decision['type'].title()}
  Campaign: {decision['campaign_id']}
  Reasoning: {decision['reasoning']}
"""
        
        report += f"""
💾 DATA INTEGRITY:
• Memory File: {self.data_file}
• Last Updated: {self.memory.get('last_updated', 'Never')}
• Backup Status: {'✅ Available' if os.path.exists(self.data_file) else '❌ Missing'}

🔄 SYNC STATUS:
• Facebook API: {'✅ Connected' if self.client else '❌ Disconnected'}
• Real-time Data: Available
"""
        
        return report

def create_campaign_brief_template():
    """Create a template for campaign briefs."""
    template = {
        "campaign_name": "",
        "brand": "",
        "objective": "",
        "target_audience": {
            "demographics": {},
            "interests": [],
            "behaviors": [],
            "custom_audiences": []
        },
        "budget": {
            "daily_budget": 0,
            "total_budget": 0,
            "bid_strategy": ""
        },
        "creative_strategy": {
            "ad_formats": [],
            "messaging": "",
            "visual_style": "",
            "call_to_action": ""
        },
        "success_metrics": {
            "primary_kpi": "",
            "target_ctr": 0,
            "target_cpc": 0,
            "target_roas": 0
        },
        "timeline": {
            "start_date": "",
            "end_date": "",
            "review_dates": []
        },
        "strategic_reasoning": "",
        "expected_challenges": [],
        "contingency_plans": []
    }
    
    return template

if __name__ == "__main__":
    # Example usage
    tracker = CampaignTracker()
    print(tracker.generate_report())
