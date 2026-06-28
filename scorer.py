import joblib
import pandas as pd
def scorer(result: dict):
    model = joblib.load("lead_scorer.pkl")
    x = pd.DataFrame([result])
    label_predict = model.predict(x)[0]
    l1 = model.classes_
    l2 = model.predict_proba(x)[0]
    percentages = [int(prob * 100) for prob in l2]
    prob_breakdown = dict(zip(l1, percentages))
    return {
        "label": label_predict,
        "score": int(prob_breakdown.get(label_predict)*100),
        "prob_breakdown": prob_breakdown
    }