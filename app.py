import streamlit as st 
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date
import json
import os

# Streamlit UI
st.title("🎈 Birthday Board | Wollongong Badminton Fam 🏸")
st.write("We’d love to wish you on your special day! Submit your birthday below 😊")

# Input fields
name = st.text_input("**Name**")
birthday = st.date_input("**Birthday**", min_value=date(1900, 1, 1), max_value=date.today())

# Submission logic
if st.button("Submit"):
    if not name.strip():
        st.warning("Please enter your name.")
    else:
        try:
            # Setup Google Sheets access
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds_dict = json.loads(os.environ["GOOGLE_SHEET_CREDS"])
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            client = gspread.authorize(creds)

            # Debug: show accessible spreadsheets
            spreadsheet_list = client.openall()
            st.write("✅ Connected to Google Sheets!")
            st.write("Accessible spreadsheets:")
            for s in spreadsheet_list:
                st.write(f"• {s.title}")

            # Open the correct sheet
            sheet = client.open_by_key("1O3j6Gu-NZS6H2wgk-ypFr4nb0sxn_Uno6aS72nw_3T0").worksheet("Sheet1")

            # Prepare values
            bday = birthday.strftime("%Y-%m-%d")
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            values = [name.strip(), bday, now]

            # Append row
            sheet.append_row(values)
            st.success("🎉 Your birthday has been saved!")

        except Exception as e:
            st.error("❌ Something went wrong. Check permissions or API settings.")
            st.exception(e)
