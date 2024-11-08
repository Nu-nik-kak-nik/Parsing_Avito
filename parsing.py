import os
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import variables


logger = variables.setup_logger()


def scrape_links(data_filtering: bool=False):
    soup = None
    driver = None

    try:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get(variables.URL)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    except Exception as e:
        logger.error(f"error checking link: {e}", exc_info=True)
    finally:
        if driver:
            driver.quit()

    if soup:
        if data_filtering:
            return filter_links(soup, variables.EXCLUDED_WORDS, variables.PRICE_THRESHOLD)
        else:
            return {f"{variables.SITE}{item['href']}" for item in soup.find_all('a', class_=variables.CLASS_LINK)}
    else:
        return None


def filter_links(soup, words: set | None=None, price_threshold: list | None=None):

    links = set()

    for item in soup.find_all('div', class_=variables.CLASS_ITEM):
        link_tag = item.find('a', class_=variables.CLASS_LINK)
        price_tag = item.find('meta', itemprop=variables.META_NAME_PRICE)

        if link_tag and price_tag:
            link = link_tag['href']
            price = int(price_tag['content'])

            if words and price_threshold:
                if not any(word in link for word in variables.EXCLUDED_WORDS):
                    if variables.PRICE_THRESHOLD[0] <= price <= variables.PRICE_THRESHOLD[1]:
                        links.add(f"{variables.SITE}{link}")
            elif words and not price_threshold:
                if not any(word in link for word in variables.EXCLUDED_WORDS):
                    links.add(f"{variables.SITE}{link}")
            elif not words and price_threshold:
                if variables.PRICE_THRESHOLD[0] <= price <= variables.PRICE_THRESHOLD[1]:
                    links.add(f"{variables.SITE}{link}")

    if not links:
        logger.error(f"page elements were not found (classes may have changed) ", exc_info=True)

    return links


def run_parser(file_path) -> None:
    variables.write_to_file(scrape_links(data_filtering=True), file_path)


if __name__ == '__main__':
    run_parser(os.path.join(variables.DIR_NAME, f"{datetime.now().strftime('%Y-%m-%d')}{variables.FILE_FORMAT}"))
    logger.info("file parsing.py executed successfully.")

else:
    ...