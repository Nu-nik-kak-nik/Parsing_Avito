import variables

# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.firefox.options import Options


logger = variables.setup_logger()


def check_avito_link_status(link: str | None) -> bool:

    # try:
    #     options = Options()
    #     options.add_argument("--headless")
    #     driver = webdriver.Firefox(options=options)
    #     driver.get(link)
    #     driver.implicitly_wait(5)

    #     if driver.find_elements(By.XPATH, "//div[@class='item-view-error__title']"):
    #         driver.quit()
    #         return False

    #     else:
    #         driver.quit()
    #         return True

    # except Exception as e:
    #     logger.error(f"error checking link {link}: {e}", exc_info=True)
    #     return False

    if int(link) < 10:
        return False
    else:
        return True


def update_avito_links_file(final_file: str) -> None:
    links = variables.read_from_file(final_file)
    valid_links = set()

    for link in links:

        if check_avito_link_status(link):
            valid_links.add(link)

    variables.write_to_file(valid_links, final_file, overwrite=True, indents=False)


if __name__ == "__main__":
    update_avito_links_file(variables.FINAL_FILE)
    logger.info("file relevance.py executed successfully.")
else:
    ...
