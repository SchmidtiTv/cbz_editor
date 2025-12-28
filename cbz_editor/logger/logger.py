import click


class Logger:
    def __init__(self, command: str, verbose: bool, log_file: str = None):
        self.command = command
        self.verbose = verbose
        self.log_file = log_file

    def info(self, message: str):
        message = f"[info] {self.command} - {message}"

        if self.verbose:
            click.echo(message)

        self.__add_to_log_file(message)

    def __add_to_log_file(self, message: str):
        if self.log_file:
            with open(self.log_file, 'a') as f:
                f.write(message + '\n')
