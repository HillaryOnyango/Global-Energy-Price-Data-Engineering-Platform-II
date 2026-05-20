from app.validation.quality_checks import validate_records


def test_validate_records_rejects_negative_price():
    records = [{
        "country": "Kenya",
        "product_type": "fuel",
        "price": -1,
        "currency": "USD",
        "unit": "liter",
        "reporting_date": "2026-05-20",
        "source": "EIA_API",
        "business_key": "abc",
    }]
    result = validate_records(records)
    assert result.invalid_count == 1
    assert result.error_breakdown["negative_price"] == 1
