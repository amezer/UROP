import time
import itertools
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import json
import os
import shutil

# Remove the 'scrolls' folder if it exists
if os.path.exists("scrolls"):
    shutil.rmtree("scrolls")

# Create a fresh 'scrolls' folder
os.makedirs("scrolls")

MAX_KEYWORDS = 5
SCROLL_LIMIT = 5

def get_keywords(topic):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": f"Identify up to {MAX_KEYWORDS} related keywords for the topic '{topic}'. Seperate them with a comma."
        },
        stream=True  # Enable streaming
    )

    full_response = ""
    # Process each streamed line
    for line in response.iter_lines(decode_unicode=True):
        if line:
            try:
                data = json.loads(line)
                full_response += data.get("response", "")
            except json.JSONDecodeError as e:
                print("Error decoding line:", line, e)
                
    # Post-process the output:
    # Split the response by commas and trim extra spaces
    keywords = [kw.strip() for kw in full_response.split(',') if kw.strip()]
    print(keywords)
    # Limit to at most 5 keywords
    keywords = keywords[:MAX_KEYWORDS]
    return keywords

def generate_keyword_combinations(keywords):
    combinations = []
    for r in range(1, len(keywords) + 1):
        combinations.extend(itertools.combinations(keywords, r))
    return combinations

def construct_search_url(keywords):
    query = "%20OR%20".join(keywords)
    url = f"https://twitter.com/search?q={query}&src=typed_query&f=live"
    return url

def scrape_tweets(url, driver):
    global scroll_counter
    driver.get(url)
    last_height = driver.execute_script("return document.body.scrollHeight")

    for scroll in range(SCROLL_LIMIT):
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Wait for new tweets to load

        # Save the HTML after each scroll iteration
        filename = f"scrolls/page_scroll_{scroll_counter}.html"
        scroll_counter += 1
        with open(filename, "w", encoding="utf-8") as file:
            file.write(driver.page_source)
        print(f"Saved {filename}")

        # Get the new scroll height and compare with the previous height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("No more new tweets loaded.")
            break
        last_height = new_height

def main():
    global scroll_counter
    scroll_counter = 0
    prompt = "nintendo switch 2"
    keywords = get_keywords(prompt)
    print(f"Extracted Keywords: {keywords}")

    keyword_combinations = generate_keyword_combinations(keywords)
    print(f"Generated {len(keyword_combinations)} keyword combinations.")

    # Configure ChromeOptions to connect to an existing Chrome session
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    # Create the driver (make sure chromedriver is installed and in your PATH)
    driver = webdriver.Chrome(options=options)

    try:
        for idx, combination in enumerate(keyword_combinations):
            search_url = construct_search_url(combination)
            print(f"Scraping tweets for combination {idx+1}: {combination}")
            print(f"URL: {search_url}")
            scrape_tweets(search_url, driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
