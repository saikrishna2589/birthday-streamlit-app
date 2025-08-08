import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re

# Google Sheets auth
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Open your Google Sheet
sheet = client.open_by_key("1O3j6Gu-NZS6H2wgk-ypFr4nb0sxn_Uno6aS72nw_3T0").sheet1

# UI
st.title("🎈 Birthday Board | Wollongong Badminton Fam 🎾")
st.markdown("We’d love to wish you on your special day! Submit your birthday below — **year is optional** 😊")

name = st.text_input("Name")
birthday_input = st.text_input("Birthday (Day and Month only, e.g. 08/08)")
year = st.text_input("Year (optional)", placeholder="e.g., 1995")

# Regex to validate MM/DD format
def valid_birthday_format(date_str):
    return re.match(r"^(0[1-9]|1[0-2])/([0][1-9]|[12][0-9]|3[01])$", date_str)

if st.button("Submit"):
    if name.strip() == "":
        st.warning("Please enter your name.")
    elif not valid_birthday_format(birthday_input):
        st.warning("Please enter birthday in MM/DD format (e.g. 08/08).")
    else:
        sheet.append_row([name, birthday_input, year])
        st.success("🎉 Submitted successfully!")
