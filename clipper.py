from clipboard import paste
from time import sleep
from os import path
from fnmatch import fnmatch
import logging

# setup logging
logger = logging.getLogger('clipper')
logger.setLevel(logging.DEBUG)
logger_file = path.join(path.dirname(path.normpath(__file__)), 'clipper.log')
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
    current_directory = path.dirname(path.normpath(__file__))
    out_file = path.join(current_directory, 'clipped.txt')
    while True:
        try:
            copied = paste()
            if copied != last_copied:
                logger.info(f'User copied: {copied}')
                if copied == exit_string:
                    logger.info('User exited program')
                    break
                for p in patterns:
                    if fnmatch(copied, p):
                        with open(out_file, 'a', encoding='utf-8') as fh:
                            fh.write(copied + '\n')
                last_copied = copied
        except OSError as e:
            logger.error(f'Could not open file: {out_file}')
            logger.error(str(e))
            logger.error(e.__traceback__)
        except Exception as e:
            logger.error(str(e))
            logger.error(e.__traceback__)

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
        logger.error(e.__traceback__)