import json
import os
import urllib.request

# Kenya Area Data API (free public key shown on their docs page)
API_URL = "https://kenyaareadata.vercel.app/api/areas?apiKey=keyPub1569gsvndc123kg9sjhg"

OUT_PATH = os.path.join(os.path.dirname(__file__), "kenya_locations.json")


def main():
    print("Downloading Kenya locations dataset...")
    with urllib.request.urlopen(API_URL) as resp:
        raw = resp.read().decode("utf-8")
        data = json.loads(raw)

    """
    The API returns a nested structure of counties -> constituencies -> wards.
    We normalize it into:
    {
      "County": {
        "Constituency": ["Ward1","Ward2",...]
      }
    }
    """

    # Some APIs wrap in {"data": ...} - handle both.
    if isinstance(data, dict) and "data" in data:
        data = data["data"]

    kenya_locations = {}

    # Try to handle common structures robustly.
    # Expect a list of counties OR a dict keyed by county.
    if isinstance(data, list):
        counties = data
        for c in counties:
            county_name = c.get("county") or c.get(
                "name") or c.get("countyName")
            if not county_name:
                continue
            kenya_locations[county_name] = {}
            constituencies = c.get("constituencies") or c.get(
                "subcounties") or []
            for con in constituencies:
                con_name = con.get("constituency") or con.get(
                    "name") or con.get("subcounty")
                if not con_name:
                    continue
                wards = con.get("wards") or []
                # wards may be list of strings or list of dicts
                ward_names = []
                for w in wards:
                    if isinstance(w, str):
                        ward_names.append(w)
                    elif isinstance(w, dict):
                        ward_names.append(w.get("ward") or w.get("name") or "")
                ward_names = [w for w in ward_names if w]
                kenya_locations[county_name][con_name] = ward_names

    elif isinstance(data, dict):
        # Might already be in the exact format
        # If values are dicts -> constituencies, values list -> wards
        # We'll normalize anyway.
        for county_name, cons in data.items():
            if not isinstance(cons, dict):
                continue
            kenya_locations[county_name] = {}
            for con_name, wards in cons.items():
                if isinstance(wards, list):
                    kenya_locations[county_name][con_name] = wards
                else:
                    kenya_locations[county_name][con_name] = []

    # Save
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(kenya_locations, f, ensure_ascii=False, indent=2)

    # Quick stats
    county_count = len(kenya_locations)
    con_count = sum(len(v) for v in kenya_locations.values())
    ward_count = sum(len(wards) for cons in kenya_locations.values()
                     for wards in cons.values())

    print(f"✅ Saved: {OUT_PATH}")
    print(
        f"Counties: {county_count}, Constituencies: {con_count}, Wards: {ward_count}")


if __name__ == "__main__":
    main()
