import json
import os
json_file_path = os.path.join(os.path.dirname(__file__), '..', 'weights.json')
with open(json_file_path, 'r') as file:
    weights = json.load(file)

def weighted_sum(issue_data):
    for issue in issue_data:
        weighted_sum=0
        if issue['piiLeak']:
            if 'title' in issue:
                for leak in issue['title']:
                    weighted_sum+=leak['score']*weights[leak['entity_group']]

            if 'description' in issue:
                for leak in issue['description']:
                    weighted_sum+=leak['score']*weights[leak['entity_group']]

            if 'comments' in issue:
                for comment in issue['comments']:
                    if comment["PII_leak"]:
                        for leak in comment["Leaks"]:
                            weighted_sum+=leak['score']*weights[leak['entity_group']]
            
            if 'attachments' in issue:
                for attachment in issue['attachments']:
                    if attachment["PII_leak"]:
                        for leak in attachment["Leaks"]:
                            weighted_sum+=leak['score']*weights[leak['entity_group']]
        issue['weighted_score']=weighted_sum
    return issue_data