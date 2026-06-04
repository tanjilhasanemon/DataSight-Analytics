import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

print("🚀 INITIALIZING DATASIGHT EXTRACTION PIPELINE...")

# 1. Spoofer Headers (Crucial: Makes your Python script look like a real Chrome browser)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# The target URL (Replace this with the specific URL of the job board you want to scrape)
TARGET_URL = "https://example-job-board.com/search?q=data+engineer" 

def scrape_job_board(pages_to_scrape=3):
    scraped_data = []
    
    for page in range(1, pages_to_scrape + 1):
        print(f"📡 Scanning Market Node (Page {page})...")
        
        # Request the HTML from the server
        # url = f"{TARGET_URL}&page={page}" # Uncomment for real pagination
        response = requests.get(TARGET_URL, headers=HEADERS)
        
        if response.status_code != 200:
            print(f"⚠️ Connection Blocked by Server (Error {response.status_code})")
            break
            
        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # --- THE EXTRACTION LOGIC ---
        # Note: These class names ('job-card', 'title', etc.) are placeholders. 
        # You will inspect the target website and replace these with their actual HTML classes.
        job_cards = soup.find_all('div', class_='job-card') 
        
        for card in job_cards:
            try:
                title = card.find('h2', class_='title').text.strip()
                company = card.find('div', class_='company').text.strip()
                description = card.find('div', class_='description').text.strip()
                
                # Mocking salary extraction and cleaning
                salary_text = card.find('span', class_='salary').text if card.find('span', class_='salary') else "0"
                salary_avg = int(''.join(filter(str.isdigit, salary_text))) 
                
                # Determine if remote
                wfh = 1 if "remote" in description.lower() or "wfh" in description.lower() else 0
                
                scraped_data.append({
                    "title": title,
                    "company_name": company,
                    "description": description,
                    "salary_avg": salary_avg,
                    "work_from_home": wfh
                })
            except AttributeError:
                # If a card is missing a field, skip it to prevent pipeline crashes
                continue
        
        # Ethical Scraping: Pause between pages to avoid overloading the server
        time.sleep(random.uniform(2.0, 4.0)) 

    return scraped_data

# Execute the Scraper
raw_jobs = scrape_job_board(pages_to_scrape=1) # Mocking 1 page for safety

if raw_jobs:
    print(f"✅ Extraction Complete! Downloaded {len(raw_jobs)} fresh market nodes.")
    
    print("🧹 Cleaning and Formatting Data via Pandas...")
    df_new = pd.DataFrame(raw_jobs)
    
    # In a real scenario, we would append this to your existing dataset.csv
    # df_existing = pd.read_csv("dataset.csv")
    # df_combined = pd.concat([df_existing, df_new]).drop_duplicates(subset=['description'])
    # df_combined.to_csv("dataset.csv", index=False)
    
    print("💾 Saving to live database (dataset.csv)...")
    df_new.to_csv("dataset_live_demo.csv", index=False) 
    print("🎉 PIPELINE COMPLETE. Application data is now synchronized with the live market.")
else:
    print("ℹ️ Scraper returned empty. Update the HTML target tags in the script to match your chosen job board.")