# Importing Python packages
import traceback
import pandas as pd
import json
from datetime import date

# Importing FastAPI packages
from fastapi import APIRouter, status, HTTPException, Security

# Importing from project files
from api_parameters import SCHEMA, TABLE_MODEL_FORECAST,TABLE_MODEL,TABLE_ASSIGN_MODEL,TABLE_MODEL_METRIC_TYPE,TABLE_MODEL_METRIC
from core.models.database import database
from core.scopes.set_scope import Role
from core.schemas.schemas import UserSchema
from internal.Token import get_current_active_user
from internal.calculationengine import CalculationEngine


router = APIRouter(
    prefix='/error_calculator',
    tags=["Error Calculator"]
)


# ---------------------------------------------------------------------------------------------------


@router.get('/get/errors/{assign_model_id}',
            summary="Gets all types of errors by providing model id")
async def calculate_errors(assign_model_id: int,
                           current_user: UserSchema = Security(get_current_active_user,
                                                               scopes=[Role.REPORTING_USER['name']])):
    """
        Returns the following values:

        `MAPE`, `MSE`,`RMSE`, `MAE`, `WAPE`, `model`

    """

    try:
        query = f"""
                    SELECT forecast_value, actual_value
                    FROM {SCHEMA}.{TABLE_MODEL_FORECAST}
                    WHERE assign_model_id = {assign_model_id};
                """
        records = await database.execute_query(query)

        if len(records) == 0:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="No records found for this assigned model range")

        # Convert list of dictionaries to json
        result = json.dumps(records, indent=1).replace("</", "<\\/")
        result = pd.read_json(result)

        errors_lstm = CalculationEngine.error_calculator(ActualVals=result["actual_value"],
                                                         ForecastedVals=result["forecast_value"])

        query2= f"SELECT id, type_name FROM {SCHEMA}.{TABLE_MODEL_METRIC_TYPE};"

        metric_types = await database.execute_query(query2)

        for type in metric_types:
            query3 = f"""
                        INSERT INTO {SCHEMA}.{TABLE_MODEL_METRIC} (metric_score, metric_type_id, assign_model_id)
                        VALUES ({errors_lstm[type['type_name']]}, {type['id']}, {assign_model_id});
                    """
            insert_model_metrice = await database.execute_query(query=query3)
    
        query4=f"""SELECT model_name 
                    FROM {SCHEMA}.{TABLE_MODEL}
                    WHERE id IN (SELECT model_id
                                 FROM {SCHEMA}.{TABLE_ASSIGN_MODEL}
                                 WHERE id = {assign_model_id});"""
        model_name = await database.execute_query(query4)
        
        return [{**errors_lstm, "model": model_name[0]["model_name"]}]

    except Exception as e:
        exception_list = traceback.format_exc()
        exception_list += "\n\n"
        exception_list += str(e)
        print('Exception --> ', exception_list)
        
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="Something went wrong")
