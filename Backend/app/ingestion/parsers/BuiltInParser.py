from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re



#NOTE: DO I NEED ALL THIS DATA?

class BuiltInParser:

    # Helper Function to compute time posted from job card (Ex. 2 hours ago, 54 seconds ago and then subtract that from current time)
    def parse_posted_time(self, posted_text: str | None):
        if not posted_text:
            return None

        text = posted_text.lower().strip()

        # BuiltIn sometimes says "Reposted"
        if "reposted" in text:
            return None

        # Find the number anywhere in the text
        match = re.search(r"\d+", text)

        if not match:
            return None

        value = int(match.group())

        now = datetime.now()

        if "second" in text:
            return now - timedelta(seconds=value)

        if "minute" in text:
            return now - timedelta(minutes=value)

        if "hour" in text:
            return now - timedelta(hours=value)

        if "day" in text:
            return now - timedelta(days=value)

        return None

    def parse(self, html: str) -> list[dict]:

        soup = BeautifulSoup(html, "html.parser")

        jobs = []

        # Each job card has data-id="job-card"
        job_cards = soup.select('[data-id="job-card"]')

        for card in job_cards:

            # Job title
            title_element = card.select_one('[data-id="job-card-title"]')

            # Company
            company_element = card.select_one('[data-id="company-title"]')

            # Job URL
            link_element = card.select_one('[data-id="job-card-title"]')

            # Location
            location_element = card.select_one(
                '.fa-location-dot'
            )

            # Date
            time_element = card.select_one('span.fs-xs.fw-bold.bg-gray-01')

            if location_element:
                location_container = location_element.parent.parent
                location = location_container.get_text(strip=True)
            else:
                location = None

            # Remote / onsite
            remote_element = card.select_one('.fa-house-building')

            if remote_element:
                remote_container = remote_element.parent.parent
                remote = remote_container.get_text(strip=True)
            else:
                remote = None

            # Salary
            salary_element = card.select_one('.fa-sack-dollar')

            if salary_element:
                salary_container = salary_element.parent.parent
                salary = salary_container.get_text(strip=True)
            else:
                salary = None

            # Experience level
            experience_element = card.select_one('.fa-trophy')

            if experience_element:
                experience_container = experience_element.parent.parent
                experience = experience_container.get_text(strip=True)
            else:
                experience = None

            # Time Posted
            if time_element:
                posted_text = time_element.get_text(strip=True)
            else:
                posted_text = None

            posted_at = self.parse_posted_time(posted_text)

            # Description
            description_element = card.select_one(
                '.collapse .fs-sm.fw-regular'
            )

            description = (
                description_element.get_text(strip=True)
                if description_element
                else None
            )

            logo_element = card.select_one('[data-id="company-img"]')

            company_logo = (
                logo_element.get("src")
                if logo_element
                else None
            )

            # Job ID
            job_id = card.get("id")

            jobs.append({
                "source":"builtin",
                "id": job_id,
                "title": (
                    title_element.get_text(strip=True)
                    if title_element
                    else None
                ),
                "company": (
                    company_element.get_text(strip=True)
                    if company_element
                    else None
                ),
                "company_logo": company_logo,
                "url": (
                    link_element.get("href")
                    if link_element
                    else None
                ),
                "location": location,
                "remote": remote,
                "salary": salary,
                "experience": experience,
                "description": description,
                "posted_at": posted_at,
            })

        return jobs