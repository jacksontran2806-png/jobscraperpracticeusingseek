import csv
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('https://www.seek.com.au/jobs?keywords=machine+learning&location=Australia&jobtype=intern')
        await page.wait_for_timeout(3000)
        jobs = await page.query_selector_all('[data-automation="normalJob"]')
        print(len(jobs))

        with open('jobs.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Company', 'Location', 'Salary'])

            for job in jobs:
                title = await job.query_selector('[data-automation="jobTitle"]')
                company = await job.query_selector('[data-automation="jobCompany"]')
                location = await job.query_selector('[data-automation="jobLocation"]')
                salary = await job.query_selector('[data-automation="jobSalary"]')

                title_text = await title.inner_text() if title else ''
                company_text = await company.inner_text() if company else ''
                location_text = await location.inner_text() if location else ''
                salary_text = await salary.inner_text() if salary else 'None'

                print(title_text)
                print(company_text)
                print(location_text)
                print(salary_text)
                print('---')

                writer.writerow([title_text, company_text, location_text, salary_text])

        await browser.close()

asyncio.run(main())


