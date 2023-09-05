import argparse
from enum import Enum
import sys


# A argument parser that will also print help upon error
class HelpArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)


class RunOpponent(Enum):
    SELF = "self"
    COMPUTER = "computer"


def run(opponent: RunOpponent):
    print(f"Running against opponent {opponent.value}")


def serve(port: int):
    print(f"Connecting to server on port {port}...")


def main():
    parser = HelpArgumentParser(description="MechMania 29 bot runner")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    serve_parser = subparsers.add_parser(
        "serve",
        help="Serves your bot to an engine on the port passed, requires engine to be running there",
    )
    serve_parser.add_argument("port", type=int, help="Port to connect to")

    run_parser = subparsers.add_parser("run", help="Run your bot against an opponent")
    run_parser.add_argument(
        "opponent",
        choices=list(map(lambda opponent: opponent.value, list(RunOpponent))),
        help="Opponent to put your bot against, where self is your own bot or computer is against a simple computer bot",
    )

    args = parser.parse_args()

    # Match to a valid command
    if args.command == "serve":
        return serve(args.port)
    elif args.command == "run":
        for opponent in list(RunOpponent):
            if opponent.value == args.opponent:
                return run(opponent)

    # If no valid command, print help
    parser.print_help()


if __name__ == "__main__":
    main()
