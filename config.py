"""
Configuration module for Facebook Ads API integration.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class FacebookConfig:
    """Configuration class for Facebook Ads API."""
    
    def __init__(self):
        self.app_id = os.getenv('FACEBOOK_APP_ID')
        self.app_secret = os.getenv('FACEBOOK_APP_SECRET')
        self.access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.ad_account_id = os.getenv('FACEBOOK_AD_ACCOUNT_ID')
        self.api_version = os.getenv('FACEBOOK_API_VERSION', 'v19.0')
        
        # Validate required credentials
        self._validate_credentials()
    
    def _validate_credentials(self):
        """Validate that all required credentials are provided."""
        required_fields = {
            'FACEBOOK_APP_ID': self.app_id,
            'FACEBOOK_APP_SECRET': self.app_secret,
            'FACEBOOK_ACCESS_TOKEN': self.access_token,
            'FACEBOOK_AD_ACCOUNT_ID': self.ad_account_id
        }
        
        missing_fields = [field for field, value in required_fields.items() if not value]
        
        if missing_fields:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_fields)}. "
                "Please check your .env file and ensure all required fields are set."
            )
    
    @property
    def is_configured(self):
        """Check if all required credentials are configured."""
        try:
            self._validate_credentials()
            return True
        except ValueError:
            return False
    
    def get_credentials_dict(self):
        """Return credentials as a dictionary."""
        return {
            'app_id': self.app_id,
            'app_secret': self.app_secret,
            'access_token': self.access_token,
            'ad_account_id': self.ad_account_id,
            'api_version': self.api_version
        }
