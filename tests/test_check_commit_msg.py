"""Test file for commit-msg tests."""
from unittest.mock import patch

import pytest

from hooks.check_commit_msg import main


def test_check_commit_msg(tmp_path):
    """Test for commit-msg pre-commit hook."""
    commit_msg_file = tmp_path / 'msg'
    patched_argv = ["anything", f"{commit_msg_file}"]
    with patch('sys.argv', patched_argv):
        with pytest.raises(SystemExit):
            commit_msg = "wrong: keyword \n exit with \n 1"
            commit_msg_file.write_text(commit_msg)
            main()
        with pytest.raises(SystemExit):
            commit_msg = "feat(chore):"
            commit_msg_file.write_text(commit_msg)
            main()
        try:
            commit_msg = "feat: correct keyword \n exit with \n 0"
            commit_msg_file.write_text(commit_msg)
            main()
            commit_msg = "feat(scope): correct keyword \n exit with \n 0"
            commit_msg_file.write_text(commit_msg)
            main()
        except SystemExit:
            assert False, \
                f"pre-hook raised SystemExit for commit-msg {commit_msg}"
