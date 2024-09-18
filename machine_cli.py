import io
import logging
import argparse

from machine import Machine

log = logging.getLogger(__name__)


def getArguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='machine_cli',
        description='Simulate running of binary program',
        epilog='Text at the bottom of help')
    parser.add_argument('--log_name', action='store', help='file name to store logs', default='machine_cli.log')
    parser.add_argument('--log_level', action='store', choices=("DEBUG", "INFO", "WARN", "ERROR", "FATAL"), default="DEBUG")

    parser.add_argument('program', help='binary program file name')
    parser.add_argument('input', help='text file name with line by line program input')
    return parser.parse_args()


def main():
    args: argparse.Namespace = getArguments()
    logging.basicConfig(filename=args.log_name, level=args.log_level)
    program_name: str = args.program
    input_name: str = args.input
    log.info("Start simulation of %s with input from %s ...", program_name, input_name)
    stdout = io.StringIO()
    with open(program_name, "r+b") as program:
        with open(input_name, "r+t") as stdin:
            Machine(program).simulate(stdin, stdout)
    log.info("Simulation output: %s", stdout.getvalue())


if __name__ == "__main__":
    main()
