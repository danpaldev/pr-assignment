import requests
from datetime import datetime, timedelta
from constants import GITHUB_API_URL, REPO_NAME, REPO_OWNER
from mail_stuff import send_email

try:
    one_week_ago = (datetime.now() - timedelta(weeks=1)).isoformat()

    headers = {
        'Accept': 'application/vnd.github+json',
    }

    response = requests.get(f'{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/pulls',
                            params={'state': 'all', 'sort': 'created', 'direction': 'desc'}, headers=headers)

    if response.status_code == 200:
        pull_requests = response.json()

        pull_requests_last_week = [
            pr for pr in pull_requests if pr['created_at'] >= one_week_ago]

        print(send_email(pull_requests_last_week))
    else:
        raise Exception(f"Error calling GitHub API: {response.json()}")

except Exception as e:
    print(f"An error occurred: {e}")
