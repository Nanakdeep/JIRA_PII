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

def aggregateScoring(issue_data):
    for issue in issue_data:
        score=0
        if issue["piiLeak"]:
            pii_scorea,pii_scored,pii_scoret=0,0,0
            if "title" in issue:
                pii_scoret = calculate_pii_score(issue["title"])

                
            if "description" in issue:
                pii_scored = calculate_pii_score(issue["description"])

                
            if "attachments" in issue:
                pii_scorea=0
                for y in issue["attachments"]:
                    pii_scorey =calculate_pii_score(y["Leaks"])
                    pii_scorea+=pii_scorey
                pii_scorea=pii_scorea/len(issue['attachments'])
            score=(pii_scorea+pii_scored+pii_scoret)/3
        issue['agg_score']=score
    return issue_data

def calculate_pii_score(ner_output):

  pii_entities = ner_output

  pii_count = len(pii_entities)
  pii_categories = set([entity["entity_group"] for entity in pii_entities])
  pii_distances = [abs(entity["start"] - next_entity["start"]) for entity, next_entity in zip(pii_entities[:-1], pii_entities[1:])]
  avg_pii_distance = sum(pii_distances) / len(pii_distances) if pii_distances else 0
  if avg_pii_distance == 0:
    return 0

  weight_count = 0.4
  weight_categories = 0.4
  weight_concentration = 0.2

  score = (
      pii_count * weight_count
      + len(pii_categories) * weight_categories
      + 1 / avg_pii_distance * weight_concentration
  )

  return score