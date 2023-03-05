# encoding=utf-8
from retrieve import test_json, logging, _log
import sys
import traceback
import argparse



if __name__ == '__main__':
    logging.getLogger().setLevel(logging.WARNING) # only show messages with level WARNING and above.
    # acceptable/<in use> levels from lowest to highest:
    # NOTSET, DEBUG, INFO, <WARNING>, <ERROR>, <CRITICAL>

    # this will differentiate between caught and uncaught exceptions, while still running it through the
    # logger.
    sys.excepthook = lambda exctype, value, tb: \
        logging.error("An uncaught exception has occurred: {}: {}".format(exctype.__name__, value))

    # collect command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="show both passing and failing tests")
    parser.add_argument("-f", "--show_failing", action="store_true", help="only show failing tests")
    parser.add_argument("--url", action="store", default="https://math.he.net/mathbot")
    parser.add_argument("--ascii", action="store_true", help="replace colored output with PASS/FAIL, useful for scripting or if terminal does not support ANSI escape codes")
    parser.add_argument("filename", help="a valid test.json file", nargs="?") # 0 (stdin) or 1 for now

    args = parser.parse_args()
    # swap to reading stdin if no file was given
    try:
        f = open(args.filename) if args.filename else sys.stdin
    except FileNotFoundError as e:
        _log(logging.ERROR, e)
    OKGREEN = 'PASS' if args.ascii else '\033[92m✓\033[0m'
    FAIL = 'FAIL' if args.ascii else '\033[91m✗\033[0m'

    results = test_json(args.url, f) # retrieve and structure the expected values, and the api responses.
    if not results:
        _log(logging.ERROR, "No tests were run. Either there were 0 tests found in test.json, or there was no HTML element tagged with an id starting with \"he-info\" in the API response's \"html_solution\" field.")
    any_failed = False
    for test_num, he_info_id, expected, response in results:
        if response == expected:
            if args.verbose:
                print("%s %s %s: %s" % (OKGREEN, he_info_id, test_num, response))
        else:
            any_failed = True
            if args.show_failing or args.verbose:
                print("%s %s %s: expected: \"%s\" received: \"%s\"" % (FAIL, he_info_id, test_num, expected, response))
    if any_failed:
        exit(1)
    # exit(0)
