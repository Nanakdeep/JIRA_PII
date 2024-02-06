from transformers import AutoTokenizer, AutoModelForTokenClassification , pipeline

class TokenClassifier:
    def __init__(self):
        self.model_path="./models/deberta_finetuned_pii"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForTokenClassification.from_pretrained(self.model_path)
        self.gen=pipeline("token-classification",model=self.model,tokenizer=self.tokenizer, device=-1)
    
    def get_leaks(self,issues):
        tagged_issues=[]
        ''' looks for
            issue["fields"]["summary"],
            issue["fields"]["description"]["content"]["content"]["text"] ,
            issue["fields"]["comment"]["comments"]["body"]["content"]["content"]["text"]
        '''   
        for issue in issues:
            issue_review={}
            PII_summary=self.get_summary_PII(issue)
            PII_description=self.get_description_PII(issue)
            PII_comments=self.get_comments_PII(issue)
            PII_attachments=self.get_attachment_PII(issue)

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

    def get_summary_PII(self,issue):
        summary=issue["fields"]["summary"]
        return self.gen(summary, aggregation_strategy="first")

    def get_description_PII(self,issue):
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
            return self.gen(description, aggregation_strategy="first")
        return None

    def get_comments_PII(self,issue):
        comments=issue["fields"]["comment"]["comments"]
        PII_comments=[]
        for comment in comments:
            comment_data=comment["body"]["content"]
            comment_string=""
            for j in comment_data:
                for k in j["content"]:
                    comment_string+=k['text']
            PII_comment=self.gen(comment_string, aggregation_strategy="first")
            if PII_comment:
                PII_comments.append({"id":f"{issue['id']}/{comment['id']}",'PII_leak':True,"Leaks":PII_comment})
        return PII_comments

    def get_attachment_PII(self,issue):
        attachments= issue["fields"].get('attachment_data',[])
        PII_attachments=[]
        for attachment in attachments:
            attachment_data=attachment["content"]
            PII_attachment=self.gen(attachment_data, aggregation_strategy="first")
            if PII_attachment:
                PII_attachments.append({"filename":f"{attachment['filename']}",'PII_leak':True,"Leaks":PII_attachment})
        return PII_attachments