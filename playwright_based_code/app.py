
import time
import re
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd
import io
from googleapiclient.http import MediaIoBaseDownload
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

        page.goto("https://www.buildzoom.com/user/sign_in")
        time.sleep(delay_time)

        try:
            page.locator("div.email-password-form-action a").last.click()
            print("✅ Clicked 'Sign up' link")
        except Exception as e:
            print(f"❌ Could not click 'Sign up' link: {e}")

        time.sleep(delay_time)

        try:
            page.locator("li.auth-screen-nav-item").last.click()
            print("✅ Clicked 'Contractor' tab")
        except Exception as e:
            print(f"❌ Could not click 'Contractor' tab: {e}")

        time.sleep(delay_time)

        try:
            page.fill('input[placeholder="e.g. ABC Flooring"]', name)
            print("✅ Filled business name")
        except Exception as e:
            print(f"❌ Failed to fill business name: {e}")

        time.sleep(delay_time)

        try:
            page.click("a.claim-business-add-prompt-link")
            print("✅ Clicked '+ Add your business'")
        except Exception as e:
            print(f"❌ Failed to click add business: {e}")

        time.sleep(delay_time)

        page.fill('input[placeholder="name@email.com"]', e_mail)
        page.fill('input[placeholder="Create a password"]', password)
        print("✅ Entered email and password")

        time.sleep(delay_time)

        page.click("button.email-password-form-submit")
        print("✅ Clicked submit")

        time.sleep(delay_time)

        page.select_option("select[ng-model='$ctrl.contractor.contractorTypeId']", value = "number:6")
        print("✅ Selected 'Roofer'")

        for label in page.locator("div.icon-button-label").all():
            label.click()
        print("✅ Selected all labels")

        time.sleep(delay_time)
        page.click("button.next-button")
        print("✅ Clicked 'Next'")

        time.sleep(delay_time)
        page.click("button.next-button")

        page.fill("input[placeholder='Street address']", address)
        time.sleep(delay_time)
        page.fill("input[placeholder='Zipcode']", zip_code)
        time.sleep(delay_time)
        page.select_option('select.travel-range-input', "number:150")
        time.sleep(delay_time)
        page.fill("input[placeholder='Mobile phone']", phone_number)

        page.click("button.next-button")

        time.sleep(delay_time)

        page.select_option("select[ng-model='$ctrl.contractor.contractorTypeId']", "number:6")
        time.sleep(delay_time)

        for box in page.locator("input").all():
            box.click()
        print("✅ Checked all checkboxes")

        page.click("button.next-button")
        time.sleep(delay_time)

        page.fill('input[placeholder="https://..."]', website)
        time.sleep(delay_time)
        checkboxes = page.locator('input').all()
        if len(checkboxes) > 1:
            checkboxes[1].click()

        page.click("button.next-button")
        time.sleep(delay_time)
        page.fill('input[placeholder="To agree, type your name here"]', signature)
        page.click("button.next-button")

        checkboxes = page.locator('input').all()
        if checkboxes:
            checkboxes[-1].click()

        page.click("button.next-button")
        time.sleep(delay_time)
        page.fill("input[placeholder='Create a password']", password)
        time.sleep(delay_time)
        page.click("button.next-button")
        time.sleep(delay_time)
        print("🎉 Done submitting the form!")
        browser.close()

# Usage
buildzoom_signup()
