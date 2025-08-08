import streamlit as st 
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date, timedelta
import json
import os

# Streamlit UI
st.title("🎈 Birthday Board | Wollongong Badminton Fam 🏸")
st.write("We’d love to wish you on your special day! Submit your birthday below 😊")

# Input fields
name = st.text_input("**Name**")
birthday = st.date_input("**Birthday**", min_value=date(1900, 1, 1), max_value=date.today())

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

            # Access the sheet
            sheet = client.open_by_key("1O3j6Gu-NZS6H2wgk-ypFr4nb0sxn_Uno6aS72nw_3T0").worksheet("Sheet1")

            # Save data
            bday = birthday.strftime("%Y-%m-%d")
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            values = [name.strip(), bday, now]
            sheet.append_row(values)

            st.success("🎉 Your birthday has been saved!")

        except Exception as e:
            st.error("Something went wrong while saving your birthday.")
            st.exception(e)

# 🎉 Always show upcoming birthdays section
st.subheader("🎉 Birthdays This Week")

try:
    # Setup again (required outside the submit button block)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = json.loads(os.environ["GOOGLE_SHEET_CREDS"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key("1O3j6Gu-NZS6H2wgk-ypFr4nb0sxn_Uno6aS72nw_3T0").worksheet("Sheet1")
    records = sheet.get_all_records()

    today = datetime.today()
    upcoming = []

    for r in records:
        try:
            # Parse birthday and ignore the year for comparison
            bday = datetime.strptime(r['Birthday'], "%Y-%m-%d")
            bday_this_year = bday.replace(year=today.year)

            # Handle Feb 29 on non-leap years
            try:
                bday_this_year = bday.replace(year=today.year)
            except ValueError:
                if bday.month == 2 and bday.day == 29:
                    bday_this_year = datetime(today.year, 2, 28)
                else:
                    raise

            days_diff = (bday_this_year - today).days
            if 0 <= days_diff <= 7:
                upcoming.append((r['Name'], bday.strftime("%B %d")))

        except Exception as e:
            st.warning(f"Skipped record with error: {e}")

    if upcoming:
        for name, bday_str in upcoming:
            st.markdown(f"**{name}** – {bday_str}")
    else:
        st.write("No birthdays in the next 7 days.")

except Exception as e:
    st.error("Could not load birthday list.")
    st.exception(e)
