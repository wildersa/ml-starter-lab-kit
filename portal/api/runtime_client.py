"""HTTP client for communicating with the Lab Runtime execution plane."""
import os
from typing import Any, Dict, Optional
import httpx


class RuntimeUnavailableError(Exception):
    """Raised when the Lab Runtime service is unreachable or offline."""
    pass


class LabRuntimeClient:
    """Client for the separate Lab Runtime execution service."""

    def __init__(self, base_url: Optional[str] = None, timeout: float = 3.0):
        self.base_url = base_url or os.getenv("LAB_RUNTIME_URL", "http://127.0.0.1:8001")
        self.timeout = timeout

    def get_status(self) -> Dict[str, Any]:
        """Queries the health and capability status of the Lab Runtime service."""
        try:
            with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
                res = client.get("/capabilities")
                res.raise_for_status()
                return {"status": "online", **res.json()}
        except Exception as e:
            return {
                "status": "offline",
                "error": f"Lab Runtime unavailable at {self.base_url}: {str(e)}",
            }

    def reset_simulation(
        self, session_id: Optional[str] = None, seed: Optional[int] = 42
    ) -> Dict[str, Any]:
        """Requests an RL simulation environment reset from the Lab Runtime."""
        try:
            with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
                res = client.post(
                    "/rl/reset",
                    json={"session_id": session_id, "seed": seed},
                )
                if res.status_code == 404:
                    raise ValueError(res.json().get("detail", "Session not found"))
                res.raise_for_status()
                return res.json()
        except (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError) as e:
            raise RuntimeUnavailableError(
                f"Lab Runtime unavailable at {self.base_url}: {str(e)}"
            ) from e
        except httpx.HTTPStatusError as e:
            if e.response.status_code >= 500:
                raise RuntimeUnavailableError(
                    f"Lab Runtime server error: {e.response.text}"
                ) from e
            raise ValueError(e.response.json().get("detail", str(e))) from e

    def step_simulation(
        self, action: int, session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Requests one simulation step and Q-update calculation from the Lab Runtime."""
        try:
            with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
                res = client.post(
                    "/rl/step",
                    json={"session_id": session_id, "action": action},
                )
                if res.status_code in (400, 404):
                    raise ValueError(res.json().get("detail", "Invalid step request"))
                res.raise_for_status()
                return res.json()
        except (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError) as e:
            raise RuntimeUnavailableError(
                f"Lab Runtime unavailable at {self.base_url}: {str(e)}"
            ) from e
        except httpx.HTTPStatusError as e:
            if e.response.status_code >= 500:
                raise RuntimeUnavailableError(
                    f"Lab Runtime server error: {e.response.text}"
                ) from e
            raise ValueError(e.response.json().get("detail", str(e))) from e


runtime_client = LabRuntimeClient()
