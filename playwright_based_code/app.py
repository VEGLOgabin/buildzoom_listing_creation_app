
import time
import re
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd
import io
from googleapiclient.http import MediaIoBaseDownload
import os
import streamlit as st
import time
from PIL import Image
import os

from playwright.sync_api import sync_playwright
import time

GOOGLE_DRIVE_FOLDER_KEY = "1vbN5nJmnVXLb2vyb143djusRkKfJWTna"

def extract_zip_code(address: str) -> str:
    match = re.search(r'\b\d{5}\b', address)
    return match.group(0) if match else 'N/A'


def google_drive_operation():
    # Setup
    SERVICE_ACCOUNT_FILE = 'credentials.json'
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=creds)

    # Folder containing your files (get this from your Google Drive)
    folder_id = GOOGLE_DRIVE_FOLDER_KEY

    file_name = 'Best Rate Roofing of Fullerton Info.xlsx'

    # Query to find Excel file inside folder
    query = f"'{folder_id}' in parents and name = '{file_name}' and mimeType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])


    if not files:
        print("⚠️ Excel file not found.")
        return None
    else:
        file_id = files[0]['id']
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        fh.seek(0)
        df = pd.read_excel(fh, engine='openpyxl', header = None)
        df.dropna(inplace=True)
        df.dropna(subset=[0, 1], inplace=True)
        data_dict = dict(zip(df[0], df[1]))
        print(data_dict)

        return data_dict



def buildzoom_signup():
    wait_time = 25
    delay_time = 5
    timeout_up = 15000

    name = ""
    address = ""
    phone_number = ""
    website = ""
    e_mail = ""
    password = ""
    signature = ""
    zip_code = ""

    data = google_drive_operation()
    if data:
        st.success("✅ Google Sheet data pulled successfully!")
        name = data.get("Name", "")
        address = data.get("Address", "")
        phone_number = data.get("Phone", "")
        website = data.get("Website", "")
        e_mail = data.get("Email", "")
        password = data.get("Password", "")
        signature = data.get("Signature", "")

    zip_code = extract_zip_code(address)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.buildzoom.com/user/sign_in", timeout=0)
        time.sleep(delay_time)

        try:
            page.locator("div.email-password-form-action a").last.click(timeout = timeout_up)
            print("✅ Clicked 'Sign up' link")
            st.success("✅ Clicked 'Sign up' link!")
        except Exception as e:
            print(f"❌ Could not click 'Sign up' link: {e}")
            st.error(f"✅ ❌ Could not click 'Sign up' link: {e}")

        time.sleep(delay_time)

        try:
            page.locator("li.auth-screen-nav-item").last.click(timeout = timeout_up)
            print("✅ Clicked 'Contractor' tab")
            st.success("✅ Clicked 'Contractor' tab")
        except Exception as e:
            print(f"❌ Could not click 'Contractor' tab: {e}")
            st.error(f"❌ Could not click 'Contractor' tab: {e}")

        time.sleep(delay_time)

        try:
            page.fill('input[placeholder="e.g. ABC Flooring"]', name)
            print("✅ Filled business name")
            st.success("✅ Filled business name")
        except Exception as e:
            print(f"❌ Failed to fill business name: {e}")
            st.error(f"❌ Failed to fill business name: {e}")

        time.sleep(delay_time)

        try:
            page.click("a.claim-business-add-prompt-link", timeout=timeout_up)
            print("✅ Clicked '+ Add your business'")
            st.success("✅ Clicked '+ Add your business'")
        except Exception as e:
            print(f"❌ Failed to click add business: {e}")
            st.error(f"❌ Failed to click add business: {e}")

        time.sleep(delay_time)

        try:
            page.fill('input[placeholder="name@email.com"]', e_mail, timeout=timeout_up)
            st.success("✅ Entered email")
            print("✅ Entered email")
        except Exception as e:
            st.error(f"❌ Failed to enter email: {e}")
            print(f"❌ Failed to enter email: {e}")

        time.sleep(delay_time)

        try:
            page.fill('input[placeholder="Create a password"]', password, timeout=timeout_up)
            st.success("✅ Entered password")
            print("✅ Entered password")
        except Exception as e:
            st.error(f"❌ Failed to enter password: {e}")
            print(f"❌ Failed to enter password: {e}")

        time.sleep(delay_time)

        try:
            page.click("button.email-password-form-submit", timeout=timeout_up)
            st.success("✅ Clicked submit")
            print("✅ Clicked submit")
        except Exception as e:
            st.error(f"❌ Failed to click submit: {e}")
            print(f"❌ Failed to click submit: {e}")

        time.sleep(delay_time)

        try:
            page.select_option("select[ng-model='$ctrl.contractor.contractorTypeId']", value="number:6", timeout=timeout_up)
            st.success("✅ Selected 'Roofer'")
            print("✅ Selected 'Roofer'")
        except Exception as e:
            st.error(f"❌ Failed to select 'Roofer': {e}")
            print(f"❌ Failed to select 'Roofer': {e}")

        try:
            page.wait_for_selector("div.icon-button-label", timeout=timeout_up)
            for label in page.locator("div.icon-button-label").all():
                label.click(timeout=timeout_up)
            st.success("✅ Selected all labels")
            print("✅ Selected all labels")
        except Exception as e:
            st.error(f"❌ Failed to select labels: {e}")
            print(f"❌ Failed to select labels: {e}")

        time.sleep(delay_time)

        try:
            page.click("button.next-button", timeout=timeout_up)
            st.success("✅ Clicked 'Next'")
            print("✅ Clicked 'Next'")
        except Exception as e:
            st.error(f"❌ Failed to click 'Next': {e}")
            print(f"❌ Failed to click 'Next': {e}")

        time.sleep(delay_time)

        try:
            page.click("button.next-button", timeout=timeout_up)
            st.success("✅ Clicked 'Next'")
            print("✅ Clicked 'Next'")
        except Exception as e:
            st.error(f"❌ Failed to click second 'Next': {e}")
            print(f"❌ Failed to click second 'Next': {e}")

        try:
            page.fill("input[placeholder='Street address']", address, timeout=timeout_up)
            st.success("✅ Entered address")
            print("✅ Entered address")
        except Exception as e:
            st.error(f"❌ Failed to enter address: {e}")
            print(f"❌ Failed to enter address: {e}")

        time.sleep(delay_time)

        try:
            page.fill("input[placeholder='Zipcode']", zip_code, timeout=timeout_up)
            st.success("✅ Entered Zipcode")
            print("✅ Entered Zipcode")
        except Exception as e:
            st.error(f"❌ Failed to enter zipcode: {e}")
            print(f"❌ Failed to enter zipcode: {e}")

        time.sleep(delay_time)

        try:
            page.select_option('select.travel-range-input', "number:150", timeout=timeout_up)
            st.success("✅ Selected travel range")
            print("✅ Selected travel range")
        except Exception as e:
            st.error(f"❌ Failed to select travel range: {e}")
            print(f"❌ Failed to select travel range: {e}")

        time.sleep(delay_time)

        try:
            page.fill("input[placeholder='Mobile phone']", phone_number, timeout=timeout_up)
            st.success("✅ Entered phone number")
            print("✅ Entered phone number")
        except Exception as e:
            st.error(f"❌ Failed to enter phone number: {e}")
            print(f"❌ Failed to enter phone number: {e}")

        try:
            page.click("button.next-button", timeout=timeout_up)
            st.success("✅ Clicked 'Next' button")
            print("✅ Clicked 'Next' button")
        except Exception as e:
            st.error(f"❌ Failed to click 'Next' button: {e}")
            print(f"❌ Failed to click 'Next' button: {e}")

        time.sleep(delay_time)

        try:
            page.select_option("select[ng-model='$ctrl.contractor.contractorTypeId']", "number:6", timeout=timeout_up)
            st.success("✅ Selected contractor type again")
            print("✅ Selected contractor type again")
        except Exception as e:
            st.error(f"❌ Failed to re-select contractor type: {e}")
            print(f"❌ Failed to re-select contractor type: {e}")

        time.sleep(delay_time)

        try:
            for box in page.locator("input").all():
                box.click(timeout=timeout_up)
            st.success("✅ Checked all news-related checkboxes")
            print("✅ Checked all news-related checkboxes")
        except Exception as e:
            st.error(f"❌ Failed to check checkboxes: {e}")
            print(f"❌ Failed to check checkboxes: {e}")

        try:
            page.click("button.next-button", timeout=timeout_up)
            st.success("✅ Clicked next after checkboxes")
            print("✅ Clicked next after checkboxes")
        except Exception as e:
            st.error(f"❌ Failed to click next after checkboxes: {e}")
            print(f"❌ Failed to click next after checkboxes: {e}")

        time.sleep(delay_time)

        try:
            page.fill('input[placeholder="https://..."]', website, timeout=timeout_up)
            st.success("✅ Entered website")
            print("✅ Entered website")
        except Exception as e:
            st.error(f"❌ Failed to enter website: {e}")
            print(f"❌ Failed to enter website: {e}")



        # page.fill('input[placeholder="name@email.com"]', e_mail, timeout=timeout_up)

        # time.sleep(delay_time)


        # page.fill('input[placeholder="Create a password"]', password, timeout=timeout_up)
        # print("✅ Entered email and password")
        # st.success("✅ Entered email and password")

        # time.sleep(delay_time)

        # page.click("button.email-password-form-submit", timeout=timeout_up)
        # print("✅ Clicked submit")
        # st.success("✅ Clicked submit")

        # time.sleep(delay_time)

        # page.select_option("select[ng-model='$ctrl.contractor.contractorTypeId']", value = "number:6", timeout=timeout_up)
        # print("✅ Selected 'Roofer'")
        # st.success("✅ Selected 'Roofer'")

        # page.wait_for_selector("div.icon-button-label", timeout=timeout_up)
        # for label in page.locator("div.icon-button-label").all():
        #     label.click(timeout=timeout_up)
        # print("✅ Selected all labels")
        # st.success("✅ Selected all labels")

        # time.sleep(delay_time)
        # page.click("button.next-button", timeout=timeout_up)
        # print("✅ Clicked 'Next'")
        # st.success("✅ Clicked 'Next'")

        # time.sleep(delay_time)
        # page.click("button.next-button", timeout=timeout_up)
        # st.success("✅ Clicked 'Next'")

        # page.fill("input[placeholder='Street address']", address, timeout=timeout_up)
        # st.success("✅ Entered address")

        # time.sleep(delay_time)
        # page.fill("input[placeholder='Zipcode']", zip_code, timeout=timeout_up)
        # st.success("✅ Entered Zipecode")

        # time.sleep(delay_time)
        # page.select_option('select.travel-range-input', "number:150", timeout=timeout_up)
        # st.success("✅ Travel range filled")

        # time.sleep(delay_time)
        # page.fill("input[placeholder='Mobile phone']", phone_number, timeout=timeout_up)
        # st.success("✅ Entered phone number")

        # page.click("button.next-button", timeout=timeout_up)
        # st.success("✅ Clicked 'Next' button")

        # time.sleep(delay_time)

        # page.select_option("select[ng-model='$ctrl.contractor.contractorTypeId']", "number:6", timeout=timeout_up)
        # st.success("✅ Choosed contractor type")
        # time.sleep(delay_time)

        # for box in page.locator("input").all():
        #     box.click(timeout=timeout_up)
        # print("✅ Checked all checkboxes related to the types of news you may want to receive")
        # st.success("✅ Checked all checkboxes related to the types of news you may want to receive")

        # page.click("button.next-button", timeout=timeout_up)

        # print("✅ Next button clicked")
        # st.success("✅ Next button clicked")

        # time.sleep(delay_time)

        # page.fill('input[placeholder="https://..."]', website, timeout=timeout_up)
        # st.success("✅ Filled in the website!")
        time.sleep(delay_time)
        checkboxes = page.locator('input').all()
        if len(checkboxes) > 1:
            checkboxes[1].click(timeout=timeout_up)
            print("✅ Checked the checkbox confirming you don't have a Facebook page to provide.")
            st.success("✅ Checked the checkbox confirming you don't have a Facebook page to provide.")

        page.click("button.next-button", timeout=timeout_up)
        print("✅ Click Next button")
        st.success("✅ Click Next button")

        time.sleep(delay_time)

        page.fill('input[placeholder="To agree, type your name here"]', signature, timeout=timeout_up)
        print("✅ Fill in Signature")
        st.success("✅ Fill in Signature")

        time.sleep(delay_time)

        page.click("button.next-button", timeout=timeout_up)

        print("✅ Click Next button")
        st.success("✅ Click Next button")

        checkboxes = page.locator('input').all()
        if checkboxes:
            checkboxes[-1].click(timeout=timeout_up)
            print("✅ Checked the checkbox confirming that you don't want to submit the license")
            st.success("✅ Checked the checkbox confirming that you don't want to submit the license")
        # Check if the password field is present
        password_input = page.locator("input[placeholder='Create a password']")
        if password_input.count() > 0 and password_input.first.is_visible():
            password_input.fill(password, timeout=timeout_up)
            print("✅ Filled in the password")
            st.success("✅ Filled in the password")
            time.sleep(delay_time)
        else:
            print("⚠️ Password field not found — skipping")
            st.error("⚠️ Password field not found — skipping")

        # Now check and click the final Next button if it's present
        done_button = page.locator("button.next-button")
        if done_button.count() > 0 and done_button.first.is_visible():
            done_button.click(timeout=timeout_up)
            print("🎉 Done submitting the form!")
            st.success("🎉 Done submitting the form!")
        else:
            print("⚠️ Final submit button not found")
            st.error("⚠️ Final submit button not found")

        time.sleep(15)
        browser.close()

# Usage




# BuildZoomListing_Bot()



st.set_page_config(page_title="BuildZoom Listing Bot", layout="centered")

# ---- Header Section ----
st.title("🤖 BuildZoom Listing Bot")
st.markdown("""
Welcome! This bot helps you automatically submit your business listing to **BuildZoom** using data from Google Drive. 
""")

st.markdown("---")


# ---- Trigger Bot Section ----
st.subheader("Run the BuildZoom Bot")
st.info("This will use the data from your Google Sheet to auto-fill the BuildZoom form.")

run_bot = st.button("Start Bot")

if run_bot:
    with st.spinner("Initializing bot and browser..."):
        try:
            buildzoom_signup()
            st.success("🎉 The form submission was completed successfully!")
        except Exception as e:
            st.error("❌ An error occurred while running the bot:")
            st.exception(e)

st.markdown("---")

# ---- Credits ----
st.caption("Built with ❤️ using Streamlit and Botasaurus")


