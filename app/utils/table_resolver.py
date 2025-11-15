# file: app/utils/table_resolver.py

from models.trip import Trip
from models.destination import Destination
from models.activity import Activity
from models.category import Category
from models.booking_request import BookingRequest
from models.model_enquireform import EnquireForm
from models.lead import Lead
from models.quotation import Quotation
from models.invoice import Invoice

# REGISTER ALL TABLES FOR GLOBAL DELETE
TABLE_MODEL_MAP = {
    "trips": Trip,
    "destinations": Destination,
    "activities": Activity,
    "categories": Category,
    "booking_requests": BookingRequest,
    "enquire_form": EnquireForm,
    "leads": Lead,

    # Newly added ↓↓↓
    "quotations": Quotation,
    "invoices": Invoice,
}


def get_model(table_name: str):
    """
    Return the SQLAlchemy model mapped to the table.
    """
    table_name = table_name.lower()
    model = TABLE_MODEL_MAP.get(table_name)
    if not model:
        raise ValueError(f"Table '{table_name}' is not registered for global delete handling.")
    return model
