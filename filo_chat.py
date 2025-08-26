#!/usr/bin/env python3
"""
💬 FILO CHAT - Interactive AI Marketing Assistant
Chat with your AI Marketing Agent for strategy, analysis, and campaign management
"""

import json
import requests
from datetime import datetime
from filo_simple import FiloSimple
import threading
import time

class FiloChat:
    """
    💬 Interactive Chat Interface with FILO
    
    Features:
    - Real-time campaign analysis
    - Strategic recommendations
    - Manual campaign adjustments
    - Performance insights
    - Budget optimization advice
    """
    
    def __init__(self):
        """Initialize FILO Chat"""
        self.filo = FiloSimple()
        self.running = False
        self.monitoring_thread = None
        
        print("💬 FILO CHAT - Your AI Marketing Assistant")
        print("=" * 55)
        print("🤖 I'm your expert Facebook marketing agent with 100cr+ spend experience")
        print("💡 Ask me anything about your campaigns, strategy, or optimizations!")
        print()
    
    def start_monitoring(self):
        """Start background monitoring"""
        if not self.running:
            self.running = True
            self.monitoring_thread = threading.Thread(target=self._background_monitor, daemon=True)
            self.monitoring_thread.start()
            print("✅ Background monitoring started")
    
    def stop_monitoring(self):
        """Stop background monitoring"""
        self.running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=1)
        print("⏸️ Background monitoring stopped")
    
    def _background_monitor(self):
        """Background monitoring loop"""
        while self.running:
            try:
                metrics = self.filo.get_campaign_metrics()
                if metrics:
                    # Store latest metrics
                    self.filo.performance_history.extend(metrics)
                    
                    # Check for optimization opportunities
                    actions = self.filo.analyze_and_optimize(metrics)
                    if actions:
                        print(f"\n🔔 ALERT: {len(actions)} optimization opportunities detected!")
                        print("💬 Type 'opportunities' to see recommendations")
                        print("📊 Type 'status' for current performance")
                        print()
                
                # Wait 5 minutes between checks (faster than normal for chat mode)
                time.sleep(300)
            except Exception as e:
                print(f"⚠️ Monitoring error: {e}")
                time.sleep(60)
    
    def get_current_status(self):
        """Get current campaign status"""
        try:
            metrics = self.filo.get_campaign_metrics()
            if not metrics:
                return "⚠️ No campaign data available. Campaigns may be new or need more time to generate data."
            
            total_spend = sum(m.spend for m in metrics)
            total_revenue = sum(m.revenue for m in metrics)
            avg_roas = total_revenue / total_spend if total_spend > 0 else 0
            
            status = f"""
📊 CURRENT CAMPAIGN STATUS:
💰 Total Spend Today: ₹{total_spend:.0f}
💵 Total Revenue Today: ₹{total_revenue:.0f}
📈 Average ROAS: {avg_roas:.2f}
💸 Profit Today: ₹{total_revenue - total_spend:.0f}

🎯 AD SET PERFORMANCE:
"""
            
            for metric in metrics:
                status += f"""
• {metric.ad_set_name}:
  ROAS: {metric.roas:.2f} | Spend: ₹{metric.spend:.0f} | Conversions: {metric.conversions}
"""
            
            # Add recommendations
            if avg_roas > 5.0:
                status += "\n🚀 RECOMMENDATION: Excellent performance! Consider scaling up budgets."
            elif avg_roas < 3.0:
                status += "\n⚠️ RECOMMENDATION: Low ROAS detected. Review targeting and creatives."
            else:
                status += "\n✅ RECOMMENDATION: Performance is stable. Monitor for optimization opportunities."
            
            return status
            
        except Exception as e:
            return f"❌ Error getting status: {e}"
    
    def get_optimization_opportunities(self):
        """Get current optimization opportunities"""
        try:
            metrics = self.filo.get_campaign_metrics()
            if not metrics:
                return "⚠️ No data available for optimization analysis."
            
            actions = self.filo.analyze_and_optimize(metrics)
            
            if not actions:
                return "✅ No immediate optimization opportunities. All campaigns performing within target ranges."
            
            opportunities = "🎯 OPTIMIZATION OPPORTUNITIES:\n\n"
            
            for i, action in enumerate(actions, 1):
                opportunities += f"{i}. {action.ad_set_name}:\n"
                opportunities += f"   Action: {action.action_type.upper()}\n"
                opportunities += f"   Reason: {action.reason}\n"
                
                if action.action_type in ['scale_up', 'scale_down']:
                    opportunities += f"   Budget Change: ₹{action.old_value:.0f} → ₹{action.new_value:.0f}\n"
                
                opportunities += f"   💬 Type 'execute {i}' to apply this optimization\n\n"
            
            return opportunities
            
        except Exception as e:
            return f"❌ Error analyzing opportunities: {e}"
    
    def execute_optimization(self, action_number):
        """Execute a specific optimization"""
        try:
            metrics = self.filo.get_campaign_metrics()
            if not metrics:
                return "⚠️ No data available for optimization."
            
            actions = self.filo.analyze_and_optimize(metrics)
            
            if not actions or action_number > len(actions):
                return "❌ Invalid optimization number."
            
            action = actions[action_number - 1]
            
            # Execute the action
            self.filo.execute_actions([action])
            
            if action.success:
                return f"✅ Successfully executed: {action.action_type.upper()} for {action.ad_set_name}"
            else:
                return f"❌ Failed to execute optimization for {action.ad_set_name}"
                
        except Exception as e:
            return f"❌ Error executing optimization: {e}"
    
    def get_strategic_advice(self, question):
        """Provide strategic marketing advice"""
        question_lower = question.lower()
        
        # Get current performance for context
        try:
            metrics = self.filo.get_campaign_metrics()
            total_spend = sum(m.spend for m in metrics) if metrics else 0
            avg_roas = sum(m.revenue for m in metrics) / total_spend if metrics and total_spend > 0 else 0
        except:
            metrics = []
            total_spend = 0
            avg_roas = 0
        
        # Strategic advice based on keywords
        if any(word in question_lower for word in ['scale', 'scaling', 'budget', 'increase']):
            if avg_roas > 4.0:
                return """
🚀 SCALING STRATEGY:
Your ROAS is strong! Here's how to scale effectively:

1. 📈 GRADUAL SCALING (Recommended):
   • Increase budgets by 20-30% every 2-3 days
   • Monitor performance closely for 48 hours after each increase
   • Scale winners, maintain stable performers

2. 🎯 TARGETING EXPANSION:
   • Create lookalike audiences from your converters
   • Test broader interest targeting
   • Expand age ranges gradually

3. 🕐 TIME-BASED SCALING:
   • Identify peak performance hours
   • Increase budgets during high-converting times
   • Use dayparting for better control

💡 NEXT STEPS: Start with 20% budget increase on your best performing ad set.
"""
            else:
                return """
⚠️ SCALING CAUTION:
Current ROAS suggests optimizing before scaling:

1. 🔍 OPTIMIZE FIRST:
   • Improve ad creatives and copy
   • Refine targeting to higher-intent audiences
   • Test different landing pages

2. 📊 PERFORMANCE TARGETS:
   • Achieve consistent ROAS > 4.0 before scaling
   • Ensure stable performance for 7+ days
   • Have at least 50 conversions for reliable data

3. 🎯 MICRO-SCALING:
   • Increase budgets by only 10-15%
   • Test small increases first
   • Focus on improving efficiency

💡 RECOMMENDATION: Focus on optimization before aggressive scaling.
"""
        
        elif any(word in question_lower for word in ['creative', 'ad copy', 'headline', 'image']):
            return """
🎨 CREATIVE OPTIMIZATION STRATEGY:

1. 📝 AD COPY BEST PRACTICES:
   • Lead with your strongest value proposition
   • Use urgency and scarcity ("Limited Time", "Free Prescription Lenses")
   • Include social proof and testimonials
   • Clear call-to-action

2. 🖼️ VISUAL STRATEGY:
   • Test lifestyle vs product-focused images
   • Use high-quality, eye-catching visuals
   • A/B test different color schemes
   • Include people wearing your products

3. 🔄 TESTING FRAMEWORK:
   • Test 3-5 creative variations per ad set
   • Change one element at a time
   • Run tests for at least 7 days
   • Keep winning creatives, refresh losing ones

💡 FOR YOUR EYEWEAR BRAND:
• Highlight "FREE prescription lenses" prominently
• Show before/after transformations
• Use premium lifestyle imagery
• Test video vs static images
"""
        
        elif any(word in question_lower for word in ['targeting', 'audience', 'interests']):
            return """
🎯 TARGETING OPTIMIZATION:

1. 📊 CURRENT SETUP ANALYSIS:
   • Ray-Ban & Oakley: Good brand affinity targeting
   • Sunglasses: Broad but relevant
   • Luxury Goods: Premium audience focus

2. 🚀 ADVANCED TARGETING IDEAS:
   • Competitor brand interests (Warby Parker, Persol)
   • Behavioral: Premium shoppers, frequent travelers
   • Lookalike audiences from your customer data
   • Retargeting website visitors

3. 🔍 TESTING STRATEGY:
   • Test narrow vs broad audiences
   • Layer interests with behaviors
   • Use exclusions to avoid overlap
   • Monitor audience saturation

💡 NEXT TESTS TO TRY:
• Fashion enthusiasts + Premium shoppers
• Business professionals + Luxury interests
• Travel enthusiasts (sunglasses need)
• Health & fitness (active lifestyle)
"""
        
        elif any(word in question_lower for word in ['roas', 'performance', 'profit', 'revenue']):
            return f"""
📈 PERFORMANCE ANALYSIS:

📊 CURRENT METRICS:
• Average ROAS: {avg_roas:.2f}
• Total Spend Today: ₹{total_spend:.0f}

🎯 PERFORMANCE BENCHMARKS:
• Excellent: ROAS > 5.0
• Good: ROAS 3.5-5.0
• Needs Improvement: ROAS < 3.5

💡 IMPROVEMENT STRATEGIES:
1. 🔍 LOW ROAS FIXES:
   • Tighten targeting to higher-intent audiences
   • Improve landing page conversion rate
   • Test premium positioning vs discount messaging
   • Optimize for purchase conversion events

2. 📈 HIGH ROAS OPTIMIZATION:
   • Scale successful campaigns gradually
   • Expand to similar audiences
   • Test higher-value product offerings
   • Increase brand awareness campaigns

3. 💰 PROFIT MAXIMIZATION:
   • Focus on lifetime value, not just ROAS
   • Upsell premium frames and add-ons
   • Implement email marketing for repeat purchases
   • Track profit margins, not just revenue
"""
        
        else:
            return """
🤖 I'm your AI Marketing Expert! I can help you with:

📊 CAMPAIGN ANALYSIS:
• Type 'status' - Current performance overview
• Type 'opportunities' - Optimization recommendations

🚀 STRATEGIC ADVICE:
• Ask about scaling strategies
• Creative optimization tips
• Targeting recommendations
• Performance improvement

⚡ QUICK ACTIONS:
• 'execute [number]' - Apply specific optimization
• 'pause [ad set name]' - Emergency pause
• 'budget [ad set] [amount]' - Adjust budget

💡 EXAMPLE QUESTIONS:
• "How should I scale my campaigns?"
• "What creatives should I test?"
• "How can I improve my ROAS?"
• "What targeting should I try next?"

Ask me anything about your Facebook ads strategy! 🎯
"""
    
    def manual_budget_change(self, ad_set_name, new_budget):
        """Manually change ad set budget"""
        try:
            # Find ad set ID by name
            ad_set_id = None
            for target_id in self.filo.config['target_ad_sets']:
                # Get ad set name
                url = f"{self.filo.api_base_url}/{target_id}"
                params = {
                    'access_token': self.filo.access_token,
                    'fields': 'name'
                }
                response = requests.get(url, params=params)
                data = response.json()
                
                if ad_set_name.lower() in data.get('name', '').lower():
                    ad_set_id = target_id
                    break
            
            if not ad_set_id:
                return f"❌ Ad set '{ad_set_name}' not found. Available ad sets: Ray-Ban, Fashion, Luxury"
            
            # Update budget
            success = self.filo.update_ad_set_budget(ad_set_id, float(new_budget))
            
            if success:
                return f"✅ Budget updated for {ad_set_name}: ₹{new_budget}/day"
            else:
                return f"❌ Failed to update budget for {ad_set_name}"
                
        except Exception as e:
            return f"❌ Error updating budget: {e}"
    
    def emergency_pause(self, ad_set_name=None):
        """Emergency pause ad set(s)"""
        try:
            if ad_set_name:
                # Pause specific ad set
                for target_id in self.filo.config['target_ad_sets']:
                    url = f"{self.filo.api_base_url}/{target_id}"
                    params = {
                        'access_token': self.filo.access_token,
                        'fields': 'name'
                    }
                    response = requests.get(url, params=params)
                    data = response.json()
                    
                    if ad_set_name.lower() in data.get('name', '').lower():
                        success = self.filo.pause_ad_set(target_id)
                        return f"{'✅' if success else '❌'} {'Paused' if success else 'Failed to pause'} {ad_set_name}"
                
                return f"❌ Ad set '{ad_set_name}' not found"
            else:
                # Pause all ad sets
                paused_count = 0
                for ad_set_id in self.filo.config['target_ad_sets']:
                    if self.filo.pause_ad_set(ad_set_id):
                        paused_count += 1
                
                return f"🚨 Emergency pause activated: {paused_count}/{len(self.filo.config['target_ad_sets'])} ad sets paused"
                
        except Exception as e:
            return f"❌ Error during emergency pause: {e}"
    
    def chat_loop(self):
        """Main chat interaction loop"""
        print("🚀 FILO Chat is ready! Type 'help' for commands or ask me anything.")
        print("💡 Type 'start monitoring' to begin automatic optimization")
        print()
        
        while True:
            try:
                user_input = input("💬 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle exit commands
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("👋 FILO: Goodbye! Your campaigns will continue running.")
                    self.stop_monitoring()
                    break
                
                # Handle specific commands
                elif user_input.lower() == 'help':
                    response = self.get_strategic_advice("help")
                
                elif user_input.lower() == 'status':
                    response = self.get_current_status()
                
                elif user_input.lower() == 'opportunities':
                    response = self.get_optimization_opportunities()
                
                elif user_input.lower().startswith('execute '):
                    try:
                        action_num = int(user_input.split()[1])
                        response = self.execute_optimization(action_num)
                    except (IndexError, ValueError):
                        response = "❌ Usage: execute [number] (e.g., 'execute 1')"
                
                elif user_input.lower().startswith('budget '):
                    try:
                        parts = user_input.split()
                        ad_set_name = parts[1]
                        new_budget = parts[2]
                        response = self.manual_budget_change(ad_set_name, new_budget)
                    except (IndexError, ValueError):
                        response = "❌ Usage: budget [ad_set_name] [amount] (e.g., 'budget rayban 5000')"
                
                elif user_input.lower().startswith('pause'):
                    if len(user_input.split()) > 1:
                        ad_set_name = ' '.join(user_input.split()[1:])
                        response = self.emergency_pause(ad_set_name)
                    else:
                        response = self.emergency_pause()
                
                elif user_input.lower() == 'start monitoring':
                    self.start_monitoring()
                    response = "✅ Background monitoring started! I'll alert you to optimization opportunities."
                
                elif user_input.lower() == 'stop monitoring':
                    self.stop_monitoring()
                    response = "⏸️ Background monitoring stopped."
                
                else:
                    # General strategic advice
                    response = self.get_strategic_advice(user_input)
                
                # Display response
                print(f"\n🤖 FILO: {response}\n")
                
            except KeyboardInterrupt:
                print("\n👋 FILO: Goodbye! Your campaigns will continue running.")
                self.stop_monitoring()
                break
            except Exception as e:
                print(f"\n❌ FILO: Error - {e}\n")


def main():
    """Run FILO Chat"""
    chat = FiloChat()
    chat.chat_loop()


if __name__ == "__main__":
    main()
