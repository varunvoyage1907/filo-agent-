"""
FILO TRUE AI AGENT
The complete AI marketing agent powered by Claude 4 Sonnet
"""

import json
import os
import time
import threading
import logging
from datetime import datetime
from typing import Dict, List, Any
from filo_ai_brain import FiloAIBrain

class FiloTrueAI:
    """
    The complete TRUE AI FILO system
    Combines Claude 4 Sonnet intelligence with Facebook API execution
    """
    
    def __init__(self, config_file: str = "filo_config.json"):
        # Load configuration
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        # Initialize AI Brain with Claude 4 Sonnet
        self.ai_brain = FiloAIBrain(
            claude_api_key=os.getenv('ANTHROPIC_API_KEY', 'your_anthropic_api_key_here'),
            facebook_access_token=self.config["facebook_access_token"],
            ad_account_id=self.config["ad_account_id"]
        )
        
        # Agent state
        self.is_running = False
        self.monitoring_thread = None
        self.last_check = None
        self.actions_taken = 0
        self.monitoring_cycles = 0
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("FILO_TRUE_AI")
        
        self.logger.info("🤖 FILO TRUE AI initialized with Claude 4 Sonnet brain")
    
    def start(self):
        """Start the TRUE AI FILO agent"""
        if self.is_running:
            return {"status": "already_running"}
        
        self.is_running = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        
        self.logger.info("🚀 FILO TRUE AI started - Claude 4 Sonnet is now monitoring your campaigns!")
        
        return {
            "status": "started",
            "message": "FILO TRUE AI is now running with Claude 4 Sonnet intelligence",
            "capabilities": [
                "Intelligent campaign monitoring",
                "Strategic decision making",
                "Automatic optimizations",
                "Natural conversation interface",
                "Facebook API execution",
                "Continuous learning"
            ]
        }
    
    def stop(self):
        """Stop the TRUE AI FILO agent"""
        self.is_running = False
        
        summary = {
            "status": "stopped",
            "session_summary": {
                "monitoring_cycles": self.monitoring_cycles,
                "actions_taken": self.actions_taken,
                "last_check": self.last_check,
                "uptime": "Active session completed"
            }
        }
        
        self.logger.info("🛑 FILO TRUE AI stopped")
        return summary
    
    def chat(self, user_message: str, context: Dict = None) -> Dict:
        """
        Chat with FILO - powered by Claude 4 Sonnet
        This is the main interface for natural conversation
        """
        try:
            self.logger.info(f"💬 User: {user_message}")
            
            # Get AI response from Claude 4 Sonnet brain
            ai_response = self.ai_brain.think(user_message, context)
            
            self.logger.info(f"🧠 FILO AI: {ai_response[:100]}...")
            
            # Check if the AI wants to execute any actions
            actions_executed = self._execute_ai_actions(ai_response)
            
            return {
                "success": True,
                "response": ai_response,
                "actions_executed": actions_executed,
                "timestamp": datetime.now().isoformat(),
                "powered_by": "Claude 4 Sonnet"
            }
            
        except Exception as e:
            self.logger.error(f"Chat error: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": "I encountered an error processing your request. Please try again."
            }
    
    def _execute_ai_actions(self, ai_response: str) -> List[Dict]:
        """
        Parse AI response and execute any requested actions
        This is where the AI's decisions get implemented
        """
        actions_executed = []
        
        # Look for action indicators in the AI response
        # The AI can request Facebook API calls or terminal commands
        
        # Example patterns the AI might use:
        # "EXECUTE_FB_API: POST /adsets {...}"
        # "EXECUTE_COMMAND: python create_campaign.py"
        
        lines = ai_response.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Facebook API execution
            if line.startswith("EXECUTE_FB_API:"):
                try:
                    # Parse the API call
                    api_call = line.replace("EXECUTE_FB_API:", "").strip()
                    # Format: METHOD /endpoint {"param": "value"}
                    
                    parts = api_call.split(' ', 2)
                    if len(parts) >= 2:
                        method = parts[0]
                        endpoint = parts[1]
                        params = json.loads(parts[2]) if len(parts) > 2 else {}
                        
                        result = self.ai_brain.execute_facebook_api_call(method, endpoint, params)
                        actions_executed.append({
                            "type": "facebook_api",
                            "action": api_call,
                            "result": result
                        })
                        
                except Exception as e:
                    actions_executed.append({
                        "type": "facebook_api",
                        "action": line,
                        "error": str(e)
                    })
            
            # Terminal command execution
            elif line.startswith("EXECUTE_COMMAND:"):
                try:
                    command = line.replace("EXECUTE_COMMAND:", "").strip()
                    result = self.ai_brain.execute_terminal_command(command)
                    actions_executed.append({
                        "type": "terminal_command",
                        "action": command,
                        "result": result
                    })
                    
                except Exception as e:
                    actions_executed.append({
                        "type": "terminal_command",
                        "action": line,
                        "error": str(e)
                    })
        
        if actions_executed:
            self.actions_taken += len(actions_executed)
            self.logger.info(f"⚡ Executed {len(actions_executed)} actions based on AI decisions")
        
        return actions_executed
    
    def _monitoring_loop(self):
        """
        Continuous monitoring loop where the AI makes autonomous decisions
        """
        self.logger.info("🔍 Starting intelligent monitoring with Claude 4 Sonnet...")
        
        while self.is_running:
            try:
                self.monitoring_cycles += 1
                self.last_check = datetime.now().isoformat()
                
                # Get current campaign performance
                campaign_data = self.ai_brain.get_campaign_context()
                
                # Let the AI analyze and make decisions
                analysis_prompt = f"""
                Please analyze the current campaign performance and make any necessary optimizations.
                
                Current data: {json.dumps(campaign_data, indent=2)}
                
                Based on this data, should we:
                1. Scale any high-performing campaigns?
                2. Pause any underperforming campaigns?
                3. Adjust targeting or budgets?
                4. Create new ad variations?
                
                If you decide to take action, use the EXECUTE_FB_API: or EXECUTE_COMMAND: format to specify what to do.
                """
                
                ai_decision = self.ai_brain.think(analysis_prompt)
                
                # Execute any actions the AI decided on
                actions = self._execute_ai_actions(ai_decision)
                
                if actions:
                    self.logger.info(f"🧠 AI made {len(actions)} autonomous decisions")
                
                # Learn from performance
                self.ai_brain.learn_from_performance(campaign_data)
                
                # Wait before next check (increased to reduce API calls)
                time.sleep(self.config.get("monitoring_interval", 30) * 60)  # Convert minutes to seconds
                
            except Exception as e:
                self.logger.error(f"Monitoring loop error: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    def get_status(self) -> Dict:
        """Get current status of TRUE AI FILO"""
        return {
            "status": "running" if self.is_running else "stopped",
            "powered_by": "Claude 4 Sonnet",
            "monitoring_cycles": self.monitoring_cycles,
            "actions_taken": self.actions_taken,
            "last_check": self.last_check,
            "ai_brain_active": True,
            "capabilities": [
                "Strategic campaign analysis",
                "Autonomous optimization",
                "Natural language conversation",
                "Facebook API execution",
                "Continuous learning",
                "Real-time decision making"
            ]
        }
    
    def get_ai_insights(self) -> Dict:
        """Get AI insights about current campaigns"""
        try:
            campaign_data = self.ai_brain.get_campaign_context()
            
            insights_prompt = f"""
            Please provide strategic insights about the current campaign performance:
            
            {json.dumps(campaign_data, indent=2)}
            
            Give me:
            1. Overall performance assessment
            2. Key opportunities for improvement
            3. Strategic recommendations
            4. Risk factors to watch
            5. Next steps for scaling
            """
            
            ai_insights = self.ai_brain.think(insights_prompt)
            
            return {
                "success": True,
                "insights": ai_insights,
                "generated_by": "Claude 4 Sonnet",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def emergency_pause(self, reason: str = "Emergency stop requested") -> Dict:
        """Emergency pause all campaigns - AI safety feature"""
        try:
            pause_prompt = f"""
            EMERGENCY: Please pause all active campaigns immediately.
            Reason: {reason}
            
            Use EXECUTE_FB_API calls to pause all active ad sets.
            """
            
            ai_response = self.ai_brain.think(pause_prompt)
            actions = self._execute_ai_actions(ai_response)
            
            return {
                "success": True,
                "message": "Emergency pause executed by AI",
                "actions_taken": len(actions),
                "ai_response": ai_response
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Example usage
if __name__ == "__main__":
    # Initialize TRUE AI FILO
    filo_ai = FiloTrueAI()
    
    # Start the agent
    start_result = filo_ai.start()
    print("🚀 Start Result:", start_result)
    
    # Test chat
    chat_result = filo_ai.chat("What's the current performance of my campaigns and what should we optimize?")
    print("💬 Chat Result:", chat_result)
    
    # Get AI insights
    insights = filo_ai.get_ai_insights()
    print("🧠 AI Insights:", insights)
