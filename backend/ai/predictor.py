import joblib
import numpy as np
import os

MODEL_PATH = os.path.join("backend", "ai", "model.pkl")

model = joblib.load(MODEL_PATH)

def predict_progression(bmi, bp, s1, s2, s3, s4, s5, s6):
    """
    Predict disease progression score using ML model.
    Diabetes dataset expects 10 features.
    We are using 8 from record + add 2 dummy (0.0) values.
    """

    X = np.array([[
        0.0,   # age (dummy)
        0.0,   # sex (dummy)
        bmi,
        bp,
        s1,
        s2,
        s3,
        s4,
        s5,
        s6
    ]])

    prediction = model.predict(X)[0]
    return float(prediction)
