const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const csvWriter = require('csv-writer').createObjectCsvWriter;

// Define the URL for the LinkedIn job search page
const url = "https://www.linkedin.com/jobs/search/?keywords=full%20stack%20developer";

(async () => {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    // Set the User-Agent to mimic a real browser
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36");

    // Navigate to the LinkedIn job search page
    await page.goto(url, { waitUntil: 'networkidle2' });

    // Scrape job details
    const jobDetails = await page.evaluate(() => {
        const jobCards = document.querySelectorAll('div.base-card.relative.w-full.hover\\:no-underline.focus\\:no-underline.base-card--link.base-search-card.base-search-card--link.job-search-card');
        const jobs = [];

        jobCards.forEach((card, index) => {
            if (index < 100) { // scrape only 30 job details
                const company = card.querySelector('h4.base-search-card__subtitle')?.innerText.trim();
                const title = card.querySelector('h3.base-search-card__title')?.innerText.trim();
                const link = card.querySelector('a.base-card__full-link')?.href;
                const place = card.querySelector('span.job-search-card__location')?.innerText.trim();
                const time = card.querySelector('time.job-search-card__listdate')?.getAttribute('datetime');
                if (company && title && link && place && time) {
                    jobs.push({ company, title, link, place, time });
                }
            }
        });

        return jobs;
    });

    // Close the browser
    await browser.close();

    // Define the CSV writer
    const writer = csvWriter({
        path: path.join(__dirname, 'linkedin_job_details10.csv'),
        header: [
            { id: 'company', title: 'Company' },
            { id: 'title', title: 'Title' },
            { id: 'link', title: 'Link' },
            { id: 'place', title: 'Place' },
            { id: 'time', title: 'Time' }
        ]
    });

    // Write the job details to a CSV file
    await writer.writeRecords(jobDetails);

    console.log("Scraping completed and data saved to linkedin_job_details10.csv");
})();