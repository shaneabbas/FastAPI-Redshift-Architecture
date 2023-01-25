# Importing FastAPI packages
from fastapi import APIRouter

# Importing from project files
from routers import auth, commodity, commodity_group, error_calculator, group, license, role, user, \
    user_system_description


# Router Object to Create Routes
router = APIRouter()


# ---------------------------------------------------------------------------------------------------


# Include all file routes
# router.include_router(algo_engine.router)
# router.include_router(assign_model.router)
# router.include_router(calendar.router)
router.include_router(commodity.router)
router.include_router(commodity_group.router)
router.include_router(error_calculator.router)
router.include_router(group.router)
# router.include_router(holiday.router)
# router.include_router(hyper_parameter.router)
# router.include_router(input_file.router)
# router.include_router(license.router)
# router.include_router(model.router)
# router.include_router(model_forecast.router)
# router.include_router(model_metric.router)
# router.include_router(model_metric_type.router)
# router.include_router(model_status.router)
# router.include_router(peak_hours.router)
router.include_router(role.router)
router.include_router(user.router)
router.include_router(user_system_description.router)
router.include_router(auth.router)
