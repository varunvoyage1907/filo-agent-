"""
Strategic Memory System for Facebook Marketing
Maintains context, learnings, and strategic insights across sessions.
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from campaign_tracker import CampaignTracker

class StrategicMemory:
    """Maintains strategic context and learnings for marketing decisions."""
    
    def __init__(self, memory_file: str = "strategic_memory.json"):
        self.memory_file = memory_file
        self.memory = self._load_memory()
        self.campaign_tracker = CampaignTracker()
    
    def _load_memory(self) -> Dict[str, Any]:
        """Load strategic memory from file."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading strategic memory: {e}")
                return self._create_empty_memory()
        return self._create_empty_memory()
    
    def _create_empty_memory(self) -> Dict[str, Any]:
        """Create empty strategic memory structure."""
        return {
            "brand_strategies": {
                "voyage": {
                    "positioning": "",
                    "target_demographics": {},
                    "successful_campaigns": [],
                    "failed_campaigns": [],
                    "learnings": [],
                    "seasonal_patterns": {},
                    "competitor_insights": {}
                },
                "goeye": {
                    "positioning": "",
                    "target_demographics": {},
                    "successful_campaigns": [],
                    "failed_campaigns": [],
                    "learnings": [],
                    "seasonal_patterns": {},
                    "competitor_insights": {}
                },
                "eyejack": {
                    "positioning": "",
                    "target_demographics": {},
                    "successful_campaigns": [],
                    "failed_campaigns": [],
                    "learnings": [],
                    "seasonal_patterns": {},
                    "competitor_insights": {}
                }
            },
            "audience_insights": {
                "high_performing_audiences": [],
                "audience_fatigue_patterns": {},
                "demographic_preferences": {},
                "behavioral_insights": {}
            },
            "creative_insights": {
                "winning_creative_patterns": [],
                "creative_fatigue_cycles": {},
                "format_performance": {},
                "messaging_insights": {}
            },
            "market_insights": {
                "seasonal_trends": {},
                "competitive_landscape": {},
                "market_opportunities": [],
                "threats": []
            },
            "optimization_playbook": {
                "proven_strategies": [],
                "optimization_sequences": [],
                "emergency_protocols": [],
                "scaling_strategies": []
            },
            "performance_benchmarks": {
                "industry_benchmarks": {},
                "brand_benchmarks": {},
                "campaign_type_benchmarks": {}
            },
            "strategic_decisions": [],
            "lessons_learned": [],
            "future_strategies": [],
            "last_updated": None
        }
    
    def save_memory(self):
        """Save strategic memory to file."""
        self.memory["last_updated"] = datetime.now().isoformat()
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=2, default=str)
            print(f"✅ Strategic memory saved to {self.memory_file}")
        except Exception as e:
            print(f"❌ Error saving strategic memory: {e}")
    
    def log_strategic_decision(self, decision_type: str, context: Dict[str, Any], reasoning: str, expected_outcome: str):
        """Log a strategic marketing decision."""
        decision = {
            "timestamp": datetime.now().isoformat(),
            "type": decision_type,
            "context": context,
            "reasoning": reasoning,
            "expected_outcome": expected_outcome,
            "actual_outcome": None,  # To be updated later
            "lessons_learned": []
        }
        
        self.memory["strategic_decisions"].append(decision)
        self.save_memory()
        print(f"📝 Logged strategic decision: {decision_type}")
    
    def update_decision_outcome(self, decision_index: int, actual_outcome: str, lessons: List[str]):
        """Update the outcome of a strategic decision."""
        if decision_index < len(self.memory["strategic_decisions"]):
            self.memory["strategic_decisions"][decision_index]["actual_outcome"] = actual_outcome
            self.memory["strategic_decisions"][decision_index]["lessons_learned"] = lessons
            
            # Add to general lessons learned
            for lesson in lessons:
                self.memory["lessons_learned"].append({
                    "timestamp": datetime.now().isoformat(),
                    "lesson": lesson,
                    "context": self.memory["strategic_decisions"][decision_index]["context"]
                })
            
            self.save_memory()
            print(f"✅ Updated decision outcome and lessons learned")
    
    def log_campaign_learning(self, brand: str, campaign_id: str, learning_type: str, insight: str, data: Dict[str, Any]):
        """Log learnings from campaign performance."""
        learning = {
            "timestamp": datetime.now().isoformat(),
            "campaign_id": campaign_id,
            "type": learning_type,
            "insight": insight,
            "supporting_data": data
        }
        
        brand_lower = brand.lower()
        if brand_lower in self.memory["brand_strategies"]:
            self.memory["brand_strategies"][brand_lower]["learnings"].append(learning)
            self.save_memory()
            print(f"📚 Logged learning for {brand}: {learning_type}")
    
    def get_brand_context(self, brand: str) -> Dict[str, Any]:
        """Get comprehensive context for a brand."""
        brand_lower = brand.lower()
        if brand_lower not in self.memory["brand_strategies"]:
            return {"error": f"Brand {brand} not found in memory"}
        
        brand_data = self.memory["brand_strategies"][brand_lower]
        
        # Get recent campaign performance from campaign tracker
        recent_campaigns = []
        for campaign_id, campaign in self.campaign_tracker.memory["campaigns"].items():
            if brand_lower in campaign.get("campaign_data", {}).get("name", "").lower():
                recent_campaigns.append(self.campaign_tracker.get_campaign_summary(campaign_id))
        
        return {
            "brand": brand,
            "strategy": brand_data,
            "recent_campaigns": recent_campaigns[-5:],  # Last 5 campaigns
            "key_learnings": brand_data["learnings"][-10:],  # Last 10 learnings
            "performance_context": self._get_performance_context(brand_lower)
        }
    
    def _get_performance_context(self, brand: str) -> Dict[str, Any]:
        """Get performance context for strategic decisions."""
        # This would analyze historical performance patterns
        return {
            "best_performing_periods": [],
            "audience_fatigue_indicators": [],
            "creative_refresh_needs": [],
            "budget_optimization_opportunities": []
        }
    
    def generate_strategic_brief(self, brand: str, campaign_objective: str) -> Dict[str, Any]:
        """Generate a strategic brief based on memory and context."""
        brand_context = self.get_brand_context(brand)
        
        if "error" in brand_context:
            return brand_context
        
        brief = {
            "brand": brand,
            "objective": campaign_objective,
            "strategic_context": {
                "brand_positioning": brand_context["strategy"]["positioning"],
                "proven_audiences": [learning["insight"] for learning in brand_context["key_learnings"] 
                                   if learning["type"] == "audience_insight"],
                "successful_creatives": [learning["insight"] for learning in brand_context["key_learnings"] 
                                       if learning["type"] == "creative_insight"],
                "seasonal_considerations": brand_context["strategy"]["seasonal_patterns"],
                "competitive_landscape": brand_context["strategy"]["competitor_insights"]
            },
            "recommendations": self._generate_recommendations(brand_context, campaign_objective),
            "risk_factors": self._identify_risk_factors(brand_context),
            "success_metrics": self._suggest_success_metrics(brand_context, campaign_objective),
            "optimization_plan": self._create_optimization_plan(brand_context)
        }
        
        return brief
    
    def _generate_recommendations(self, brand_context: Dict[str, Any], objective: str) -> List[str]:
        """Generate strategic recommendations based on context."""
        recommendations = []
        
        # Analyze past successful campaigns
        successful_patterns = []
        for learning in brand_context["key_learnings"]:
            if "successful" in learning.get("insight", "").lower():
                successful_patterns.append(learning["insight"])
        
        if successful_patterns:
            recommendations.append(f"Leverage proven patterns: {', '.join(successful_patterns[:3])}")
        
        # Add objective-specific recommendations
        if objective.lower() in ["conversions", "purchase"]:
            recommendations.append("Focus on high-intent audiences and retargeting")
            recommendations.append("Use social proof and urgency in creative messaging")
        elif objective.lower() in ["awareness", "reach"]:
            recommendations.append("Prioritize broad audience reach with engaging creative")
            recommendations.append("Test video content for higher engagement rates")
        
        return recommendations
    
    def _identify_risk_factors(self, brand_context: Dict[str, Any]) -> List[str]:
        """Identify potential risk factors based on historical data."""
        risks = []
        
        # Analyze failed campaigns for patterns
        failed_patterns = []
        for learning in brand_context["key_learnings"]:
            if "failed" in learning.get("insight", "").lower() or "poor" in learning.get("insight", "").lower():
                failed_patterns.append(learning["insight"])
        
        if failed_patterns:
            risks.append(f"Avoid patterns that led to poor performance: {', '.join(failed_patterns[:2])}")
        
        # Add general risks
        risks.extend([
            "Monitor audience fatigue indicators",
            "Watch for creative performance decline",
            "Be prepared for seasonal fluctuations"
        ])
        
        return risks
    
    def _suggest_success_metrics(self, brand_context: Dict[str, Any], objective: str) -> Dict[str, Any]:
        """Suggest success metrics based on context and objective."""
        base_metrics = {
            "primary_kpi": "",
            "target_ctr": 1.5,
            "target_cpc": 30,  # INR
            "target_roas": 4.0
        }
        
        if objective.lower() in ["conversions", "purchase"]:
            base_metrics["primary_kpi"] = "ROAS"
            base_metrics["target_roas"] = 4.0
        elif objective.lower() in ["awareness", "reach"]:
            base_metrics["primary_kpi"] = "CPM"
            base_metrics["target_cpm"] = 100  # INR
        elif objective.lower() in ["traffic", "clicks"]:
            base_metrics["primary_kpi"] = "CPC"
            base_metrics["target_cpc"] = 25  # INR
        
        return base_metrics
    
    def _create_optimization_plan(self, brand_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create an optimization plan based on historical learnings."""
        plan = [
            {
                "timeline": "Day 1-3",
                "action": "Monitor initial performance and audience response",
                "trigger": "Campaign launch",
                "expected_outcome": "Baseline performance establishment"
            },
            {
                "timeline": "Day 4-7",
                "action": "Optimize based on early performance indicators",
                "trigger": "Performance data availability",
                "expected_outcome": "Improved efficiency"
            },
            {
                "timeline": "Week 2",
                "action": "Scale winning ad sets and pause underperformers",
                "trigger": "Clear performance patterns",
                "expected_outcome": "Increased ROI"
            },
            {
                "timeline": "Week 3-4",
                "action": "Test new creative variations and audiences",
                "trigger": "Potential creative fatigue",
                "expected_outcome": "Sustained performance"
            }
        ]
        
        return plan
    
    def create_session_context(self) -> str:
        """Create context summary for new sessions."""
        overview = {
            "total_decisions": len(self.memory["strategic_decisions"]),
            "total_learnings": sum(len(brand["learnings"]) for brand in self.memory["brand_strategies"].values()),
            "recent_activity": []
        }
        
        # Get recent strategic decisions
        recent_decisions = sorted(
            self.memory["strategic_decisions"],
            key=lambda x: x["timestamp"],
            reverse=True
        )[:5]
        
        context = f"""
🧠 STRATEGIC MEMORY CONTEXT
{'='*40}

📊 MEMORY OVERVIEW:
• Strategic Decisions Tracked: {overview['total_decisions']}
• Brand Learnings Captured: {overview['total_learnings']}
• Last Updated: {self.memory.get('last_updated', 'Never')}

🎯 RECENT STRATEGIC DECISIONS:
"""
        
        for decision in recent_decisions:
            context += f"""
• {decision['timestamp'][:10]} - {decision['type']}
  Reasoning: {decision['reasoning'][:100]}...
  Expected: {decision['expected_outcome'][:50]}...
"""
        
        context += f"""
🏷️ BRAND STRATEGIES:
• Voyage: {len(self.memory['brand_strategies']['voyage']['learnings'])} learnings
• GoEye: {len(self.memory['brand_strategies']['goeye']['learnings'])} learnings  
• Eyejack: {len(self.memory['brand_strategies']['eyejack']['learnings'])} learnings

💡 KEY INSIGHTS AVAILABLE:
• Audience performance patterns
• Creative optimization strategies
• Seasonal trend analysis
• Competitive positioning insights
"""
        
        return context

if __name__ == "__main__":
    # Example usage
    memory = StrategicMemory()
    print(memory.create_session_context())
