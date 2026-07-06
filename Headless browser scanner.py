from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def get_links(html):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for anchor in soup.find_all("a", href=True):
        links.append(anchor['href'])
    return links

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://en.wikipedia.org/wiki/Main_Page")
    html_content = page.content()
    extracted_links = get_links(html_content)
    print(f"Page Title: {page.title()}\nlinks: {extracted_links}")

    page.screenshot(path="example.png")

    browser.close()