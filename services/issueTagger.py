import os
from utils.fetchJiraIssues import JiraFetcher
from utils.tokenClassification import TokenClassifier
from utils.scoring import weighted_sum,aggregateScoring
from dotenv import load_dotenv
load_dotenv()

model=TokenClassifier()
fetcher=JiraFetcher()
def issueTagger():
    projectKey=os.environ['ProjectKey']
    issues=fetcher.get_issues(projectKey)
    # issues=fetcher.get_issue_by_date(projectKey,last_n_days=2)
    issue_data=model.get_jira_leaks(issues)
    issue_data=aggregateScoring(issue_data)
    print(issue_data)
    return issue_data