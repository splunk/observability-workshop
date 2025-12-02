import os
import json
import base64
import requests
from datetime import datetime, timedelta

class TokenManager:
    def __init__(
        self,
        client_id,
        client_secret,
        app_key,
        cache_file="/tmp/cisco_token_cache.json",
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.app_key = app_key
        self.cache_file = cache_file
        self.token_url = "https://id.cisco.com/oauth2/default/v1/token"

    def _get_cached_token(self):
        if not os.path.exists(self.cache_file):
            return None

        try:
            with open(self.cache_file, "r") as f:
                cache_data = json.load(f)

            expires_at = datetime.fromisoformat(cache_data["expires_at"])
            if datetime.now() < expires_at - timedelta(minutes=5):
                return cache_data["access_token"]
        except (json.JSONDecodeError, KeyError, ValueError):
            pass
        return None

    def _fetch_new_token(self):
        payload = "grant_type=client_credentials"
        value = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode("utf-8")
        ).decode("utf-8")
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {value}",
        }

        response = requests.post(self.token_url, headers=headers, data=payload)
        response.raise_for_status()

        token_data = response.json()
        expires_in = token_data.get("expires_in", 3600)
        expires_at = datetime.now() + timedelta(seconds=expires_in)

        cache_data = {
            "access_token": token_data["access_token"],
            "expires_at": expires_at.isoformat(),
        }

        # Create file with secure permissions (owner read/write only)
        with open(self.cache_file, "w") as f:
            json.dump(cache_data, f, indent=2)
        os.chmod(self.cache_file, 0o600)  # rw------- (owner only)
        return token_data["access_token"]

    def get_token(self):
        token = self._get_cached_token()
        if token:
            return token
        return self._fetch_new_token()

    def cleanup_token_cache(self):
        """Securely remove token cache file"""
        if os.path.exists(self.cache_file):
            # Overwrite file with zeros before deletion for security
            with open(self.cache_file, "r+b") as f:
                length = f.seek(0, 2)  # Get file size
                f.seek(0)
                f.write(b"\0" * length)  # Overwrite with zeros
            os.remove(self.cache_file)