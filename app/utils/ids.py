from hashlib import sha256

def build_business_key(record: dict) -> str:
    parts = [
        str(record.get("country", "")).strip().lower(),
        str(record.get("product_type", "")).strip().lower(),
        str(record.get("reporting_date", ""))[:10],
        str(record.get("unit", "")).strip().lower(),
        str(record.get("source", "")).strip().lower(),
    ]
    return sha256("|".join(parts).encode("utf-8")).hexdigest()
