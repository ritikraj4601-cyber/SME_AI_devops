import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from models import db, Operation, DataLog
import requests
import logging

logging.basicConfig(level=logging.INFO)

class AIEngine:
    def __init__(self):
        self.model = LinearRegression()
        self.trained = False

    def train_model(self):
        data = pd.DataFrame({
            'input': np.random.rand(100),
            'output': np.random.rand(100) * 2
        })
        X = data[['input']]
        y = data['output']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        self.model.fit(X_train, y_train)
        self.trained = True
        logging.info("AI model trained automatically.")

    def predict(self, input_value):
        if not self.trained:
            self.train_model()
        return self.model.predict([[input_value]])[0]

    def automate_operation(self, operation_id):
        try:
            response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
            data = response.json()
            metric_value = len(data.get('body', ''))
            prediction = self.predict(metric_value)
            
            operation = Operation.query.get(operation_id)
            if operation:
                operation.predicted_outcome = prediction
                operation.status = 'completed' if prediction > 0.5 else 'pending'
                db.session.add(DataLog(operation_id=operation_id, metric='body_length', value=metric_value))
                db.session.commit()
                logging.info(f"Operation {operation_id} automated automatically: Prediction {prediction}")
        except Exception as e:
            logging.error(f"Automation error: {e}")

ai_engine = AIEngine()