from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# Number of links to extract from the page
link_tree_width = 5

def get_links(html):
    """Extracts links from the HTML content."""
    # soup used as an easy HTML extractor
    soup = BeautifulSoup(html, "html.parser")
    links = []

    #anchor as in <a href="...">...</a>, we extract the href attribute
    for iterations, anchor in enumerate(soup.find_all("a", href=True), start=1):
        # we use pythons enumerate with the variable
        # iterations to limit the number of links we extract with the link_tree_width variable
        links.append(anchor['href'])


        if iterations == link_tree_width:
            break
    return links

# Launching the browser
with sync_playwright() as p:
    # We make it headless for speed and to make it seem less cluncky
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Example of a wikipedia page
    page.goto("https://en.wikipedia.org/wiki/Main_Page")
    html_content = page.content()
    extracted_links = get_links(html_content)

    # Printing the title and links
    print(f"Page Title: {page.title()}\nlinks: {extracted_links}")

    page.screenshot(path="example.png")

    browser.close()