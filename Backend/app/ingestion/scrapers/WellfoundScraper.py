from playwright.async_api import async_playwright


class WellfoundScraper:

    BASE_URL = "https://wellfound.com"

    def __init__(self, headless=True):
        self.headless = headless

    async def fetch_page(self, url: str) -> str:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=self.headless
            )

            page = await browser.new_page()

            await page.goto(
                url,
                wait_until="domcontentloaded"
            )

            await page.wait_for_timeout(2000)

            html = await page.content()

            await browser.close()

            return html

    # NOTE: This is only filtering Canada jobs,
    # would need to supplement in location + need filters
    # to change output later
    async def fetch_jobs_page(self) -> str:
        url = f"{self.BASE_URL}/location/canada-startups"
        return await self.fetch_page(url)