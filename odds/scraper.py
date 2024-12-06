from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime

# Path to ChromeDriver
CHROME_DRIVER_PATH = "/path/to/chromedriver"

# Set up WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (optional)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)

# URL for NRL Draw
BASE_URL = "https://www.nrl.com/draw/"
SEASON = "2025"
COMPETITION = "111"

# Data storage
matches = []

# Loop through all 27 rounds
for round_number in range(1, 28):
    print(f"Scraping Round {round_number}...")
    url = f"{BASE_URL}?competition={COMPETITION}&round={round_number}&season={SEASON}"
    driver.get(url)

    try:
        # Wait for match sections to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "section ul.l-grid"))
        )

        # Find all match sections
        match_sections = driver.find_elements(By.CSS_SELECTOR, "section ul.l-grid li.l-grid__cell")

        for match_section in match_sections:
            try:
                # Extract match date and time
                match_date_text = match_section.find_element(By.CSS_SELECTOR, "p.match-header__title").text
                match_time_element = match_section.find_element(By.CSS_SELECTOR, "time")
                match_time = match_time_element.text if match_time_element else "TBA"
                match_datetime = datetime.strptime(f"{match_date_text} {match_time}", "%A %d %B %I:%M%p")

                # Extract teams
                home_team = match_section.find_element(By.CSS_SELECTOR, "div.match-team--home p.match-team__name").text
                away_team = match_section.find_element(By.CSS_SELECTOR, "div.match-team--away p.match-team__name").text

                # Extract venue
                match_location = match_section.find_element(By.CSS_SELECTOR, "p.match-venue").text

                # Extract odds
                odds_elements = match_section.find_elements(By.CSS_SELECTOR, "dd a.o-button")
                home_odds = float(odds_elements[0].text.replace("$", "")) if len(odds_elements) > 0 else None
                away_odds = float(odds_elements[1].text.replace("$", "")) if len(odds_elements) > 1 else None

                # Append to matches list
                matches.append({
                    "match_date": match_datetime.date(),
                    "match_time": match_datetime.time(),
                    "match_location": match_location,
                    "home_team": home_team,
                    "away_team": away_team,
                    "home_score": 0,  # Placeholder
                    "away_score": 0,  # Placeholder
                    "home_odds": home_odds,
                    "draw_odds": None,  # Assuming no draw odds available
                    "away_odds": away_odds,
                    "status": "Scheduled"
                })
            except Exception as e:
                print(f"Error processing match: {e}")
                continue

    except Exception as e:
        print(f"Failed to scrape Round {round_number}: {e}")
        continue

# Close the driver
driver.quit()

# Save to CSV
df = pd.DataFrame(matches)
csv_file = "nrl_matches_2025.csv"
df.to_csv(csv_file, index=False)
print(f"Data saved to {csv_file}")
