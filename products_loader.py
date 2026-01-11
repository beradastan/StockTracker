import os
import json

def load_products():
    raw = os.environ.get("PRODUCTS_JSON")
    if not raw:
        raise RuntimeError("PRODUCTS_JSON secret bulunamadı")

    return json.loads(raw)
