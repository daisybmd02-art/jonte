from fastapi import APIRouter, Query
import json
import os

router = APIRouter(prefix="/locations", tags=["locations"])

DATA_PATH = os.path.join(os.path.dirname(
    __file__), "..", "knowledge", "kenya_locations.json")


def load_locations():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/counties")
def counties():
    data = load_locations()
    return sorted(list(data.keys()))


@router.get("/constituencies")
def constituencies(county: str = Query(...)):
    data = load_locations()
    return sorted(list(data.get(county, {}).keys()))


@router.get("/wards")
def wards(county: str = Query(...), constituency: str = Query(...)):
    data = load_locations()
    return sorted(data.get(county, {}).get(constituency, []))
