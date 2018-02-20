import logging
from ConfigParser import ConfigParser
from os import path, mkdir, chmod
from datetime import datetime


def log(log_message):

    try:
        logger
    except NameError:
        start_logger()

    logger.info(log_message)


def start_logger():

    global logger
    logger = get_logger()


def get_logger(format='%(asctime)s %(levelname)s %(threadName)s %(message)s',
               logfile=True,
               logout=True):

    config = ConfigParser()
    config.read("config.ini")

    now = datetime.now()

    home_path = path.expanduser('~')

    log_name = config.get('Log Settings', 'Log Name')
    log_dir = config.get('Log Settings', 'Log Directory')

    log_dir = "%s/%s" % (home_path, log_dir)

    if not path.exists(log_dir):
        print 'creating log directory: {}'.format(log_dir)
        mkdir(log_dir)
        chmod(log_dir, 0777)

    log_dir_sub_dir = ["%s%02d" % (now.year, now.month)]
    for new_dir in log_dir_sub_dir:
        log_dir = "%s%s/" % (log_dir, new_dir)
        if not path.exists(log_dir):
            print 'creating log directory: {}'.format(log_dir)
            mkdir(log_dir)
            chmod(log_dir, 0777)

    if not path.exists(log_dir):
        print 'creating log directory: {}'.format(log_dir)
        mkdir(log_dir)
        chmod(log_dir, 0777)

    log_path = path.join(
        log_dir, '{}_{}.log'.format(now.strftime('%Y%m%d_%H%M'), log_name)
    )
    logger = logging.getLogger('logger')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(format)

    if logfile is True:
        print '{} logging to path: {}'.format(now, log_path)
        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    if logout is True:
        print 'logging to stdout'
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger
