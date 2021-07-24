import pickle
import pandas as pd


class Prediction:
    """
    Load the model which train in notebook

    """

    def __init__(self):
        with open('models/scalar.pickle', 'rb') as handle:
            self.scalar = pickle.load(handle)

        with open('models/decision_tree.pickle', 'rb') as handle:
            self.model = pickle.load(handle)

    def predict_direction(self, input_df: pd.DataFrame):
        input_df = input_df.values
        input_scaled = self.scalar.transform(input_df)
        prediction = self.model.predict_proba(input_scaled)
        return prediction
