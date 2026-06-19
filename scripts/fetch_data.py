import os
import sys
import argparse
import requests
import urllib.parse
import re
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TIMEOUT = 5  # Seconds for network requests
# ---------------------

def get_auth_token(base_url, username, apikey):
    """
    Authenticates with FreshRSS using the ClientLogin endpoint to get an Auth token.
    """
    login_url = f"{base_url}/api/greader.php/accounts/ClientLogin"
    params = {
        'Email': username,
        'Passwd': apikey
    }

    try:
        response = requests.get(login_url, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        # FreshRSS typically returns "SID=...\nLSID=...\nAuth=..." as text/plain
        match = re.search(r"Auth=(.+)", response.text)
        if match:
            return match.group(1).strip()

        # Fallback for JSON response format
        try:
            data = response.json()
            if isinstance(data, dict):
                return data.get('Auth') or data.get('token') or data.get('access_token')
        except:
            pass
        return None
    except Exception as e:
        print(f"Authentication failed: {e}")
        return None

def fetch_news(base_url, token, category, n=1000):
    """
    Fetches news articles using the obtained Auth token.
    """
    if not token:
        return []

    encoded_category = urllib.parse.quote(category)
    url = f"{base_url}/api/greader.php/reader/api/0/stream/contents/user/-/label/{encoded_category}?n={n}"
    headers = {'Authorization': f'GoogleLogin auth={token}'}

    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        return data.get('items', [])
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def extract_text(summary_obj):
    """
    Handles summary/content that might be a string or a dictionary (e.g., {'content': '...', 'type': 'text/html'}).
    """
    if isinstance(summary_obj, str):
        return summary_obj
    if isinstance(summary_obj, dict):
        return summary_obj.get('content', '')
    return ''

def report_news(hours=24):
    """
    Main logic: Authenticate, Fetch, Filter, and Print formatted Markdown.
    """
    base_url = os.environ.get('SELF_HOSTED_FRESHRSS_BASE_URL')
    username = os.environ.get('SELF_HOSTED_FRESHRSS_USERNAME')
    apikey = os.environ.get('SELF_HOSTED_FRESHRSS_API_KEY')
    category = os.environ.get('SELF_HOSTED_FRESHRSS_CATEGORY')

    if not all([base_url, username, apikey, category]):
        print("Error: Missing environment variables (SELF_HOSTED_FRESHRSS_BASE_URL, SELF_HOSTED_FRESHRSS_USERNAME, SELF_HOSTED_FRESHRSS_API_KEY, SELF_HOSTED_FRESHRSS_CATEGORY)", file=sys.stderr)
        sys.exit(-1)

    token = get_auth_token(base_url, username, apikey)
    if not token:
        print("Error: Failed to obtain authentication token.", file=sys.stderr)
        sys.exit(-2)

    items = fetch_news(base_url, token, category)
    if not items:
        print(f"No news found in category '{category}'.", file=sys.stderr)
        sys.exit(-3)

    now = datetime.now(timezone.utc)
    threshold = now - timedelta(hours=hours)

    filtered = []
    seen = set()

    for item in items:
        pub_ts = item.get('published')
        if pub_ts is None:
            continue

        try:
            dt = datetime.fromtimestamp(float(pub_ts), tz=timezone.utc)
        except (ValueError, TypeError):
            continue

        if dt >= threshold:
            title = item.get('title', '')
            links = item.get('canonical', [])
            link = links[0].get('href') if links else item.get('alternate', [{}])[0].get('href', '')
            key = (title, link)

            if key not in seen:
                seen.add(key)
                filtered.append((dt, item))

    # Sort by timestamp descending (most recent first)
    filtered.sort(key=lambda x: x[0], reverse=True)

    if not filtered:
        print(f"No news found in the last {hours} hours.")
        return

    for dt, item in filtered:
        title = item.get('title')
        raw_summary = item.get('summary') or item.get('content') or ""

        # Ensure we have a string for the regex
        summary_text = extract_text(raw_summary)
        clean_summary = re.sub('<[^<]+?>', '', summary_text).strip()

        local_dt = dt.astimezone()
        offset_hours = int(local_dt.strftime('%z')) // 100

        # Markdown Formatting
        print(f"#### [{local_dt.strftime('%m-%d %H:%M')} UTC{offset_hours:+d}] {title}\n")
        if clean_summary:
            print(f"**摘要：** {clean_summary}\n")
        else:
            print("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and report news from FreshRSS.")
    parser.add_argument('--hours', type=int, default=24, help='Time range in hours (default: 24)')
    args = parser.parse_args()

    report_news(args.hours)
