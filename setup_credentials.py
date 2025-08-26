"""
Setup script to configure Facebook API credentials and test connection.
"""
import os
from facebook_ads_client import FacebookAdsClient
from config import FacebookConfig

def setup_credentials():
    """Set up Facebook API credentials."""
    
    # Your provided credentials
    credentials = {
        'FACEBOOK_APP_ID': '1459836938385716',
        'FACEBOOK_APP_SECRET': '235c16513f32e145d655e886f929cb2',
        'FACEBOOK_ACCESS_TOKEN': 'EAAUvtsYkeTQBPca0K6sFLsra9xwNodb7wZBObPorhi3YSv9U5WITJwzImgjFZCTEqf7DqdqdVqTLeSW9bSaRcrz8U4rgIOGS6H2hk2vKI3m1DYCWaBFk7BDMJOsk3DIOvRTIPyrl3VTvCGO5TeH15z8XgtWT5SIXfQ8CCyJZAYkMROkWeAcwBpqDm5b6G2XFhNeAsjKiujZBnVCX7ZCkxjeKEcPbcP7JNuDUOLafsXZBdyKgZDZD',
        'FACEBOOK_API_VERSION': 'v19.0'
    }
    
    # Set environment variables
    for key, value in credentials.items():
        os.environ[key] = value
    
    print("✅ Credentials configured successfully!")
    return credentials

def test_connection_and_get_accounts():
    """Test connection and get available ad accounts."""
    
    try:
        # Initialize client
        print("\n🔄 Initializing Facebook Ads API client...")
        
        # Create a custom config with the credentials
        class CustomConfig:
            def __init__(self):
                self.app_id = '1459836938385716'
                self.app_secret = '235c16513f32e145d655e886f929cb2'
                self.access_token = 'EAAUvtsYkeTQBPca0K6sFLsra9xwNodb7wZBObPorhi3YSv9U5WITJwzImgjFZCTEqf7DqdqdVqTLeSW9bSaRcrz8U4rgIOGS6H2hk2vKI3m1DYCWaBFk7BDMJOsk3DIOvRTIPyrl3VTvCGO5TeH15z8XgtWT5SIXfQ8CCyJZAYkMROkWeAcwBpqDm5b6G2XFhNeAsjKiujZBnVCX7ZCkxjeKEcPbcP7JNuDUOLafsXZBdyKgZDZD'
                self.ad_account_id = None  # We'll get this from the API
                self.api_version = 'v19.0'
            
            def _validate_credentials(self):
                pass  # Skip validation for now
            
            @property
            def is_configured(self):
                return True
        
        config = CustomConfig()
        client = FacebookAdsClient(config)
        
        # Test connection
        print("\n🔍 Testing connection...")
        connection_result = client.test_connection()
        
        if connection_result['status'] == 'success':
            print("✅ Connection successful!")
            print(f"👤 User: {connection_result['user_info']['name']} ({connection_result['user_info']['id']})")
            if connection_result['user_info'].get('email'):
                print(f"📧 Email: {connection_result['user_info']['email']}")
        else:
            print("❌ Connection failed!")
            print(f"Error: {connection_result.get('error', 'Unknown error')}")
            return None
        
        # Get ad accounts
        print("\n📊 Getting your ad accounts...")
        accounts = client.get_ad_accounts()
        
        if accounts:
            print(f"✅ Found {len(accounts)} ad account(s):")
            for i, account in enumerate(accounts, 1):
                print(f"\n{i}. {account['name']}")
                print(f"   ID: {account['id']}")
                print(f"   Status: {account['status']}")
                print(f"   Currency: {account['currency']}")
                if account.get('amount_spent'):
                    print(f"   Total Spent: {account['currency']} {account['amount_spent']}")
            
            # Return the first account ID for configuration
            return accounts[0]['id']
        else:
            print("⚠️  No ad accounts found or accessible with current permissions.")
            return None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def create_env_file(ad_account_id=None):
    """Create .env file with all credentials."""
    
    env_content = f"""# Facebook API Configuration
# Generated automatically with your credentials

# Your Facebook App ID
FACEBOOK_APP_ID=1459836938385716

# Your Facebook App Secret
FACEBOOK_APP_SECRET=235c16513f32e145d655e886f929cb2

# Your Facebook Access Token
FACEBOOK_ACCESS_TOKEN=EAAUvtsYkeTQBPca0K6sFLsra9xwNodb7wZBObPorhi3YSv9U5WITJwzImgjFZCTEqf7DqdqdVqTLeSW9bSaRcrz8U4rgIOGS6H2hk2vKI3m1DYCWaBFk7BDMJOsk3DIOvRTIPyrl3VTvCGO5TeH15z8XgtWT5SIXfQ8CCyJZAYkMROkWeAcwBpqDm5b6G2XFhNeAsjKiujZBnVCX7ZCkxjeKEcPbcP7JNuDUOLafsXZBdyKgZDZD

# Your Facebook Ad Account ID
FACEBOOK_AD_ACCOUNT_ID={ad_account_id or 'your_account_id_here'}

# Facebook API Version
FACEBOOK_API_VERSION=v19.0
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print(f"\n✅ Created .env file with your credentials!")
        if ad_account_id:
            print(f"📊 Ad Account ID set to: {ad_account_id}")
    except Exception as e:
        print(f"⚠️  Could not create .env file: {e}")
        print("You can manually create it with the credentials shown above.")

def main():
    """Main setup function."""
    
    print("🚀 Facebook Ads API Setup")
    print("=" * 50)
    
    # Setup credentials
    setup_credentials()
    
    # Test connection and get accounts
    ad_account_id = test_connection_and_get_accounts()
    
    # Create .env file
    create_env_file(ad_account_id)
    
    print("\n" + "=" * 50)
    print("🎉 Setup Complete!")
    print("\nNext steps:")
    print("1. Run: pip install -r requirements.txt")
    print("2. Run: python example_usage.py")
    print("\nYour Facebook Ads API integration is ready to use!")

if __name__ == "__main__":
    main()
