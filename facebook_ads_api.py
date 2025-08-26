"""
Direct Facebook Ads API client using HTTP requests.
This avoids SDK authentication issues while providing full functionality.
"""
import requests
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from config import FacebookConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FacebookAdsAPI:
    """Direct HTTP client for Facebook Ads API."""
    
    def __init__(self, config: Optional[FacebookConfig] = None):
        """Initialize the Facebook Ads API client."""
        self.config = config or FacebookConfig()
        self.base_url = f"https://graph.facebook.com/{self.config.api_version}"
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
        
        logger.info("Facebook Ads API client initialized")
    
    def _make_request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None) -> Dict:
        """Make a request to the Facebook API."""
        url = f"{self.base_url}/{endpoint}"
        
        # Add access token to params
        if params is None:
            params = {}
        params['access_token'] = self.config.access_token
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params)
            elif method.upper() == 'POST':
                response = self.session.post(url, params=params, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    logger.error(f"Error response: {json.dumps(error_data, indent=2)}")
                    return {'error': error_data}
                except:
                    logger.error(f"Error response: {e.response.text}")
                    return {'error': {'message': e.response.text}}
            raise
    
    def test_connection(self) -> Dict[str, Any]:
        """Test the connection to Facebook API."""
        try:
            # Get user info
            user_data = self._make_request('GET', 'me', {'fields': 'id,name,email'})
            
            if 'error' in user_data:
                return {
                    'status': 'error',
                    'error': user_data['error'].get('message', 'Unknown error'),
                    'error_code': user_data['error'].get('code')
                }
            
            result = {
                'status': 'success',
                'user_info': {
                    'id': user_data.get('id'),
                    'name': user_data.get('name'),
                    'email': user_data.get('email')
                },
                'api_version': self.config.api_version
            }
            
            # Test ad account access if configured
            if self.config.ad_account_id:
                account_data = self._make_request('GET', self.config.ad_account_id, {
                    'fields': 'id,name,account_status,currency,timezone_name'
                })
                
                if 'error' not in account_data:
                    result['ad_account_info'] = {
                        'id': account_data.get('id'),
                        'name': account_data.get('name'),
                        'status': account_data.get('account_status'),
                        'currency': account_data.get('currency'),
                        'timezone': account_data.get('timezone_name')
                    }
                else:
                    result['ad_account_error'] = account_data['error'].get('message', 'Cannot access ad account')
            
            logger.info("Connection test successful")
            return result
            
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def get_ad_accounts(self) -> List[Dict[str, Any]]:
        """Get all ad accounts accessible to the current user."""
        try:
            accounts_data = self._make_request('GET', 'me/adaccounts', {
                'fields': 'id,name,account_status,currency,timezone_name,amount_spent'
            })
            
            if 'error' in accounts_data:
                raise Exception(f"API Error: {accounts_data['error'].get('message', 'Unknown error')}")
            
            accounts = accounts_data.get('data', [])
            logger.info(f"Retrieved {len(accounts)} ad accounts")
            return accounts
            
        except Exception as e:
            logger.error(f"Error retrieving ad accounts: {e}")
            raise
    
    def get_campaigns(self, ad_account_id: str = None, limit: int = 25) -> List[Dict[str, Any]]:
        """Get campaigns from the specified ad account."""
        account_id = ad_account_id or self.config.ad_account_id
        if not account_id:
            raise ValueError("No ad account ID provided")
        
        try:
            campaigns_data = self._make_request('GET', f'{account_id}/campaigns', {
                'fields': 'id,name,status,objective,created_time,updated_time,start_time,stop_time',
                'limit': limit
            })
            
            if 'error' in campaigns_data:
                raise Exception(f"API Error: {campaigns_data['error'].get('message', 'Unknown error')}")
            
            campaigns = campaigns_data.get('data', [])
            logger.info(f"Retrieved {len(campaigns)} campaigns")
            return campaigns
            
        except Exception as e:
            logger.error(f"Error retrieving campaigns: {e}")
            raise
    
    def get_campaign_insights(self, campaign_id: str, date_preset: str = 'last_7_days') -> Dict[str, Any]:
        """Get insights for a specific campaign."""
        try:
            insights_data = self._make_request('GET', f'{campaign_id}/insights', {
                'fields': 'impressions,clicks,spend,reach,frequency,cpm,cpc,ctr,cost_per_unique_click',
                'date_preset': date_preset
            })
            
            if 'error' in insights_data:
                raise Exception(f"API Error: {insights_data['error'].get('message', 'Unknown error')}")
            
            insights = insights_data.get('data', [])
            if insights:
                insight = insights[0]
                return {
                    'campaign_id': campaign_id,
                    'date_preset': date_preset,
                    'impressions': insight.get('impressions'),
                    'clicks': insight.get('clicks'),
                    'spend': insight.get('spend'),
                    'reach': insight.get('reach'),
                    'frequency': insight.get('frequency'),
                    'cpm': insight.get('cpm'),
                    'cpc': insight.get('cpc'),
                    'ctr': insight.get('ctr'),
                    'cost_per_unique_click': insight.get('cost_per_unique_click')
                }
            else:
                return {'campaign_id': campaign_id, 'error': 'No insights data available'}
                
        except Exception as e:
            logger.error(f"Error retrieving campaign insights: {e}")
            raise
    
    def get_account_insights(self, ad_account_id: str = None, date_preset: str = 'last_7_days') -> Dict[str, Any]:
        """Get insights for the entire ad account."""
        account_id = ad_account_id or self.config.ad_account_id
        if not account_id:
            raise ValueError("No ad account ID provided")
        
        try:
            insights_data = self._make_request('GET', f'{account_id}/insights', {
                'fields': 'impressions,clicks,spend,reach,frequency,cpm,cpc,ctr,cost_per_unique_click',
                'date_preset': date_preset
            })
            
            if 'error' in insights_data:
                raise Exception(f"API Error: {insights_data['error'].get('message', 'Unknown error')}")
            
            insights = insights_data.get('data', [])
            if insights:
                insight = insights[0]
                return {
                    'account_id': account_id,
                    'date_preset': date_preset,
                    'impressions': insight.get('impressions'),
                    'clicks': insight.get('clicks'),
                    'spend': insight.get('spend'),
                    'reach': insight.get('reach'),
                    'frequency': insight.get('frequency'),
                    'cpm': insight.get('cpm'),
                    'cpc': insight.get('cpc'),
                    'ctr': insight.get('ctr'),
                    'cost_per_unique_click': insight.get('cost_per_unique_click')
                }
            else:
                return {'account_id': account_id, 'error': 'No insights data available'}
                
        except Exception as e:
            logger.error(f"Error retrieving account insights: {e}")
            raise
    
    def get_ad_sets(self, campaign_id: str, limit: int = 25) -> List[Dict[str, Any]]:
        """Get ad sets for a specific campaign."""
        try:
            adsets_data = self._make_request('GET', f'{campaign_id}/adsets', {
                'fields': 'id,name,status,created_time,updated_time,start_time,end_time,daily_budget,lifetime_budget',
                'limit': limit
            })
            
            if 'error' in adsets_data:
                raise Exception(f"API Error: {adsets_data['error'].get('message', 'Unknown error')}")
            
            adsets = adsets_data.get('data', [])
            logger.info(f"Retrieved {len(adsets)} ad sets")
            return adsets
            
        except Exception as e:
            logger.error(f"Error retrieving ad sets: {e}")
            raise
    
    def get_ads(self, adset_id: str, limit: int = 25) -> List[Dict[str, Any]]:
        """Get ads for a specific ad set."""
        try:
            ads_data = self._make_request('GET', f'{adset_id}/ads', {
                'fields': 'id,name,status,created_time,updated_time',
                'limit': limit
            })
            
            if 'error' in ads_data:
                raise Exception(f"API Error: {ads_data['error'].get('message', 'Unknown error')}")
            
            ads = ads_data.get('data', [])
            logger.info(f"Retrieved {len(ads)} ads")
            return ads
            
        except Exception as e:
            logger.error(f"Error retrieving ads: {e}")
            raise
