from pydantic import BaseModel
import json
from typing import List
from gemini_client import generate_config
instructions = """You are a B2B sales analyst. You will be given scraped text from a company website.
Analyse it and return ONLY a JSON object with this exact structure — no explanation, no markdown, just the JSON:

{
  "company_name": "string",
  "industry": "string (e.g. edtech, fintech, healthcare, ecommerce, saas, real_estate, other)",
  "company_size": "small or medium or large",
  "main_product_or_service": "string, one sentence",
  "likely_pain_points": ["string", "string", "string"],
  "tech_sophistication": "low or medium or high",
  "has_clear_value_proposition": true or false,
  "summary": "string, exactly 2 sentences describing what this company does and who they serve"
}

Rules:
- pain_points must be SPECIFIC to this company, not generic. Bad: 'increase revenue'. Good: 'converting free trial users to paid customers'.
- company_size: small = <50 employees or local/regional, medium = 50-500 or national, large = 500+ or international
- tech_sophistication: based on their product complexity and digital presence
- If you cannot determine something from the text, make a reasonable inference based on context clues
- Validate the email and make sure that the email that was scraped is a valid email """

class userProfile(BaseModel):
    company_name: str
    industry: str
    company_size: str
    main_product_or_service: str
    likely_pain_points: List[str]
    tech_sophistication: str
    has_clear_value_proposition: bool
    summary: str

cleanerClient = generate_config(instructions, userProfile)

def analyse_company(scraped_dict,client,cleanerClient=cleanerClient):
    to_model = json.dumps(scraped_dict)
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=to_model,
            config = cleanerClient
            )
        result = json.loads(response.text)
        return result
    except Exception as e:
        print(f"Error : {e}" )
        result = {k: None for k in scraped_dict} 
        return result
    
    
def extract_feature(result:dict, scrapper_dict:dict)->dict:
    company_size_map = { "small" : 1, "medium" : 2, "large" : 3}

    tech_map = {"low" :1 ,"medium":2, "high":3}

    web_quality = 0
    
    if scrapper_dict.get("url").startswith("https"):
        web_quality +=1 
    if len(scrapper_dict.get("body").split())>500:
        web_quality +=1

    return{
        "company_size" : company_size_map.get(
            result.get("company_size","").lower(),0
        ),

        "tech_sophistication" : tech_map.get(
            result.get("tech_sophistication","").lower(),0
        ),

        "likely_pain_points" : min(max(len(result.get("likely_pain_points")),0),5),

        "has_clear_value_proposition" : int(result.get("has_clear_value_proposition",False)),

        "has_contact_info" : int(scrapper_dict.get("has_emails",False)),

        "website_quality" : web_quality

    }