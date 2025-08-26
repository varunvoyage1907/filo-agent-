#!/usr/bin/env python3
"""
🤖 FILO - Facebook Intelligence & Learning Optimizer
Your 24/7 AI Marketing Agent for Facebook Ads

Author: Claude (Anthropic)
Created for: Varun Agarwal - Eyewear Business
Purpose: Automated Facebook ads optimization with expert-level decision making
"""

import time
import json
import logging
import schedule
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import requests
import os
from dataclasses import dataclass
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - FILO - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('filo_agent.log'),
        logging.StreamHandler()
    ]
)

@dataclass
class CampaignMetrics:
    """Campaign performance metrics"""
    ad_set_id: str
    ad_set_name: str
    spend: float
    revenue: float
    roas: float
    cpc: float
    ctr: float
    impressions: int
    clicks: int
    conversions: int
    timestamp: datetime

@dataclass
class OptimizationAction:
    """Optimization action taken by Filo"""
    action_type: str  # 'scale_up', 'scale_down', 'pause', 'resume'
    ad_set_id: str
    ad_set_name: str
    old_value: Any
    new_value: Any
    reason: str
    timestamp: datetime
    success: bool

class FiloAgent:
    """
    🤖 FILO - Your AI Facebook Marketing Agent
    
    Capabilities:
    - 24/7 campaign monitoring
    - Automatic budget optimization
    - Performance-based scaling
    - Emergency protection
    - Smart notifications
    """
    
    def __init__(self, config_path: str = "filo_config.json"):
        """Initialize Filo with configuration"""
        self.config_path = config_path
        self.config = self.load_config()
        self.running = False
        self.last_check = None
        self.performance_history = []
        self.actions_taken = []
        
        # Facebook API setup
        self.access_token = self.config.get('facebook_access_token')
        self.ad_account_id = self.config.get('ad_account_id')
        self.api_base_url = "https://graph.facebook.com/v18.0"
        
        logging.info("🤖 FILO Agent initialized successfully")
        logging.info(f"📊 Monitoring ad account: {self.ad_account_id}")
        logging.info(f"⏰ Check interval: {self.config['monitoring_interval']} minutes")
    
    def load_config(self) -> Dict:
        """Load Filo configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            logging.info(f"✅ Configuration loaded from {self.config_path}")
            return config
        except FileNotFoundError:
            logging.warning(f"⚠️ Config file not found, creating default: {self.config_path}")
            return self.create_default_config()
    
    def create_default_config(self) -> Dict:
        """Create default configuration for Filo"""
        default_config = {
            "facebook_access_token": "YOUR_ACCESS_TOKEN_HERE",
            "ad_account_id": "act_612972137428654",
            "monitoring_interval": 15,  # minutes
            "rules": {
                "scale_up_roas": 5.0,
                "scale_down_roas": 3.5,
                "pause_roas": 3.0,
                "scale_up_percentage": 20,
                "scale_down_percentage": 15,
                "max_daily_spend": 12000,
                "min_daily_spend": 500,
                "max_cpc_increase": 50,  # percentage
                "min_conversions_for_action": 5
            },
            "notifications": {
                "email_enabled": True,
                "email_address": "your@email.com",
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "smtp_username": "your@gmail.com",
                "smtp_password": "your_app_password",
                "sms_enabled": False,
                "sms_number": "+91XXXXXXXXXX"
            },
            "safety": {
                "emergency_pause_enabled": True,
                "max_actions_per_hour": 10,
                "require_approval_for_large_changes": True,
                "large_change_threshold": 50  # percentage
            },
            "target_ad_sets": [
                "120233161126020134",  # Ray-Ban & Oakley Premium
                "120233169389280134",  # Expert Fashion & Luxury Lifestyle  
                "120233169411530134"   # Expert Career Peak Luxury
            ]
        }
        
        # Save default config
        with open(self.config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        logging.info(f"📝 Default configuration created: {self.config_path}")
        return default_config
    
    def get_campaign_metrics(self) -> List[CampaignMetrics]:
        """Fetch current performance metrics for all monitored ad sets"""
        metrics = []
        
        for ad_set_id in self.config['target_ad_sets']:
            try:
                # Get ad set insights
                url = f"{self.api_base_url}/{ad_set_id}/insights"
                params = {
                    'access_token': self.access_token,
                    'fields': 'spend,purchase_roas,cpc,ctr,impressions,clicks,actions',
                    'time_range': '{"since":"today","until":"today"}'
                }
                
                response = requests.get(url, params=params)
                data = response.json()
                
                if 'data' in data and data['data']:
                    insight = data['data'][0]
                    
                    # Get ad set name
                    ad_set_url = f"{self.api_base_url}/{ad_set_id}"
                    ad_set_params = {
                        'access_token': self.access_token,
                        'fields': 'name'
                    }
                    ad_set_response = requests.get(ad_set_url, params=ad_set_params)
                    ad_set_data = ad_set_response.json()
                    
                    # Extract metrics
                    spend = float(insight.get('spend', 0))
                    roas = float(insight.get('purchase_roas', [{'value': '0'}])[0]['value']) if insight.get('purchase_roas') else 0
                    revenue = spend * roas if roas > 0 else 0
                    cpc = float(insight.get('cpc', 0))
                    ctr = float(insight.get('ctr', 0))
                    impressions = int(insight.get('impressions', 0))
                    clicks = int(insight.get('clicks', 0))
                    
                    # Get conversions
                    conversions = 0
                    if insight.get('actions'):
                        for action in insight['actions']:
                            if action['action_type'] == 'purchase':
                                conversions = int(action['value'])
                                break
                    
                    metric = CampaignMetrics(
                        ad_set_id=ad_set_id,
                        ad_set_name=ad_set_data.get('name', f'Ad Set {ad_set_id}'),
                        spend=spend,
                        revenue=revenue,
                        roas=roas,
                        cpc=cpc,
                        ctr=ctr,
                        impressions=impressions,
                        clicks=clicks,
                        conversions=conversions,
                        timestamp=datetime.now()
                    )
                    
                    metrics.append(metric)
                    logging.info(f"📊 {metric.ad_set_name}: ROAS {metric.roas:.2f}, Spend ₹{metric.spend:.0f}")
                
            except Exception as e:
                logging.error(f"❌ Error fetching metrics for ad set {ad_set_id}: {str(e)}")
        
        return metrics
    
    def analyze_and_optimize(self, metrics: List[CampaignMetrics]) -> List[OptimizationAction]:
        """Analyze performance and determine optimization actions"""
        actions = []
        rules = self.config['rules']
        
        for metric in metrics:
            try:
                # Skip if not enough data
                if metric.conversions < rules['min_conversions_for_action']:
                    logging.info(f"⏸️ {metric.ad_set_name}: Insufficient conversions ({metric.conversions}), skipping optimization")
                    continue
                
                # Get current budget
                current_budget = self.get_ad_set_budget(metric.ad_set_id)
                if not current_budget:
                    continue
                
                # Scale up logic
                if metric.roas >= rules['scale_up_roas']:
                    new_budget = current_budget * (1 + rules['scale_up_percentage'] / 100)
                    
                    # Check safety limits
                    if new_budget <= rules['max_daily_spend']:
                        action = OptimizationAction(
                            action_type='scale_up',
                            ad_set_id=metric.ad_set_id,
                            ad_set_name=metric.ad_set_name,
                            old_value=current_budget,
                            new_value=new_budget,
                            reason=f"High ROAS ({metric.roas:.2f}) - scaling up {rules['scale_up_percentage']}%",
                            timestamp=datetime.now(),
                            success=False  # Will be updated after execution
                        )
                        actions.append(action)
                
                # Scale down logic
                elif metric.roas <= rules['scale_down_roas'] and metric.roas > rules['pause_roas']:
                    new_budget = current_budget * (1 - rules['scale_down_percentage'] / 100)
                    
                    # Check minimum budget
                    if new_budget >= rules['min_daily_spend']:
                        action = OptimizationAction(
                            action_type='scale_down',
                            ad_set_id=metric.ad_set_id,
                            ad_set_name=metric.ad_set_name,
                            old_value=current_budget,
                            new_value=new_budget,
                            reason=f"Low ROAS ({metric.roas:.2f}) - scaling down {rules['scale_down_percentage']}%",
                            timestamp=datetime.now(),
                            success=False
                        )
                        actions.append(action)
                
                # Pause logic
                elif metric.roas <= rules['pause_roas']:
                    action = OptimizationAction(
                        action_type='pause',
                        ad_set_id=metric.ad_set_id,
                        ad_set_name=metric.ad_set_name,
                        old_value='active',
                        new_value='paused',
                        reason=f"Very low ROAS ({metric.roas:.2f}) - pausing for protection",
                        timestamp=datetime.now(),
                        success=False
                    )
                    actions.append(action)
                
            except Exception as e:
                logging.error(f"❌ Error analyzing {metric.ad_set_name}: {str(e)}")
        
        return actions
    
    def execute_actions(self, actions: List[OptimizationAction]) -> None:
        """Execute optimization actions via Facebook API"""
        for action in actions:
            try:
                success = False
                
                if action.action_type in ['scale_up', 'scale_down']:
                    success = self.update_ad_set_budget(action.ad_set_id, action.new_value)
                elif action.action_type == 'pause':
                    success = self.pause_ad_set(action.ad_set_id)
                elif action.action_type == 'resume':
                    success = self.resume_ad_set(action.ad_set_id)
                
                action.success = success
                self.actions_taken.append(action)
                
                if success:
                    logging.info(f"✅ {action.action_type.upper()}: {action.ad_set_name} - {action.reason}")
                    self.send_notification(action)
                else:
                    logging.error(f"❌ FAILED {action.action_type.upper()}: {action.ad_set_name}")
                
            except Exception as e:
                logging.error(f"❌ Error executing action for {action.ad_set_name}: {str(e)}")
                action.success = False
    
    def get_ad_set_budget(self, ad_set_id: str) -> Optional[float]:
        """Get current daily budget for an ad set"""
        try:
            url = f"{self.api_base_url}/{ad_set_id}"
            params = {
                'access_token': self.access_token,
                'fields': 'daily_budget'
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'daily_budget' in data:
                return float(data['daily_budget']) / 100  # Convert from cents
            
        except Exception as e:
            logging.error(f"❌ Error getting budget for ad set {ad_set_id}: {str(e)}")
        
        return None
    
    def update_ad_set_budget(self, ad_set_id: str, new_budget: float) -> bool:
        """Update ad set daily budget"""
        try:
            url = f"{self.api_base_url}/{ad_set_id}"
            data = {
                'access_token': self.access_token,
                'daily_budget': int(new_budget * 100)  # Convert to cents
            }
            
            response = requests.post(url, data=data)
            return response.status_code == 200
            
        except Exception as e:
            logging.error(f"❌ Error updating budget for ad set {ad_set_id}: {str(e)}")
            return False
    
    def pause_ad_set(self, ad_set_id: str) -> bool:
        """Pause an ad set"""
        try:
            url = f"{self.api_base_url}/{ad_set_id}"
            data = {
                'access_token': self.access_token,
                'status': 'PAUSED'
            }
            
            response = requests.post(url, data=data)
            return response.status_code == 200
            
        except Exception as e:
            logging.error(f"❌ Error pausing ad set {ad_set_id}: {str(e)}")
            return False
    
    def resume_ad_set(self, ad_set_id: str) -> bool:
        """Resume a paused ad set"""
        try:
            url = f"{self.api_base_url}/{ad_set_id}"
            data = {
                'access_token': self.access_token,
                'status': 'ACTIVE'
            }
            
            response = requests.post(url, data=data)
            return response.status_code == 200
            
        except Exception as e:
            logging.error(f"❌ Error resuming ad set {ad_set_id}: {str(e)}")
            return False
    
    def send_notification(self, action: OptimizationAction) -> None:
        """Send notification about optimization action"""
        if not self.config['notifications']['email_enabled']:
            return
        
        try:
            subject = f"🤖 FILO Action: {action.action_type.title()} - {action.ad_set_name}"
            
            body = f"""
🤖 FILO has taken an optimization action:

📊 Ad Set: {action.ad_set_name}
⚡ Action: {action.action_type.upper()}
📈 Reason: {action.reason}
⏰ Time: {action.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

"""
            
            if action.action_type in ['scale_up', 'scale_down']:
                body += f"💰 Budget: ₹{action.old_value:.0f} → ₹{action.new_value:.0f}\n"
            
            body += f"""
✅ Status: {'SUCCESS' if action.success else 'FAILED'}

---
🤖 FILO - Your AI Marketing Agent
Protecting and optimizing your Facebook ads 24/7
"""
            
            self.send_email(subject, body)
            
        except Exception as e:
            logging.error(f"❌ Error sending notification: {str(e)}")
    
    def send_email(self, subject: str, body: str) -> None:
        """Send email notification"""
        try:
            config = self.config['notifications']
            
            msg = MimeMultipart()
            msg['From'] = config['smtp_username']
            msg['To'] = config['email_address']
            msg['Subject'] = subject
            
            msg.attach(MimeText(body, 'plain'))
            
            server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
            server.starttls()
            server.login(config['smtp_username'], config['smtp_password'])
            server.send_message(msg)
            server.quit()
            
            logging.info(f"📧 Email notification sent: {subject}")
            
        except Exception as e:
            logging.error(f"❌ Error sending email: {str(e)}")
    
    def monitoring_cycle(self) -> None:
        """Main monitoring and optimization cycle"""
        try:
            logging.info("🔍 Starting monitoring cycle...")
            
            # Get current metrics
            metrics = self.get_campaign_metrics()
            if not metrics:
                logging.warning("⚠️ No metrics retrieved, skipping cycle")
                return
            
            # Store metrics history
            self.performance_history.extend(metrics)
            
            # Analyze and determine actions
            actions = self.analyze_and_optimize(metrics)
            
            if actions:
                logging.info(f"🎯 {len(actions)} optimization actions planned")
                
                # Execute actions
                self.execute_actions(actions)
                
                # Send summary
                self.send_cycle_summary(metrics, actions)
            else:
                logging.info("✅ All campaigns performing well, no actions needed")
            
            self.last_check = datetime.now()
            
        except Exception as e:
            logging.error(f"❌ Error in monitoring cycle: {str(e)}")
    
    def send_cycle_summary(self, metrics: List[CampaignMetrics], actions: List[OptimizationAction]) -> None:
        """Send summary of monitoring cycle"""
        try:
            total_spend = sum(m.spend for m in metrics)
            total_revenue = sum(m.revenue for m in metrics)
            avg_roas = total_revenue / total_spend if total_spend > 0 else 0
            
            subject = f"📊 FILO Cycle Summary - ROAS: {avg_roas:.2f}"
            
            body = f"""
📊 FILO MONITORING CYCLE SUMMARY
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

💰 PERFORMANCE OVERVIEW:
• Total Spend: ₹{total_spend:.0f}
• Total Revenue: ₹{total_revenue:.0f}
• Average ROAS: {avg_roas:.2f}

📈 AD SET PERFORMANCE:
"""
            
            for metric in metrics:
                body += f"• {metric.ad_set_name}: ROAS {metric.roas:.2f}, Spend ₹{metric.spend:.0f}\n"
            
            if actions:
                body += f"\n⚡ ACTIONS TAKEN ({len(actions)}):\n"
                for action in actions:
                    status = "✅" if action.success else "❌"
                    body += f"{status} {action.action_type.upper()}: {action.ad_set_name}\n"
            
            body += """
---
🤖 FILO continues monitoring your campaigns
Next check in 15 minutes
"""
            
            self.send_email(subject, body)
            
        except Exception as e:
            logging.error(f"❌ Error sending cycle summary: {str(e)}")
    
    def start(self) -> None:
        """Start Filo agent"""
        if self.running:
            logging.warning("⚠️ Filo is already running")
            return
        
        self.running = True
        logging.info("🚀 FILO Agent starting...")
        
        # Schedule monitoring cycles
        schedule.every(self.config['monitoring_interval']).minutes.do(self.monitoring_cycle)
        
        # Send startup notification
        self.send_startup_notification()
        
        # Run initial cycle
        self.monitoring_cycle()
        
        # Main loop
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            logging.info("🛑 Filo stopped by user")
        except Exception as e:
            logging.error(f"❌ Filo crashed: {str(e)}")
        finally:
            self.stop()
    
    def stop(self) -> None:
        """Stop Filo agent"""
        self.running = False
        logging.info("🛑 FILO Agent stopped")
        
        # Send shutdown notification
        try:
            self.send_email(
                "🛑 FILO Agent Stopped",
                f"""
🤖 FILO has been stopped at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 SESSION SUMMARY:
• Monitoring cycles completed: {len(self.performance_history) // len(self.config['target_ad_sets'])}
• Actions taken: {len(self.actions_taken)}
• Last check: {self.last_check.strftime('%Y-%m-%d %H:%M:%S') if self.last_check else 'Never'}

Your campaigns are no longer being monitored automatically.
Restart FILO to resume optimization.

---
🤖 FILO - Your AI Marketing Agent
"""
            )
        except:
            pass
    
    def send_startup_notification(self) -> None:
        """Send notification when Filo starts"""
        try:
            self.send_email(
                "🚀 FILO Agent Started",
                f"""
🤖 FILO is now monitoring your Facebook campaigns!

⚙️ CONFIGURATION:
• Monitoring interval: {self.config['monitoring_interval']} minutes
• Scale up ROAS threshold: {self.config['rules']['scale_up_roas']}
• Scale down ROAS threshold: {self.config['rules']['scale_down_roas']}
• Pause ROAS threshold: {self.config['rules']['pause_roas']}
• Max daily spend: ₹{self.config['rules']['max_daily_spend']}

🎯 MONITORING AD SETS:
"""
                + "\n".join([f"• {ad_set_id}" for ad_set_id in self.config['target_ad_sets']]) +
                """

🛡️ SAFETY FEATURES ACTIVE:
• Emergency pause enabled
• Budget limits enforced
• Action logging enabled

FILO will now optimize your campaigns automatically.
You'll receive notifications for all actions taken.

---
🤖 FILO - Your AI Marketing Agent
Protecting and growing your investment 24/7
"""
            )
        except Exception as e:
            logging.error(f"❌ Error sending startup notification: {str(e)}")


def main():
    """Main function to run Filo"""
    print("🤖 FILO - Facebook Intelligence & Learning Optimizer")
    print("=" * 55)
    print("Your 24/7 AI Marketing Agent")
    print()
    
    # Initialize Filo
    filo = FiloAgent()
    
    # Start monitoring
    try:
        filo.start()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Filo...")
        filo.stop()


if __name__ == "__main__":
    main()
