import sys
import argparse
from pathlib import Path

from atomize import atomize
from main import annotate_file
from split_sentence_type import split


def cmdline_args():
    # Make parser object
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    #
    # p.add_argument("required_positional_arg",
    #                help="desc")
    # p.add_argument("required_int", type=int,
    #                help="req number")
    # p.add_argument("--on", action="store_true",
    #                help="include to enable")
    # p.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2], default=0,
    #                help="increase output verbosity (default: %(default)s)")

    p.add_argument(
        "action_type",
        help="""
        What to do?
        1) 'atomize'
        2) 'classify' (sentence type)
        3) 'tag' (with IG)
        """
    )
    p.add_argument(
        "input_file_path",
        help="""
        path to file to process
        """
    )

    p.add_argument(
        "output_file_path",
        help="""
        path to save the result
        """
    )

    p.add_argument(
        "--sentence_type",
        help="""
        'regulative' or 'constitutive'
        """,
        required=False
    )

    # group1 = p.add_mutually_exclusive_group(required=True)
    # group1.add_argument('--enable', action="store_true")
    # group1.add_argument('--disable', action="store_false")

    return p.parse_args()


if __name__ == '__main__':

    if sys.version_info < (3, 5, 0):
        sys.stderr.write("You need python 3.5 or later to run this script\n")
        sys.exit(1)

    try:
        args = cmdline_args()
        input_path = Path(args.input_file_path) if args.input_file_path else ValueError()
        output_path = Path(args.output_file_path) if args.output_file_path else ValueError()
        if args.action_type == 'atomize':
            atomize(input_path, output_path)
        elif args.action_type == 'classify':
            split(input_path, output_path)
        elif args.action_type == 'tag' and args.sentence_type in ['regulative', 'constitutive']:
            annotate_file(input_path, output_path, args.sentence_type, True)
        else:
            ValueError()
    except Exception as e:
        print(e)

    print()
