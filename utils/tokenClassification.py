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
        issue_review={}
        PII_summary=get_summary_PII(issue,gen)
        PII_description=get_description_PII(issue,gen)
        PII_comments=get_comments_PII(issue,gen)
        PII_attachments=get_attachment_PII(issue,gen)

        if PII_summary or PII_comments or PII_description or PII_attachments:
            issue_review['id']=issue["id"]
            issue_review['piiLeak']= True
            if PII_summary:
                issue_review["title"]=PII_summary
            if PII_description:
                issue_review["description"]=PII_description
            if PII_comments:
                issue_review["comments"]=PII_comments
            if PII_attachments:
                issue_review['attachments']=PII_attachments


        else:
            issue_review['id']=issue["id"]
            issue_review['piiLeak']= False

        tagged_issues.append(issue_review)
        
    return tagged_issues

def get_summary_PII(issue,gen):
    summary=issue["fields"]["summary"]
    return gen(summary, aggregation_strategy="first")

def get_description_PII(issue,gen):
    description=issue["fields"].get('description')
    if description:
            description=description["content"]
            des_string=""
            for i in description:
                for j in i["content"]:
                    # print(j)
                    des_string+=j["text"]
            description=des_string
    if description:
        return gen(description, aggregation_strategy="first")
    return None

def get_comments_PII(issue,gen):
    comments=issue["fields"]["comment"]["comments"]
    PII_comments=[]
    for comment in comments:
        comment_data=comment["body"]["content"]
        comment_string=""
        for j in comment_data:
            for k in j["content"]:
                comment_string+=k['text']
        PII_comment=gen(comment_string, aggregation_strategy="first")
        if PII_comment:
            PII_comments.append({"id":f"{issue['id']}/{comment['id']}",'PII_leak':True,"Leaks":PII_comment})
    return PII_comments

def get_attachment_PII(issue,gen):
    attachments= issue["fields"].get('attachment_data',[])
    PII_attachments=[]
    for attachment in attachments:
        attachment_data=attachment["content"]
        PII_attachment=gen(attachment_data, aggregation_strategy="first")
        if PII_attachment:
            PII_attachments.append({"filename":f"{attachment['filename']}",'PII_leak':True,"Leaks":PII_attachment})
    return PII_attachments