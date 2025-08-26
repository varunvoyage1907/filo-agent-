"""
Simple test script to verify Facebook API connection without appsecret_proof issues.
"""
import requests
import json

def test_facebook_connection():
    """Test Facebook API connection using direct requests."""
    
    # Your credentials
    app_id = '1459836938385716'
    app_secret = '235c16513f32e145d655e886f929cb2'
    access_token = 'EAAUvtsYkeTQBPca0K6sFLsra9xwNodb7wZBObPorhi3YSv9U5WITJwzImgjFZCTEqf7DqdqdVqTLeSW9bSaRcrz8U4rgIOGS6H2hk2vKI3m1DYCWaBFk7BDMJOsk3DIOvRTIPyrl3VTvCGO5TeH15z8XgtWT5SIXfQ8CCyJZAYkMROkWeAcwBpqDm5b6G2XFhNeAsjKiujZBnVCX7ZCkxjeKEcPbcP7JNuDUOLafsXZBdyKgZDZD'
    
    print("🚀 Testing Facebook API Connection")
    print("=" * 50)
    
    # Test 1: Get user info
    print("\n1️⃣ Testing user info...")
    try:
        url = f"https://graph.facebook.com/v19.0/me"
        params = {
            'access_token': access_token,
            'fields': 'id,name,email'
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            user_data = response.json()
            print("✅ User info retrieved successfully!")
            print(f"👤 Name: {user_data.get('name', 'N/A')}")
            print(f"🆔 ID: {user_data.get('id', 'N/A')}")
            print(f"📧 Email: {user_data.get('email', 'N/A')}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False
    
    # Test 2: Get ad accounts
    print("\n2️⃣ Testing ad accounts access...")
    try:
        url = f"https://graph.facebook.com/v19.0/me/adaccounts"
        params = {
            'access_token': access_token,
            'fields': 'id,name,account_status,currency,timezone_name'
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            accounts_data = response.json()
            accounts = accounts_data.get('data', [])
            
            print(f"✅ Found {len(accounts)} ad account(s)!")
            
            for i, account in enumerate(accounts, 1):
                print(f"\n📊 Account {i}:")
                print(f"   Name: {account.get('name', 'N/A')}")
                print(f"   ID: {account.get('id', 'N/A')}")
                print(f"   Status: {account.get('account_status', 'N/A')}")
                print(f"   Currency: {account.get('currency', 'N/A')}")
                print(f"   Timezone: {account.get('timezone_name', 'N/A')}")
            
            # Return the first account ID for configuration
            if accounts:
                return accounts[0]['id']
            else:
                print("⚠️  No ad accounts found. You may need additional permissions.")
                return None
                
        else:
            print(f"❌ Error getting ad accounts: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception getting ad accounts: {e}")
        return False

def create_working_env_file(ad_account_id):
    """Create a working .env file with the discovered ad account."""
    
    env_content = f"""# Facebook API Configuration - Working Setup
FACEBOOK_APP_ID=1459836938385716
FACEBOOK_APP_SECRET=235c16513f32e145d655e886f929cb2
FACEBOOK_ACCESS_TOKEN=EAAUvtsYkeTQBPca0K6sFLsra9xwNodb7wZBObPorhi3YSv9U5WITJwzImgjFZCTEqf7DqdqdVqTLeSW9bSaRcrz8U4rgIOGS6H2hk2vKI3m1DYCWaBFk7BDMJOsk3DIOvRTIPyrl3VTvCGO5TeH15z8XgtWT5SIXfQ8CCyJZAYkMROkWeAcwBpqDm5b6G2XFhNeAsjKiujZBnVCX7ZCkxjeKEcPbcP7JNuDUOLafsXZBdyKgZDZD
FACEBOOK_AD_ACCOUNT_ID={ad_account_id}
FACEBOOK_API_VERSION=v19.0
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print(f"\n✅ Created .env file with ad account: {ad_account_id}")
        return True
    except Exception as e:
        print(f"⚠️  Could not create .env file: {e}")
        return False

def main():
    """Main function."""
    
    # Test connection
    ad_account_id = test_facebook_connection()
    
    if ad_account_id:
        # Create .env file with working configuration
        create_working_env_file(ad_account_id)
        
        print("\n" + "=" * 50)
        print("🎉 SUCCESS! Your Facebook API connection is working!")
        print("\n📋 Summary:")
        print("✅ Authentication successful")
        print("✅ Ad account access confirmed")
        print("✅ Configuration file created")
        
        print(f"\n🔧 Your ad account ID: {ad_account_id}")
        print("\n🚀 Next steps:")
        print("1. Your .env file is ready")
        print("2. Run: python3 example_usage.py")
        print("3. Start managing your Facebook ads!")
        
    else:
        print("\n" + "=" * 50)
        print("❌ Connection test failed")
        print("\n🔍 Troubleshooting:")
        print("1. Check if your access token has expired")
        print("2. Verify your app has the required permissions:")
        print("   - ads_read")
        print("   - ads_management")
        print("   - business_management")
        print("3. Make sure your Facebook app is not in development mode restrictions")

if __name__ == "__main__":
    main()
