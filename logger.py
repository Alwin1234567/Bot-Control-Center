import logging
from os.path import exists
from os import makedirs
from datetime import date

def setup_logger(name):
    logger = logging.getLogger(name)

    logger.setLevel(logging.DEBUG)
    filename, errorname = date_log()
    
    chat_logger = logging.StreamHandler()
    file_logger = logging.FileHandler(filename)
    error_logger = logging.FileHandler(errorname)
    
    chat_logger.setLevel(logging.WARNING)
    file_logger.setLevel(logging.INFO)
    error_logger.setLevel(logging.ERROR)

    chat_logger.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    file_logger.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    error_logger.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(message)s"))

    logger.addHandler(chat_logger)
    logger.addHandler(file_logger)
    logger.addHandler(error_logger)

def date_log():

    today = date.today().strftime("%Y_%m_%d")
    makedirs("Logs/", exist_ok = True)
    makedirs("Logs/Errors", exist_ok = True)
    if not exists("Logs/{}.log".format(today)):
        f = open("Logs/{}.log".format(today), "w")
        f.close()
        f = open("Logs/Errors/{}.log".format(today), "w")
        f.close()
        return "Logs/{}.log".format(today), "Logs/Errors/{}.log".format(today)
    counter = 2
    while True:
        if not exists("Logs/{}_{}.log".format(today,counter)):
            f = open("Logs/{}_{}.log".format(today, counter), "w")
            f.close()
            f = open("Logs/Errors/{}_{}.log".format(today, counter), "w")
            f.close()
            return "Logs/{}_{}.log".format(today, counter), "Logs/Errors/{}_{}.log".format(today, counter)
        counter += 1
