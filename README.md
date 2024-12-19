# Automated Avito Ad Parser

This project is an automated parser for Avito ads. It's designed to find and collect links to current ads that meet specified criteria. The parser uses Selenium for web page interaction and BeautifulSoup for HTML processing.

This is a small project that works via the command line, its logical development will be made in the form of another project that I have started writing now.

## Functionality

The project consists of several scripts:

* **`main.py`:** The main script provides the user with an interactive menu to run different parsing stages.
* **`parsing.py`:** Parses ads from a given URL, extracting links to them. Uses filters to find ads within the desired price range and without specified words.
* **`check.py`:** Checks for new links in the parsing results folder and adds unique links to the final file.
* **`relevance.py`:** Checks the validity of links from the final file, removing links to closed ads.

## Setup

1. **Install required libraries:**
   ```bash
   pip install -r requirements.txt

## Configuration

To configure the parser, edit the `variables.py` file and specify the following parameters:

| Parameter          | Description                                                      |
|----------------------|------------------------------------------------------------------|
| `URL`               | The Avito page URL containing the ads.                             |
| `SEARCH_LOCATION`   | Location (extracted from the URL).                               |
| `SITE`              | The base Avito URL.                                               |
| `DIR_NAME`          | Name of the directory to store link files.                        |
| `FILE_FORMAT`       | Extension of the link files (e.g., ".txt").                      |
| `TIME`              | Parsing timeout (in seconds).                                    |
| `LOG`               | Name of the log file.                                             |
| `FINAL_FILE`        | Name of the file containing unique links.                         |
| `ENCODING`          | File encoding (e.g., "utf-8").                                  |
| `CLASS_ITEM`        | The class of the ad `div` element on the Avito page.             |
| `CLASS_LINK`        | The class of the `a` element containing the ad link.              |
| `META_NAME_PRICE`   | The name of the meta tag containing the ad price.                |
| `EXCLUDED_WORDS`    | A list of words that should not appear in the links.             |
| `PRICE_THRESHOLD`   | The price range for searching ads (a list: [min, max]).           |
| `MARKER`            | The HTML attribute used to identify closed ads.                   |
| `CLOSURE_MESSAGE`   | The value of the `MARKER` attribute indicating a closed ad.       |
| `START_OF_LINK`     | The link prefix (for correctness check).                         |


## Dependencies

* **Install Firefox and geckodriver:** Ensure Firefox is installed, and `geckodriver` is either in your system's PATH or explicitly specified in the code.


## Running the Parser

Execute the `main.py` script from your terminal.  A menu will appear, allowing you to select the desired action:

1. Parse data from the URL (`parsing.py`).
2. Write unique URLs to a file (`check.py`).
3. Check URL relevance (`relevance.py`).
4. Run all project stages.
5. Exit.


## Logging

Error messages and important information are logged to `log.txt`.


## Project Structure

```tree
.
├── main.py
├── parsing.py
├── check.py
├── relevance.py
├── variables.py
└── requirements.txt
