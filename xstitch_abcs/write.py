import os
import argparse
import json
import sys
from xstitch_abcs.letters import CrossStitchLetter, CrossStitchMessage


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", type=str,
                    help="The JSON file containing the letters in the cross stitch alphabet you'd like to use")

    ap.add_argument("--message", "-m", type=str,
                    help="The message you would like to display in the cross stitch alphabet")

    ap.add_argument("--interactive", "-i", action="store_true",
                    help="Instead of providing a message through the command line, give the message to the program interactively.")

    ap.add_argument("--sep", "-s", type=str,
                    help="The separator between columns")

    return ap.parse_args()




if __name__ == "__main__":
    args = parse_args()

    letters = {}

    if not os.path.exists(args.file):
        print("Error: cannot find file {} to load the cross stitch alphabet from.".format(args.file), file=sys.stderr)
        exit(1)
        pass

    with open(args.file, "r") as f:
        letters = json.loads(f.read())
        pass

    alphabet = {k: CrossStitchLetter(v, name=k) for k, v in letters.items()}

    if args.interactive:
        pass
    else:
        print(type(alphabet["A"]))
        messageLetters = [alphabet[m] for m in args.message]

        writing = CrossStitchMessage(*messageLetters)
        if args.sep:
            print(writing.formatContents(letterSep="\t"))
            pass
        else:
            print(writing)
        
