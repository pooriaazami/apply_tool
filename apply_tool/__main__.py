from dotenv import load_dotenv

load_dotenv()

from installation import install
install()

from utils import build_command_parser

def main():
    parser = build_command_parser()

    while True:
        command = input('>> ').strip()
        parser.parse(command)

        if command.lower() == 'exit':
            break

if __name__ == '__main__':
    main()
