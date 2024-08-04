import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import urllib.parse

# Function to create the LinkedIn job search URL based on user input
def create_url(role, location):
    base_url = "https://www.linkedin.com/jobs/search/?"
    query_params = {
        "keywords": role,
        "location": location
    }
    query_string = urllib.parse.urlencode(query_params)
    return f"{base_url}{query_string}"

# Get the job role and location from the user
role = input("Enter the job role you want to search for: ")
location = input("Enter the location you want to search for: ")

# Create the URL for the LinkedIn job search page
url = create_url(role, location)

# Make a request to the LinkedIn job search page
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def make_request_with_retries(url, headers, max_retries=5):
    retries = 0
    while retries < max_retries:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response
        elif response.status_code == 429:
            retries += 1
            wait_time = 2 ** retries  # Exponential backoff
            print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            print(f"Failed to retrieve the web page. Status code: {response.status_code}")
            return None
    print("Max retries exceeded. Exiting.")
    return None

response = make_request_with_retries(url, headers)

if response:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Create empty lists for company name and job title
    companyname = []
    titlename = []
    linkname = []
    placename = []
    timedetail = []

    # Find job cards
    job_cards = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')

    # Extract company names, job titles, and job links
    for card in job_cards[:100]:  # scrape only 100 company details
        company = card.find('h4', class_='base-search-card__subtitle')
        title = card.find('h3', class_='base-search-card__title')
        link = card.find('a', class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]')
        place = card.find('span', class_='job-search-card__location')
        time = card.find('time', class_='job-search-card__listdate')

        if company and title and link and place and time:
            companyname.append(company.text.strip())
            titlename.append(title.text.strip())
            linkname.append(link['href'])
            placename.append(place.text.strip())
            timedetail.append(time['datetime'])

    # Create a DataFrame for company names and job titles
    job_details = pd.DataFrame({
        "company": companyname,
        "title": titlename,
        "link": linkname,
        "place": placename,
        "time": timedetail
    })

    # Save the DataFrame to a CSV file
    job_details.to_csv('linkedin_job_details.csv', index=False)

    print("Scraping completed and data saved to linkedin_job_details.csv")
