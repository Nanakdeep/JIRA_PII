import requests
from requests.auth import HTTPBasicAuth
import json
import os

# token = os.environ['jiraToken']
# adminId= os.environ['adminId']
token="ATATT3xFfGF02nXCViEDY9VhflTc8llK2nyayBSqPLdHm7n9kF0PRsjO8YspGnyFUYmmQ7wUe2g84Zg7MacduiaFycABqESyT0XhDKxiL465UJl8pFZe_rLNVSCQgJa7HJAmDMbZhvjLOlgWwXA8_BmpWXT-aBH7KN7MgPMkJP7ozycbr7aFMzE=E40165D6"
adminId="nanakdeep37@gmail.com"
base_url='https://ndsingh.atlassian.net'

def get_issues(project_key:str):
    url = f"{base_url}/rest/api/2/search?jql=project={project_key}&fields=id&maxResults=100"

    auth = HTTPBasicAuth(adminId, token)

    headers = {
    "Accept": "application/json"
    }

    response = requests.request(
    "GET",
    url,
    headers=headers,
    auth=auth
    )
    out=json.loads(response.text)
    issueIds=out["issues"]
    issues_data=[]
    for issue in issueIds:
        issues_data.append(fetch_issue(issue['id']))
    return issues_data
#ideally we should fetch these datapoints at once by jql


def fetch_issue(id):
    
    url = f"{base_url}/rest/api/3/issue/{id}"
    auth = HTTPBasicAuth(adminId,token)

    headers = {
    "Accept": "application/json"
    }

    res = requests.request(
    "GET",
    url,
    headers=headers,
    auth=auth
    )

    return json.loads(res.text)

#not required

def fetch_attachments(id):
    url =f"{base_url}/rest/api/3/attachment/content/{id}"
    auth = HTTPBasicAuth(adminId,token)

    headers = {
    "Accept": "application/json"
    }

    response = requests.request(
    "GET",
    url,
    headers=headers,
    auth=auth
    )
    out = json.loads(response.text)
    return out

def fetch_comments(id):
    url = "https://your-domain.atlassian.net/rest/api/3/issue/{issueIdOrKey}/comment"

    auth = HTTPBasicAuth("email@example.com", "<api_token>")

    headers = {
    "Accept": "application/json"
    }

    response = requests.request(
    "GET",
    url,
    headers=headers,
    auth=auth
    )

    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
