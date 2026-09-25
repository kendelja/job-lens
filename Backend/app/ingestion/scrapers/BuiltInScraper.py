from playwright.async_api import async_playwright


class BuiltInScraper:
    BASE_URL = "https://builtin.com"

    def __init__(self, headless=True, pages=3):
        self.headless = headless
        self.pages = pages

    async def fetch_page(self, url: str) -> str:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)

            page = await browser.new_page()

            await page.goto(url, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)

            html = await page.content()

            await browser.close()

            return html

    async def fetch_jobs_page(self) -> str:
        pages = []

        for page_number in range(1, self.pages + 1):
            if page_number == 1:
                url = f"{self.BASE_URL}/jobs"
            else:
                url = f"{self.BASE_URL}/jobs?page={page_number}"

            print(f"Fetching Built In page {page_number}...")

            html = await self.fetch_page(url)

            pages.append(html)

        return "\n".join(pages)