
from utils.fetchJiraIssues import JiraFetcher
from utils.tokenClassification import TokenClassifier
from utils.scoring import weighted_sum,aggregateScoring

model=TokenClassifier()
fetcher=JiraFetcher()
def issueTagger():

    issues=fetcher.get_issues("KAN")
    # issues=fetcher.get_issue_by_date("KAN",last_n_days=2)
    issue_data=model.get_jira_leaks(issues)
    issue_data=aggregateScoring(issue_data)
    print(issue_data)
    return None