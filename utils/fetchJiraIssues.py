import requests
from requests.auth import HTTPBasicAuth
import json
import os
from utils.io import FileProcessor
from utils.constants import FileEntry


class JiraFetcher:
    def __init__(self):
        #env fetch
        self.__token="ATATT3xFfGF02nXCViEDY9VhflTc8llK2nyayBSqPLdHm7n9kF0PRsjO8YspGnyFUYmmQ7wUe2g84Zg7MacduiaFycABqESyT0XhDKxiL465UJl8pFZe_rLNVSCQgJa7HJAmDMbZhvjLOlgWwXA8_BmpWXT-aBH7KN7MgPMkJP7ozycbr7aFMzE=E40165D6"
        self.__adminId="nanakdeep37@gmail.com"
        self.__baseURL='https://ndsingh.atlassian.net'
        self.__auth = HTTPBasicAuth(self.__adminId, self.__token)
        self.__headers = {
        "Accept": "application/json"
        }

    def get_issues(self,project_key:str):
        url = f"{self.__baseURL}/rest/api/2/search?jql=project={project_key}&fields=id&maxResults=100"

        response = requests.request(
        "GET",
        url,
        headers=self.__headers,
        auth=self.__auth
        )
        out=json.loads(response.text)
        issueIds=out["issues"]
        issues_data=[]
        for issue in issueIds:
            issues_data.append(self.fetch_issue(issue['id']))
        return issues_data

    def fetch_issue(self,id):
        url = f"{self.__baseURL}/rest/api/3/issue/{id}"
        res = requests.request(
        "GET",
        url,
        headers=self.__headers,
        auth=self.__auth
        )
        out=json.loads(res.text)
        attachment_content=[]
        if "attachment" in out.get('fields',{}):
            temp=out.get('fields',{}).get('attachment',[])
            for i in temp:
                content=self.handle_file({"filename":i["filename"],"content":self.fetch_attachments(i['id'])})
                attachment_content.append({"filename":i["filename"],"content":content})
        if attachment_content:
            out['fields']["attachment_data"]=attachment_content
        return out

    def fetch_attachments(self,id):
        url =f"{self.__baseURL}/rest/api/3/attachment/content/{id}"
        response = requests.request(
        "GET",
        url,
        headers=self.__headers,
        auth=self.__auth
        )
        out = response.content
        return out

    
    def handle_file(self,file):
        documents=[]
        document = FileEntry(file["filename"], file["content"])
        documents.append(document)
        obj=FileProcessor(documents,0) 
        out=obj.process_files()
        out=out.split(sep=',')
        return out[-2]
