#!/usr/bin/env python3
"""
FILO 6-Hour Monitoring Protocol
Campaign: ai-filo-agent (Premium Eyewear)
Target: ROAS 5+ Maintenance
"""

import json
import os
from datetime import datetime, timedelta
from facebook_ads_api import FacebookAdsAPI

class FiloMonitor:
    def __init__(self):
        self.campaign_id = "120233161125750134"
        self.account_id = "act_612972137428654"
        self.target_roas = 5.0
        self.total_budget = 15000
        
        # Load campaign memory
        with open('/workspace/filo_campaign_memory.json', 'r') as f:
            self.memory = json.load(f)
    
    def check_performance(self):
        """6-hour performance check with actionable insights"""
        
        print("🔍 FILO 6-HOUR PERFORMANCE ANALYSIS")
        print("=" * 60)
        
        try:
            api = FacebookAdsAPI()
            
            # Get campaign insights
            insights = api.get_campaign_insights(self.campaign_id, 'today')
            
            current_spend = float(insights.get('spend', 0))
            current_clicks = int(insights.get('clicks', 0))
            current_cpc = float(insights.get('cpc', 0))
            current_ctr = float(insights.get('ctr', 0))
            
            print(f"📊 CURRENT PERFORMANCE:")
            print(f"   💰 Spend: ₹{current_spend:,.2f} / ₹{self.total_budget:,}")
            print(f"   👆 Clicks: {current_clicks:,}")
            print(f"   💵 CPC: ₹{current_cpc:.2f}")
            print(f"   📊 CTR: {current_ctr:.2f}%")
            
            # Performance analysis
            spend_utilization = (current_spend / self.total_budget) * 100
            
            print(f"\n🎯 PERFORMANCE ANALYSIS:")
            print(f"   📈 Budget Utilization: {spend_utilization:.1f}%")
            
            # Alert conditions
            alerts = []
            recommendations = []
            
            if current_cpc > 5.0:
                alerts.append(f"🚨 HIGH CPC: ₹{current_cpc:.2f} (Target: <₹5.00)")
                recommendations.append("Reduce budgets on underperforming ad sets")
            
            if current_ctr < 1.0:
                alerts.append(f"🚨 LOW CTR: {current_ctr:.2f}% (Target: >1.0%)")
                recommendations.append("Test new ad creatives immediately")
            
            if spend_utilization < 80:
                alerts.append(f"🟡 LOW SPEND: {spend_utilization:.1f}% (Target: >80%)")
                recommendations.append("Check ad set delivery issues")
            
            # Ad set level analysis
            print(f"\n📋 AD SET PERFORMANCE:")
            
            adsets = api.get_ad_sets(self.campaign_id, limit=10)
            
            for adset in adsets:
                adset_id = adset.get('id')
                name = adset.get('name', 'Unknown')
                budget = int(adset.get('daily_budget', 0)) / 100
                
                try:
                    adset_insights = api._make_request('GET', f'{adset_id}/insights', {
                        'fields': 'spend,clicks,cpc,ctr',
                        'date_preset': 'today'
                    })
                    
                    if 'data' in adset_insights and adset_insights['data']:
                        data = adset_insights['data'][0]
                        spend = float(data.get('spend', 0))
                        clicks = int(data.get('clicks', 0))
                        cpc = float(data.get('cpc', 0))
                        ctr = float(data.get('ctr', 0))
                        
                        utilization = (spend / budget) * 100 if budget > 0 else 0
                        
                        print(f"   {name}:")
                        print(f"     💰 ₹{spend:.0f} / ₹{budget:.0f} ({utilization:.1f}%)")
                        print(f"     📊 CPC: ₹{cpc:.2f} | CTR: {ctr:.2f}%")
                        
                        # Performance flags
                        if utilization < 50:
                            alerts.append(f"🔴 {name}: Low spend utilization ({utilization:.1f}%)")
                        if cpc > 5.0:
                            alerts.append(f"🔴 {name}: High CPC (₹{cpc:.2f})")
                        if ctr > 2.5:
                            recommendations.append(f"🚀 {name}: Excellent CTR - Scale budget")
                    
                except:
                    print(f"   {name}: No performance data available")
            
            # ROAS projection
            estimated_revenue = current_spend * 5.0  # Target ROAS
            print(f"\n💰 ROAS PROJECTION:")
            print(f"   Current Revenue Estimate: ₹{estimated_revenue:,.0f}")
            print(f"   Target Revenue: ₹{self.total_budget * 5:,.0f}")
            
            # Alerts and recommendations
            if alerts:
                print(f"\n🚨 ALERTS ({len(alerts)}):")
                for alert in alerts:
                    print(f"   {alert}")
            
            if recommendations:
                print(f"\n💡 RECOMMENDATIONS ({len(recommendations)}):")
                for rec in recommendations:
                    print(f"   {rec}")
            
            if not alerts and not recommendations:
                print(f"\n✅ ALL SYSTEMS OPTIMAL - ROAS 5+ ON TRACK")
            
            # Save monitoring report
            report = {
                'timestamp': datetime.now().isoformat(),
                'performance': {
                    'spend': current_spend,
                    'clicks': current_clicks,
                    'cpc': current_cpc,
                    'ctr': current_ctr,
                    'utilization': spend_utilization
                },
                'alerts': alerts,
                'recommendations': recommendations,
                'next_action': 'Continue monitoring' if not alerts else 'Immediate optimization needed'
            }
            
            with open('/workspace/filo_6hour_report.json', 'w') as f:
                json.dump(report, f, indent=2)
            
            print(f"\n📝 Report saved: filo_6hour_report.json")
            print(f"🕐 Next check: {(datetime.now() + timedelta(hours=6)).strftime('%H:%M %d/%m')}")
            
        except Exception as e:
            print(f"❌ Monitoring Error: {e}")

if __name__ == "__main__":
    monitor = FiloMonitor()
    monitor.check_performance()