# utils/table_resolver.py

from models.trip import Trip
from models.destination import Destination
from models.activity import Activity
from models.category import Category
from models.booking_request import BookingRequest
from models.model_enquireform import EnquireForm
from models.lead import Lead

TABLE_MODEL_MAP = {
    "trips": Trip,
    "destinations": Destination,
    "activities": Activity,
    "categories": Category,
    "booking_requests": BookingRequest,
    "enquire_form": EnquireForm,
    "leads": Lead,
}

def get_model(table_name: str):
    table_name = table_name.lower()
    if table_name not in TABLE_MODEL_MAP:
        raise ValueError(f"Table '{table_name}' is not registered for global delete handling.")
    return TABLE_MODEL_MAP[table_name]
