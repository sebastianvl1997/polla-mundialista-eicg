import gspread

SPREADSHEET_ID = "1ny7DoyHOd4MipYtBWew9EoQYiXFgvgyaerGRZVhH3UQ"

def connect():
    gc = gspread.service_account(
        filename="credentials/service_account.json"
    )

    spreadsheet = gc.open_by_key(SPREADSHEET_ID)

    return spreadsheet