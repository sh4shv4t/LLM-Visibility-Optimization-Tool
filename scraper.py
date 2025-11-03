from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import sys

def scrape_to_markdown(url_to_scrape, markdown_filepath="scraped_content.md"):
    """
    Scrapes a website's main content *after* JavaScript has loaded,
    and saves it as a Markdown file.

    Args:
        url_to_scrape (str): The full URL of the website to scrape.
        markdown_filepath (str): The name of the file to save the content to.
    """
    print(f"Attempting to scrape with Playwright: {url_to_scrape}")

    try:
        with sync_playwright() as p:
            
            browser = p.chromium.launch(headless=True)
            
            page = browser.new_page()

            print("Navigating to page...")
            page.goto(url_to_scrape, wait_until='networkidle', timeout=15000)
            
            print("Page loaded, getting content...")
            html_content = page.content()

            browser.close()

            soup = BeautifulSoup(html_content, 'html.parser')

            print("Converting entire HTML content to Markdown.")
            markdown_text = md(str(soup))

            with open(markdown_filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_text)

            print(f"Successfully scraped content and saved to {markdown_filepath}")

    except Exception as e:
        if "timeout" in str(e).lower():
            print(f"Timeout Error: The page took too long to load: {e}")
        else:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
        
        scrape_to_markdown(target_url, markdown_filepath="scraped_content.md")
    else:
        print("Please provide a URL to scrape.")
        print("Example: python scraper.py \"https://some-javascript-heavy-site.com\"")

