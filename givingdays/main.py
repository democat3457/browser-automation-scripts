import os
from playwright.sync_api import Playwright, sync_playwright, expect

from dotenv import load_dotenv
load_dotenv()

def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()
    times = 0
    try:
        while True:
            page = context.new_page()
            page.goto(
                "https://givingday.utdallas.edu/giving-day/99039/department/99132?utm_source=scalefunder&utm_campaign=amb_share&utm_content=7oq5ue7smqw2apqi640d04l&utm_medium=plain"
            )
            page.get_by_role("button", name="Give Now").click()
            page.get_by_role("spinbutton", name="Gift Amount").fill(os.environ.get("GD_DONATION_AMNT"))
            page.get_by_role("textbox", name="Email*").fill(os.environ.get("GD_EMAIL"))
            page.get_by_role("textbox", name="First Name*").fill(os.environ.get("GD_FIRSTNAME"))
            page.get_by_role("textbox", name="Last Name*").fill(os.environ.get("GD_LASTNAME"))
            page.get_by_role("textbox", name="Address 1*").fill(os.environ.get("GD_ADDRL1"))
            page.get_by_role("textbox", name="Address 2").fill(os.environ.get("GD_ADDRL2"))
            page.get_by_role("textbox", name="City*").fill(os.environ.get("GD_ADDRCITY"))
            page.get_by_label("State / Province / Region*").select_option(os.environ.get("GD_ADDRSTATE"))
            page.get_by_role("textbox", name="Zip / Postal Code*").fill(os.environ.get("GD_ADDRZIP"))
            page.get_by_role("textbox", name="Telephone*").fill(os.environ.get("GD_PHONE"))
            page.get_by_role("searchbox", name="Select options").click()
            page.get_by_role("option", name="Student").click()
            page.get_by_role("textbox", name="What inspires you to give to").fill(os.environ.get("GD_INSPIRE"))
            page.locator("#select2-19209-container").click()
            page.get_by_role("option", name="No", exact=True).click()
            page.get_by_role("button", name="Give Now").click()
            page.locator("#bbcheckout-iframe").content_frame.get_by_role(
                "textbox", name="Card number"
            ).fill(os.environ.get("GD_PAY_CARDNO"))
            page.locator("#bbcheckout-iframe").content_frame.get_by_role(
                "textbox", name="Expiry"
            ).fill(os.environ.get("GD_PAY_EXPIRY"))
            page.locator("#bbcheckout-iframe").content_frame.get_by_role(
                "textbox", name="CSC"
            ).fill(os.environ.get("GD_PAY_CSC"))
            # page.locator("#bbcheckout-iframe").content_frame.get_by_role(
            #     "button", name="Finish and pay"
            # ).click()
            expect(page.get_by_text("THANK YOU FOR YOUR DONATION!")).to_be_visible(timeout=15_000)
            page.close()
            times += 1
            print("# of Donations:", times)
    except KeyboardInterrupt:
        pass

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
