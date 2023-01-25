# Importing Python packages
import numpy as np


# ---------------------------------------------------------------------------------------------------


class CalculationEngine:
    @staticmethod
    def error_calculator(ActualVals, ForecastedVals):
        MAPE = np.mean(np.abs((np.array(ActualVals) - np.array(ForecastedVals)) / ActualVals)) * 100
        MSE = np.square(np.subtract(ForecastedVals, ActualVals)).mean()
        RMSE = np.sqrt(np.mean(np.square(ForecastedVals - ActualVals)))
        MAE = np.mean(abs(ForecastedVals -ActualVals))
        WAPE = (ActualVals - ForecastedVals).abs().sum() / ActualVals.sum()
        return {"MAPE": MAPE, "MSE": MSE, "RMSE": RMSE, "MAE": MAE, "WAPE": WAPE}


    @staticmethod
    def accuracy_calculator(actual_vals, forecasted_vals):
        error = np.mean(np.abs((np.array(actual_vals) - np.array(forecasted_vals)) / actual_vals)) * 100
        accuracy = 100-error
        return {"Accuracy": accuracy, "Error": error}


    @staticmethod
    def accuracy_calculator_single(actual_vals, forecasted_vals):
        error = ((actual_vals - forecasted_vals) / actual_vals) * 100
        accuracy = 100 - error
        return {"Accuracy": accuracy, "Error": error}
