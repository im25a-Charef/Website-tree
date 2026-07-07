from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

link = "youtube.com"
link_tree_width = 5000


def get_links(html):
    """Extracts links from the HTML content."""
    # soup used as an easy HTML extractor
    soup = BeautifulSoup(html, "html.parser")
    links = []

    # anchor as in <a href="...">...</a>, we extract the href attribute
    for iterations, anchor in enumerate(soup.find_all("a", href=True), start=1):
        # we use pythons enumerate with the variable
        # iterations to limit the number of links we extract with the link_tree_width variable
        links.append(anchor['href'])

        if iterations == link_tree_width:
            break
    return links


def get_links_from_page(browsercontext, link: str):
    # Number of links to extract from the page

    domain = link.replace("https://", "").split("/")[
        0]  # ".replace", so we can work with the link nomatter if the full link was given.

    try:
        page = browsercontext.new_page()
        page.goto(f"https://{domain}")  # Here we can add the https back in, because we know that it's not there anyway
        html_content = page.content()

        extracted_links = get_links(html_content)
        page.close()
        return extracted_links
    except Exception:
        return []


def main():
    initial_domain = link.replace("https://", "").split("/")[0]

    # Launching the browser
    with sync_playwright() as p:
        # We make it headless for speed and to make it seem less cluncky
        browser = p.chromium.launch(headless=True)

        browsercontext = browser.new_context()

        browsercontext.add_cookies([
            {
                "name": "MoodleSession",
                "value": os.getenv("SESSION_TOKEN"),  # value is the session cookie
                "domain": initial_domain,  # Here given domain can be used
                "path": "/"  # Path is always /
            }
        ])

        gather_count = 1

        extracted_links = get_links_from_page(browsercontext, link)

        end_links = [[gather_count, list(extracted_links)]]

        for target_link in extracted_links:
            if target_link.startswith("http"):
                try:
                    new_links = get_links_from_page(browsercontext, target_link)
                    if new_links:
                        gather_count += 1
                        end_links.append([gather_count, new_links])
                except Exception:
                    pass

        browser.close()

    print(f"links: {end_links}")


if __name__ == "__main__":
    main()