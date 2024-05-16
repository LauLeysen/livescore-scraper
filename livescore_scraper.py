import time
import json
import asyncio
from rich import print
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def get_driver():
    """
    Return a Chrome driver instance.
    """
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--log-level=3')

    try:
        return webdriver.Chrome(options=options)
    except WebDriverException as e:
        print(f"[bold red]An error occurred while trying to create the Chrome driver:[/bold red] {e}")
        return None

def fetch_data(driver, url):
    driver.get(url)
    time.sleep(3)  # Allow time for the page to load

    matches = driver.find_elements(By.CLASS_NAME, 'wo')
    match_data = []

    for match in matches:
        try:
            
            match_time = match.find_element(By.ID, match.get_attribute('id') + '__status-or-time').text
            if "'" not in match_time:
                match_date = match.find_element(By.CLASS_NAME, 'ft').text

            home_team = match.find_element(By.ID, match.get_attribute('id') + '__home-team-name').text
            away_team = match.find_element(By.ID, match.get_attribute('id') + '__away-team-name').text
            home_score_element = match.find_element(By.ID, match.get_attribute('id') + '__home-team-score')
            away_score_element = match.find_element(By.ID, match.get_attribute('id') + '__away-team-score')
            
            home_score = home_score_element.text if home_score_element.text else None
            away_score = away_score_element.text if away_score_element.text else None
            
            match_info = {
                'home_team': home_team,
                'away_team': away_team
            }
            
            if match_time == 'FT':
                match_info['status'] = 'Finished'
                match_info['result'] = f"{home_team} {home_score} - {away_score} {away_team}"
            elif "'" in match_time:
                match_info['status'] = 'Live'
                match_info['time'] = match_time
                match_info['score'] = f"{home_score} - {away_score}"
            elif 'HT' in match_time:
                match_info['status'] = 'Halftime'
                match_info['score'] = f"{home_team} {home_score} - {away_team} {away_score}"
            else:
                match_info['status'] = f'Upcoming {match_date} {match_time}'
                match_info['start_time'] = match_time
            
            match_data.append(match_info)
        except Exception as e:
            print(f'Error extracting data for a match: {e}')
    
    return match_data

def save_to_json(data, filename):
    """
    Save the data to a JSON file.
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

async def run_scraper():
    while True:
        # Read URLs from the file
        with open('urls.txt', 'r') as file:
            urls = [line.strip() for line in file.readlines()]

        driver = get_driver()
        if driver:
            all_data = []
            try:
                for url in urls:
                    data = fetch_data(driver, url)
                    all_data.extend(data)
                driver.quit()
                # Print the final result
                print(json.dumps(all_data, indent=2))
                # Save the data to a JSON file
                save_to_json(all_data, '../match_data.json')
            except Exception as e:
                print(f"[bold red]An error occurred during fetching data:[/bold red] {e}")
            finally:
                driver.quit()
        await asyncio.sleep(5)

if __name__ == '__main__':
    try:
        asyncio.run(run_scraper())
    except KeyboardInterrupt:
        print("[bold red]Scraper stopped by user.[/bold red]")
