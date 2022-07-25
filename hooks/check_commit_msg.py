"""Hook to Check if a commit message is valid."""
import sys

from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    level="INFO",
    format="<d>{message}</>"
)

keywords = [
    'feat', 'fix', 'chore', 'refactor', 'docs',
    'style', 'test', 'perf', 'ci', 'build', 'revert'
]


def main(*args):
    """Check if a commit message is valid."""
    with open(sys.argv[1]) as FILE:
        data = FILE.read()
        msg = data.split('\n')[0]
        keyword = msg.split(':', maxsplit=1)[0]
        all_keyword = keywords + [s.capitalize() for s in keywords]
        if keyword not in all_keyword:
            logger.info(
                "\tCommit message must start with a keyword"
                f"\n\tvalid keywords {*all_keyword,}\n"
                "\tsee https://github.com/Gorgeous-Ghouls/commit-msg-validator#keywords for description\n"  # noqa: E501
                f"\n\tCurrent keyword is {keyword} \n"
            )
            sys.exit(1)
