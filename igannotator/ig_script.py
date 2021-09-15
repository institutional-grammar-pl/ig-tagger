import sys
import argparse
from pathlib import Path

from igannotator.frontend import (
    atomize,
    annotate_sentence_type,
    annotate_ig
)


def cmdline_args():
    # Make parser object
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)

    p.add_argument(
        "action_type",
        help="""
        What to do?
        1) 'atomize' - split into sentences
        2) 'classify' - sentence type regulative/constitutive
        3) 'tag' - annotate with IG
        """
    )
    p.add_argument(
        "input_file_path",
        help="""
        path to read the input file
        """
    )

    p.add_argument(
        "output_file_path",
        help="""
        path to save the result
        """
    )

    # p.add_argument(
    #     "--sentence_type",
    #     help="""
    #     'regulative' or 'constitutive'
    #     """,
    #     required=False
    # )

    p.add_argument(
        "--split_type",
        help="""
        optional setting for split type ('rule_based' or 'ml') while using `atomize` action
        """
    )

    return p.parse_args()


def return_or_raise(x):
    if x:
        return x
    else:
        raise ValueError()


def main():
    if sys.version_info < (3, 6, 0):
        sys.stderr.write("You need python 3.6 or later to run this script\n")
        sys.exit(1)

    try:
        args = cmdline_args()
        input_path = Path(return_or_raise(args.input_file_path))
        output_path = Path(return_or_raise(args.output_file_path))
        if args.action_type == 'atomize':
            if args.split_type in ['ml', 'rule_based']:
                atomize(input_path, output_path, args.split_type)
            else:
                atomize(input_path, output_path)
            print('Done')
        elif args.action_type == 'classify':
            annotate_sentence_type(input_path, output_path)
            print('Done')
        elif args.action_type == 'tag':
            annotate_ig(input_path, output_path)
        else:
            raise ValueError("Wrong parameters.")
    except Exception as e:
        print("Error during processing:")
        print(e)


if __name__ == '__main__':
    main()
