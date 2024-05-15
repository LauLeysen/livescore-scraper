
# Soccer Match Data Scraper

This project is a soccer match data scraper that uses Selenium to fetch live match data from a given list of URLs. The data is then saved to a JSON file for further use.

## Features
- Fetches live match data from specified URLs. It takes URLs from league's for example https://www.livescore.com/en/football/england/premier-league/
- Extracts home team, away team, match status, and scores.
- Saves the extracted data to a JSON file.
- Handles different match statuses such as Finished, Halftime, Live, and Upcoming.

## Requirements
- Python 3.11.4 (tested)
- Selenium
- rich
- Chrome WebDriver

## Setup
1. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
2. Download and install the [Chrome WebDriver](https://googlechromelabs.github.io/chrome-for-testing/) suitable for your Chrome version.
3. Place the `chromedriver` executable in a known directory and update the `get_driver` function if necessary. Or put chromedriver.exe in your path environment.

## Usage
1. Create a `urls.txt` file in the project directory and list the URLs you want to scrape, one per line.
2. Run the script:
    ```bash
    python livescore_scraper.py
    ```

## Functions

### get_driver()
Returns a configured instance of the Chrome WebDriver.

### fetch_data(driver, url)
Fetches match data from the provided URL using the given WebDriver instance.

### save_to_json(data, filename)
Saves the provided data to a JSON file with the given filename.

## Error Handling
- Handles errors during WebDriver initialization.
- Handles errors during data extraction for each match.

## License
This project is licensed under the MIT License.
