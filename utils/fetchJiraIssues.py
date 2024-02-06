import requests
from requests.auth import HTTPBasicAuth
import json
import os

# token = os.environ['jiraToken']
# adminId= os.environ['adminId']
# baseURL=os.environ['baseURL']

token="ATATT3xFfGF02nXCViEDY9VhflTc8llK2nyayBSqPLdHm7n9kF0PRsjO8YspGnyFUYmmQ7wUe2g84Zg7MacduiaFycABqESyT0XhDKxiL465UJl8pFZe_rLNVSCQgJa7HJAmDMbZhvjLOlgWwXA8_BmpWXT-aBH7KN7MgPMkJP7ozycbr7aFMzE=E40165D6"
adminId="nanakdeep37@gmail.com"
baseURL='https://ndsingh.atlassian.net'

def get_issues(project_key:str):
    url = f"{baseURL}/rest/api/2/search?jql=project={project_key}&fields=id&maxResults=100"

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
    
    url = f"{baseURL}/rest/api/3/issue/{id}"
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

    out=json.loads(res.text)
    attachment_content=[]
    if "attachment" in out.get('fields',{}):
        temp=out.get('fields',{}).get('attachment',[])
        for i in temp:
            content=handle_file({"filename":i["filename"],"content":fetch_attachments(i['id'])})
            attachment_content.append({"filename":i["filename"],"content":content})
    # print('attachment_content',attachment_content)
    if attachment_content:
        out['fields']["attachment_data"]=attachment_content
    return out


def fetch_attachments(id):
    url =f"{baseURL}/rest/api/3/attachment/content/{id}"
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
    out = response.content

    return out


from utils.io import FileProcessor
from utils.constants import FileEntry

def handle_file(file):
    # print(file)
    documents=[]
    document = FileEntry(file["filename"], file["content"])
    documents.append(document)
    obj=FileProcessor(documents,0) 
    out=obj.process_files()
    out=out.split(sep=',')
    return out[-2]