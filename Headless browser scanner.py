from logging import exception

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

link = "https://moodle.zli.ch/course/section.php?id=30164"
 def get_links_from_page(link: str):
    # Number of links to extract from the page
    link_tree_width = 5000
    domain = link.replace("https://", "") # ".replace", so we can work with the link nomatter if the full link was given.

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

        browsercontext = browser.new_context()

        browsercontext.add_cookies([
            {
                "name": "MoodleSession",
                "value": "YOUR_TOKEN_HERE", # value is the session cookie
                "domain": domain, # Here given domain can be used
                "path": "/" # Path is always /
            }
        ])

    page = browsercontext.new_page()
    page.goto(f"https://{domain}") # Here we can add the https back in, because we know that it's not there anyway
    html_content = page.content()

    extracted_links = get_links(html_content)
    end_links = extracted_links
    for link in extracted_links:
        try:
            end_links.append(get_links(link))
        except Exception:
            pass

    # Printing the title and links
    print(f"Page Title: {page.title()}\nlinks: {end_links}")

    browser.close()