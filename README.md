installation:

Clone the repo

`cd JIRA_PII`

`virtualvenv .venv`

`source .venv/bin/activate`

`pip install -r requirements`

To test out the code:
Create an env file in the root folder with these as the variables

`jiraToken="your_Jira_token"`
`adminId="Your admin id"`
`baseURL='The base url for the jira'`
`ProjectKey='The project key for your jira project'`

Then simply run 
`python test.py`
or run all cells for commands.ipynb


