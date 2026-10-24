from datetime import datetime, timezone
from statistics import mean


def process_records(records):
    # Deterministic data profiling; no AI or machine learning is used.
    if not isinstance(records, list):
        raise ValueError("Input must be a list.")
    if not all(isinstance(row, dict) for row in records):
        raise ValueError("Every record must be an object.")

    fields = sorted({key for row in records for key in row.keys()})
    missing_by_field = {}
    numeric_summary = {}
    for field in fields:
        missing_by_field[field] = sum(
            1 for row in records
            if field not in row or row[field] is None or row[field] == ""
        )
        values = [
            row[field] for row in records
            if isinstance(row.get(field), (int, float))
            and not isinstance(row.get(field), bool)
        ]
        if values:
            numeric_summary[field] = {
                "count": len(values), "min": min(values), "max": max(values),
                "mean": round(mean(values), 4),
            }

    return {
        "recordCount": len(records),
        "fieldCount": len(fields),
        "fields": fields,
        "missingValuesByField": missing_by_field,
        "numericSummary": numeric_summary,
        "preview": records[:5],
        "processedAt": datetime.now(timezone.utc).isoformat(),
    }
