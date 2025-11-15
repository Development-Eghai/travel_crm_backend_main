# app/api/global_delete.py

from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.orm import Session
from sqlalchemy import text

from core.database import get_db
from models.api_key import APIKey
from utils.table_resolver import get_model

router = APIRouter(prefix="/global", tags=["Global Delete"])


# --------------------------------------------------------------------
# COMMON UTIL FUNCTIONS
# --------------------------------------------------------------------
def json_response(success: bool, message: str, data=None):
    return {"success": success, "message": message, "data": data}


def validate_api_key(key: str, db: Session):
    if not key:
        raise HTTPException(status_code=401, detail="x-api-key missing")

    entry = db.query(APIKey).filter(APIKey.key_value == key).first()
    if not entry:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return entry.user_id


# --------------------------------------------------------------------
# EXPAND QUOTATION (FULL STRUCTURE)
# --------------------------------------------------------------------
def expand_quotation(db: Session, quotation_id: int):
    """
    Build and return a dict containing the full quotation structure
    (base row + agent, company, trip, trip_sections, itinerary, costing,
    policies, payment). Returns None if the base quotation row does not exist.
    """
    base = db.execute(
        text("SELECT * FROM quotations WHERE id = :id"),
        {"id": quotation_id}
    ).fetchone()

    if not base:
        return None

    q = dict(base._mapping)

    # Agent
    agent = db.execute(
        text("SELECT * FROM quotation_agents WHERE quotation_id = :id"),
        {"id": quotation_id}
    ).fetchone()
    q["agent"] = dict(agent._mapping) if agent else {}

    # Company
    company = db.execute(
        text("SELECT * FROM quotation_companies WHERE quotation_id = :id"),
        {"id": quotation_id}
    ).fetchone()
    q["company"] = dict(company._mapping) if company else {}

    # Trip (base)
    trip = db.execute(
        text("SELECT * FROM quotation_trips WHERE quotation_id = :id"),
        {"id": quotation_id}
    ).fetchone()
    q["trip"] = dict(trip._mapping) if trip else {}

    # Trip sections
    sections = db.execute(
        text("SELECT * FROM quotation_trip_sections WHERE quotation_id = :id ORDER BY id"),
        {"id": quotation_id}
    ).fetchall()
    q["trip_sections"] = [dict(s._mapping) for s in sections] if sections else []

    # Itinerary
    itinerary = db.execute(
        text("SELECT * FROM quotation_itinerary WHERE quotation_id = :id ORDER BY day"),
        {"id": quotation_id}
    ).fetchall()
    q["itinerary"] = [dict(i._mapping) for i in itinerary] if itinerary else []

    # Costing
    costing = db.execute(
        text("SELECT * FROM quotation_costing WHERE quotation_id = :id"),
        {"id": quotation_id}
    ).fetchone()
    q["costing"] = dict(costing._mapping) if costing else {}

    # Policies
    policies = db.execute(
        text("SELECT * FROM quotation_policies WHERE quotation_id = :id"),
        {"id": quotation_id}
    ).fetchone()
    q["policies"] = dict(policies._mapping) if policies else {}

    # Payment
    payment = db.execute(
        text("SELECT * FROM quotation_payment WHERE quotation_id = :id"),
        {"id": quotation_id}
    ).fetchone()
    q["payment"] = dict(payment._mapping) if payment else {}

    return q


# --------------------------------------------------------------------
# SOFT DELETE
# --------------------------------------------------------------------
@router.post("/soft-delete")
def soft_delete(
    table: str = Query(...),
    id: int = Query(...),
    x_api_key: str = Header(None),
    db: Session = Depends(get_db)
):
    validate_api_key(x_api_key, db)

    # normalize and validate table
    table = table.lower()
    try:
        get_model(table)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        sql = text(f"UPDATE `{table}` SET is_deleted = 1 WHERE id = :id")
        db.execute(sql, {"id": id})
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to soft-delete: {e}")

    return json_response(True, f"{table} moved to trash", {"id": id})


# --------------------------------------------------------------------
# RESTORE
# --------------------------------------------------------------------
@router.post("/restore")
def restore(
    table: str = Query(...),
    id: int = Query(...),
    x_api_key: str = Header(None),
    db: Session = Depends(get_db)
):
    validate_api_key(x_api_key, db)

    table = table.lower()
    try:
        get_model(table)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        sql = text(f"UPDATE `{table}` SET is_deleted = 0 WHERE id = :id")
        db.execute(sql, {"id": id})
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to restore: {e}")

    return json_response(True, f"{table} restored", {"id": id})


# --------------------------------------------------------------------
# HARD DELETE
# --------------------------------------------------------------------
@router.delete("/hard-delete")
def hard_delete(
    table: str = Query(...),
    id: int = Query(...),
    x_api_key: str = Header(None),
    db: Session = Depends(get_db)
):
    validate_api_key(x_api_key, db)

    table = table.lower()
    try:
        get_model(table)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        sql = text(f"DELETE FROM `{table}` WHERE id = :id")
        db.execute(sql, {"id": id})
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to hard-delete: {e}")

    return json_response(True, f"{table} permanently deleted", {"id": id})


# --------------------------------------------------------------------
# TRASH VIEW (FULL EXPANDED)
# --------------------------------------------------------------------
@router.get("/trash")
def trash(
    table: str = Query(...),
    x_api_key: str = Header(None),
    db: Session = Depends(get_db)
):
    validate_api_key(x_api_key, db)

    table = table.lower()
    try:
        get_model(table)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Get IDs of deleted rows
    try:
        sql = text(f"SELECT id FROM `{table}` WHERE is_deleted = 1 ORDER BY id DESC")
        deleted_ids = db.execute(sql).fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to query deleted ids: {e}")

    result = []

    for row in deleted_ids:
        # support both Row and RowMapping shapes
        try:
            row_id = row._mapping["id"]
        except Exception:
            # fallback for tuple-like rows
            row_id = row[0]

        try:
            # special-case: quotations expand to nested structure
            if table == "quotations":
                expanded = expand_quotation(db, row_id)
                if expanded is not None:
                    result.append(expanded)
                else:
                    # if base row missing, skip (or append {}) — here we append a minimal dict
                    result.append({"id": row_id})
                continue

            # special-case: invoices (return full invoice row + possibly items/payments)
            if table == "invoices":
                base = db.execute(
                    text("SELECT * FROM invoices WHERE id = :id"),
                    {"id": row_id}
                ).fetchone()
                if base:
                    invoice_obj = dict(base._mapping)
                    # optionally fetch invoice items/payments here if needed later
                    result.append(invoice_obj)
                else:
                    result.append({"id": row_id})
                continue

            # default: return full base row
            base = db.execute(
                text(f"SELECT * FROM `{table}` WHERE id = :id"),
                {"id": row_id}
            ).fetchone()
            if base:
                result.append(dict(base._mapping))
            else:
                result.append({"id": row_id})
        except Exception as e:
            # If any single row expansion fails, include an error placeholder but continue
            result.append({"id": row_id, "error": str(e)})

    return json_response(True, f"🔥 TRASH FETCH SUCCESS for table: {table}", result)
