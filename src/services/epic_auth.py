import pathlib
import time
import uuid
import jwt
import requests
from .base_auth import BaseAuthService
from .redis_service import RedisService
from configs.config import Config

class EpicAuthService(BaseAuthService):
    def __init__(self):
        self.source = "EPIC"
        self.client_id = Config.EPIC_CLIENT_ID
        self.private_key_path = Config.EPIC_PRIVATE_KEY_PATH
        self.token_url = Config.EPIC_TOKEN_URL
        self.scopes = Config.EPIC_SCOPES
        self.token = None
        self.token_expiry = 0
        self.redis_service = RedisService()
        self._get_private_key()
    
    def _get_private_key(self):
        if self.private_key_path is None:
            raise ValueError(f"private key path is not set for {self.source} auth service")
        self.private_key = pathlib.Path(self.private_key_path).read_text()
     
    def _generate_jwt(self):
        try:
            now = int(time.time())
            payload = {
                "iss": self.client_id,
                "sub": self.client_id,
                "aud": self.token_url,
                "jti": str(uuid.uuid4()),
                "iat": now,
                "nbf": now,
                "exp": now + 300, 
            }
            headers = {
                "alg": "RS384",
                "typ": "JWT",
            }
            jwt_token = jwt.encode(payload, self.private_key, algorithm="RS384", headers=headers)
            return jwt_token
        except Exception as e:
            raise Exception(f"failed to generate JWT for source: {self.source}, err : {str(e)}")

    def _fetch_token_from_epic(self, jwt_token):
        try: 
            data = {
                "grant_type": "client_credentials",
                "scope": self.scopes,
                "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
                "client_assertion": jwt_token
            }
            headers = {"Content-Type": "application/x-www-form-urlencoded"}

            response = requests.post(self.token_url, data=data, headers=headers)
            if response.status_code != 200:
                raise Exception(f"Failed to get token: {response.text}")
            
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"error occured while fetching token for source: {self.source}, err: {str(e)}")
        except Exception as e:
            raise Exception(f"error occured while fetching token for source: {self.source}, err: {str(e)}")
    
    async def generate_access_token(self) -> str:
        try:
            cached_token = self.redis_service.get("epic_access_token")
            if cached_token:
                return cached_token

            jwt_token = self._generate_jwt()
            res = self._fetch_token_from_epic(jwt_token)

            self.token = res.get("access_token")
            expires_in = res.get("expires_in", 300)
            self.token_expiry = int(time.time()) + expires_in
            if not self.token:
                raise Exception(f"invalid access_token returned from {self.source}")

            self.redis_service.set("epic_access_token", self.token, ttl=expires_in)
            return self.token
        except Exception as e:
            raise Exception(f"failed to generate access token for source:{self.source}, err: {str(e)}")
    
    def is_token_valid(self):
        return self.token and time.time() < self.token_expiry

    def generate_refresh_token(self):
        pass

    
