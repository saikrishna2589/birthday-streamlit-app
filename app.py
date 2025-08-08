import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
import os

# Set up Google Sheets access
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(os.environ["GOOGLE_SHEET_CREDS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Open your Google Sheet
sheet_url = "https://docs.google.com/spreadsheets/d/1_lW_b6duH1jqLbQKtpx9xnKsJHErQkB_89K4ULLEb3s"
sheet = client.open_by_url(sheet_url).sheet1  # First sheet/tab

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
        # Prepare the data
        bday = birthday.strftime("%d-%m")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        values = [name.strip(), bday, year_optional.strip(), now]

        # Append to Google Sheet
        sheet.append_row(values)
        st.success("🎉 Your birthday has been saved!")
