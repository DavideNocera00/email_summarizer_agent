import httpx
from app.config import settings

TOKEN_URL = "https://oauth2.googleapis.com/token"

def get_access_token(client: httpx.Client, refresh_token: str) -> str:
    response = client.post(
        TOKEN_URL,
        data = {
            "client_id": settings.google_client_id,
            "client_secret": settings.google_client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token", #grant_type ask for a new access token using the refresh token
        },
    )

    response.raise_for_status() #Raise an error if Google response with an HTTP error code
    return response.json()["access_token"]

API_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages"

def list_recent_emails(client: httpx.Client, access_token: str, max_results: int = 10) -> list[dict]:
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get(
        API_URL,
        headers=headers,
        params={"maxResults": max_results, "labelIds": "INBOX"}
    )
    response.raise_for_status()
    messages = response.json().get("messages", [])

    emails = []
    for message in messages:
        detail = client.get(f"{API_URL}/{message['id']}", headers=headers, params={"format": "metadata", "metadataHeaders": ["From", "Subject"]})
        detail.raise_for_status()
        data = detail.json()
        header_map = {h["name"]: h["value"] for h in data["payload"]["headers"]}
        emails.append({
            "id": data["id"],
            "sender": header_map.get("From", ""),
            "subject": header_map.get("Subject", ""),
            "snippet": data.get("snippet", ""),
        })
    return emails