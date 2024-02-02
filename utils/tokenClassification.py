from transformers import AutoTokenizer, AutoModelForTokenClassification , pipeline
model_path="./models/deberta_finetuned_pii"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForTokenClassification.from_pretrained(model_path)


## seperate out the the methods for processing comments description and title add file uploader create a class


def get_leaks(issues):

    gen = pipeline("token-classification",model=model,tokenizer=tokenizer, device=-1)
    tagged_issues=[]
    ''' look for issue["fields"]["summary"], issue["fields"]["description"]["content"]["content"]["text"] , issue["fields"]["comment"]["comments"]["body"]["content"]["content"]["text"]
    '''   
    for issue in issues:
        summary=issue["fields"]["summary"]
        # print(issue)
        PII_summary,PII_comments,PII_description=None,None,None
        description=issue["fields"].get('description')
        if description:
            description=description["content"]
            des_string=""
            for i in description:
                for j in i["content"]:
                    # print(j)
                    des_string+=j["text"]
            description=des_string
        # print("******************************************")
        if description:
            PII_description=gen(description, aggregation_strategy="first")
        comments=issue["fields"]["comment"]["comments"]
        # print(comments)
        
        issue_review={}
        PII_summary=gen(summary, aggregation_strategy="first")

        PII_comments=[]
        for comment in comments:
            # print(comment["body"])
            comment_data=comment["body"]["content"]
            comment_string=""
            for j in comment_data:
                # print(j["content"])
                for k in j["content"]:
                    # print(k)
                    comment_string+=k['text']
            PII_comment=gen(comment_string, aggregation_strategy="first")
            if PII_comment:
                PII_comments.append({"id":f"{issue['id']}/{comment['id']}",'PII_leak':True,"Leaks":PII_comment})

        if PII_summary or PII_comments or PII_description:
            issue_review['id']=issue["id"]
            issue_review['piiLeak']= True
            if PII_summary:
                issue_review["title"]=PII_summary
            if PII_description:
                issue_review["description"]=PII_description
            if PII_comments:
                issue_review["comments"]=PII_comments


        else:
            issue_review['id']=issue["id"]
            issue_review['piiLeak']= False

        tagged_issues.append(issue_review)
        
    return tagged_issues


