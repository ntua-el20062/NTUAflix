import subprocess
import json
import pytest
from argparse import Namespace
from se2305 import searchtitle, title, searchname, name, bygenre, newtitles, newnames, newcrew, newakas, newepisode, newratings, newprincipals, healthcheck, resetall, top10genre

def run_cli_command(command, args):
    result = subprocess.run(['python', '-m', 'se2305', command] + args, capture_output=True, text=True)
    return result

# Functional tests using pytest
def test_newtitles_valid_input():
    args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\title.tsv']
    result = run_cli_command('newtitles', args)
    assert result.returncode == 0
    assert '"status": "titlebasics data added"' in result.stdout

# ... Other test functions for each CLI command ...

def test_resetall():
    result = run_cli_command('resetall', [])
    assert result.returncode == 0
    assert '"Database repopulated successfully"' in result.stdout

if __name__ == '__main__':
    pytest.main()