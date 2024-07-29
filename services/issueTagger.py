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
    print(projectKey)
    issues=fetcher.fetch_all_issues("NDS")
    # issues=fetcher.get_issue_by_date(projectKey,last_n_days=2)
    issue_data=model.get_jira_leaks(issues)
    issue_data=aggregateScoring(issue_data)
    for issue in issue_data:
        if issue["agg_score"]>=3:
            fetcher.addPIILabel(issue['id'])
    print(issue_data)
    return issue_data