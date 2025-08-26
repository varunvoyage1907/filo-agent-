"""
Example usage of the Facebook Ads API client.
"""
import json
from facebook_ads_client import FacebookAdsClient
from facebook_business.exceptions import FacebookRequestError

def main():
    """Main example function demonstrating Facebook Ads API usage."""
    
    try:
        # Initialize the client
        print("Initializing Facebook Ads API client...")
        client = FacebookAdsClient()
        
        # Test the connection
        print("\n=== Testing Connection ===")
        connection_result = client.test_connection()
        print(json.dumps(connection_result, indent=2))
        
        if connection_result['status'] != 'success':
            print("Connection failed. Please check your credentials.")
            return
        
        # Get all accessible ad accounts
        print("\n=== Getting Ad Accounts ===")
        try:
            accounts = client.get_ad_accounts()
            print(f"Found {len(accounts)} ad accounts:")
            for account in accounts:
                print(f"  - {account['name']} ({account['id']}) - Status: {account['status']}")
        except FacebookRequestError as e:
            print(f"Error getting ad accounts: {e}")
        
        # Get campaigns (if ad account is configured)
        if hasattr(client, 'ad_account') and client.ad_account:
            print("\n=== Getting Campaigns ===")
            try:
                campaigns = client.get_campaigns(limit=10)
                print(f"Found {len(campaigns)} campaigns:")
                for campaign in campaigns:
                    print(f"  - {campaign['name']} ({campaign['id']}) - Status: {campaign['status']}")
                
                # Get insights for the first campaign
                if campaigns:
                    print(f"\n=== Getting Insights for Campaign: {campaigns[0]['name']} ===")
                    insights = client.get_campaign_insights(campaigns[0]['id'])
                    print(json.dumps(insights, indent=2))
                    
            except FacebookRequestError as e:
                print(f"Error getting campaigns: {e}")
            
            # Get account-level insights
            print("\n=== Getting Account Insights ===")
            try:
                account_insights = client.get_account_insights()
                print(json.dumps(account_insights, indent=2))
            except FacebookRequestError as e:
                print(f"Error getting account insights: {e}")
        
        print("\n=== Example completed successfully! ===")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("1. Created a .env file with your Facebook API credentials")
        print("2. Installed the required packages: pip install -r requirements.txt")
        print("3. Set up your Facebook App with the correct permissions")

if __name__ == "__main__":
    main()
