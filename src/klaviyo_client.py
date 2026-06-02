"""
Klaviyo Audit Katie — API Client
Read-only HTTP client for the Klaviyo REST API (revision 2026-04-15).

Usage:
    export KLAVIYO_API_KEY=pk_xxxxxxxxxxxx
    client = KlaviyoClient.from_env()
    data = client.get("/api/accounts/")

Security rules (from security-and-privacy.md):
  - API key loaded from env var only — never passed as an argument in CLI output
  - Key never logged — only endpoint, status code, and record count are logged
  - All calls are GET (read-only); any non-GET attempt raises immediately
  - Server-side only — this module must never be imported in browser/frontend code
"""
from __future__ import annotations

import os
import time
import urllib.request
import urllib.parse
import urllib.error
import json
import logging
from typing import Any, Dict, Iterator, List, Optional

API_BASE = "https://a.klaviyo.com"
REVISION = "2024-02-15"

# Rate limit: Klaviyo burst = 75 req / 10 sec; steady-state ~10 req/sec
_BACKOFF_INITIAL = 2.0   # seconds
_BACKOFF_MAX = 64.0
_MAX_RETRIES = 6

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
            raise KlaviyoAuthError("API key is empty — set KLAVIYO_API_KEY env var.")
        self._key = api_key
        self._revision = revision

    @classmethod
    def from_env(cls) -> "KlaviyoClient":
        key = os.environ.get("KLAVIYO_API_KEY", "")
        if not key:
            raise KlaviyoAuthError(
                "KLAVIYO_API_KEY environment variable is not set. "
                "Export it before running: export KLAVIYO_API_KEY=pk_..."
            )
        return cls(key)

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Klaviyo-API-Key {self._key}",
            "revision": self._revision,
            "Accept": "application/vnd.api+json",
        }

    def _safe_key_hint(self) -> str:
        """Returns a non-sensitive hint for log messages (first 6 chars only)."""
        return self._key[:6] + "..." if len(self._key) > 6 else "***"

    @staticmethod
    def _build_qs(params: Dict[str, Any]) -> str:
        """Build query string keeping [ ] literal — urlencode encodes them as %5B%5D
        which Klaviyo does not decode, causing 'page_size' invalid field errors."""
        parts = []
        for k, v in params.items():
            if v is not None:
                parts.append(f"{k}={urllib.parse.quote(str(v), safe='')}")
        return "&".join(parts)

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict:
        """
        Make a single authenticated GET request.
        Returns the parsed JSON response body.
        Raises on 4xx/5xx after retries.
        """
        url = API_BASE + path
        if params:
            url += "?" + self._build_qs({k: v for k, v in params.items() if v is not None})

        delay = _BACKOFF_INITIAL
        for attempt in range(_MAX_RETRIES):
            req = urllib.request.Request(url, headers=self._headers(), method="GET")
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    body = json.loads(resp.read().decode())
                    record_count = len(body.get("data", [])) if isinstance(body.get("data"), list) else 1
                    log.info("GET %s → %d (%d records)", path, resp.status, record_count)
                    return body

            except urllib.error.HTTPError as e:
                status = e.code
                body_bytes = e.read()
                try:
                    err_body = json.loads(body_bytes)
                except Exception:
                    err_body = {}

                log.warning("GET %s → %d (attempt %d/%d)", path, status, attempt + 1, _MAX_RETRIES)

                if status == 401:
                    raise KlaviyoAuthError(
                        f"Authentication failed (401). Check your API key (hint: {self._safe_key_hint()})."
                    )
                if status == 403:
                    raise KlaviyoPermissionError(
                        f"Permission denied (403) on {path}. "
                        "Ensure the key has read-only scopes for this resource."
                    )
                if status == 404:
                    # Endpoint may not be available on this plan — return empty
                    log.warning("GET %s → 404 (endpoint not available)", path)
                    return {"data": []}
                if status == 429:
                    # Rate limited — back off and retry
                    retry_after = float(e.headers.get("Retry-After", delay))
                    wait = min(retry_after, _BACKOFF_MAX)
                    log.info("Rate limited — waiting %.1fs before retry", wait)
                    time.sleep(wait)
                    delay = min(delay * 2, _BACKOFF_MAX)
                    continue
                if status >= 500:
                    if attempt < _MAX_RETRIES - 1:
                        time.sleep(delay)
                        delay = min(delay * 2, _BACKOFF_MAX)
                        continue
                    raise KlaviyoClientError(f"Server error ({status}) on {path} after {_MAX_RETRIES} attempts.")

                raise KlaviyoClientError(f"HTTP {status} on {path}: {err_body}")

            except urllib.error.URLError as e:
                if attempt < _MAX_RETRIES - 1:
                    log.warning("Network error on %s: %s — retrying in %.1fs", path, e.reason, delay)
                    time.sleep(delay)
                    delay = min(delay * 2, _BACKOFF_MAX)
                    continue
                raise KlaviyoClientError(f"Network error on {path}: {e.reason}")

        raise KlaviyoClientError(f"Exhausted {_MAX_RETRIES} retries on {path}")

    def paginate(self, path: str, params: Optional[Dict[str, Any]] = None) -> Iterator[Dict]:
        """
        Yield every record from a paginated Klaviyo endpoint.
        Handles cursor-based pagination via links.next automatically.
        """
        params = dict(params or {})
        if "page[size]" not in params:
            params["page[size]"] = 100

        url = API_BASE + path
        if params:
            url += "?" + self._build_qs({k: v for k, v in params.items() if v is not None})

        while url:
            req = urllib.request.Request(url, headers=self._headers(), method="GET")
            delay = _BACKOFF_INITIAL
            for attempt in range(_MAX_RETRIES):
                try:
                    with urllib.request.urlopen(req, timeout=30) as resp:
                        body = json.loads(resp.read().decode())
                        records = body.get("data", [])
                        log.info("GET %s → 200 (%d records)", url.split("?")[0], len(records))
                        for record in records:
                            yield record
                        url = (body.get("links") or {}).get("next")
                        break  # successful — exit retry loop

                except urllib.error.HTTPError as e:
                    status = e.code
                    if status == 401:
                        raise KlaviyoAuthError("Authentication failed (401).")
                    if status == 403:
                        raise KlaviyoPermissionError(f"Permission denied (403) on {url.split('?')[0]}.")
                    if status == 404:
                        log.warning("Endpoint not available (404): %s", url.split("?")[0])
                        url = None
                        break
                    if status == 429:
                        retry_after = float(e.headers.get("Retry-After", delay))
                        wait = min(retry_after, _BACKOFF_MAX)
                        time.sleep(wait)
                        delay = min(delay * 2, _BACKOFF_MAX)
                        continue
                    if status >= 500 and attempt < _MAX_RETRIES - 1:
                        time.sleep(delay)
                        delay = min(delay * 2, _BACKOFF_MAX)
                        continue
                    raise KlaviyoClientError(f"HTTP {status} during pagination of {url.split('?')[0]}")

                except urllib.error.URLError as e:
                    if attempt < _MAX_RETRIES - 1:
                        time.sleep(delay)
                        delay = min(delay * 2, _BACKOFF_MAX)
                        continue
                    raise KlaviyoClientError(f"Network error: {e.reason}")
            else:
                raise KlaviyoClientError(f"Exhausted retries paginating {url.split('?')[0]}")

    def validate_connection(self) -> Dict[str, str]:
        """
        Confirms the API key is valid and returns basic account info.
        Call this before any data pull to catch auth errors early.
        Returns {"account_id": ..., "account_name": ...}
        """
        body = self.get("/api/accounts/")
        accounts = body.get("data", [])
        if not accounts:
            raise KlaviyoClientError("No account data returned — key may lack account read scope.")
        first = accounts[0]
        attrs = first.get("attributes", {})
        return {
            "account_id": first.get("id", ""),
            "account_name": attrs.get("contact_information", {}).get("organization_name", ""),
            "timezone": attrs.get("timezone", ""),
            "currency": attrs.get("preferred_currency", "USD"),
            "public_api_key": attrs.get("public_api_key", ""),
        }
