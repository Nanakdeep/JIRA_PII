
from utils.fetchJiraIssues import JiraFetcher
from utils.tokenClassification import TokenClassifier

model=TokenClassifier()
fetcher=JiraFetcher()
def issueTagger():

    issues=fetcher.get_issues("KAN")
    print(model.get_leaks(issues))
    return None