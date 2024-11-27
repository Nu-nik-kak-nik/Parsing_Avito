import os
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import variables


logger = variables.setup_logger()


def scrape_links(url: str, data_filtering: bool=False) -> set | None:
    driver = None
    received_links = set()

    try:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        received_links.update(extract_links(soup, variables.SITE, variables.CLASS_LINK, data_filtering))

    except Exception as e:
        logger.error(f"error checking link: {e}", exc_info=True)

    finally:
        if driver:
            driver.quit()

    return received_links if received_links else None


def extract_links(soup, link_parsing: str, class_link: str, data_filtering: bool=False) -> set | None:

    if data_filtering:
        links =  filter_links(soup, variables.CLASS_ITEM, variables.CLASS_LINK,
                              variables.META_NAME_PRICE, variables.SEARCH_LOCATION, link_parsing,
                              variables.EXCLUDED_WORDS, variables.PRICE_THRESHOLD)
        logger.info(f"Filtered {len(links)} links.")
    else:
        links = {f"{link_parsing}{item['href']}" for item in soup.find_all('a', class_=class_link)}
        logger.info(f"Extracted {len(links)} links without filtering.")

    return links


def filter_links(soup, class_item: str, class_link: str,
                 meta_name_price: str, location: str, link_parsing: str,
                 words: set | None=None, price_threshold: list | None=None) -> set:

    links = set()

    for item in soup.find_all('div', class_=class_item):
        link_tag = item.find('a', class_=class_link)
        price_tag = item.find('meta', itemprop=meta_name_price)

        if link_tag and price_tag:
            link = link_tag['href']
            price = int(price_tag['content'])
            if location in link:
                if words and price_threshold:
                    if not any(word in link for word in words):
                        if price_threshold[0] <= price <= price_threshold[1]:
                            links.add(f"{link_parsing}{link}")
                elif words and not price_threshold:
                    if not any(word in link for word in words):
                        links.add(f"{link_parsing}{link}")
                elif not words and price_threshold:
                    if price_threshold[0] <= price <= price_threshold[1]:
                        links.add(f"{link_parsing}{link}")

    if not links:
        logger.error(f"page elements were not found (classes may have changed) ", exc_info=True)

    return links


def run_parser(file_path) -> None:
    variables.write_to_file(scrape_links(variables.URL, data_filtering=True), file_path) # !!!!!!!!!!!!!!!!!!!!!!!!!!


if __name__ == '__main__':
    run_parser(os.path.join(variables.DIR_NAME, f"{datetime.now().strftime('%Y-%m-%d')}{variables.FILE_FORMAT}"))
    # variables.write_to_file(scrape_links(variables.URL, data_filtering=True),
    #                         os.path.join(variables.DIR_NAME,
    #                                      f"{datetime.now().strftime('%Y-%m-%d')}{variables.FILE_FORMAT}"))
    logger.info("file parsing.py executed.")

else:
    ...