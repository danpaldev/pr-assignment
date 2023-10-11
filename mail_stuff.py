from constants import *
import boto3

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

    email_body = f'''
    Pull requests in the last week for repository {REPO_NAME} by {REPO_OWNER}:
    Opened: {opened}
    Closed: {closed}
    Draft: {draft}
    '''

    return email_body


def send_email(data):
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
                'Text': {
                    'Data': get_email_body(data)
                }
            }
        }
    )

    return response
