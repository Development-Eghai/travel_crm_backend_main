# api/global_delete.py

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from utils.table_resolver import get_model

router = APIRouter()

def api_json_response(success, message, data=None):
    return {"success": success, "message": message, "data": data}

# ----------------------------
#   SOFT DELETE
# ----------------------------
@router.post("/soft-delete")
def soft_delete(table: str, id: int, db: Session = Depends(get_db)):
    try:
        model = get_model(table)
        item = db.query(model).filter(model.id == id).first()

        if not item:
            raise HTTPException(status_code=404, detail="Record not found")

        item.is_deleted = True
        db.commit()
        return api_json_response(True, f"{table} record moved to trash", {"id": id})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------------
#   RESTORE
# ----------------------------
@router.post("/restore")
def restore(table: str, id: int, db: Session = Depends(get_db)):
    try:
        model = get_model(table)
        item = db.query(model).filter(model.id == id).first()

        if not item:
            raise HTTPException(status_code=404, detail="Record not found")

        item.is_deleted = False
        db.commit()
        return api_json_response(True, f"{table} restored successfully", {"id": id})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------------
#   GET TRASH ITEMS
# ----------------------------
@router.get("/trash")
def view_trash(table: str, db: Session = Depends(get_db)):
    try:
        model = get_model(table)
        items = db.query(model).filter(model.is_deleted == True).all()

        data = [item.id for item in items]
        return api_json_response(True, "Trash retrieved", data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------
#   HARD DELETE
# ----------------------------
@router.delete("/hard-delete")
def hard_delete(table: str, id: int, db: Session = Depends(get_db)):
    try:
        model = get_model(table)
        item = db.query(model).filter(model.id == id).first()

        if not item:
            raise HTTPException(status_code=404, detail="Record not found")

        db.delete(item)
        db.commit()

        return api_json_response(True, f"{table} permanently deleted", {"id": id})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
