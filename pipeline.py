from scrapper import scraper
from gemini_client import client
from data_cleaner import analyse_company, extract_feature
from scorer import scorer
from email_generator import email_generator
import json





def pipeline(url):

    try:
        raw_data = scraper(url)
    except Exception as e:
        return {
            "status": False,
            "stage": "Website Scraper",
            "error": str(e)
        }

    try:
        clean_data = analyse_company(raw_data, client)
    except Exception as e:
        return {
            "status": False,
            "stage": "Company Analysis",
            "error": str(e)
        }

    try:
        feature_dict = extract_feature(clean_data, raw_data)
    except Exception as e:
        return {
            "status": False,
            "stage": "Feature Extraction",
            "error": str(e)
        }

    try:
        score_dict = scorer(feature_dict)
    except Exception as e:
        return {
            "status": False,
            "stage": "Scoring",
            "error": str(e)
        }

    try:
        final = email_generator(clean_data, score_dict, client)
    except Exception as e:
        return {
            "status": False,
            "stage": "Email Generation",
            "error": str(e)
        }

    return {
        "status": True,
        "data": final
    }



if __name__ == "__main__":
    result = pipeline("https://razorpay.com")

    print(result)

    