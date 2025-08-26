"""
Working example using the direct HTTP Facebook Ads API client.
"""
import json
from facebook_ads_api import FacebookAdsAPI

def main():
    """Main example function demonstrating Facebook Ads API usage."""
    
    try:
        # Initialize the client
        print("🚀 Initializing Facebook Ads API client...")
        client = FacebookAdsAPI()
        
        # Test the connection
        print("\n=== 🔍 Testing Connection ===")
        connection_result = client.test_connection()
        print(json.dumps(connection_result, indent=2))
        
        if connection_result['status'] != 'success':
            print("❌ Connection failed. Please check your credentials.")
            return
        
        print(f"✅ Connected as: {connection_result['user_info']['name']}")
        
        # Get all accessible ad accounts
        print("\n=== 📊 Getting Ad Accounts ===")
        try:
            accounts = client.get_ad_accounts()
            print(f"✅ Found {len(accounts)} ad accounts:")
            
            for i, account in enumerate(accounts[:5], 1):  # Show first 5
                status_emoji = "🟢" if account['account_status'] == 1 else "🔴" if account['account_status'] == 2 else "🟡"
                print(f"  {i}. {status_emoji} {account['name']}")
                print(f"     ID: {account['id']}")
                print(f"     Currency: {account['currency']}")
                if account.get('amount_spent'):
                    print(f"     Total Spent: {account['currency']} {account['amount_spent']}")
                print()
            
            if len(accounts) > 5:
                print(f"     ... and {len(accounts) - 5} more accounts")
                
        except Exception as e:
            print(f"❌ Error getting ad accounts: {e}")
            return
        
        # Use the configured ad account for detailed analysis
        if client.config.ad_account_id:
            print(f"\n=== 🎯 Analyzing Account: {client.config.ad_account_id} ===")
            
            # Get campaigns
            print("\n📈 Getting Campaigns...")
            try:
                campaigns = client.get_campaigns(limit=10)
                print(f"✅ Found {len(campaigns)} campaigns:")
                
                active_campaigns = []
                for campaign in campaigns:
                    status_emoji = "🟢" if campaign['status'] == 'ACTIVE' else "🔴" if campaign['status'] == 'PAUSED' else "🟡"
                    print(f"  {status_emoji} {campaign['name']}")
                    print(f"     ID: {campaign['id']}")
                    print(f"     Status: {campaign['status']}")
                    print(f"     Objective: {campaign.get('objective', 'N/A')}")
                    
                    if campaign['status'] == 'ACTIVE':
                        active_campaigns.append(campaign)
                    print()
                
                # Get insights for the first active campaign
                if active_campaigns:
                    campaign = active_campaigns[0]
                    print(f"\n📊 Getting Insights for: {campaign['name']}")
                    try:
                        insights = client.get_campaign_insights(campaign['id'], 'last_7_days')
                        
                        if 'error' not in insights:
                            print("✅ Campaign Performance (Last 7 Days):")
                            print(f"  💰 Spend: ₹{insights.get('spend', '0')}")
                            print(f"  👁️  Impressions: {insights.get('impressions', '0'):,}")
                            print(f"  👆 Clicks: {insights.get('clicks', '0')}")
                            print(f"  📈 CTR: {insights.get('ctr', '0')}%")
                            print(f"  💵 CPC: ₹{insights.get('cpc', '0')}")
                            print(f"  📺 CPM: ₹{insights.get('cpm', '0')}")
                            if insights.get('reach'):
                                print(f"  🎯 Reach: {insights.get('reach', '0'):,}")
                        else:
                            print(f"⚠️  No insights available: {insights.get('error')}")
                            
                    except Exception as e:
                        print(f"❌ Error getting campaign insights: {e}")
                
            except Exception as e:
                print(f"❌ Error getting campaigns: {e}")
            
            # Get account-level insights
            print(f"\n📈 Getting Account Insights...")
            try:
                account_insights = client.get_account_insights(date_preset='last_30_days')
                
                if 'error' not in account_insights:
                    print("✅ Account Performance (Last 30 Days):")
                    print(f"  💰 Total Spend: ₹{account_insights.get('spend', '0')}")
                    print(f"  👁️  Total Impressions: {account_insights.get('impressions', '0'):,}")
                    print(f"  👆 Total Clicks: {account_insights.get('clicks', '0')}")
                    print(f"  📈 Average CTR: {account_insights.get('ctr', '0')}%")
                    print(f"  💵 Average CPC: ₹{account_insights.get('cpc', '0')}")
                    print(f"  📺 Average CPM: ₹{account_insights.get('cpm', '0')}")
                    if account_insights.get('reach'):
                        print(f"  🎯 Total Reach: {account_insights.get('reach', '0'):,}")
                else:
                    print(f"⚠️  No account insights available: {account_insights.get('error')}")
                    
            except Exception as e:
                print(f"❌ Error getting account insights: {e}")
        
        print("\n" + "="*60)
        print("🎉 Facebook Ads API Integration Complete!")
        print("\n✅ What you can do now:")
        print("  • Monitor campaign performance")
        print("  • Track spending and ROI")
        print("  • Analyze audience reach")
        print("  • Get detailed insights")
        print("  • Manage multiple ad accounts")
        
        print(f"\n📚 Available accounts: {len(accounts)}")
        print(f"🎯 Current account: {client.config.ad_account_id}")
        print("\n🚀 Your Facebook Ads API is ready for automation!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your .env file has all credentials")
        print("2. Verify your access token hasn't expired")
        print("3. Ensure your app has required permissions")

if __name__ == "__main__":
    main()
