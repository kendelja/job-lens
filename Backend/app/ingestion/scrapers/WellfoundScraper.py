from playwright.sync_api import sync_playwright


class WellfoundScraper:

    BASE_URL = "https://wellfound.com"

    def __init__(self, headless=True):
        self.headless = headless

    def fetch_page(self, url: str) -> str:
        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=self.headless
            )

            page = browser.new_page()

            page.goto(
                url,
                wait_until="domcontentloaded"
            )

            page.wait_for_timeout(2000)

            html = page.content()

            browser.close()

            return html
    #NOTE: This is only filtering canada jobs, would need to supplement in location + need filters to change output later 
    def fetch_jobs_page(self) -> str:
        url = f"{self.BASE_URL}/location/canada-startups"

        return self.fetch_page(url)