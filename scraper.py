import csv
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        with open('jobs.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Company', 'Location', 'Salary'])
            seen_jobs = set()
            for page_num in range(1, 6):
                await page.goto(f'https://au.seek.com/machine-learning-graduate-jobs?page={page_num}')
                await page.wait_for_timeout(3000)
                jobs = await page.query_selector_all('[data-automation="normalJob"]')             
                print(len(jobs))
                
                for job in jobs:
                        
                        title = await job.query_selector('[data-automation="jobTitle"]')
                        company = await job.query_selector('[data-automation="jobCompany"]')
                        location = await job.query_selector('[data-automation="jobLocation"]')
                        salary = await job.query_selector('[data-automation="jobSalary"]')

                        title_text = await title.inner_text() if title else ''
                        company_text = await company.inner_text() if company else ''
                        location_text = await location.inner_text() if location else ''
                        salary_text = await salary.inner_text() if salary else 'Not listed'

                        
                        job_key = (title_text, company_text, location_text)
                        if job_key in seen_jobs:
                            continue
                        seen_jobs.add(job_key)

                        print(title_text)
                        print(company_text)
                        print(location_text)
                        print(salary_text)
                        print('---')

                        writer.writerow([title_text, company_text, location_text, salary_text])

            await browser.close()

asyncio.run(main())


