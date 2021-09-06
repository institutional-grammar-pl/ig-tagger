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

    p.add_argument(
        "--split_type",
        help="""
        optional setting for split type:
        'spacy' or 'regex'
        to check which one is a better heuristic"""
    )

    # group1 = p.add_mutually_exclusive_group(required=True)
    # group1.add_argument('--enable', action="store_true")
    # group1.add_argument('--disable', action="store_false")

    return p.parse_args()


def return_or_raise(x):
    if x:
        return x
    else:
        raise ValueError()


if __name__ == '__main__':
    if sys.version_info < (3, 5, 0):
        sys.stderr.write("You need python 3.5 or later to run this script\n")
        sys.exit(1)

    try:
        args = cmdline_args()
        input_path = Path(return_or_raise(args.input_file_path))
        output_path = Path(return_or_raise(args.output_file_path))
        if args.action_type == 'atomize':
            atomize(input_path, output_path)
            print('Done')
        elif args.action_type == 'classify':
            if args.split_type in ['spacy', 'regex']:
                split(input_path, output_path, args.split_type)
            else:
                split(input_path, output_path)
            print('Done')
        elif args.action_type == 'tag' and args.sentence_type in ['regulative', 'constitutive']:
            type_param = 'reg' if args.sentence_type == 'regulative' else 'cons'
            annotate_file(input_path, output_path, type_param, True)
        else:
            raise ValueError("Wrong parameters.")
    except Exception as e:
        print(e)
