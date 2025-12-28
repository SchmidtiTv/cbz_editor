from .logger import Logger


def create_logger(command: str, verbose: bool, log_file: str) -> Logger:
    return Logger(command=command, verbose=verbose, log_file=log_file)
