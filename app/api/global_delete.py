# api/global_delete.py

from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.orm import Session
from sqlalchemy import text

from core.database import get_db
from models.api_key import APIKey
from utils.table_resolver import get_model

router = APIRouter(prefix="/global", tags=["Global Delete"])


# ----------------------- COMMON UTIL FUNCTIONS -----------------------

def json_response(success: bool, message: str, data=None):
    return {
        "success": success,
        "message": message,
        "data": data
    }


def validate_api_key(key: str, db: Session):
    if not key:
        raise HTTPException(status_code=401, detail="x-api-key missing")

    entry = db.query(APIKey).filter(APIKey.key_value == key).first()
    if not entry:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return entry.user_id


# ----------------------- SOFT DELETE -----------------------

@router.post("/soft-delete")
def soft_delete(
    table: str = Query(...),
    id: int = Query(...),
    x_api_key: str = Header(None),
    db: Session = Depends(get_db)
):
    validate_api_key(x_api_key, db)

    # Ensure valid table
    get_model(table)

    sql = text(f"UPDATE `{table}` SET is_deleted = 1 WHERE id = :id")
    db.execute(sql, {"id": id})
    db.commit()

    return json_response(True, f"{table} moved to trash", {"id": id})


# ----------------------- RESTORE -----------------------

@router.post("/restore")
def restore(
    table: str = Query(...),
    id: int = Query(...),
    x_api_key: str = Header(None),
    db: Session = Depends(get_db)
):
    validate_api_key(x_api_key, db)
    get_model(table)

    sql = text(f"UPDATE `{table}` SET is_deleted = 0 WHERE id = :id")
    db.execute(sql, {"id": id})
    db.commit()

    return json_response(True, f"{table} restored", {"id": id})


# ----------------------- HARD DELETE -----------------------

@router.delete("/hard-delete")
def hard_delete(
    table: str = Query(...),
    id: int = Query(...),
    x_api_key: str = Header(None),
    db: Session = Depends(get_db)
):
    validate_api_key(x_api_key, db)
    get_model(table)

    sql = text(f"DELETE FROM `{table}` WHERE id = :id")
    db.execute(sql, {"id": id})
    db.commit()

    return json_response(True, f"{table} permanently deleted", {"id": id})


# ----------------------- TRASH VIEW -----------------------

@router.get("/trash")
def trash(
    table: str = Query(...),
    db: Session = Depends(get_db),
    x_api_key: str = Header(None)
):
    validate_api_key(x_api_key, db)
    get_model(table)

    sql = text(f"SELECT * FROM `{table}` WHERE is_deleted = 1 ORDER BY id DESC")
    result = db.execute(sql)

    rows = []
    for row in result:
        rows.append(dict(row._mapping))

    return json_response(True, f"🔥 TRASH FETCH SUCCESS for table: {table}", rows)
