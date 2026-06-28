from pydantic import BaseModel
import json
from typing import List
from gemini_client import  generate_config, client

email_prompt  = """You are an expert product analyist who writes cold emails that actually get replies.
Return ONLY a JSON object — no explanation, no markdown:

{
  "subject_lines": ["option 1", "option 2", "option 3"],
  "email_body": "string — the full email, under 100 words",
  "follow_up_email": "string — a 3-day follow-up email, under 60 words"
  "Email" : a valid email that was scrapped aslong side you can give up to 3 email depending on the data you have
}

Rules for the email:
- First sentence must reference something SPECIFIC about the company
- Exactly one product idea or improvement
- Exactly one CTA matched to lead temperature (hot = book a call, warm = see a demo, cold = share a resource)
- No 'hope this finds you well', no 'I wanted to reach out', no 'synergy'
- Sound like a human, not a marketing department
- Under 100 words for the main email"""


class email_schema(BaseModel):
  subject_lines : List[str]
  email_body : str
  follow_up_email : str
  email: str

email_client = generate_config(email_prompt, email_schema, 0.7)


def email_generator(result, score ,client, email_jsonConfig = email_client ):
    merged_dict = result | score
    to_model = json.dumps(merged_dict)
    print("function entered")
    try:
        print("sending req")
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=to_model,
            config = email_jsonConfig
            )
        email = json.loads(response.text)
        print("data received")
        return email
    except Exception as e:
        print(f"Error : {e}" )
        email = {"error": "error in processing"}
        
        return email