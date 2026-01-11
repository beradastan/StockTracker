import os
import json

def load_state():
    raw = os.getenv("STOCK_STATE", "{}")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}

def is_new_stock(state, url, size):
    return not state.get(url, {}).get("sizes", {}).get(size, False)

def mark_in_stock(state, url, size):
    state.setdefault(url, {}).setdefault("sizes", {})[size] = True

def mark_out_of_stock(state, url, size):
    state.setdefault(url, {}).setdefault("sizes", {})[size] = False
