"""
Klaviyo Audit Katie — API Client
Read-only HTTP client for the Klaviyo REST API (revision 2024-02-15).
Uses httpx for requests so bracket params like page[size] are never
percent-encoded (urllib encodes [ ] as %5B %5D which Klaviyo rejects).
"""
from __future__ import annotations

import time
import json
import logging
from typing import Any, Dict, Iterator, List, Optional

import httpx

API_BASE = "https://a.klaviyo.com"
REVISION = "2024-10-15"

_BACKOFF_INITIAL = 2.0
_BACKOFF_MAX = 32.0
_MAX_RETRIES = 5
_TIMEOUT = 30

log = logging.getLogger("klaviyo_client")


class KlaviyoAuthError(Exception):
    pass

class KlaviyoPermissionError(Exception):
    pass

class KlaviyoClientError(Exception):
    pass


class KlaviyoClient:
    def __init__(self, api_key: str, revision: str = REVISION) -> None:
        if not api_key:
            raise KlaviyoAuthError("API key is empty.")
        self._key = api_key
        self._revision = revision
        # Shared sync client — httpx preserves [ ] in params natively
        self._client = httpx.Client(
            base_url=API_BASE,
            headers={
                "Authorization": f"Klaviyo-API-Key {self._key}",
                "revision": self._revision,
                "Accept": "application/vnd.api+json",
            },
            timeout=_TIMEOUT,
        )

    def _safe_key_hint(self) -> str:
        return self._key[:6] + "..." if len(self._key) > 6 else "***"

    def _headers(self) -> Dict[str, str]:
        """Legacy helper kept for compatibility."""
        return {
            "Authorization": f"Klaviyo-API-Key {self._key}",
            "revision": self._revision,
            "Accept": "application/vnd.api+json",
        }

    def _request(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict:
        """
        Make one GET request with retry/backoff.
        httpx passes params dict as query string keeping [ ] literal.
        """
        delay = _BACKOFF_INITIAL
        for attempt in range(_MAX_RETRIES):
            try:
                if url.startswith("http"):
                    # Absolute URL (e.g. links.next from Klaviyo)
                    resp = self._client.get(url)
                else:
                    resp = self._client.get(url, params=params or {})

                status = resp.status_code
                if status == 200:
                    body = resp.json()
                    records = body.get("data", [])
                    count = len(records) if isinstance(records, list) else 1
                    log.info("GET %s → %d (%d records)", url.split("?")[0].replace(API_BASE, ""), status, count)
                    return body

                body_text = resp.text
                log.warning("GET %s → %d (attempt %d/%d): %s",
                            url.split("?")[0].replace(API_BASE, ""), status, attempt + 1, _MAX_RETRIES,
                            body_text[:200])

                if status == 401:
                    raise KlaviyoAuthError(
                        f"Authentication failed (401). Check your API key (hint: {self._safe_key_hint()}).")
                if status == 403:
                    raise KlaviyoPermissionError(
                        f"Permission denied (403) on {url}. Key may lack required read scopes.")
                if status == 404:
                    log.warning("Endpoint not available (404): %s", url)
                    return {"data": []}
                if status == 429:
                    wait = min(float(resp.headers.get("Retry-After", delay)), _BACKOFF_MAX)
                    log.info("Rate limited — waiting %.1fs before retry", wait)
                    time.sleep(wait)
                    delay = min(delay * 2, _BACKOFF_MAX)
                    continue
                if status >= 500 and attempt < _MAX_RETRIES - 1:
                    time.sleep(delay)
                    delay = min(delay * 2, _BACKOFF_MAX)
                    continue

                try:
                    err = resp.json()
                except Exception:
                    err = body_text
                raise KlaviyoClientError(f"HTTP {status} on {url.split('?')[0]}: {err}")

            except (httpx.TimeoutException, httpx.NetworkError) as e:
                if attempt < _MAX_RETRIES - 1:
                    log.warning("Network error on %s: %s — retrying in %.1fs", url, e, delay)
                    time.sleep(delay)
                    delay = min(delay * 2, _BACKOFF_MAX)
                    continue
                raise KlaviyoClientError(f"Network error: {e}")

        raise KlaviyoClientError(f"Exhausted {_MAX_RETRIES} retries on {url}")

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict:
        return self._request(path, params)

    def paginate(self, path: str, params: Optional[Dict[str, Any]] = None,
                 page_size: Optional[int] = 10) -> Iterator[Dict]:
        """Yield every record from a paginated Klaviyo endpoint.
        Set page_size=None to omit the page[size] param (required for campaigns)."""
        p = dict(params or {})
        if page_size is not None and "page[size]" not in p:
            p["page[size]"] = page_size

        # First page uses path + params; subsequent pages use absolute links.next URL
        next_url: Optional[str] = None
        first = True

        while True:
            if first:
                body = self._request(path, p)
                first = False
            else:
                if not next_url:
                    break
                body = self._request(next_url)

            records = body.get("data", [])
            for rec in records:
                yield rec

            next_url = (body.get("links") or {}).get("next")
            if not next_url:
                break

    def validate_connection(self) -> Dict[str, str]:
        body = self.get("/api/accounts/")
        accounts = body.get("data", [])
        if not accounts:
            raise KlaviyoClientError("No account data returned.")
        first = accounts[0]
        attrs = first.get("attributes", {})
        return {
            "account_id": first.get("id", ""),
            "account_name": attrs.get("contact_information", {}).get("organization_name", ""),
            "timezone": attrs.get("timezone", ""),
            "currency": attrs.get("preferred_currency", "USD"),
            "public_api_key": attrs.get("public_api_key", ""),
        }

    @classmethod
    def from_env(cls) -> "KlaviyoClient":
        import os
        key = os.environ.get("KLAVIYO_API_KEY", "")
        if not key:
            raise KlaviyoAuthError("KLAVIYO_API_KEY not set.")
        return cls(key)
