installation:

Clone the repo

`cd JIRA_PII`

`virtualvenv .venv`

`source .venv/bin/activate`

`pip install -r requirements`

To test out the code:
Please run these commands with appropriate values to set the env variables

`echo "jiraToken=\"your_Jira_token\"" >> .env`

`echo "adminId=\"Your admin id\"" >> .env`

`echo "baseURL='The base url for the jira'" >> .env`

`echo "ProjectKey='The project key for your jira project'" >> .env`


Then simply run 
`python test.py`
or run all cells for commands.ipynb


