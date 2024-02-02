from utils.io import FileProcessor
from utils.fetchJiraIssues import get_issues
from utils.tokenClassification import get_leaks
from utils.constants import FileEntry
from docx import Document

def issueTagger():
    issues=get_issues("KAN")
    print(get_leaks(issues))
    return None