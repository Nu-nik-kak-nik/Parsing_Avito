import variables

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


logger = variables.setup_logger()


def check_ad_status(link: str | None, driver) -> bool | None:
    try:
        driver.get(link)
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "body")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        has_data_marker = any(item.has_attr('data-marker') and item['data-marker'] == "item-view/closed-warning" for item in soup.find_all())
        return has_data_marker

    except Exception as e:
        print(f"Error checking URL {link}: {e}")
        return None


def update_avito_links_file(final_file: str) -> None:
    links = variables.read_from_file(final_file)
    valid_links = set()

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    try:
        for link in links:
            if link:
                status = check_ad_status(link, driver)
                if status is False:
                    valid_links.add(link)

        variables.write_to_file(valid_links, final_file, overwrite=True, indents=False)
        logger.info(f"File {final_file} updated. Number of valid links: {len(valid_links)}")

    except Exception as e:
        logger.error(f"File update error {final_file}: {e}")

    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    update_avito_links_file(variables.FINAL_FILE)
    logger.info("file relevance.py executed.")
else:
    ...
