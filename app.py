from botasaurus.browser import Driver, browser, Wait
from botasaurus.request import request, Request
from botasaurus.lang import Lang
import time
from botasaurus.soupify import soupify
import re
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd
import io
from googleapiclient.http import MediaIoBaseDownload
import os




GOOGLE_DRIVE_FOLDER_KEY = "1EI-LPywNMutSiS0Rm-fZ-PO3TOkfuPnc0ZfnLVeUnqY"



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




@browser(
    headless = True, 
    lang=Lang.English,
    max_retry=5,
    reuse_driver=True,
    # block_images_and_css=True,
    retry_wait=10,
    create_error_logs=False,
    output=None,
)
def BuildZoomListing_Bot(driver: Driver, data):
    wait_time = 15
    delay_time = 2
    name = ""
    address = ""
    phone_number = ""
    website = ""
    e_mail = ""
    password = ""
    zipe_code = ""
    signature = ""
    
    aut_status = False

    MAIN_URL = "https://www.buildzoom.com/user/sign_in"

    driver.google_get(MAIN_URL, bypass_cloudflare=True)

    data = google_drive_operation()
    if data:
        name = data['Name']
        address = data['Address']
        phone_number = data['Phone']
        website = data['Website']
        signature = data["Signature"]
    else:
        print("Something went wrong while pulling data from the Google Sheet.")

    if address:
        zipe_code = extract_zip_code(address)


    driver.sleep(delay_time)

    driver.enable_human_mode()

    try:
        sign_in_sign_up = driver.select_all("div.email-password-form-action", wait=wait_time)
        if sign_in_sign_up:
            sign_in_sign_up[-1].select("a").click()
            print("✅ Clicked the 'Sign up.' or 'Sing in' link.")
        else:
            print(f"❌ Failed to find 'Sign up.' or 'Sign in'")
    except Exception as e:
        print(f"❌ Failed to click 'Sign up.' or 'Sign in': {e}")

    driver.sleep(delay_time)

    try:
        contractor_tabs = driver.select_all("li.auth-screen-nav-item", wait=wait_time)
   
        if contractor_tabs:
            contractor_tabs[-1].click()
            print("✅ Clicked 'Contractor' tab.")
        else:
            print("❌ Contractor tab not found in list.")
    except Exception as e:
        print(f"❌ Error selecting 'Contractor' tab: {e}")


    driver.sleep(delay_time)
    try:
        driver.type('input[placeholder="e.g. ABC Flooring"]', name, wait=wait_time)
        print("✅ Typed 'Best Rate Roofing of Fullerton' into the business name field.")
    except Exception as e:
        print(f"❌ Error typing into the input field: {e}")
        return
    

    driver.sleep(delay_time)    
    try:
        add_business_link = driver.select('a.claim-business-add-prompt-link', wait=wait_time)
        if add_business_link:
            add_business_link.click()
            print("✅ Clicked '+ Add your business to BuildZoom' link.")
        else:
            print("⚠️ '+ Add your business' link not found.")
    except Exception as e:
        print(f"❌ Error clicking 'Add your business' link: {e}")

    driver.sleep(delay_time)

 # Type email
    try:
        driver.type('input[placeholder="name@email.com"]', e_mail, wait=wait_time)
        print("✅ Entered email.")
    except Exception as e:
        print(f"❌ Error typing email: {e}")
        return
    

    driver.sleep(delay_time)

    try:
        driver.type('input[placeholder="Create a password"]', password, wait=wait_time)
        print("✅ Entered password.")
    except Exception as e:
        print(f"❌ Error typing password: {e}")
        return

    driver.sleep(delay_time)

   #Click the 'Submit' button
    try:
        submit_btn = driver.select('button.email-password-form-submit', wait=wait_time)
        if submit_btn:
            submit_btn.click()
            print("✅ Clicked the 'Submit' button.")
        else:
            print("❌ 'Submit' button not found.")
    except Exception as e:
        print(f"❌ Error clicking 'Submit' button: {e}")

    driver.sleep(delay_time)

    try:
        driver.select_option("select[ng-model='$ctrl.contractor.contractorTypeId']", value="number:6", wait=wait_time)
        print("✅ Selected 'Roofer' from dropdown.")
    except Exception as e:
        print(f"❌ Failed to select 'Roofer': {e}")


    # driver.sleep(5)
    driver.sleep(delay_time)
    try:
        labels_div = driver.select_all("div.icon-button-label", wait=wait_time)
        if labels_div:
            for option in labels_div:
                option.click()

        print("✅ Select  all contract type label")
    except Exception as e:
        print(f"❌ Failed to select labels : {e}")

    driver.sleep(delay_time)

    try:
        next_button = driver.select("button.next-button.v3-button.v3-solid-light-blue-button.v3-square-button", wait=wait_time)
        next_button.click()
        print("✅ Clicked the 'Next' button.")
    except Exception as e:
        print(f"❌ Failed to click the 'Next' button: {e}")


    driver.sleep(delay_time)

    try:
        next_button = driver.select("button.next-button.v3-button.v3-solid-light-blue-button.v3-square-button", wait=wait_time)
        next_button.click()
        print("✅ Clicked the 'Next' button.")
    except Exception as e:
        print(f"❌ Failed to click the 'Next' button: {e}")


    # driver.sleep(8)
    driver.sleep(delay_time)

    try:
        driver.type(
            'input[placeholder="Street address"]',
            address,
            wait=wait_time
        )
        print("✅ Entered street address.")
    except Exception as e:
        print(f"❌ Failed to enter street address: {e}")


    # driver.sleep(5)
    driver.sleep(delay_time)


    try:
        driver.type(
            'input[placeholder="Zipcode"]',
            zipe_code,
            wait=wait_time
        )
        print("✅ Entered ZIP code.")
    except Exception as e:
        print(f"❌ Failed to enter ZIP code: {e}")



    # driver.sleep(8)
    driver.sleep(delay_time)

    try:
        driver.select_option('select.travel-range-input', value="number:150", wait=wait_time)
        print(f"✅ Selected '150 miles' from travel range dropdown.")
    except Exception as e:
        print(f"❌ Failed to select travel range: {e}")


    # driver.sleep(8)
    driver.sleep(delay_time)

    try:
        driver.type("input[placeholder='Mobile phone']", phone_number, wait=wait_time)
        print("✅ Entered phone number successfully.")
    except Exception as e:
        print(f"❌ Failed to input phone number: {e}")



    # driver.sleep(10)
    driver.sleep(delay_time)

    try:
        next_button = driver.select("button.next-button.v3-button.v3-solid-light-blue-button.v3-square-button", wait=wait_time)
        next_button.click()
        print("✅ Clicked the 'Next' button.")
    except Exception as e:
        print(f"❌ Failed to click the 'Next' button: {e}")


    driver.sleep(delay_time)


    try:
        driver.select_option("select[ng-model='$ctrl.contractor.contractorTypeId']", value="number:6", wait=wait_time)

        print("✅ Selected 'Roofer' from contractor type dropdown.")
    except Exception as e:
        print(f"❌ Failed to select 'Roofer': {e}")

    # driver.sleep(5)
    driver.sleep(delay_time)

    try:
        # Select all project type checkboxes
        checkboxes = driver.select_all("input", wait=wait_time)

        for checkbox in checkboxes:
            # if not checkbox.is_selected():
            checkbox.click()

        print(f"✅ Checked all project type options ({len(checkboxes)} total).")
    except Exception as e:
        print(f"❌ Failed to check all project types: {e}")


    driver.sleep(delay_time)

    # driver.sleep(10)

    try:
        next_button = driver.select("button.next-button.v3-button.v3-solid-light-blue-button.v3-square-button", wait=wait_time)
        next_button.click()
        print("✅ Clicked the 'Next' button.")
    except Exception as e:
        print(f"❌ Failed to click the 'Next' button: {e}")


    # driver.sleep(8)

    driver.sleep(delay_time)

    # Input Website URL
    try:
        website_input = driver.select('input[placeholder="https://..."]', wait=wait_time)
        if website_input:
            website_input.clear()
            website_input.type(website, wait=wait_time)
            print("✅ Successfully inputted the website URL.")
        else:
            print("❌ Website input field not found.")
    except Exception as e:
        print(f"❌ Failed to input website URL: {e}")

    # driver.sleep(8)
    driver.sleep(delay_time)
    # Check the "No Website" checkbox
    try:
        checkbox = driver.select_all('input', wait=wait_time)
        if checkbox:
            checkbox[1].click()
            print("✅ 'No Website' checkbox checked.")
        elif checkbox:
            print("✅ 'No Website' checkbox was already checked.")
        else:
            print("❌ 'No Website' checkbox not found.")
    except Exception as e:
        print(f"❌ Failed to check 'No Website' checkbox: {e}")

    # driver.sleep(5)
    driver.sleep(delay_time)


    try:
        next_button = driver.select("button.next-button.v3-button.v3-solid-light-blue-button.v3-square-button", wait=wait_time)
        next_button.click()
        print("✅ Clicked the 'Next' button.")
    except Exception as e:
        print(f"❌ Failed to click the 'Next' button: {e}")

    # driver.sleep(5)
    driver.sleep(delay_time)

    # Type "TATA" into the signature input
    try:
        driver.type('input[placeholder="To agree, type your name here"]', signature, wait=wait_time)
        print("✅ Entered 'TATA' into the signature field.")
    except Exception as e:
        print(f"❌ Failed to enter signature: {e}")

    # driver.sleep(5)
    driver.sleep(delay_time)

    try:
        next_button = driver.select("button.next-button.v3-button.v3-solid-light-blue-button.v3-square-button", wait=wait_time)
        next_button.click()
        print("✅ Clicked the 'Next' button.")
    except Exception as e:
        print(f"❌ Failed to click the 'Next' button: {e}")



    # driver.sleep(5)
    driver.sleep(delay_time)

    # Check the "License not needed" checkbox
    try:
        checkbox = driver.select_all('input', wait=wait_time)
        if checkbox:
            checkbox[-1].click()
            print("✅ Checked 'License not needed' checkbox.")
        else:
            print("⚠️ Checkbox already checked or not found.")
    except Exception as e:
        print(f"❌ Failed to check 'License not needed' checkbox: {e}")

    driver.sleep(delay_time)




    # driver.sleep(5)

    # Click the final "Done" button
    try:
        done_button = driver.select(
            'button.next-button.v3-button.v3-solid-light-blue-button.v3-square-button',
            wait=wait_time
        )
        if done_button:
            done_button.click()
            print("✅ Clicked the final 'Done' button.")
        else:
            print("❌ Final 'Done' button not found.")
    except Exception as e:
        print(f"❌ Failed to click the final 'Done' button: {e}")

    # driver.sleep(8)
    driver.sleep(delay_time)

    try:
        driver.type("input[placeholder='Create a password']", password, wait=wait_time)
        print("✅ Successfully entered password.")
    except Exception as e:
        print(f"❌ Failed to enter password: {e}")

    driver.sleep(delay_time)

    try:
        driver.click("button.next-button", wait=wait_time)
        
        print("✅ Clicked the 'done' button.")
        aut_status = True
    except Exception as e:
        print(f"❌ Failed to click 'done' button: {e}")

    # driver.sleep(25)
    driver.sleep(delay_time)

    # driver.sleep(20)
    print("🎉 Form submission process completed!")

 







  


# BuildZoomListing_Bot()

import streamlit as st
import time
from PIL import Image
import os

st.set_page_config(page_title="BuildZoom Listing Bot", layout="centered")

# ---- Header Section ----
st.title("🤖 BuildZoom Listing Bot")
st.markdown("""
Welcome! This bot helps you automatically submit your business listing to **BuildZoom** using data from Google Drive. 
""")

st.markdown("---")

# ---- Load Image Preview ----
# st.subheader("📸 Google Drive Logo Images")
# st.markdown("---")

# ---- Trigger Bot Section ----
st.subheader("Run the BuildZoom Bot")
st.info("This will use the data from your Google Sheet to auto-fill the BuildZoom form.")

run_bot = st.button("Start Bot")

if run_bot:
    with st.spinner("Initializing bot and browser..."):
        try:
            BuildZoomListing_Bot()
            st.success("🎉 The form submission was completed successfully!")
        except Exception as e:
            st.error("❌ An error occurred while running the bot:")
            st.exception(e)

st.markdown("---")

# ---- Credits ----
st.caption("Built with ❤️ using Streamlit and Botasaurus")


