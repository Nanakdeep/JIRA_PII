import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
import json
import os
from utils.io import FileProcessor
from utils.constants import FileEntry
from dotenv import load_dotenv
load_dotenv()


class JiraFetcher:
    def __init__(self):
        #env fetch
        self.__token=os.environ['jiraToken']
        self.__adminId=os.environ['adminId']
        self.__baseURL=os.environ['baseURL']
        self.__auth = HTTPBasicAuth(self.__adminId, self.__token)
        self.__headers = {
        "Accept": "application/json"
        }

    def get_issue_by_date(self,project_key:str,last_n_days=2):
        seven_days_ago = datetime.now() - timedelta(days=last_n_days)
        seven_days_ago_str = seven_days_ago.strftime("%Y-%m-%d")
        jql_query = f"project={project_key} AND created>='{seven_days_ago_str}'"
        api_route = f"{self.__baseURL}/rest/api/2/search?jql={jql_query}&fields=id&maxResults=100"
        response = requests.request(
        "GET",
        api_route,
        headers=self.__headers,
        auth=self.__auth
        )
        out=json.loads(response.text)
        issueIds=out["issues"]
        issues_data=[]
        for issue in issueIds:
            issues_data.append(self.fetch_issue(issue['id']))
        return issues_data
    

    def get_issues(self,project_key:str):
        url = f"{self.__baseURL}/rest/api/2/search?jql=project={project_key}&fields=id&maxResults=100"
        print(url, self.__baseURL)
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
        url = f"{self.__baseURL}/rest/api/3/issue/{id}?fields=summary,description,comment,attachment"
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
