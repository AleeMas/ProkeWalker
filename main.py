import logging
import threading
import time

from windowHandler import WindowHandler

timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

logging.basicConfig(filename='ProkeWalker.log', filemode='w', level=logging.DEBUG)


if __name__ == '__main__':
    window_handler = WindowHandler(580, 540, "ProkeWalker")
    logging.debug('{}:window created'.format(timestamp))
    window_handler_updater = threading.Thread(target=window_handler.update_window_tick)
    logging.debug('{}:thread for updater ON'.format(timestamp))

    window_handler_updater.start()

    logging.debug('ProkeWalker Starting')
    window_handler.run()
