"""Check TCEX Version"""
# standard library
import argparse
import sys
from typing import Optional, Sequence

# third-party
import sh


def check_tcex(pip_location):
    """Check TCEX version"""
    try:
        pip_command = sh.Command(pip_location)
    except Exception:
        print(f'pip could not be found using provided location: {pip_location}')
        print('Please provide full path of target pip installation (provide output of "which pip"')
        return 1

    results = pip_command('list', outdated=True)

    if results.exit_code != 0:
        print('An unexpected error occurred while listing outdated packages')
        print(results.stderr.decode())
        return 1

    output = results.stdout.decode()
    output = output.splitlines()
    for line in output:
        if 'tcex' in line:
            version = line.split()[-2]
            print(f'A new version of TCEX is available: {version}')
            return 1
    else:
        print('TCEX is up to date')
        # return 1 to see if pre-commit prints output on failure
        return 1


def main(argv: Optional[Sequence[str]] = None):
    """Entry point for pre-commit hook."""

    parser = argparse.ArgumentParser()
    parser.add_argument('--pip_location', required=True)
    args = parser.parse_args(argv)
    check_tcex(args.pip_location)


if __name__ == '__main__':
    sys.exit(main())
