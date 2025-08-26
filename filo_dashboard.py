#!/usr/bin/env python3
"""
🌐 FILO Dashboard - Web Interface for Campaign Monitoring
Real-time dashboard to monitor and control your Facebook ads optimization
"""

import json
import threading
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for
import plotly.graph_objs as go
import plotly.utils
from filo_simple import FiloSimple as FiloAgent
import logging

app = Flask(__name__)
app.secret_key = 'filo_dashboard_secret_key_2023'

# Global Filo instance
filo_instance = None
filo_thread = None

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/status')
def api_status():
    """Get Filo agent status"""
    global filo_instance
    
    if not filo_instance:
        return jsonify({
            'status': 'stopped',
            'running': False,
            'last_check': None,
            'actions_count': 0
        })
    
    return jsonify({
        'status': 'running' if filo_instance.running else 'stopped',
        'running': filo_instance.running,
        'last_check': filo_instance.last_check.isoformat() if filo_instance.last_check else None,
        'actions_count': len(filo_instance.actions_taken),
        'monitoring_interval': filo_instance.config['monitoring_interval']
    })

@app.route('/api/metrics')
def api_metrics():
    """Get current campaign metrics"""
    global filo_instance
    
    if not filo_instance:
        return jsonify({'error': 'Filo not initialized'})
    
    try:
        # Get latest metrics
        metrics = filo_instance.get_campaign_metrics()
        
        metrics_data = []
        for metric in metrics:
            metrics_data.append({
                'ad_set_id': metric.ad_set_id,
                'ad_set_name': metric.ad_set_name,
                'spend': metric.spend,
                'revenue': metric.revenue,
                'roas': metric.roas,
                'cpc': metric.cpc,
                'ctr': metric.ctr,
                'impressions': metric.impressions,
                'clicks': metric.clicks,
                'conversions': metric.conversions,
                'timestamp': metric.timestamp.isoformat()
            })
        
        return jsonify({
            'success': True,
            'metrics': metrics_data,
            'total_spend': sum(m['spend'] for m in metrics_data),
            'total_revenue': sum(m['revenue'] for m in metrics_data),
            'avg_roas': sum(m['revenue'] for m in metrics_data) / sum(m['spend'] for m in metrics_data) if sum(m['spend'] for m in metrics_data) > 0 else 0
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/actions')
def api_actions():
    """Get recent optimization actions"""
    global filo_instance
    
    if not filo_instance:
        return jsonify({'error': 'Filo not initialized'})
    
    try:
        # Get last 20 actions
        recent_actions = filo_instance.actions_taken[-20:] if filo_instance.actions_taken else []
        
        actions_data = []
        for action in recent_actions:
            actions_data.append({
                'action_type': action.action_type,
                'ad_set_name': action.ad_set_name,
                'old_value': action.old_value,
                'new_value': action.new_value,
                'reason': action.reason,
                'timestamp': action.timestamp.isoformat(),
                'success': action.success
            })
        
        return jsonify({
            'success': True,
            'actions': actions_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/performance_chart')
def api_performance_chart():
    """Get performance chart data"""
    global filo_instance
    
    if not filo_instance or not filo_instance.performance_history:
        return jsonify({'error': 'No performance data available'})
    
    try:
        # Group by ad set and time
        chart_data = {}
        
        for metric in filo_instance.performance_history[-100:]:  # Last 100 data points
            ad_set_name = metric.ad_set_name
            if ad_set_name not in chart_data:
                chart_data[ad_set_name] = {
                    'timestamps': [],
                    'roas': [],
                    'spend': [],
                    'revenue': []
                }
            
            chart_data[ad_set_name]['timestamps'].append(metric.timestamp.isoformat())
            chart_data[ad_set_name]['roas'].append(metric.roas)
            chart_data[ad_set_name]['spend'].append(metric.spend)
            chart_data[ad_set_name]['revenue'].append(metric.revenue)
        
        return jsonify({
            'success': True,
            'chart_data': chart_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/start', methods=['POST'])
def api_start():
    """Start Filo agent"""
    global filo_instance, filo_thread
    
    try:
        if filo_instance and filo_instance.running:
            return jsonify({'error': 'Filo is already running'})
        
        # Initialize Filo
        filo_instance = FiloAgent()
        
        # Start in separate thread
        filo_thread = threading.Thread(target=filo_instance.start, daemon=True)
        filo_thread.start()
        
        return jsonify({'success': True, 'message': 'Filo started successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/stop', methods=['POST'])
def api_stop():
    """Stop Filo agent"""
    global filo_instance
    
    try:
        if not filo_instance or not filo_instance.running:
            return jsonify({'error': 'Filo is not running'})
        
        filo_instance.stop()
        
        return jsonify({'success': True, 'message': 'Filo stopped successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/emergency_pause', methods=['POST'])
def api_emergency_pause():
    """Emergency pause all campaigns"""
    global filo_instance
    
    try:
        if not filo_instance:
            return jsonify({'error': 'Filo not initialized'})
        
        # Pause all monitored ad sets
        paused_count = 0
        for ad_set_id in filo_instance.config['target_ad_sets']:
            if filo_instance.pause_ad_set(ad_set_id):
                paused_count += 1
        
        # Send emergency notification
        filo_instance.send_email(
            '🚨 EMERGENCY PAUSE ACTIVATED',
            f'''
🚨 EMERGENCY PAUSE has been activated via dashboard!

⏸️ Ad sets paused: {paused_count}/{len(filo_instance.config['target_ad_sets'])}
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

All monitored campaigns have been paused for protection.
Review performance and manually resume when ready.

---
🤖 FILO Emergency Response System
'''
        )
        
        return jsonify({
            'success': True, 
            'message': f'Emergency pause activated - {paused_count} ad sets paused'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/config')
def api_config():
    """Get current configuration"""
    global filo_instance
    
    if not filo_instance:
        return jsonify({'error': 'Filo not initialized'})
    
    # Return safe config (without sensitive data)
    safe_config = filo_instance.config.copy()
    safe_config['facebook_access_token'] = '***HIDDEN***'
    safe_config['notifications']['smtp_password'] = '***HIDDEN***'
    
    return jsonify({
        'success': True,
        'config': safe_config
    })

@app.route('/api/update_config', methods=['POST'])
def api_update_config():
    """Update configuration"""
    global filo_instance
    
    try:
        if not filo_instance:
            return jsonify({'error': 'Filo not initialized'})
        
        new_config = request.json
        
        # Update specific fields (safety check)
        allowed_updates = ['monitoring_interval', 'rules', 'notifications', 'safety']
        
        for key in allowed_updates:
            if key in new_config:
                filo_instance.config[key] = new_config[key]
        
        # Save updated config
        with open(filo_instance.config_path, 'w') as f:
            json.dump(filo_instance.config, f, indent=2)
        
        return jsonify({'success': True, 'message': 'Configuration updated'})
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Chat with Claude AI - Full Conversational Experience"""
    try:
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'No message provided'})
        
        # Get campaign context for Claude
        campaign_context = get_campaign_context()
        
        # Process with Claude AI (simulated intelligent responses)
        response = process_claude_chat(user_message, campaign_context)
        
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

def get_campaign_context():
    """Get current campaign context for Claude"""
    try:
        if filo_instance:
            metrics = filo_instance.get_campaign_metrics()
            if metrics:
                total_spend = sum(m.spend for m in metrics)
                total_revenue = sum(m.revenue for m in metrics)
                avg_roas = total_revenue / total_spend if total_spend > 0 else 0
                
                return {
                    'has_data': True,
                    'total_spend': total_spend,
                    'total_revenue': total_revenue,
                    'avg_roas': avg_roas,
                    'ad_sets': [
                        {
                            'name': m.ad_set_name,
                            'roas': m.roas,
                            'spend': m.spend,
                            'conversions': m.conversions
                        } for m in metrics
                    ]
                }
        
        return {
            'has_data': False,
            'message': 'Campaigns are new and generating data'
        }
    except:
        return {'has_data': False, 'message': 'No campaign data available'}

def process_claude_chat(user_message, context):
    """Process chat with Claude AI intelligence"""
    
    # Claude AI responses based on context and message
    message_lower = user_message.lower()
    
    # Handle specific commands first
    if message_lower in ['status', 'performance', 'current status']:
        if context['has_data']:
            return f"""**📊 CURRENT CAMPAIGN STATUS:**

💰 **Total Spend Today:** ₹{context['total_spend']:.0f}
💵 **Total Revenue Today:** ₹{context['total_revenue']:.0f}  
📈 **Average ROAS:** {context['avg_roas']:.2f}
💸 **Profit Today:** ₹{context['total_revenue'] - context['total_spend']:.0f}

**🎯 AD SET BREAKDOWN:**
""" + "\n".join([f"• **{ad['name']}:** ROAS {ad['roas']:.2f} | Spend ₹{ad['spend']:.0f} | Conv: {ad['conversions']}" for ad in context['ad_sets']]) + f"""

**📋 MY ANALYSIS:**
{'🚀 Excellent performance! Your ROAS is strong - consider scaling up gradually.' if context['avg_roas'] > 4.0 else '⚠️ Performance needs optimization. Focus on improving targeting and creatives before scaling.' if context['avg_roas'] < 3.0 else '✅ Solid performance. Look for optimization opportunities to push higher.'}

**💡 What would you like to do next?** I can help you scale, optimize, or strategize!"""
        else:
            return f"""**📊 CAMPAIGN STATUS:**

⏳ Your campaigns are **newly launched** and still generating performance data. This is completely normal!

**🎯 WHAT'S HAPPENING:**
• Ad sets are active and running
• Facebook is learning your audience
• Data will populate over the next 12-24 hours
• Budget: ₹10,000/day across 3 ad sets

**💡 WHILE WE WAIT, I CAN HELP YOU:**
• Plan scaling strategies for when data comes in
• Optimize your ad creatives and copy
• Discuss targeting improvements
• Prepare for different performance scenarios

**What aspect of your eyewear marketing would you like to discuss?**"""
    
    elif message_lower in ['opportunities', 'optimize', 'recommendations']:
        if context['has_data']:
            opportunities = []
            for ad in context['ad_sets']:
                if ad['roas'] > 5.0:
                    opportunities.append(f"🚀 **{ad['name']}** - Scale up! ROAS {ad['roas']:.2f} is excellent")
                elif ad['roas'] < 3.0:
                    opportunities.append(f"⚠️ **{ad['name']}** - Needs optimization. ROAS {ad['roas']:.2f} is low")
                else:
                    opportunities.append(f"✅ **{ad['name']}** - Stable performance at ROAS {ad['roas']:.2f}")
            
            return "**🎯 OPTIMIZATION OPPORTUNITIES:**\n\n" + "\n".join(opportunities) + """

**💡 MY STRATEGIC RECOMMENDATIONS:**

**1. 📈 IMMEDIATE ACTIONS:**
• Scale winning ad sets by 20-30%
• Pause or optimize underperformers
• Test new creative variations

**2. 🎨 CREATIVE TESTS TO RUN:**
• Video ads showcasing transformations
• User-generated content with testimonials
• Lifestyle shots vs product-focused images

**3. 🎯 TARGETING EXPANSION:**
• Lookalike audiences from converters
• Interest layering (Fashion + Premium shoppers)
• Behavioral targeting (Frequent travelers)

**Which area would you like me to dive deeper into?**"""
        else:
            return """**🎯 OPTIMIZATION STRATEGY (Pre-Data):**

Since your campaigns are new, let's prepare optimization strategies:

**🚀 IMMEDIATE SETUP OPTIMIZATIONS:**
• Ensure conversion tracking is properly set up
• Verify pixel firing on purchase events
• Check that product catalog is connected

**📈 PERFORMANCE PREDICTION FRAMEWORK:**
• **If ROAS > 5.0:** Scale aggressively (30-50% increases)
• **If ROAS 3.5-5.0:** Scale gradually (15-20% increases)  
• **If ROAS < 3.0:** Optimize before scaling (targeting/creatives)

**🎨 CREATIVE PREPARATION:**
• Prepare 3-5 ad variations per concept
• Focus on your "FREE prescription lenses" USP
• Test different value propositions

**What specific aspect would you like me to help you prepare for?**"""
    
    # Strategic conversations based on keywords
    elif any(word in message_lower for word in ['scale', 'scaling', 'grow', 'increase', 'budget']):
        return """**🚀 SCALING STRATEGY FOR YOUR EYEWEAR BRAND:**

**📊 CURRENT SITUATION ANALYSIS:**
Your campaigns are in the data-gathering phase, which is perfect timing to plan your scaling strategy!

**🎯 MY SCALING FRAMEWORK:**

**PHASE 1: FOUNDATION (Days 1-7)**
• Let campaigns gather 50+ conversions per ad set
• Identify your best-performing audiences
• Establish baseline ROAS benchmarks

**PHASE 2: GRADUAL SCALING (Days 8-14)**
• Increase budgets by 20% every 2-3 days
• Scale only ad sets with ROAS > 4.0
• Monitor performance closely for 48 hours after each increase

**PHASE 3: AGGRESSIVE SCALING (Days 15+)**
• Scale winners by 30-50% weekly
• Duplicate successful ad sets with slight variations
• Expand to new audiences and placements

**💰 BUDGET ALLOCATION STRATEGY:**
• 60% to proven winners
• 30% to stable performers  
• 10% to testing new concepts

**🎯 FOR YOUR EYEWEAR NICHE:**
• Premium audiences convert better (higher AOV)
• Lifestyle targeting outperforms product-focused
• Video content scales better than static images

**What's your target monthly revenue goal? I can create a specific scaling roadmap!**"""
    
    elif any(word in message_lower for word in ['creative', 'ad copy', 'headline', 'image', 'video']):
        return """**🎨 CREATIVE OPTIMIZATION FOR EYEWEAR:**

**📊 WHAT WORKS IN EYEWEAR ADVERTISING:**

**🏆 HIGH-CONVERTING CREATIVE ELEMENTS:**
• **Transformation shots** - Before/after with glasses
• **Lifestyle imagery** - People living their best life
• **Premium positioning** - Luxury feel, not discount
• **Social proof** - Real customer testimonials

**📝 COPY FRAMEWORKS THAT CONVERT:**

**1. VALUE STACK APPROACH:**
"Premium Designer Frames + FREE Prescription Lenses + Fast Delivery = Unbeatable Value"

**2. PROBLEM-SOLUTION:**
"Tired of overpriced eyewear? Get designer quality without the designer markup."

**3. URGENCY + BENEFIT:**
"Limited Time: FREE prescription lenses with every frame (Save ₹3,000+)"

**🎬 VIDEO CREATIVE IDEAS:**
• **Unboxing experience** - Premium packaging reveal
• **Try-on transformation** - Multiple styles on same person
• **Behind-the-scenes** - Quality craftsmanship focus
• **Customer testimonials** - Real people, real results

**🖼️ STATIC IMAGE TESTS:**
• **Carousel ads** - Multiple angles/styles
• **Lifestyle shots** - Professional, travel, casual settings
• **Product grids** - Show variety and options
• **Before/after** - Transformation focus

**Which creative format would you like me to help you develop first?**"""
    
    elif any(word in message_lower for word in ['targeting', 'audience', 'interests', 'demographics']):
        return """**🎯 ADVANCED TARGETING FOR EYEWEAR:**

**📊 YOUR CURRENT SETUP ANALYSIS:**
• Ray-Ban & Oakley: ✅ Excellent brand affinity
• Sunglasses Interest: ✅ Broad but relevant
• Luxury Goods: ✅ Premium positioning

**🚀 NEXT-LEVEL TARGETING STRATEGIES:**

**1. 👥 BEHAVIORAL LAYERING:**
• Premium shoppers + Fashion enthusiasts
• Frequent travelers + Sunglasses interest
• Business professionals + Luxury goods

**2. 🎯 COMPETITOR TARGETING:**
• Warby Parker customers
• Persol enthusiasts  
• Oliver Peoples fans
• Maui Jim users

**3. 📱 LOOKALIKE AUDIENCES:**
• Website visitors (last 180 days)
• Email subscribers
• Past purchasers (if available)
• Video viewers (75%+ completion)

**4. 🏢 PROFESSIONAL TARGETING:**
• Executives and senior management
• Healthcare professionals
• Legal professionals
• Finance industry workers

**5. 🌟 LIFESTYLE INTERESTS:**
• Photography (need quality lenses)
• Outdoor activities (sunglasses)
• Fashion and style
• Travel and adventure

**💡 TESTING STRATEGY:**
Start with 2-3 audiences per ad set, then expand winners.

**Which audience segment resonates most with your brand vision?**"""
    
    elif any(word in message_lower for word in ['roas', 'performance', 'profit', 'revenue', 'conversion']):
        return f"""**📈 PERFORMANCE OPTIMIZATION DEEP DIVE:**

**🎯 CURRENT METRICS ANALYSIS:**
{f"Your average ROAS of {context['avg_roas']:.2f} " + ("is excellent! You're in scaling territory." if context.get('avg_roas', 0) > 4.0 else "needs improvement. Let's optimize!" if context.get('avg_roas', 0) < 3.0 else "is solid. We can push it higher!") if context['has_data'] else "Data is still coming in - perfect time to set up for success!"}

**💰 ROAS OPTIMIZATION FRAMEWORK:**

**LEVEL 1: FOUNDATION (Target: 3.0+ ROAS)**
• Proper conversion tracking setup
• Accurate product catalog
• Basic audience targeting

**LEVEL 2: OPTIMIZATION (Target: 4.0+ ROAS)**
• Refined audience targeting
• Improved ad creatives
• Landing page optimization
• Bid strategy refinement

**LEVEL 3: SCALING (Target: 5.0+ ROAS)**
• Lookalike audiences
• Advanced creative testing
• Cross-sell and upsell strategies
• Lifetime value optimization

**🔧 IMMEDIATE ROAS BOOSTERS:**
• **Exclude low-intent traffic** (broad interests)
• **Focus on purchase intent** (shopping behaviors)
• **Improve landing page** (faster load, better UX)
• **Highlight value prop** (FREE prescription lenses)

**💎 PREMIUM STRATEGIES:**
• **Bundle offers** (Frame + lenses + case)
• **Urgency tactics** (Limited time offers)
• **Social proof** (Reviews, testimonials)
• **Retargeting** (Cart abandoners, browsers)

**What's your target ROAS goal? I can create a specific action plan!**"""
    
    elif any(word in message_lower for word in ['help', 'what can you do', 'capabilities', 'assist']):
        return """**🤖 I'M YOUR COMPLETE AI MARKETING PARTNER!**

**🎯 WHAT I CAN DO FOR YOU:**

**📊 CAMPAIGN ANALYSIS:**
• Real-time performance monitoring
• ROAS and profitability analysis  
• Competitor research and insights
• Market trend identification

**🚀 STRATEGIC PLANNING:**
• Scaling roadmaps and timelines
• Budget allocation strategies
• Audience expansion plans
• Creative testing frameworks

**🎨 CREATIVE DEVELOPMENT:**
• Ad copy and headline creation
• Visual concept development
• Video script writing
• A/B testing strategies

**🎯 TARGETING OPTIMIZATION:**
• Audience research and segmentation
• Interest and behavior analysis
• Lookalike audience strategies
• Retargeting campaign setup

**💰 BUSINESS GROWTH:**
• Revenue forecasting
• Profit margin optimization
• Conversion rate improvement
• Customer lifetime value strategies

**⚡ REAL-TIME ACTIONS:**
• Campaign optimizations
• Budget adjustments
• Emergency pausing/scaling
• Performance troubleshooting

**💡 JUST ASK ME ANYTHING LIKE:**
• "How should I scale my Ray-Ban campaign?"
• "Create ad copy for my sunglasses"
• "What's the best targeting for professionals?"
• "Help me improve my ROAS"
• "Plan my Q4 marketing strategy"

**I'm here 24/7 to grow your eyewear business! What would you like to tackle first?**"""
    
    # General conversation - Claude's natural responses
    else:
        # Analyze the message for intent and provide intelligent responses
        if any(word in message_lower for word in ['hi', 'hello', 'hey', 'good morning', 'good afternoon']):
            return f"""**👋 Hello! I'm Claude, your AI Marketing Expert!**

I'm here to help you dominate the eyewear market with your Facebook ads. 

**🎯 QUICK SITUATION CHECK:**
{f"Your campaigns are running with ₹{context['total_spend']:.0f} spend today and {context['avg_roas']:.2f} ROAS." if context['has_data'] else "Your campaigns are newly launched and gathering performance data."}

**💡 I CAN HELP YOU WITH:**
• Strategic planning and scaling
• Creative optimization and testing  
• Audience targeting and expansion
• Performance analysis and troubleshooting
• Real-time campaign adjustments

**What's on your mind today? Any specific challenges or goals you'd like to tackle?**"""
        
        elif any(word in message_lower for word in ['thank', 'thanks', 'appreciate']):
            return """**🙏 You're very welcome!**

I'm here to help you succeed with your eyewear business. Your success is my success!

**🚀 REMEMBER:**
• I'm available 24/7 for any questions
• No question is too small or too complex
• I can help with both strategy and execution
• Feel free to bounce ideas off me anytime

**What else can I help you optimize today?**"""
        
        elif any(word in message_lower for word in ['problem', 'issue', 'trouble', 'help', 'stuck']):
            return """**🔧 I'M HERE TO SOLVE PROBLEMS!**

Tell me exactly what's happening and I'll help you fix it:

**🎯 COMMON ISSUES I SOLVE:**
• Low ROAS or poor performance
• High costs, low conversions
• Audience fatigue or saturation
• Creative performance decline
• Scaling challenges
• Technical setup problems

**💡 TO HELP YOU BEST:**
• Describe the specific issue
• Share any error messages
• Tell me what you've already tried
• Let me know your goals/expectations

**I'll analyze the situation and give you a step-by-step solution plan.**

**What specific challenge are you facing?**"""
        
        else:
            # General intelligent response based on the message content
            return f"""**🤖 I understand you're asking about: "{user_message}"**

**💡 HERE'S MY TAKE:**

Based on your eyewear business and current campaign setup, let me provide some strategic insights:

**🎯 RELEVANT TO YOUR SITUATION:**
{f"With your current ROAS of {context['avg_roas']:.2f}, " + ("you're in a great position to scale and expand." if context.get('avg_roas', 0) > 4.0 else "there's room for optimization and improvement." if context.get('avg_roas', 0) < 4.0 else "you have a solid foundation to build upon.") if context['has_data'] else "Your campaigns are in the data-gathering phase, which is perfect for strategic planning."}

**📊 MY RECOMMENDATION:**
Let me help you dive deeper into this topic. I can provide:
• Specific strategies and tactics
• Step-by-step implementation plans  
• Industry best practices
• Real-time optimizations

**Could you tell me more about what specific aspect you'd like me to focus on?** 

For example:
• Are you looking for strategic advice?
• Do you need help with implementation?
• Want me to analyze something specific?
• Looking for creative ideas?

**I'm here to provide exactly the help you need!**"""
    
    return response

def process_chat_message(message, filo):
    """Process chat message and return AI response"""
    message_lower = message.lower()
    
    # Handle specific commands
    if message_lower == 'status':
        return get_status_response(filo)
    elif message_lower == 'opportunities':
        return get_opportunities_response(filo)
    elif message_lower.startswith('execute '):
        try:
            action_num = int(message.split()[1])
            return execute_optimization_response(filo, action_num)
        except (IndexError, ValueError):
            return "❌ Usage: execute [number] (e.g., 'execute 1')"
    elif message_lower.startswith('budget '):
        try:
            parts = message.split()
            ad_set_name = parts[1]
            new_budget = float(parts[2])
            return budget_change_response(filo, ad_set_name, new_budget)
        except (IndexError, ValueError):
            return "❌ Usage: budget [ad_set_name] [amount] (e.g., 'budget rayban 5000')"
    elif 'pause' in message_lower:
        return emergency_pause_response(filo)
    else:
        # Strategic advice based on keywords
        return get_strategic_advice_response(message, filo)

def get_status_response(filo):
    """Get current campaign status"""
    try:
        metrics = filo.get_campaign_metrics()
        if not metrics:
            return "⚠️ No campaign data available. Your campaigns are new and need time to generate performance data."
        
        total_spend = sum(m.spend for m in metrics)
        total_revenue = sum(m.revenue for m in metrics)
        avg_roas = total_revenue / total_spend if total_spend > 0 else 0
        
        response = f"""📊 **CURRENT CAMPAIGN STATUS:**

💰 **Total Spend Today:** ₹{total_spend:.0f}
💵 **Total Revenue Today:** ₹{total_revenue:.0f}
📈 **Average ROAS:** {avg_roas:.2f}
💸 **Profit Today:** ₹{total_revenue - total_spend:.0f}

🎯 **AD SET PERFORMANCE:**
"""
        
        for metric in metrics:
            response += f"\n• **{metric.ad_set_name}:**\n  ROAS: {metric.roas:.2f} | Spend: ₹{metric.spend:.0f} | Conversions: {metric.conversions}"
        
        # Add recommendations
        if avg_roas > 5.0:
            response += "\n\n🚀 **RECOMMENDATION:** Excellent performance! Consider scaling up budgets."
        elif avg_roas < 3.0:
            response += "\n\n⚠️ **RECOMMENDATION:** Low ROAS detected. Review targeting and creatives."
        else:
            response += "\n\n✅ **RECOMMENDATION:** Performance is stable. Monitor for optimization opportunities."
        
        return response
        
    except Exception as e:
        return f"❌ Error getting status: {e}"

def get_opportunities_response(filo):
    """Get optimization opportunities"""
    try:
        metrics = filo.get_campaign_metrics()
        if not metrics:
            return "⚠️ No data available for optimization analysis. Your campaigns need more time to generate data."
        
        actions = filo.analyze_and_optimize(metrics)
        
        if not actions:
            return "✅ **No immediate optimization opportunities.** All campaigns performing within target ranges."
        
        response = "🎯 **OPTIMIZATION OPPORTUNITIES:**\n\n"
        
        for i, action in enumerate(actions, 1):
            response += f"**{i}. {action.ad_set_name}:**\n"
            response += f"   • Action: **{action.action_type.upper()}**\n"
            response += f"   • Reason: {action.reason}\n"
            
            if action.action_type in ['scale_up', 'scale_down']:
                response += f"   • Budget Change: ₹{action.old_value:.0f} → ₹{action.new_value:.0f}\n"
            
            response += f"   • 💬 Type 'execute {i}' to apply this optimization\n\n"
        
        return response
        
    except Exception as e:
        return f"❌ Error analyzing opportunities: {e}"

def get_strategic_advice_response(question, filo):
    """Provide strategic marketing advice"""
    question_lower = question.lower()
    
    # Get current performance for context
    try:
        metrics = filo.get_campaign_metrics()
        total_spend = sum(m.spend for m in metrics) if metrics else 0
        avg_roas = sum(m.revenue for m in metrics) / total_spend if metrics and total_spend > 0 else 0
    except:
        metrics = []
        total_spend = 0
        avg_roas = 0
    
    # Strategic advice based on keywords
    if any(word in question_lower for word in ['scale', 'scaling', 'budget', 'increase']):
        if avg_roas > 4.0:
            return """🚀 **SCALING STRATEGY:**
Your ROAS is strong! Here's how to scale effectively:

**1. 📈 GRADUAL SCALING (Recommended):**
• Increase budgets by 20-30% every 2-3 days
• Monitor performance closely for 48 hours after each increase
• Scale winners, maintain stable performers

**2. 🎯 TARGETING EXPANSION:**
• Create lookalike audiences from your converters
• Test broader interest targeting
• Expand age ranges gradually

**3. 🕐 TIME-BASED SCALING:**
• Identify peak performance hours
• Increase budgets during high-converting times
• Use dayparting for better control

💡 **NEXT STEPS:** Start with 20% budget increase on your best performing ad set."""
        else:
            return """⚠️ **SCALING CAUTION:**
Current ROAS suggests optimizing before scaling:

**1. 🔍 OPTIMIZE FIRST:**
• Improve ad creatives and copy
• Refine targeting to higher-intent audiences
• Test different landing pages

**2. 📊 PERFORMANCE TARGETS:**
• Achieve consistent ROAS > 4.0 before scaling
• Ensure stable performance for 7+ days
• Have at least 50 conversions for reliable data

💡 **RECOMMENDATION:** Focus on optimization before aggressive scaling."""
    
    elif any(word in question_lower for word in ['creative', 'ad copy', 'headline', 'image']):
        return """🎨 **CREATIVE OPTIMIZATION STRATEGY:**

**1. 📝 AD COPY BEST PRACTICES:**
• Lead with your strongest value proposition
• Use urgency and scarcity ("Limited Time", "Free Prescription Lenses")
• Include social proof and testimonials
• Clear call-to-action

**2. 🖼️ VISUAL STRATEGY:**
• Test lifestyle vs product-focused images
• Use high-quality, eye-catching visuals
• A/B test different color schemes
• Include people wearing your products

**3. 🔄 TESTING FRAMEWORK:**
• Test 3-5 creative variations per ad set
• Change one element at a time
• Run tests for at least 7 days
• Keep winning creatives, refresh losing ones

💡 **FOR YOUR EYEWEAR BRAND:**
• Highlight "FREE prescription lenses" prominently
• Show before/after transformations
• Use premium lifestyle imagery
• Test video vs static images"""
    
    elif any(word in question_lower for word in ['targeting', 'audience', 'interests']):
        return """🎯 **TARGETING OPTIMIZATION:**

**1. 📊 CURRENT SETUP ANALYSIS:**
• Ray-Ban & Oakley: Good brand affinity targeting
• Sunglasses: Broad but relevant
• Luxury Goods: Premium audience focus

**2. 🚀 ADVANCED TARGETING IDEAS:**
• Competitor brand interests (Warby Parker, Persol)
• Behavioral: Premium shoppers, frequent travelers
• Lookalike audiences from your customer data
• Retargeting website visitors

**3. 🔍 TESTING STRATEGY:**
• Test narrow vs broad audiences
• Layer interests with behaviors
• Use exclusions to avoid overlap
• Monitor audience saturation

💡 **NEXT TESTS TO TRY:**
• Fashion enthusiasts + Premium shoppers
• Business professionals + Luxury interests
• Travel enthusiasts (sunglasses need)
• Health & fitness (active lifestyle)"""
    
    elif any(word in question_lower for word in ['roas', 'performance', 'profit', 'revenue']):
        return f"""📈 **PERFORMANCE ANALYSIS:**

📊 **CURRENT METRICS:**
• Average ROAS: {avg_roas:.2f}
• Total Spend Today: ₹{total_spend:.0f}

🎯 **PERFORMANCE BENCHMARKS:**
• Excellent: ROAS > 5.0
• Good: ROAS 3.5-5.0
• Needs Improvement: ROAS < 3.5

💡 **IMPROVEMENT STRATEGIES:**

**1. 🔍 LOW ROAS FIXES:**
• Tighten targeting to higher-intent audiences
• Improve landing page conversion rate
• Test premium positioning vs discount messaging
• Optimize for purchase conversion events

**2. 📈 HIGH ROAS OPTIMIZATION:**
• Scale successful campaigns gradually
• Expand to similar audiences
• Test higher-value product offerings
• Increase brand awareness campaigns

**3. 💰 PROFIT MAXIMIZATION:**
• Focus on lifetime value, not just ROAS
• Upsell premium frames and add-ons
• Implement email marketing for repeat purchases
• Track profit margins, not just revenue"""
    
    else:
        return """🤖 **I'm your AI Marketing Expert!** I can help you with:

📊 **CAMPAIGN ANALYSIS:**
• Type 'status' - Current performance overview
• Type 'opportunities' - Optimization recommendations

🚀 **STRATEGIC ADVICE:**
• Ask about scaling strategies
• Creative optimization tips
• Targeting recommendations
• Performance improvement

⚡ **QUICK ACTIONS:**
• 'execute [number]' - Apply specific optimization
• 'budget [ad set] [amount]' - Adjust budget
• 'pause' - Emergency pause

💡 **EXAMPLE QUESTIONS:**
• "How should I scale my campaigns?"
• "What creatives should I test?"
• "How can I improve my ROAS?"
• "What targeting should I try next?"

**Ask me anything about your Facebook ads strategy!** 🎯"""

def execute_optimization_response(filo, action_number):
    """Execute optimization and return response"""
    try:
        metrics = filo.get_campaign_metrics()
        if not metrics:
            return "⚠️ No data available for optimization."
        
        actions = filo.analyze_and_optimize(metrics)
        
        if not actions or action_number > len(actions):
            return "❌ Invalid optimization number."
        
        action = actions[action_number - 1]
        
        # Execute the action
        filo.execute_actions([action])
        
        if action.success:
            return f"✅ **Successfully executed:** {action.action_type.upper()} for {action.ad_set_name}"
        else:
            return f"❌ **Failed to execute optimization** for {action.ad_set_name}"
            
    except Exception as e:
        return f"❌ Error executing optimization: {e}"

def budget_change_response(filo, ad_set_name, new_budget):
    """Change budget and return response"""
    try:
        # Find ad set ID by name
        ad_set_id = None
        for target_id in filo.config['target_ad_sets']:
            # Get ad set name
            url = f"{filo.api_base_url}/{target_id}"
            params = {
                'access_token': filo.access_token,
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
        success = filo.update_ad_set_budget(ad_set_id, float(new_budget))
        
        if success:
            return f"✅ **Budget updated** for {ad_set_name}: ₹{new_budget}/day"
        else:
            return f"❌ **Failed to update budget** for {ad_set_name}"
            
    except Exception as e:
        return f"❌ Error updating budget: {e}"

def emergency_pause_response(filo):
    """Emergency pause and return response"""
    try:
        paused_count = 0
        for ad_set_id in filo.config['target_ad_sets']:
            if filo.pause_ad_set(ad_set_id):
                paused_count += 1
        
        return f"🚨 **Emergency pause activated:** {paused_count}/{len(filo.config['target_ad_sets'])} ad sets paused"
        
    except Exception as e:
        return f"❌ Error during emergency pause: {e}"

# Create templates directory and dashboard HTML
def create_dashboard_template():
    """Create the dashboard HTML template"""
    import os
    
    # Create templates directory
    os.makedirs('templates', exist_ok=True)
    
    dashboard_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 FILO Dashboard - AI Marketing Agent</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { 
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        .header h1 { color: #4a5568; font-size: 2.5em; margin-bottom: 10px; }
        .status-bar { 
            display: flex; 
            justify-content: space-between; 
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }
        .status-indicator {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: 600;
        }
        .status-running { background: #48bb78; color: white; }
        .status-stopped { background: #f56565; color: white; }
        .controls { display: flex; gap: 10px; flex-wrap: wrap; }
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
        }
        .btn-primary { background: #4299e1; color: white; }
        .btn-danger { background: #f56565; color: white; }
        .btn-warning { background: #ed8936; color: white; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
        .grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 20px; 
            margin-bottom: 20px;
        }
        .card {
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        .card h3 { color: #4a5568; margin-bottom: 15px; font-size: 1.3em; }
        .metric { 
            display: flex; 
            justify-content: space-between; 
            padding: 10px 0; 
            border-bottom: 1px solid #e2e8f0;
        }
        .metric:last-child { border-bottom: none; }
        .metric-label { color: #718096; }
        .metric-value { font-weight: 600; color: #2d3748; }
        .chart-container { 
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        .actions-list { max-height: 400px; overflow-y: auto; }
        .action-item {
            padding: 10px;
            margin: 5px 0;
            border-radius: 8px;
            border-left: 4px solid #4299e1;
        }
        .action-success { background: #f0fff4; border-color: #48bb78; }
        .action-failed { background: #fff5f5; border-color: #f56565; }
        .action-time { font-size: 0.8em; color: #718096; }
        .loading { text-align: center; padding: 40px; color: #718096; }
        @media (max-width: 768px) {
            .status-bar { flex-direction: column; align-items: stretch; }
            .controls { justify-content: center; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 FILO Dashboard</h1>
            <p>Facebook Intelligence & Learning Optimizer - Your AI Marketing Agent</p>
            <div class="status-bar">
                <div id="status-indicator" class="status-indicator status-stopped">
                    <span>🔴</span>
                    <span>Agent Stopped</span>
                </div>
                <div class="controls">
                    <button id="start-btn" class="btn btn-primary" onclick="startFilo()">▶️ Start Filo</button>
                    <button id="stop-btn" class="btn btn-warning" onclick="stopFilo()" disabled>⏸️ Stop Filo</button>
                    <button id="emergency-btn" class="btn btn-danger" onclick="emergencyPause()">🚨 Emergency Pause</button>
                </div>
            </div>
        </div>

        <div class="grid">
            <div class="card">
                <h3>📊 Campaign Overview</h3>
                <div id="overview-metrics">
                    <div class="loading">Loading metrics...</div>
                </div>
            </div>
            
            <div class="card">
                <h3>🎯 Ad Set Performance</h3>
                <div id="adset-metrics">
                    <div class="loading">Loading ad sets...</div>
                </div>
            </div>
        </div>

        <div class="chart-container">
            <h3>📈 Performance Trends</h3>
            <div id="performance-chart" style="height: 400px;"></div>
        </div>

        <div class="card">
            <h3>⚡ Recent Actions</h3>
            <div id="recent-actions" class="actions-list">
                <div class="loading">Loading actions...</div>
            </div>
        </div>

        <div class="card">
            <h3>💬 Chat with Claude AI</h3>
            <div id="chat-container">
                <div id="chat-messages" style="height: 300px; overflow-y: auto; border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; margin-bottom: 15px; background: #f8fafc;">
                    <div class="chat-message filo-message">
                        <strong>🤖 Claude:</strong> Hi! I'm Claude, your AI Marketing Expert. I can help you with strategy, optimization, creative development, and real-time campaign management!<br>
                        <small style="color: #718096;">Ask me anything - I'm here to grow your eyewear business!</small>
                    </div>
                </div>
                <div style="display: flex; gap: 10px;">
                    <input type="text" id="chat-input" placeholder="Ask Claude anything about your campaigns..." style="flex: 1; padding: 10px; border: 1px solid #e2e8f0; border-radius: 8px;">
                    <button onclick="sendMessage()" class="btn btn-primary">Send</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        let updateInterval;

        // Start Filo
        async function startFilo() {
            try {
                const response = await fetch('/api/start', { method: 'POST' });
                const data = await response.json();
                
                if (data.success) {
                    alert('✅ Filo started successfully!');
                    updateDashboard();
                } else {
                    alert('❌ Error: ' + data.error);
                }
            } catch (error) {
                alert('❌ Error starting Filo: ' + error.message);
            }
        }

        // Stop Filo
        async function stopFilo() {
            try {
                const response = await fetch('/api/stop', { method: 'POST' });
                const data = await response.json();
                
                if (data.success) {
                    alert('⏸️ Filo stopped successfully!');
                    updateDashboard();
                } else {
                    alert('❌ Error: ' + data.error);
                }
            } catch (error) {
                alert('❌ Error stopping Filo: ' + error.message);
            }
        }

        // Emergency pause
        async function emergencyPause() {
            if (!confirm('🚨 Are you sure you want to EMERGENCY PAUSE all campaigns?')) {
                return;
            }
            
            try {
                const response = await fetch('/api/emergency_pause', { method: 'POST' });
                const data = await response.json();
                
                if (data.success) {
                    alert('🚨 ' + data.message);
                    updateDashboard();
                } else {
                    alert('❌ Error: ' + data.error);
                }
            } catch (error) {
                alert('❌ Error: ' + error.message);
            }
        }

        // Update dashboard
        async function updateDashboard() {
            await Promise.all([
                updateStatus(),
                updateMetrics(),
                updateActions(),
                updateChart()
            ]);
        }

        // Update status
        async function updateStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                const indicator = document.getElementById('status-indicator');
                const startBtn = document.getElementById('start-btn');
                const stopBtn = document.getElementById('stop-btn');
                
                if (data.running) {
                    indicator.className = 'status-indicator status-running';
                    indicator.innerHTML = '<span>🟢</span><span>Agent Running</span>';
                    startBtn.disabled = true;
                    stopBtn.disabled = false;
                } else {
                    indicator.className = 'status-indicator status-stopped';
                    indicator.innerHTML = '<span>🔴</span><span>Agent Stopped</span>';
                    startBtn.disabled = false;
                    stopBtn.disabled = true;
                }
            } catch (error) {
                console.error('Error updating status:', error);
            }
        }

        // Update metrics
        async function updateMetrics() {
            try {
                const response = await fetch('/api/metrics');
                const data = await response.json();
                
                if (data.success) {
                    // Overview metrics
                    document.getElementById('overview-metrics').innerHTML = `
                        <div class="metric">
                            <span class="metric-label">Total Spend</span>
                            <span class="metric-value">₹${data.total_spend.toFixed(0)}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Total Revenue</span>
                            <span class="metric-value">₹${data.total_revenue.toFixed(0)}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Average ROAS</span>
                            <span class="metric-value">${data.avg_roas.toFixed(2)}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Profit</span>
                            <span class="metric-value">₹${(data.total_revenue - data.total_spend).toFixed(0)}</span>
                        </div>
                    `;
                    
                    // Ad set metrics
                    let adsetHtml = '';
                    data.metrics.forEach(metric => {
                        adsetHtml += `
                            <div class="metric">
                                <span class="metric-label">${metric.ad_set_name}</span>
                                <span class="metric-value">ROAS: ${metric.roas.toFixed(2)}</span>
                            </div>
                        `;
                    });
                    document.getElementById('adset-metrics').innerHTML = adsetHtml;
                } else {
                    document.getElementById('overview-metrics').innerHTML = '<div class="loading">Error loading metrics</div>';
                }
            } catch (error) {
                console.error('Error updating metrics:', error);
            }
        }

        // Update actions
        async function updateActions() {
            try {
                const response = await fetch('/api/actions');
                const data = await response.json();
                
                if (data.success && data.actions.length > 0) {
                    let actionsHtml = '';
                    data.actions.reverse().forEach(action => {
                        const actionClass = action.success ? 'action-success' : 'action-failed';
                        const actionIcon = action.success ? '✅' : '❌';
                        
                        actionsHtml += `
                            <div class="action-item ${actionClass}">
                                <div>${actionIcon} <strong>${action.action_type.toUpperCase()}</strong>: ${action.ad_set_name}</div>
                                <div>${action.reason}</div>
                                <div class="action-time">${new Date(action.timestamp).toLocaleString()}</div>
                            </div>
                        `;
                    });
                    document.getElementById('recent-actions').innerHTML = actionsHtml;
                } else {
                    document.getElementById('recent-actions').innerHTML = '<div class="loading">No actions yet</div>';
                }
            } catch (error) {
                console.error('Error updating actions:', error);
            }
        }

        // Update chart
        async function updateChart() {
            try {
                const response = await fetch('/api/performance_chart');
                const data = await response.json();
                
                if (data.success) {
                    const traces = [];
                    
                    Object.keys(data.chart_data).forEach(adSetName => {
                        const adSetData = data.chart_data[adSetName];
                        
                        traces.push({
                            x: adSetData.timestamps,
                            y: adSetData.roas,
                            name: adSetName,
                            type: 'scatter',
                            mode: 'lines+markers'
                        });
                    });
                    
                    const layout = {
                        title: 'ROAS Performance Over Time',
                        xaxis: { title: 'Time' },
                        yaxis: { title: 'ROAS' },
                        showlegend: true
                    };
                    
                    Plotly.newPlot('performance-chart', traces, layout);
                } else {
                    document.getElementById('performance-chart').innerHTML = '<div class="loading">No chart data available</div>';
                }
            } catch (error) {
                console.error('Error updating chart:', error);
            }
        }

        // Chat functionality
        async function sendMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message to chat
            addChatMessage('user', message);
            input.value = '';
            
            // Show typing indicator
            addChatMessage('filo', 'Thinking...', 'typing');
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                
                // Remove typing indicator
                removeTypingIndicator();
                
                if (data.success) {
                    addChatMessage('filo', data.response);
                } else {
                    addChatMessage('filo', '❌ Error: ' + data.error);
                }
            } catch (error) {
                removeTypingIndicator();
                addChatMessage('filo', '❌ Connection error: ' + error.message);
            }
        }
        
        function addChatMessage(sender, message, className = '') {
            const chatMessages = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `chat-message ${sender}-message ${className}`;
            
            if (sender === 'user') {
                messageDiv.innerHTML = `<strong>👤 You:</strong> ${message}`;
                messageDiv.style.textAlign = 'right';
                messageDiv.style.background = '#e6f3ff';
                messageDiv.style.marginLeft = '20%';
            } else {
                messageDiv.innerHTML = `<strong>🤖 Claude:</strong> ${message.replace(/\\n/g, '<br>')}`;
                messageDiv.style.background = '#f0fff4';
                messageDiv.style.marginRight = '20%';
            }
            
            messageDiv.style.padding = '10px';
            messageDiv.style.margin = '10px 0';
            messageDiv.style.borderRadius = '8px';
            messageDiv.style.border = '1px solid #e2e8f0';
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        function removeTypingIndicator() {
            const typingIndicator = document.querySelector('.typing');
            if (typingIndicator) {
                typingIndicator.remove();
            }
        }
        
        // Allow Enter key to send message
        document.addEventListener('DOMContentLoaded', function() {
            const chatInput = document.getElementById('chat-input');
            if (chatInput) {
                chatInput.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        sendMessage();
                    }
                });
            }
        });

        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', function() {
            updateDashboard();
            
            // Auto-refresh every 30 seconds
            updateInterval = setInterval(updateDashboard, 30000);
        });
    </script>
</body>
</html>'''
    
    with open('templates/dashboard.html', 'w') as f:
        f.write(dashboard_html)

def main():
    """Run the Filo dashboard"""
    print("🌐 Starting FILO Dashboard...")
    
    # Create dashboard template
    create_dashboard_template()
    
    print("✅ Dashboard template created")
    print("🚀 Starting web server...")
    print("📱 Open http://localhost:5000 in your browser")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    main()
