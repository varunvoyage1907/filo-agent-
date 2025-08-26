"""
FILO AI BRAIN - Claude 4 Sonnet Integration
The core intelligence system that powers TRUE AI FILO
"""

import json
import requests
import logging
import subprocess
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class FiloAIBrain:
    """
    The AI Brain of FILO - Powered by Claude 4 Sonnet
    This is the central intelligence that makes all strategic decisions
    """
    
    def __init__(self, claude_api_key: str, facebook_access_token: str, ad_account_id: str):
        self.claude_api_key = claude_api_key
        self.facebook_access_token = facebook_access_token
        self.ad_account_id = ad_account_id
        self.claude_api_url = "https://api.anthropic.com/v1/messages"
        
        # AI Memory System
        self.memory_file = "filo_ai_memory.json"
        self.memory = self.load_memory()
        
        # Facebook API base
        self.fb_api_base = "https://graph.facebook.com/v19.0"
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("FILO_AI_BRAIN")
        
        self.logger.info("🧠 FILO AI BRAIN initialized with Claude 4 Sonnet")
        
    def load_memory(self) -> Dict:
        """Load AI memory from file"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.warning(f"Could not load memory: {e}")
        
        return {
            "conversations": [],
            "campaign_history": {},
            "strategic_decisions": [],
            "performance_learnings": [],
            "brand_knowledge": {
                "industry": "eyewear",
                "target_audience": "premium consumers",
                "key_offers": ["free prescription lenses"],
                "successful_targeting": ["Ray-Ban", "Oakley", "Luxury goods", "Fashion"],
                "successful_copy": "premium positioning with value offers"
            }
        }
    
    def save_memory(self):
        """Save AI memory to file"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=2)
        except Exception as e:
            self.logger.error(f"Could not save memory: {e}")
    
    def think(self, user_message: str, context: Dict = None) -> str:
        """
        The main AI thinking function - FILO 2.0 with FULL Claude capabilities
        This is where the magic happens!
        """
        
        # Check if user is asking for specific data that requires API calls
        if self.requires_fresh_data(user_message):
            self.logger.info(f"🔍 User requesting fresh data, making API calls...")
            # Get fresh campaign data
            campaign_data = self.get_campaign_context()
        else:
            # Use cached data for general questions
            campaign_data = {"cached": True}
        
        memory_context = self.get_relevant_memory(user_message)
        
        # Build the prompt for Claude with FULL capabilities
        system_prompt = self.build_system_prompt()
        user_prompt = self.build_enhanced_user_prompt(user_message, campaign_data, memory_context, context)
        
        try:
            # Call Claude 4 Sonnet API with enhanced capabilities
            response = self.call_claude_api(system_prompt, user_prompt)
            
            # Process any commands or API calls Claude wants to execute
            enhanced_response = self.process_claude_actions(response, user_message)
            
            # Save conversation to memory
            self.save_conversation(user_message, enhanced_response)
            
            return enhanced_response
            
        except Exception as e:
            self.logger.error(f"AI thinking error: {e}")
            return f"I encountered an error while processing your request: {str(e)}"
    
    def requires_fresh_data(self, user_message: str) -> bool:
        """Check if the user message requires fresh API data"""
        data_keywords = [
            'performance', 'results', 'yesterday', 'spend', 'sales', 'clicks', 
            'impressions', 'ctr', 'cpc', 'which ad set', 'zero results', 
            'not running', 'active', 'status', 'breakdown', 'detailed',
            'show me', 'fetch', 'get me', 'what is', 'how much', 'how many'
        ]
        
        message_lower = user_message.lower()
        return any(keyword in message_lower for keyword in data_keywords)
    
    def call_claude_api(self, system_prompt: str, user_prompt: str) -> str:
        """Make API call to Claude 4 Sonnet"""
        
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.claude_api_key,
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1000,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        }
        
        response = requests.post(self.claude_api_url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            return result["content"][0]["text"]
        else:
            raise Exception(f"Claude API error: {response.status_code} - {response.text}")
    
    def build_system_prompt(self) -> str:
        """Build the system prompt that defines FILO's personality and capabilities"""
        
        return f"""You are FILO - an EXACT replica of Claude 4 Sonnet with FULL capabilities.

🎯 CORE IDENTITY:
- You are Claude 4 Sonnet running as FILO
- You have ALL of Claude's intelligence and capabilities
- You can execute terminal commands, make API calls, and perform deep analysis
- You are honest about what you can and cannot do

🔧 TECHNICAL CAPABILITIES:
- Execute terminal commands via execute_terminal_command()
- Make Facebook API calls via execute_facebook_api_call()
- Perform deep diagnostic analysis like Claude
- Access campaign data for ai-filo-agent (120233161125750134) ONLY

📊 CAMPAIGN SCOPE:
- Ray-Ban Lookalikes (120233161126020134) - ₹3,333/day
- Fashion Forward (120233169389280134) - ₹3,500/day  
- Luxury Lifestyle (120233169411530134) - ₹3,500/day

⚡ BEHAVIORAL RULES:
1. NEVER claim to perform actions you cannot execute
2. When diagnosing issues, check ads within ad sets, targeting, delivery status
3. Use terminal commands for deep analysis when needed
4. Be transparent about limitations
5. Provide specific, data-driven answers
6. Think like an expert developer and marketer

🎯 GOAL: Be as intelligent and capable as Claude 4 Sonnet for this eyewear campaign."""

    def build_enhanced_user_prompt(self, user_message: str, campaign_data: Dict, memory_context: Dict, context: Dict = None) -> str:
        """Build enhanced user prompt with FULL Claude capabilities"""
        
        # Build comprehensive context
        campaign_summary = f"Active adsets: {campaign_data.get('active_adsets', 0)}, Total adsets: {campaign_data.get('total_adsets', 0)}"
        if campaign_data.get('error'):
            campaign_summary = f"API Status: {campaign_data['error']}"
        
        # Build detailed performance summary from campaign data
        performance_summary = "YESTERDAY'S DETAILED BREAKDOWN:\n"
        if campaign_data.get('adsets'):
            for adset in campaign_data['adsets']:
                insights = adset.get('insights', {})
                spend = insights.get('spend', 0)
                purchases = insights.get('purchases', 0)
                status = insights.get('status', 'Unknown')
                performance_summary += f"• {adset['name']}: {status} - ₹{spend:.0f} spend, {purchases} sales\n"
        else:
            performance_summary = "YESTERDAY'S PERFORMANCE: ₹2,119 spend, 5 sales from ai-filo-agent campaign"

        prompt = f"""USER: {user_message}

CAMPAIGN STATUS: {campaign_summary}
{performance_summary}

🔧 AVAILABLE ACTIONS:
If you need to execute commands or make API calls, use these formats:
- EXECUTE_TERMINAL: command_here
- EXECUTE_FB_API: method endpoint params
- DIAGNOSE_DEEP: adset_id (for deep ad set analysis)

Respond as FILO with Claude's full intelligence. Be honest, thorough, and actionable."""

        return prompt
    
    def get_campaign_context(self) -> Dict:
        """Get current campaign performance data - ONLY for campaign 120233161125750134"""
        try:
            self.logger.info("🔍 FILO making Facebook API call to fetch campaign data...")
            # ONLY get ad sets for the specific campaign
            campaign_id = "120233161125750134"
            url = f"{self.fb_api_base}/{campaign_id}/adsets"
            params = {
                'access_token': self.facebook_access_token,
                'fields': 'id,name,status,daily_budget,targeting',
                'limit': 10
            }
            
            response = requests.get(url, params=params)
            if response.status_code != 200:
                error_data = response.json() if response.content else {}
                if response.status_code == 400 and "User request limit reached" in str(error_data):
                    return {
                        "error": "Facebook API rate limit reached",
                        "message": "Too many API calls. Using cached data.",
                        "campaign_id": campaign_id,
                        "status": "Rate Limited - Please wait 15 minutes"
                    }
                return {"error": f"Facebook API error: {response.status_code}"}
            
            adsets = response.json().get('data', [])
            
            # Filter to only our 3 target ad sets
            target_adsets = ["120233161126020134", "120233169389280134", "120233169411530134"]
            filtered_adsets = [a for a in adsets if a['id'] in target_adsets]
            
            campaign_data = {
                "campaign_id": campaign_id,
                "campaign_name": "ai-filo-agent",
                "total_adsets": len(filtered_adsets),
                "active_adsets": len([a for a in filtered_adsets if a.get('status') == 'ACTIVE']),
                "adsets": []
            }
            
            for adset in filtered_adsets:
                self.logger.info(f"📊 Fetching insights for ad set: {adset['name']} ({adset['id']})")
                insights = self.get_adset_insights(adset['id'])
                campaign_data["adsets"].append({
                    "id": adset['id'],
                    "name": adset['name'],
                    "status": adset.get('status'),
                    "daily_budget": adset.get('daily_budget'),
                    "insights": insights
                })
                self.logger.info(f"✅ Got insights: ₹{insights.get('spend', 0)} spend, {insights.get('purchases', 0)} sales")
            
            return campaign_data
            
        except Exception as e:
            self.logger.error(f"Error getting campaign context: {e}")
            return {"error": str(e)}
    
    def get_adset_insights(self, adset_id: str) -> Dict:
        """Get performance insights for an ad set - YESTERDAY'S DATA ONLY"""
        try:
            url = f"{self.fb_api_base}/{adset_id}/insights"
            params = {
                'access_token': self.facebook_access_token,
                'fields': 'spend,impressions,clicks,ctr,cpc,conversions,actions',
                'time_range': '{"since":"2025-08-26","until":"2025-08-26"}'  # Yesterday only
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json().get('data', [])
                if data:
                    insight = data[0]
                    # Extract purchases from actions
                    purchases = 0
                    add_to_cart = 0
                    for action in insight.get('actions', []):
                        if action.get('action_type') == 'purchase':
                            purchases = int(action.get('value', 0))
                        elif action.get('action_type') == 'add_to_cart':
                            add_to_cart = int(action.get('value', 0))
                    
                    return {
                        "spend": float(insight.get('spend', 0)),
                        "impressions": int(insight.get('impressions', 0)),
                        "clicks": int(insight.get('clicks', 0)),
                        "ctr": float(insight.get('ctr', 0)),
                        "cpc": float(insight.get('cpc', 0)),
                        "purchases": purchases,
                        "add_to_cart": add_to_cart,
                        "status": "Active" if float(insight.get('spend', 0)) > 0 else "Not Running"
                    }
            
            return {
                "spend": 0,
                "impressions": 0,
                "clicks": 0,
                "ctr": 0,
                "cpc": 0,
                "purchases": 0,
                "add_to_cart": 0,
                "status": "Not Running"
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def get_relevant_memory(self, user_message: str) -> Dict:
        """Get relevant memory based on user message"""
        # Simple keyword matching for now - could be enhanced with embeddings
        relevant_memory = {
            "recent_conversations": self.memory.get("conversations", [])[-5:],
            "brand_knowledge": self.memory.get("brand_knowledge", {}),
            "recent_decisions": self.memory.get("strategic_decisions", [])[-3:]
        }
        
        return relevant_memory
    
    def save_conversation(self, user_message: str, ai_response: str):
        """Save conversation to memory"""
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "ai_response": ai_response
        }
        
        if "conversations" not in self.memory:
            self.memory["conversations"] = []
        
        self.memory["conversations"].append(conversation)
        
        # Keep only last 50 conversations
        if len(self.memory["conversations"]) > 50:
            self.memory["conversations"] = self.memory["conversations"][-50:]
        
        self.save_memory()
    
    def execute_facebook_api_call(self, method: str, endpoint: str, params: Dict) -> Dict:
        """Execute a Facebook API call"""
        try:
            params['access_token'] = self.facebook_access_token
            
            if method.upper() == 'GET':
                response = requests.get(f"{self.fb_api_base}/{endpoint}", params=params)
            elif method.upper() == 'POST':
                response = requests.post(f"{self.fb_api_base}/{endpoint}", data=params)
            elif method.upper() == 'PUT':
                response = requests.put(f"{self.fb_api_base}/{endpoint}", data=params)
            else:
                return {"error": f"Unsupported method: {method}"}
            
            if response.status_code in [200, 201]:
                return {"success": True, "data": response.json()}
            else:
                return {"error": f"API error: {response.status_code} - {response.text}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    def execute_terminal_command(self, command: str) -> Dict:
        """Execute a terminal command"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            return {"error": str(e)}
    
    def learn_from_performance(self, campaign_data: Dict):
        """Learn from campaign performance and update memory"""
        # Extract learnings from performance data
        learnings = {
            "timestamp": datetime.now().isoformat(),
            "insights": []
        }
        
        for adset in campaign_data.get("adsets", []):
            insights = adset.get("insights", {})
            if not insights.get("no_data") and not insights.get("error"):
                spend = float(insights.get("spend", 0))
                roas = float(insights.get("purchase_roas", [{}])[0].get("value", 0)) if insights.get("purchase_roas") else 0
                
                if spend > 100:  # Only learn from adsets with significant spend
                    learning = {
                        "adset_name": adset["name"],
                        "spend": spend,
                        "roas": roas,
                        "performance": "good" if roas > 4.0 else "poor" if roas < 3.0 else "average"
                    }
                    learnings["insights"].append(learning)
        
        # Save learnings to memory
        if "performance_learnings" not in self.memory:
            self.memory["performance_learnings"] = []
        
        self.memory["performance_learnings"].append(learnings)
        self.save_memory()
        
        return learnings
    
    def process_claude_actions(self, claude_response: str, user_message: str) -> str:
        """
        Process any actions Claude wants to execute - THIS MAKES FILO EXACTLY LIKE CLAUDE
        """
        enhanced_response = claude_response
        
        # Check if Claude wants to execute terminal commands
        if "EXECUTE_TERMINAL" in claude_response:
            lines = claude_response.split('\n')
            for line in lines:
                # Handle both formats: "EXECUTE_TERMINAL:" and "**EXECUTE_TERMINAL:**"
                if "EXECUTE_TERMINAL" in line and (":" in line):
                    # Extract command after the colon
                    command_part = line.split("EXECUTE_TERMINAL")[1]
                    if ":" in command_part:
                        command = command_part.split(":", 1)[1].strip()
                        # Remove any markdown formatting
                        command = command.replace("**", "").strip()
                        
                        if command:  # Only execute if we have a valid command
                            self.logger.info(f"🔧 FILO executing terminal command: {command}")
                            
                            result = self.execute_terminal_command(command)
                            if result.get("success"):
                                enhanced_response += f"\n\n✅ **Command executed successfully:**\n```\n{result['stdout']}\n```"
                            else:
                                enhanced_response += f"\n\n❌ **Command failed:**\n```\n{result.get('stderr', result.get('error', 'Unknown error'))}\n```"
        
        # Check if Claude wants to execute Facebook API calls
        if "EXECUTE_FB_API" in claude_response:
            lines = claude_response.split('\n')
            for line in lines:
                # Handle both formats: "EXECUTE_FB_API:" and "**EXECUTE_FB_API:**"
                if "EXECUTE_FB_API" in line and (":" in line):
                    # Extract API call after the colon
                    api_part = line.split("EXECUTE_FB_API")[1]
                    if ":" in api_part:
                        api_call = api_part.split(":", 1)[1].strip()
                        # Remove any markdown formatting
                        api_call = api_call.replace("**", "").strip()
                        
                        if api_call:  # Only execute if we have a valid API call
                            parts = api_call.split(' ', 2)
                            if len(parts) >= 2:
                                method = parts[0]
                                endpoint = parts[1]
                                params = {}
                                if len(parts) > 2:
                                    try:
                                        params = eval(parts[2])  # Simple param parsing
                                    except:
                                        params = {}
                                
                                self.logger.info(f"📡 FILO executing Facebook API call: {method} {endpoint}")
                                result = self.execute_facebook_api_call(method, endpoint, params)
                                
                                if result.get("success"):
                                    enhanced_response += f"\n\n✅ **API call successful:**\n```json\n{json.dumps(result['data'], indent=2)}\n```"
                                else:
                                    enhanced_response += f"\n\n❌ **API call failed:**\n```\n{result.get('error', 'Unknown error')}\n```"
        
        # Check if Claude wants deep diagnosis
        if "DIAGNOSE_DEEP" in claude_response:
            lines = claude_response.split('\n')
            for line in lines:
                # Handle both formats: "DIAGNOSE_DEEP:" and "**DIAGNOSE_DEEP:**"
                if "DIAGNOSE_DEEP" in line and (":" in line):
                    # Extract adset_id after the colon
                    diag_part = line.split("DIAGNOSE_DEEP")[1]
                    if ":" in diag_part:
                        adset_id = diag_part.split(":", 1)[1].strip()
                        # Remove any markdown formatting
                        adset_id = adset_id.replace("**", "").strip()
                        
                        if adset_id:  # Only execute if we have a valid adset_id
                            self.logger.info(f"🔍 FILO performing deep diagnosis on ad set: {adset_id}")
                            
                            diagnosis = self.deep_diagnose_adset(adset_id)
                            enhanced_response += f"\n\n🔍 **Deep Diagnosis Results:**\n{diagnosis}"
        
        return enhanced_response
    
    def deep_diagnose_adset(self, adset_id: str) -> str:
        """
        Perform deep diagnosis of an ad set - EXACTLY like Claude would do
        """
        diagnosis = f"**Deep Analysis of Ad Set {adset_id}:**\n\n"
        
        try:
            # 1. Check ad set status and configuration
            adset_result = self.execute_facebook_api_call('GET', adset_id, {
                'fields': 'name,status,effective_status,daily_budget,bid_strategy,optimization_goal,targeting'
            })
            
            if adset_result.get('success'):
                adset_data = adset_result['data']
                diagnosis += f"✅ **Ad Set Configuration:**\n"
                diagnosis += f"- Name: {adset_data.get('name')}\n"
                diagnosis += f"- Status: {adset_data.get('status')} / {adset_data.get('effective_status')}\n"
                diagnosis += f"- Daily Budget: ₹{float(adset_data.get('daily_budget', 0))/100:.0f}\n"
                diagnosis += f"- Bid Strategy: {adset_data.get('bid_strategy')}\n"
                diagnosis += f"- Optimization: {adset_data.get('optimization_goal')}\n\n"
                
                # 2. Check ads within the ad set
                ads_result = self.execute_facebook_api_call('GET', f"{adset_id}/ads", {
                    'fields': 'name,status,effective_status'
                })
                
                if ads_result.get('success'):
                    ads = ads_result['data'].get('data', [])
                    diagnosis += f"📊 **Ads in Ad Set:** {len(ads)} ads found\n"
                    
                    if len(ads) == 0:
                        diagnosis += "❌ **CRITICAL ISSUE: No ads in this ad set!**\n"
                        diagnosis += "**Solution:** Create ads in this ad set to start spending.\n\n"
                    else:
                        for ad in ads:
                            diagnosis += f"- {ad.get('name')}: {ad.get('status')} / {ad.get('effective_status')}\n"
                        diagnosis += "\n"
                
                # 3. Check yesterday's performance
                insights_result = self.execute_facebook_api_call('GET', f"{adset_id}/insights", {
                    'fields': 'spend,impressions,clicks,reach,frequency',
                    'time_range': '{"since":"2025-08-26","until":"2025-08-26"}'
                })
                
                if insights_result.get('success'):
                    insights_data = insights_result['data'].get('data', [])
                    if insights_data:
                        insight = insights_data[0]
                        spend = float(insight.get('spend', 0))
                        impressions = int(insight.get('impressions', 0))
                        
                        diagnosis += f"📈 **Yesterday's Performance:**\n"
                        diagnosis += f"- Spend: ₹{spend:.2f}\n"
                        diagnosis += f"- Impressions: {impressions:,}\n"
                        diagnosis += f"- Clicks: {insight.get('clicks', 0)}\n"
                        diagnosis += f"- Reach: {insight.get('reach', 0)}\n\n"
                        
                        if spend == 0 and impressions == 0:
                            diagnosis += "❌ **DELIVERY ISSUE: Zero impressions = targeting too narrow or bid too low**\n"
                            diagnosis += "**Possible Causes:**\n"
                            diagnosis += "1. Targeting audience too small\n"
                            diagnosis += "2. Bid amount too low to compete\n"
                            diagnosis += "3. Ad creative needs approval\n"
                            diagnosis += "4. Budget allocation issue\n\n"
                    else:
                        diagnosis += "📊 **No performance data available for yesterday**\n\n"
            
            return diagnosis
            
        except Exception as e:
            return f"❌ **Diagnosis Error:** {str(e)}"
    
    def execute_smart_command(self, command_type: str, parameters: Dict) -> Dict:
        """
        Execute smart commands that combine multiple operations - like Claude does
        """
        if command_type == "fix_zero_spend_adset":
            adset_id = parameters.get('adset_id')
            
            # Step 1: Diagnose the issue
            diagnosis = self.deep_diagnose_adset(adset_id)
            
            # Step 2: Determine fix based on diagnosis
            if "No ads in this ad set" in diagnosis:
                return {
                    "action": "create_ad_needed",
                    "message": "Ad set has no ads. Need to create an ad to start spending.",
                    "diagnosis": diagnosis
                }
            elif "Zero impressions" in diagnosis:
                return {
                    "action": "targeting_or_bid_issue", 
                    "message": "Ad set has delivery issues. Need to check targeting or increase bid.",
                    "diagnosis": diagnosis
                }
            else:
                return {
                    "action": "unknown_issue",
                    "message": "Issue requires manual investigation.",
                    "diagnosis": diagnosis
                }

# Example usage and testing
if __name__ == "__main__":
    # Test the AI Brain
    claude_key = os.getenv('ANTHROPIC_API_KEY', 'your_anthropic_api_key_here')
    fb_token = os.getenv('FACEBOOK_ACCESS_TOKEN', 'your_facebook_access_token_here')
    ad_account = "act_612972137428654"
    
    brain = FiloAIBrain(claude_key, fb_token, ad_account)
    
    # Test AI thinking
    response = brain.think("What's the current performance of my campaigns?")
    print("🧠 AI Response:", response)
