
from utils.fetchJiraIssues import get_issues
from utils.tokenClassification import TokenClassifier

model=TokenClassifier()

def issueTagger():
    issues=get_issues("KAN")
    print(model.get_leaks(issues))
    return None