installation:
Clone the repo
cd JIRA_PII
virtualvenv .venv
source .venv/bin/activate
pip install -r requirements

To test out the code:
Create an env file in the root folder with these as the variables
jiraToken="your_Jira_token"
adminId="Your admin id"
baseURL='The base url for the jira'

In the issue tagger file at line 10:
set your Project name here
issues=fetcher.get_issues("your_project name")

In commands.ipynb set the kernel to .venv
run the first cell
