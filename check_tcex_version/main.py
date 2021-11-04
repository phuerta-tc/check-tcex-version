"""Check TCEX Version"""
# standard library
import sys
from typing import Optional, Sequence

# third-party
import sh


def main(argv: Optional[Sequence[str]] = None):
    """Entry point for pre-commit hook."""
    output = sh.pip('list', outdated=True).strip()
    if output is not None:
        output = output.splitlines()
        for line in output:
            if 'tcex' in line:
                version = line.split()[-2]
                print(f'A new version of TCEX is available: {version}')
                return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
