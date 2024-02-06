
from utils.fetchJiraIssues import get_issues
from utils.tokenClassification import get_leaks


def issueTagger():
    issues=get_issues("KAN")
    print(get_leaks(issues))
    return None