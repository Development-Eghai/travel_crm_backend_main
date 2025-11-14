from sqlalchemy.orm import Query
from sqlalchemy import inspect

# Save original filter() to wrap it later
_original_filter = Query.filter


def _filter_with_soft_delete(self, *criteria):
    """
    Automatically apply `is_deleted = 0`
    for any model that has the `is_deleted` column.
    """
    try:
        mapper = self._primary_entity.entities[0].mapper
        model = mapper.class_
        table = model.__table__

        # Only add filter if model has is_deleted AND it wasn't already filtered
        if "is_deleted" in table.columns:
            if not any("is_deleted" in str(c) for c in criteria):
                criteria = (table.c.is_deleted == 0, *criteria)

    except Exception:
        pass

    return _original_filter(self, *criteria)


# Patch globally
Query.filter = _filter_with_soft_delete

print("✔ Global soft-delete filter active")
