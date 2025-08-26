"""
Facebook Ads API Client for connecting to and managing Facebook ad accounts.
"""
import logging
from typing import Dict, List, Optional, Any
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.user import User
from facebook_business.exceptions import FacebookRequestError
from config import FacebookConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FacebookAdsClient:
    """Client for interacting with Facebook Ads API."""
    
    def __init__(self, config: Optional[FacebookConfig] = None):
        """
        Initialize the Facebook Ads API client.
        
        Args:
            config: FacebookConfig instance. If None, will create from environment variables.
        """
        self.config = config or FacebookConfig()
        self.api = None
        self.ad_account = None
        self._initialize_api()
    
    def _initialize_api(self):
        """Initialize the Facebook Ads API connection."""
        try:
            # Initialize the API
            FacebookAdsApi.init(
                app_id=self.config.app_id,
                app_secret=self.config.app_secret,
                access_token=self.config.access_token,
                api_version=self.config.api_version
            )
            self.api = FacebookAdsApi.get_default_api()
            
            # Set default account if provided
            if self.config.ad_account_id and self.config.ad_account_id.startswith('act_'):
                self.api.set_default_account_id(self.config.ad_account_id)
            
            logger.info("Facebook Ads API initialized successfully")
            
            # Initialize ad account
            if self.config.ad_account_id:
                self.ad_account = AdAccount(self.config.ad_account_id)
                logger.info(f"Ad account {self.config.ad_account_id} initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize Facebook Ads API: {str(e)}")
            raise
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the connection to Facebook Ads API.
        
        Returns:
            Dict containing connection status and account information.
        """
        try:
            # Test API connection by getting user info
            me = User(fbid='me')
            user_info = me.api_get(fields=['id', 'name', 'email'])
            
            result = {
                'status': 'success',
                'user_info': {
                    'id': user_info.get('id'),
                    'name': user_info.get('name'),
                    'email': user_info.get('email')
                },
                'api_version': self.config.api_version
            }
            
            # Test ad account access if configured
            if self.ad_account:
                try:
                    account_info = self.ad_account.api_get(fields=[
                        'id', 'name', 'account_status', 'currency', 'timezone_name'
                    ])
                    result['ad_account_info'] = {
                        'id': account_info.get('id'),
                        'name': account_info.get('name'),
                        'status': account_info.get('account_status'),
                        'currency': account_info.get('currency'),
                        'timezone': account_info.get('timezone_name')
                    }
                except FacebookRequestError as e:
                    result['ad_account_error'] = f"Cannot access ad account: {str(e)}"
            
            logger.info("Connection test successful")
            return result
            
        except FacebookRequestError as e:
            logger.error(f"Facebook API error during connection test: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'error_code': e.api_error_code() if hasattr(e, 'api_error_code') else None
            }
        except Exception as e:
            logger.error(f"Unexpected error during connection test: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def get_ad_accounts(self) -> List[Dict[str, Any]]:
        """
        Get all ad accounts accessible to the current user.
        
        Returns:
            List of ad account information dictionaries.
        """
        try:
            me = User(fbid='me')
            accounts = me.get_ad_accounts(fields=[
                'id', 'name', 'account_status', 'currency', 'timezone_name', 'amount_spent'
            ])
            
            account_list = []
            for account in accounts:
                account_list.append({
                    'id': account.get('id'),
                    'name': account.get('name'),
                    'status': account.get('account_status'),
                    'currency': account.get('currency'),
                    'timezone': account.get('timezone_name'),
                    'amount_spent': account.get('amount_spent')
                })
            
            logger.info(f"Retrieved {len(account_list)} ad accounts")
            return account_list
            
        except FacebookRequestError as e:
            logger.error(f"Error retrieving ad accounts: {str(e)}")
            raise
    
    def get_campaigns(self, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Get campaigns from the configured ad account.
        
        Args:
            limit: Maximum number of campaigns to retrieve.
            
        Returns:
            List of campaign information dictionaries.
        """
        if not self.ad_account:
            raise ValueError("No ad account configured")
        
        try:
            campaigns = self.ad_account.get_campaigns(
                fields=[
                    'id', 'name', 'status', 'objective', 'created_time', 
                    'updated_time', 'start_time', 'stop_time'
                ],
                params={'limit': limit}
            )
            
            campaign_list = []
            for campaign in campaigns:
                campaign_list.append({
                    'id': campaign.get('id'),
                    'name': campaign.get('name'),
                    'status': campaign.get('status'),
                    'objective': campaign.get('objective'),
                    'created_time': campaign.get('created_time'),
                    'updated_time': campaign.get('updated_time'),
                    'start_time': campaign.get('start_time'),
                    'stop_time': campaign.get('stop_time')
                })
            
            logger.info(f"Retrieved {len(campaign_list)} campaigns")
            return campaign_list
            
        except FacebookRequestError as e:
            logger.error(f"Error retrieving campaigns: {str(e)}")
            raise
    
    def get_campaign_insights(self, campaign_id: str, date_preset: str = 'last_7_days') -> Dict[str, Any]:
        """
        Get insights for a specific campaign.
        
        Args:
            campaign_id: The campaign ID to get insights for.
            date_preset: Date range preset (e.g., 'last_7_days', 'last_30_days').
            
        Returns:
            Campaign insights dictionary.
        """
        try:
            campaign = Campaign(campaign_id)
            insights = campaign.get_insights(
                fields=[
                    'impressions', 'clicks', 'spend', 'reach', 'frequency',
                    'cpm', 'cpc', 'ctr', 'cost_per_unique_click'
                ],
                params={'date_preset': date_preset}
            )
            
            if insights:
                insight_data = insights[0]  # Get first (and usually only) result
                return {
                    'campaign_id': campaign_id,
                    'date_preset': date_preset,
                    'impressions': insight_data.get('impressions'),
                    'clicks': insight_data.get('clicks'),
                    'spend': insight_data.get('spend'),
                    'reach': insight_data.get('reach'),
                    'frequency': insight_data.get('frequency'),
                    'cpm': insight_data.get('cpm'),
                    'cpc': insight_data.get('cpc'),
                    'ctr': insight_data.get('ctr'),
                    'cost_per_unique_click': insight_data.get('cost_per_unique_click')
                }
            else:
                return {'campaign_id': campaign_id, 'error': 'No insights data available'}
                
        except FacebookRequestError as e:
            logger.error(f"Error retrieving campaign insights: {str(e)}")
            raise
    
    def get_account_insights(self, date_preset: str = 'last_7_days') -> Dict[str, Any]:
        """
        Get insights for the entire ad account.
        
        Args:
            date_preset: Date range preset (e.g., 'last_7_days', 'last_30_days').
            
        Returns:
            Account insights dictionary.
        """
        if not self.ad_account:
            raise ValueError("No ad account configured")
        
        try:
            insights = self.ad_account.get_insights(
                fields=[
                    'impressions', 'clicks', 'spend', 'reach', 'frequency',
                    'cpm', 'cpc', 'ctr', 'cost_per_unique_click'
                ],
                params={'date_preset': date_preset}
            )
            
            if insights:
                insight_data = insights[0]
                return {
                    'account_id': self.config.ad_account_id,
                    'date_preset': date_preset,
                    'impressions': insight_data.get('impressions'),
                    'clicks': insight_data.get('clicks'),
                    'spend': insight_data.get('spend'),
                    'reach': insight_data.get('reach'),
                    'frequency': insight_data.get('frequency'),
                    'cpm': insight_data.get('cpm'),
                    'cpc': insight_data.get('cpc'),
                    'ctr': insight_data.get('ctr'),
                    'cost_per_unique_click': insight_data.get('cost_per_unique_click')
                }
            else:
                return {'account_id': self.config.ad_account_id, 'error': 'No insights data available'}
                
        except FacebookRequestError as e:
            logger.error(f"Error retrieving account insights: {str(e)}")
            raise
