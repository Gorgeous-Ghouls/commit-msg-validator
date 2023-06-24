"""Hook to Check if a commit message is valid."""
import re
import sys

from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    level="DEBUG",
    format="<d>{message}</>"
)

keywords = [
    'feat', 'fix', 'chore', 'refactor', 'docs',
    'style', 'test', 'perf', 'ci', 'build', 'revert'
]


def main(*args):
    """Check if a commit message is valid."""
    with open(sys.argv[1]) as FILE:
        msg = FILE.readline().strip()  # get commit message
        # keyword(scope): msg
        try:
            if not (
                    regex_matches := re.findall(
                        r"([A-Za-z]+)(?:\(([^)]*)\))?:\s?(.+)",
                        msg
                    )
            ):
                raise ValueError

            keyword, scope, msg = regex_matches[0]
            keyword = keyword.lower()
        except ValueError:
            logger.error(
                "\tCommit message must be in the format"
                "\n\tkeyword(scope):msg"
                "\n\tKeyword and Message are required (Scope is optional)"
                f"\n\tCurrent commit message is {msg}"
            )
            sys.exit(1)
        if keyword not in keywords:
            logger.warning(
                "\tCommit message must start with a keyword"
                f"\n\tvalid keywords {*keywords,}\n"
                "\tsee https://github.com/p0lygun/commit-msg-validator#keywords for description\n"  # noqa: E501
                f"\n\tCurrent keyword is {keyword} \n"
                f"\tScope: {scope}\n"
                f"\tCommit message: {msg}\n"
            )  # noqa: E501
            sys.exit(1)

    # write commit message back to file
    with open(sys.argv[1], 'w') as FILE:
        FILE.write(f"{keyword}({scope}): {msg}")
