from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://www.youtube.com/")
    print("Page Title:", page.title())

    page.screenshot(path="example.png")

    browser.close()