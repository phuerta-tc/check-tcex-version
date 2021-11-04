"""Check TCEX Version"""
# standard library
import sys
from typing import Optional, Sequence

# third-party
import sh


def main(argv: Optional[Sequence[str]] = None):
    """Entry point for pre-commit hook."""
    return_code = 0
    output = sh.pip('list', outdated=True).strip()
    print(output)
    if output is not None:
        output = output.splitlines()
        for line in output:
            if 'tcex' in line:
                version = line.split()[-2]
                print(f'A new version of TCEX is available: {version}')
                return_code = 1
                break
        else:
            print('TCEX is up to date')
            # return 1 to see if pre-commit prints output on failure
            return_code = 1
    else:
        print('Unable to list outdated packages')
        return_code = 1

    return return_code


if __name__ == '__main__':
    sys.exit(main())
