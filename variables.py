import logging


URL = 'https://www.avito.ru/krasnoyarsk/nastolnye_kompyutery' # link for parsing
SITE = 'https://www.avito.ru' # name of site
DIR_NAME = 'DataSet' # directory for saving test files with links
FILE_FORMAT = '.txt' # file format where links are written
# TIME = 10 # time of parsing
LOG = 'log.txt' # file with recorded parsing errors
FINAL_FILE = 'final.txt' # file with all unique links
LOG_FILE = 'log.txt' # file for writing logs
ENCODING = 'utf-8' # text file encoding
FMT = '%(asctime)s - %(levelname)s - %(message)s' # message recording format in log.txt
DATE_FMT = '%d.%m.%Y %H:%M:%S' # time output format
CLASS_ITEM = 'iva-item-content-OWwoq' # name of the class of the object being searched
CLASS_LINK = 'iva-item-sliderLink-Fvfau' # name of the class where the link to the object being searched is stored
META_NAME_PRICE = 'price' # name of the object where the price information is stored
EXCLUDED_WORDS = {'xeon'} # list of words that are not needed in the ad
PRICE_THRESHOLD = [8_000, 40_000] # price range in which to search for ads


logger = logging.getLogger(__name__)


def setup_logger(log_file=LOG_FILE) -> logging.Logger:
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt=FMT, datefmt=DATE_FMT)
    file_handler = logging.FileHandler(log_file, mode='a', encoding=ENCODING)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def write_to_file(links: set | None, file_path: str, overwrite: bool=False, indents: bool=True) -> None:
    if links:

        try:

            mode = 'w' if overwrite else 'a'

            with open(file_path, mode, encoding=ENCODING) as file:

                if indents:
                    file.seek(0, 2)
                    file.write('\n' * 2)
                for link in links:
                    file.write(f'{link}\n')

        except Exception as e:
            logger.error(f"error writing link: {e}", exc_info=True)
    else:
        logger.error(f"The list was empty")


def read_from_file(file_path: str) -> set:
    links = set()

    try:

        with open(file_path, 'r', encoding=ENCODING) as file:
            links = {line.strip() for line in file if line.strip()}

    except FileNotFoundError as e:
        logger.error(f"file {file_path} not found: {e}", exc_info=True)

    except Exception as e:
        logger.error(f"error reading file {file_path}: {e}", exc_info=True)

    return links
