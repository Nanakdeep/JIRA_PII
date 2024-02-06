
from utils.fetchJiraIssues import JiraFetcher
from utils.tokenClassification import TokenClassifier
from utils.scoring import weighted_sum

model=TokenClassifier()
fetcher=JiraFetcher()
def issueTagger():

    issues=fetcher.get_issues("KAN")
    issue_data=model.get_leaks(issues)
    issue_data=weighted_sum(issue_data)
    print(issue_data)
    return None