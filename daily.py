import os
import datetime
from playwright.sync_api import sync_playwright

# Define the start and end dates
start_date = datetime.date(2023, 3, 18)
end_date = datetime.date(2024, 5, 1)

# Directory to save screenshots
output_dir = "screenshots"
os.makedirs(output_dir, exist_ok=True)

# Main script
with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False
    )  # Set headless to False to see the browser actions
    page = browser.new_page()

    # Navigate to the base URL
    page.goto("https://www.ventusky.com/?p=42.47;1.37;7&l=snow")

    current_date = start_date
    while current_date <= end_date:
        try:
            # Click on the "Change date" button
            page.click("text=Change date")
            page.wait_for_timeout(1000)

            # Change the year
            page.select_option("#l", str(current_date.year))
            page.wait_for_timeout(1000)

            # Change the month
            page.select_option(
                "#h", str(current_date.month - 1)
            )  # Month is 0-indexed in the select element
            page.wait_for_timeout(1000)

            # Click on the correct day
            day_selector = f"td >> text={current_date.day}"
            page.click(day_selector)
            page.wait_for_timeout(1000)

            # Wait for the page to update (adjust the waiting time if necessary)
            page.wait_for_timeout(3000)

            # Take screenshot
            screenshot_path = os.path.join(
                output_dir, f"{current_date.strftime('%Y%m%d')}.png"
            )
            page.screenshot(path=screenshot_path)
            print(
                f"Saved screenshot for {current_date.strftime('%Y-%m-%d')} to {screenshot_path}"
            )
            page.click("text=Change date")

            # Move to the next day
            current_date += datetime.timedelta(days=1)

        except Exception as e:
            print(f"Error on {current_date}: {e}")
            # Move to the next day even if there's an error
            current_date += datetime.timedelta(days=1)

    browser.close()
