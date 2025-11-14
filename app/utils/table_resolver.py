# utils/table_resolver.py

from models.trip import Trip
from models.destination import Destination
from models.activity import Activity
from models.category import Category
from models.booking_request import BookingRequest
from models.model_enquireform import EnquireForm

# ADD MORE MODELS HERE WHEN YOU CREATE NEW MODULES

TABLE_MODEL_MAP = {
    "trips": Trip,
    "destinations": Destination,
    "activities": Activity,
    "categories": Category,
    "booking_requests": BookingRequest,
    "enquire_form": EnquireForm
}

def get_model(table_name: str):
    model = TABLE_MODEL_MAP.get(table_name.lower())
    if not model:
        raise ValueError(f"Table '{table_name}' is not registered for global delete handling.")
    return model
