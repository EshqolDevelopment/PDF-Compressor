import logging


def log(text, kind="normal"):
    if kind == "normal":
        print(text)
    elif kind == "info":
        logging.info(text)
    elif kind == "error":
        logging.error(text)
    else:
        raise ValueError("kind is not one of the valid options - ['normal', 'info', 'error']")

log("hello", kind="info")