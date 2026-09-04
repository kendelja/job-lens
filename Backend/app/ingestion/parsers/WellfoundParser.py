from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re



#NOTE: DO I NEED ALL THIS DATA?

class WellfoundParser:

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
        job_cards = soup.select('div.mb-6.w-full.rounded.border.border-gray-400.bg-white')

        for card in job_cards:

            # Job title
            title_element = card.select_one('.mr-2.text-sm.font-semibold.text-brand-burgandy.hover\\:underline')

            # Company
            company_element = card.select_one('.text-neutral-1000.hover\\:underline.focus\\:no-underline')

            # Job URL
            link_element = card.select_one('.mr-2.text-sm.font-semibold.text-brand-burgandy.hover\\:underline')

            # Date
            time_element = card.select_one('.text-xs.lowercase.text-dark-a.md\\:hidden')

            # Location + Remote handling
            location_element = card.select_one(".pl-1.text-xs")

            if location_element:
                location_text = location_element.get_text(" ", strip=True)
            else:
                location_text = None

            if location_text:
                if "Remote only" in location_text:
                    remote_type = "Remote only"
                    location = location_text.replace("Remote only • ", "")
                
                elif "Remote" in location_text:
                    remote_type = "Remote"
                    location = location_text.replace("Remote • ", "")
                
                else:
                    remote_type = None
                    location = location_text
            else:
                remote_type = None
                location = None

            # # Remote / onsite
            # remote_element = card.select_one('.fa-house-building')

            # if remote_element:
            #     remote_container = remote_element.parent.parent
            #     remote = remote_container.get_text(strip=True)
            # else:
            #     remote = None

            # Salary
            salary_element = card.find("span",class_="pl-1 text-xs",string=re.compile(r"\$"))

            if salary_element:
                salary = salary_element.get_text(strip=True)
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

            logo_element = card.select_one('.flex.h-14.w-14.justify-center.overflow-hidden.rounded-2xl.border.border-gray-400.bg-gray-100 img')

            if logo_element:
                logo_src = logo_element.get("src")

                if logo_src and "https://" in logo_src:
                    company_logo = "https://" + logo_src.split("https://", 1)[1]
                else:
                    company_logo = logo_src
            else:
                company_logo = None

            # Job ID
            job_id = card.get("id")

            jobs.append({
                "source":"wellfound",
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
                "remote": remote_type,
                "salary": salary,
                "experience": experience,
                "description": description,
                "posted_at": posted_at,
            })

        return jobs