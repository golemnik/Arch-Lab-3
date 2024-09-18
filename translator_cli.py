from translator import Translator
import logging
import argparse

log = logging.getLogger(__name__)


def getArguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='translator_cli',
        description='Translate a program from text source to binary destination',
        epilog='Text at the bottom of help')
    parser.add_argument('--log_name', action='store', help='file name to store logs', default='translator_cli.log')
    parser.add_argument('--log_level', action='store', choices=("DEBUG", "INFO", "WARN", "ERROR", "FATAL"), default="DEBUG")

    parser.add_argument('source', help='text file name with a program source codes')
    parser.add_argument('destination', help='binary file name with result of translation')
    return parser.parse_args()


def main():
    args: argparse.Namespace = getArguments()
    logging.basicConfig(filename=args.log_name, level=args.log_level)
    source_name: str = args.source
    destination_name: str = args.destination
    log.info("translate %s into %s ...", source_name, destination_name)
    with open(source_name, "r+t") as source:
        with open(destination_name, "w+b") as destination:
            Translator(source, destination).translate()


if __name__ == "__main__":
    main()
