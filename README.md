
## Overview
This project demonstrates web scraping, API integration, and cross-browser testing using Selenium and BrowserStack.

## Features
1. Scrapes the first 5 articles from the El País Opinion section.
2. Extracts article titles and content.
3. Downloads cover images for each article.
4. Translates Spanish titles into English using a translation API.
5. Identifies words repeated more than twice in translated titles.
6. Runs cross-browser tests on BrowserStack using 5 parallel threads.

## Setup

Install dependencies:

pip install -r requirements.txt

## Run Locally

python main.py

## Run on BrowserStack

Set credentials:

set BROWSERSTACK_USERNAME=your_username  
set BROWSERSTACK_ACCESS_KEY=your_access_key  

Run:

python browserstack_run.py
