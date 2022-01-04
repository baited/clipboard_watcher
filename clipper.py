import logging
import sys
import traceback
from datetime import datetime
from os import path
from pathlib import Path
from time import sleep

from pyperclip import paste
from urlextract import URLExtract

# get data directory
if getattr(sys, 'frozen', False):
    # running in a bundle
    data_dir = Path.home() / 'Documents' / 'clipboard_watcher'
    data_dir.mkdir(parents=True, exist_ok=True)
else:
    # running in a normal Python environment
    data_dir = Path(__file__).parent

# date prefix for file names
date_prefix = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
print(f'{date_prefix = } {type(date_prefix) = }')

# setup logging
logger = logging.getLogger('clipper')
logger.setLevel(logging.DEBUG)
logger_file = path.join(data_dir / f'log_{date_prefix}.txt')
logger_fh = logging.FileHandler(logger_file)
logger_fh.setLevel(logging.DEBUG)
logger_ch = logging.StreamHandler()
logger_ch.setLevel(logging.INFO)
logger_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
logger_fh.setFormatter(logger_formatter)
logger.addHandler(logger_fh)
logger.addHandler(logger_ch)


# list of glob style patterns
patterns = ('http://*', 'https://*', 'ftp://*')
# delay in seconds
delay = 0.5
# copying the following string will break the loop, exit
exit_string = '!EXIT'


def main():
    "main loop, 'listens' to the clipboard. saves copied URLs to a text file"
    last_copied = paste()
    out_file = data_dir / f'copied_{date_prefix}.txt'
    logger.info('saving to file: %s', out_file)
    url_extractor = URLExtract().find_urls
    while True:
        try:
            copied = paste()
            if copied != last_copied:
                log_copied = copied.split('\n')[0][:70]
                logger.info(f'User copied: {log_copied}')
                if copied == exit_string:
                    logger.info('User exited program')
                    break
                with open(out_file, 'a', encoding='utf-8') as fh:
                    for url in url_extractor(copied):
                        fh.write(url + '\n')

                last_copied = copied
        except OSError as e:
            logger.error(f'Could not open file: {out_file}')
            logger.error(str(e))
            logger.error(''.join(traceback.format_tb(e.__traceback__)))
        except Exception as e:
            logger.error(str(e))
            logger.error(''.join(traceback.format_tb(e.__traceback__)))

        sleep(delay)


if __name__ == '__main__':
    try:
        logger.info('Use "ctrl+z" or "ctrl+c" to exit')
        main()
    except KeyboardInterrupt:
        logger.info('User exited program')
    except Exception as e:
        logger.error('Unhandled exception, program exited. Info follows.')
        logger.error(str(e))
        logger.error(''.join(traceback.format_tb(e.__traceback__)))
