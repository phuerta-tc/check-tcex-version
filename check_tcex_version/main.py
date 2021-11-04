"""Check TCEX Version"""
# standard library
import argparse
import os
import sys
from typing import Optional, Sequence

# third-party
import sh


def check_tcex(pip_location):
    """Check TCEX version"""

    if pip_location.startswith('$'):
        _env_var = pip_location
        print(f'pip location has been provided as an environment variable: {_env_var}')
        pip_location = os.getenv(pip_location[1:], None)
        print(f'Environment variable value: {pip_location}')

        if not pip_location:
            print(
                f'pip location was provided as environment variable "{_env_var}", but environment '
                'variable has no value or is blank'
            )
            return 1

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

    print('TCEX is up to date')
    return 0


def main(argv: Optional[Sequence[str]] = None):
    """Entry point for pre-commit hook."""

    parser = argparse.ArgumentParser()
    parser.add_argument('--pip_location', required=True)
    parser.add_argument('--skip_on_gitlab_ci', action='store_true', default=False)
    args = parser.parse_args(argv)

    if args.skip_on_gitlab_ci and os.getenv('CI', False):
        print('Hook is currently running within a GitLab Pipeline environment. Skipping execution')
        return 0

    return check_tcex(args.pip_location)


if __name__ == '__main__':
    sys.exit(main())
