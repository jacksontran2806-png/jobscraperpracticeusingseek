import csv
import asyncio
from playwright.async_api import async_playwright


async def main():
    # 1. Read existing CSV
    jobs = []
    with open('jobs.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            jobs.append(row)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 2. Loop through jobs
        for job in jobs:
            url = job['URL']

            if not url:
                job['Description'] = ''
                continue

            await page.goto(url)
            await page.wait_for_timeout(3000)

            # 3. Extract description
            desc = await page.query_selector('[data-automation="jobAdDetails"]')
            desc_text = await desc.inner_text() if desc else ''

            job['Description'] = desc_text

            print(job['Title'])
            print(url)
            print('---')

            # 4. Delay (important)
            await asyncio.sleep(2)

        await browser.close()

    # 5. Save new CSV (don’t overwrite original)
    with open('jobs_with_desc.csv', 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['Title', 'Company', 'Location', 'Salary', 'URL', 'Description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(jobs)


asyncio.run(main())