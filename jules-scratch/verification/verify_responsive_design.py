import os
from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = f"file://{os.path.join(base_dir, 'index.html')}"

        page.goto(file_path)

        # --- Test Desktop View ---
        page.set_viewport_size({"width": 1280, "height": 800})
        page.wait_for_timeout(1000) # Wait for render
        page.screenshot(path="jules-scratch/verification/desktop_view.png")

        # --- Test Mobile View ---
        page.set_viewport_size({"width": 375, "height": 812}) # iPhone X
        page.wait_for_timeout(1000) # Wait for render
        page.screenshot(path="jules-scratch/verification/mobile_view.png")

        # --- Functional Test ---
        birth_date_to_test = "2000-01-01"
        expected_age = "25歳"

        birth_date_input = page.locator("#birth-date-input")
        birth_date_input.fill(birth_date_to_test)

        age_result_locator = page.locator("#age-result")
        expect(age_result_locator).to_have_text(expected_age)

        print("Verification screenshots saved.")
        browser.close()

if __name__ == "__main__":
    run_verification()
