import requests
import json

# Replace with your actual API key
api_key = 'eyJhbGciOiJFZERTQSIsImtpZCI6IjcyNWM2M2I2LTcwMGUtNTQzZi0wNDg2LTgyYTFlZDMxNzBlZiJ9.eyJhdWQiOiJrb25ndSIsImV4cCI6MTczNTEyMDYwNywiaWF0IjoxNzAzNTYzNjU1LCJpc3MiOiJodHRwczovL29wcy5jb3Jlc2lnbmFsLmNvbTo4MzAwL3YxL2lkZW50aXR5L29pZGMiLCJuYW1lc3BhY2UiOiJyb290IiwicHJlZmVycmVkX3VzZXJuYW1lIjoia29uZ3UiLCJzdWIiOiJmYTBjNGM5Yy1jMjFjLWZmZGYtYzBiOS00OGFlZDVhZjljMTYiLCJ1c2VyaW5mbyI6eyJzY29wZXMiOiJjZGFwaSJ9fQ.YAfY7_T_ejlLz1YQFTSPB7K59XcxZTv5ZLJRTIR0E3bwTlPaFr41MlI13wwEZXLmFRtWiCpieJQviPzCyIUvBA'

# Define the headers
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

# Define the URL for the POST request
post_url = "https://api.coresignal.com/cdapi/v1/linkedin/job/search/filter"

# Define the payload for the POST request
payload = {
    "title": "(Full Stack Developer) OR (Data Scientist)",
    "application_active": "False",
    "country": "India"
}

# Make the POST request to get job IDs
response = requests.post(post_url, headers=headers, json=payload)

if response.status_code == 200:
    job_ids = response.json()
    print(f"Job IDs: {job_ids}")
else:
    print(f'Error: {response.status_code} - {response.text}')
    exit()

# List to hold detailed job information
job_details = []
count=0
# Fetch details for each job ID
for job_id in job_ids:
    if (count<10):
        job_detail_url = f"https://api.coresignal.com/cdapi/v1/linkedin/job/collect/{job_id}"
        response = requests.get(job_detail_url, headers=headers)
        if response.status_code == 200:
            job_data = response.json()
            job_details.append(job_data)
        else:
            print(f'Error retrieving job ID {job_id}: {response.status_code} - {response.text}')
        count+=1

# Save the job details to a JSON file
with open('job_details.json', 'w') as f:
    json.dump(job_details, f, indent=4)

print("Job details saved to job_details.json")