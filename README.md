# Facebook Ads API Integration

This project provides a Python client for connecting to and interacting with the Facebook Ads API.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Your Facebook API Credentials

Create a `.env` file in the project root with your Facebook API credentials:

```env
# Your Facebook App ID (already set)
FACEBOOK_APP_ID=1459836938385716

# Your Facebook App Secret (get from Facebook Developer Console)
FACEBOOK_APP_SECRET=your_app_secret_here

# Your Facebook Access Token (User or System User Token)
FACEBOOK_ACCESS_TOKEN=your_access_token_here

# Your Facebook Ad Account ID (format: act_XXXXXXXXXX)
FACEBOOK_AD_ACCOUNT_ID=act_your_account_id_here

# Optional: Facebook API Version (default: v19.0)
FACEBOOK_API_VERSION=v19.0
```

### 3. Getting Your Credentials

#### App Secret
1. Go to [Facebook Developer Console](https://developers.facebook.com/apps/)
2. Select your app (ID: 1459836938385716)
3. Go to Settings > Basic
4. Copy the "App Secret"

#### Access Token
You have several options:

**Option 1: User Access Token (for testing)**
1. Go to [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Select your app
3. Generate a User Access Token with these permissions:
   - `ads_read`
   - `ads_management` (if you want to modify ads)
   - `business_management`

**Option 2: System User Access Token (recommended for production)**
1. Go to your Facebook Business Manager
2. Create a System User
3. Generate a System User Access Token with required permissions

#### Ad Account ID
1. Go to [Facebook Ads Manager](https://www.facebook.com/adsmanager/)
2. Your account ID is in the URL or top-left corner
3. Format it as `act_XXXXXXXXXX` (add "act_" prefix)

## Usage

### Basic Connection Test

```python
from facebook_ads_client import FacebookAdsClient

# Initialize client
client = FacebookAdsClient()

# Test connection
result = client.test_connection()
print(result)
```

### Get Ad Accounts

```python
# Get all accessible ad accounts
accounts = client.get_ad_accounts()
for account in accounts:
    print(f"{account['name']} - {account['id']}")
```

### Get Campaigns

```python
# Get campaigns from your ad account
campaigns = client.get_campaigns(limit=10)
for campaign in campaigns:
    print(f"{campaign['name']} - Status: {campaign['status']}")
```

### Get Insights

```python
# Get campaign insights
insights = client.get_campaign_insights(campaign_id, date_preset='last_7_days')
print(f"Spend: ${insights['spend']}")
print(f"Impressions: {insights['impressions']}")

# Get account insights
account_insights = client.get_account_insights(date_preset='last_30_days')
```

### Run the Example

```bash
python example_usage.py
```

## Features

- ✅ Facebook Ads API authentication
- ✅ Connection testing
- ✅ Ad account management
- ✅ Campaign retrieval
- ✅ Performance insights
- ✅ Error handling and logging
- ✅ Environment-based configuration

## Required Facebook App Permissions

Make sure your Facebook App has these permissions:
- `ads_read` - Read ads data
- `ads_management` - Manage ads (if modifying)
- `business_management` - Access business data

## Troubleshooting

### Common Issues

1. **"Invalid App ID"**: Make sure your App ID is correct
2. **"Invalid Access Token"**: Generate a new access token with proper permissions
3. **"Insufficient Permissions"**: Add required permissions to your access token
4. **"Ad Account Access Denied"**: Make sure your user/system user has access to the ad account

### Debug Mode

Set logging level to DEBUG for more detailed output:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Next Steps

To extend this integration, you can:
1. Add campaign creation functionality
2. Implement ad set and ad management
3. Add more detailed reporting
4. Create automated optimization rules
5. Add webhook support for real-time updates

## API Documentation

- [Facebook Marketing API Documentation](https://developers.facebook.com/docs/marketing-apis/)
- [Facebook Business SDK for Python](https://github.com/facebook/facebook-python-business-sdk)
