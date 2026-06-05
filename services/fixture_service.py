import requests
import pandas as pd
from datetime import datetime, timedelta

FIXTURE_URL = "https://fixturedownload.com/view/json/fifa-world-cup-2026"


import requests
import json
import re
import pandas as pd

FIXTURE_URL = "https://fixturedownload.com/feed/json/fifa-world-cup-2026"


def _load_fixture():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(FIXTURE_URL, headers=headers)

    if response.status_code != 200:
        raise Exception(f"HTTP error {response.status_code}")

    html = response.text

    # ----------------------------------------------------
    # 🔥 1. Intento de extracción del JSON embebido
    # ----------------------------------------------------

    # Caso típico: JSON dentro de <script> ... var data = [...]
    patterns = [
        r"var\s+data\s*=\s*(\[\{.*?\}\]);",
        r"data\s*=\s*(\[\{.*?\}\]);",
        r"(\[\{.*?\}\])"
    ]

    for pattern in patterns:
        match = re.search(pattern, html, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except:
                continue

    # ----------------------------------------------------
    # 🔥 2. fallback: buscar JSON más grande (greedy controlado)
    # ----------------------------------------------------

    match = re.search(r"(\[\s*\{.*\}\s*\])", html, re.DOTALL)

    if match:
        try:
            return json.loads(match.group(1))
        except Exception:
            pass

    # ----------------------------------------------------
    # ❌ si falla todo
    # ----------------------------------------------------
    raise Exception("No se pudo extraer JSON del HTML")


def get_all_matches():
    data = _load_fixture()
    df = pd.json_normalize(data)
    return df


def get_group_stage_matches():
    df = get_all_matches()
    return df


def get_match(match_number):
    df = get_all_matches()
    match = df[df["MatchNumber"] == match_number]
    return match.to_dict("records")[0] if not match.empty else None


def is_locked(match):
    kickoff = pd.to_datetime(match["Date"])
    lock_time = kickoff - timedelta(minutes=5)
    return datetime.utcnow() >= lock_time.to_pydatetime()

import pycountry

EXCEPTIONS = {
    "USA": "us",
    "United States": "us",
    "South Korea": "kr",
    "Korea Republic": "kr",
    "England": "gb-eng",
    "Scotland": "gb-sct",
    "Wales": "gb-wls",
}

def get_country_code(country_name):

    EXCEPTIONS = {
        "USA": "us",
        "United States": "us",
        "South Korea": "kr",
        "Korea Republic": "kr",
        "England": "gb-eng",
        "Scotland": "gb-sct",
        "Wales": "gb-wls",
    }

    if country_name in EXCEPTIONS:
        return EXCEPTIONS[country_name]

    try:
        import pycountry
        country = pycountry.countries.lookup(country_name)
        return country.alpha_2.lower()
    except:
        return None
    
def get_flag_url(country_name):
    code = get_country_code(country_name)

    if not code:
        return "https://via.placeholder.com/40x30?text=?"

    return f"https://flagcdn.com/w40/{code}.png"


