import logging
import time
import subprocess

import variables


logger = variables.setup_logger()


def run_script(script_name: str) -> None:
    start_time = time.time()

    try:
        subprocess.run(['python', script_name], text=True)
        logger.info(f"{script_name} execution time: {time.time() - start_time:.2f}s")
        print(f"{script_name} execution time: {time.time() - start_time:.2f}s")

    except subprocess.CalledProcessError as e:
        logging.error(f'Error running script {script_name}: {e}')
        print(f'Error running script {script_name}: {e}')


def run_main():
    print('Hi!')
    logger.info("file main.py started")

    while True:
        try:
            choice = input(
                  '1) Parsing data from the URL set in the variables.py file (parsing.py)\n'
                  '2) Writing all unique URLs to the file final.txt (check.py)\n'
                  '3) Checking the URL for the relevance of the announcement (relevance.py)\n'
                  '4) Run all project at once\n'
                  '5) Exit\n'
                  'Enter a number: ')

            match choice:
                case '1':
                    run_script('parsing.py')
                case '2':
                    run_script('check.py')
                case '3':
                    run_script('relevance.py')
                case '4':
                    run_script('parsing.py')
                    run_script('check.py')
                    run_script('relevance.py')
                case _:
                    print('\n\nFinish')
                    break

        except ValueError:
            print('Invalid input. Please enter a number')
            time.sleep(2)

        except KeyboardInterrupt:
            print('\n\nFinish')
            break

        print('\n' * 3)


if __name__ == '__main__':
    run_main()
    logger.info("file main.py executed.")

else:
    ...