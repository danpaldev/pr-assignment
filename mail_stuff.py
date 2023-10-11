from constants import *
import boto3
from botocore.exceptions import BotoCoreError


# Initialize a boto3 & SES
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION)

client = session.client('ses')


def get_email_subject():
    email_subject = f'GitHub pull request summary for {REPO_OWNER}/{REPO_NAME}'
    return email_subject


def get_email_body(pr_data):
    opened = len(
        [pr for pr in pr_data if pr['state'] == 'open'])
    closed = len(
        [pr for pr in pr_data if pr['state'] == 'closed'])
    draft = len([pr for pr in pr_data if pr['draft'] == True])

    # Generating a summary for every Pull Request
    pr_summaries = ""
    for pr in pr_data:
        labels = ", ".join([label['name'] for label in pr['labels']])
        # A Closed PR could be merged or not, we check if it was merged or not
        if pr['state'] == 'closed':
            pr_state = 'Merged' if pr['merge_commit_sha'] else 'Closed without merging'
        # If it’s not closed, it will have either a “draft” or “open” status
        else:
            pr_state = 'Draft' if pr['draft'] else 'Open'

        pr_summaries += f"""
        <li>
        <b>PR#{pr['number']} ({pr_state}):</b> <em> {pr['title']} </em> <br>
        {f"<b>Labels</b>: {labels} <br>" if labels else ""}
        Opened at {pr['created_at']} by {pr['user']['login']} <br>
        <a href='{pr['html_url']}'>Link to PR</a>
        </li><br>"""

    email_body = f"""<html>
    <head></head>
    <body>
    <b> Summary of the last 7 days: </b>
        <p>Opened: {opened}</p>
        <p>Closed: {closed}</p>
        <p>Drafts: {draft}</p>
        <ul>
        {pr_summaries}
        </ul>
    </body>
    </html>"""

    return email_body


def send_email(data):
    try:
        response = client.send_email(
            Source=FROM_EMAIL,
            Destination={
                'ToAddresses': [
                    TO_EMAIL,
                ],
            },
            Message={
                'Subject': {
                    'Data': get_email_subject()
                },
                'Body': {
                    'Html': {
                        'Data': get_email_body(data)
                    }
                }
            }
        )
        return response

    except BotoCoreError as e:
        print(f"Error sending email: {e}")
        raise
