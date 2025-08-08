import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
import os

# Streamlit UI
st.title("🎈 Birthday Board | Wollongong Badminton Fam 🏸")
st.write("We’d love to wish you on your special day! Submit your birthday below — year is optional 😊")

name = st.text_input("Name")
birthday = st.date_input("Birthday (Day and Month only)")
year_optional = st.text_input("Year (optional)")

if st.button("Submit"):
    if not name.strip():
        st.warning("Please enter your name.")
    else:
        # Setup Google Sheets access
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_dict = json.loads(os.environ["GOOGLE_SHEET_CREDS"])
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)

        # Open by key
        sheet = client.open_by_key("1O3j6Gu-NZS6H2wgk-ypFr4nb0sxn_Uno6aS72nw_3T0").worksheet("Sheet1")

        # Prepare the data
        bday = birthday.strftime("%d-%m")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        values = [name.strip(), bday, year_optional.strip(), now]

        # Append to Google Sheet
        sheet.append_row(values)
        st.success("🎉 Your birthday has been saved!")
