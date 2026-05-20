from app.transformation.normalizer import normalize_record


def test_normalize_record_maps_fields():
    record = normalize_record({
        "country_name": "Kenya",
        "value": "1.25",
        "period": "2026-05-20",
        "product": "gasoline",
        "units": "liter",
        "currency_code": "USD",
    })
    assert record["country"] == "Kenya"
    assert record["product_type"] == "fuel"
    assert float(record["price"]) == 1.25
    assert record["business_key"]
