import os
import variables


logger = variables.setup_logger()


def check_links_in_directory(directory: str, final_file: str) -> None:
    for filename in os.listdir(directory):

        all_links = variables.read_from_file(final_file)

        if filename.endswith(variables.FILE_FORMAT):
            new_links = variables.read_from_file(os.path.join(directory, filename))
            different_links = new_links - all_links
            variables.write_to_file(different_links, final_file)


if __name__ == '__main__':
    check_links_in_directory(variables.DIR_NAME, variables.FINAL_FILE)
    logger.info("file check.py executed successfully.")

else:
    ...
