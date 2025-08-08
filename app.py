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

            # ✅ Upcoming birthdays display logic
            st.subheader("🎉 Birthdays This Week")

            records = sheet.get_all_records()
            today = datetime.today()
            upcoming = []

            for r in records:
                try:
                    bday_dt = datetime.strptime(r['Birthday'], "%Y-%m-%d").replace(year=today.year)
                    days_until = (bday_dt - today).days
                    if 0 <= days_until <= 7:
                        upcoming.append((r['Name'], bday_dt.strftime("%b %d")))
                except:
                    pass  # Skip invalid records

            if upcoming:
                for name, bday in upcoming:
                    st.markdown(f"**{name}** – {bday}")
            else:
                st.write("No birthdays in the next 7 days.")

        except Exception as e:
            st.error("Something went wrong. Please try again later.")
            st.exception(e)
