import subprocess
import json
import pytest
import re

def run_cli_command(command, args):
    try:
        result = subprocess.run(['python', '-m', 'se2305', command] + args, capture_output=True, text=True, check=True)
        status_code_match = re.search(r'Response Status Code: (\d+)', result.stdout)
        if status_code_match:
            status_code = int(status_code_match.group(1))
        else:
            # If the status code is not found in the output, default to 0
            status_code = 0

        try:
            # Attempt to parse output as JSON
            return status_code, json.loads(result.stdout), result.stderr
        except json.JSONDecodeError:
            # If parsing fails, return raw output as a string
            return status_code, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stdout, e.stderr

#Functional Testing

def test_newtitles_valid_input():
    args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\title.tsv']
    status_code, _, _ = run_cli_command('newtitles', args)
    assert status_code == 200

def test_newtitles_edge_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\titles.tsv']
        status_code, _, _ = run_cli_command('newtitles', args)
        assert status_code == 200
        #assert '"status": "titlebasics data added"' in result.stdout

def test_newtitles_invalid_input1():
    args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\name.tsv']
    status_code, _, _ = run_cli_command('newtitles', args)

    assert status_code == 500
    #assert '"this error": "(1054, \\"Unknown column \'nconst\' in \'field list\'\\")"' in result.stderr


def test_newtitles_invalid_input2():
    args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\title.tsv']
    status_code, _, _ = run_cli_command('newtitles', args)
    assert status_code == 500
    #assert '"Duplicate entry' in result.stderr

def test_searchtitle_valid_input():
        args = ['--titlepart','Kleb']
        status_code, _, _ = run_cli_command('searchtitle', args)
        assert status_code == 200

def test_searchtitle_invalid_input():
        args = ['--titlepart','Νύχτα']
        status_code, _, _ = run_cli_command('searchtitle', args)
        assert status_code == 404

def test_title_valid_input():
        args = ['--titleID','tt0000929']
        status_code, _, _ = run_cli_command('title', args)
        assert status_code == 200

def test_title_invalid_input():
        args = ['--titleID', 'tt4444444']
        status_code, _, _ = run_cli_command('title', args)
        assert status_code == 404

def test_searchname_valid_input():
        args = ['--name','Ernst']
        status_code, _, _ = run_cli_command('searchname', args)
        assert status_code == 200

def test_searchname_invalid_input():
        args = ['--name','Areti']
        status_code, _, _ = run_cli_command('searchname', args)
        assert status_code == 404

def test_name_valid_input():
        args = ['--nameid','nm0066941']
        status_code, _, _ = run_cli_command('name', args)
        assert status_code == 200


def test_name_invalid_input():
        args = ['--nameid' ,'nm4444444']
        status_code, _, _ = run_cli_command('name', args)
        assert status_code == 404

def test_bygenre_valid_input():
        args = ['--genre', 'Comedy', '--min', '5', '--from', '1998', '--to', '2030']
        status_code, _, _ = run_cli_command('bygenre', args)
        assert status_code == 200

def test_bygenre_invalid_input():
        args = ['--genre', 'Comedy', '--min', '5', '--from', '2040', '--to', '2050']
        status_code, _, _ = run_cli_command('bygenre', args)
        assert status_code == 404

def test_newnames_valid_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\name.tsv']
        status_code, _, _ = run_cli_command('newnames', args)
        assert status_code == 200

def test_newnames_edge_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\names.tsv']
        status_code, _, _ = run_cli_command('newnames', args)
        assert status_code == 200

def test_aqnewnames_invalid_input1():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\title.tsv']
        status_code, _, _ = run_cli_command('newnames', args)
        assert status_code == 500

def test_newnames_invalid_input2():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\name.tsv']
        status_code, _, _ = run_cli_command('newnames', args)
        assert status_code == 500

def test_newcrew_valid_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\crew.tsv']
        status_code, _, _ = run_cli_command('newcrew', args)
        assert status_code == 200

def test_newcrew_edge_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\crews.tsv']
        status_code, _, _ = run_cli_command('newcrew', args)
        assert status_code == 200

def test_newcrew_invalid_input1():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\title.tsv']
        status_code, _, _ = run_cli_command('newcrew', args)
        assert status_code == 500

def test_newcrew_invalid_input2():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\crew.tsv']
        status_code, _, _ = run_cli_command('newcrew', args)
        assert status_code == 500

def test_newakas_valid_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\aka.tsv']
        status_code, _, _ = run_cli_command('newakas', args)
        assert status_code == 200

def test_newakas_edge_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\akas.tsv']
        status_code, _, _ = run_cli_command('newakas', args)
        assert status_code == 200
    
def test_newakas_invalid_input1():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\title.tsv']
        status_code, _, _ = run_cli_command('newakas', args)
        assert status_code == 500


def test_newakas_invalid_input2():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\aka.tsv']
        status_code, _, _ = run_cli_command('newakas', args)
        assert status_code == 500
        
def test_newepisode_valid_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\episode.tsv']
        status_code, _, _ = run_cli_command('newepisode', args)
        assert status_code == 200

def test_newepisode_edge_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\episodes.tsv']
        status_code, _, _ = run_cli_command('newepisode', args)
        assert status_code == 200

def test_newepisode_invalid_input1():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\title.tsv']
        status_code, _, _ = run_cli_command('newepisode', args)
        assert status_code == 500

def test_newepisode_invalid_input2():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\episode.tsv']
        status_code, _, _ = run_cli_command('newepisode', args)
        assert status_code == 500

def test_newratings_valid_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\rating.tsv']
        status_code, _, _ = run_cli_command('newratings', args)
        assert status_code == 200

def test_newratings_edge_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\ratings.tsv']
        status_code, _, _ = run_cli_command('newratings', args)
        assert status_code == 200

def test_newratings_invalid_input1():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\title.tsv']
        status_code, _, _ = run_cli_command('newratings', args)
        assert status_code == 500

def test_newratings_invalid_input2():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\rating.tsv']
        status_code, _, _ = run_cli_command('newratings', args)
        assert status_code == 500

def test_newprincipals_valid_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\principal.tsv']
        status_code, _, _ = run_cli_command('newprincipals', args)
        assert status_code == 200

def test_newprincipals_edge_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\principals.tsv']
        status_code, _, _ = run_cli_command('newprincipals', args)
        assert status_code == 200

def test_newprincipals_invalid_input1():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\title.tsv']
        status_code, _, _ = run_cli_command('newprincipals', args)
        assert status_code == 500

def test_newprincipals_invalid_input2():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\principal.tsv']
        status_code, _, _ = run_cli_command('newprincipals', args)
        assert status_code == 500

def test_healthcheck():
        status_code, _, _ = run_cli_command('healthcheck', [])
        assert status_code == 200


def test_top10genre():
        status_code, _, _ = run_cli_command('top10genre', [])
        assert status_code == 200

def test_resetall():
    status_code, _, _ = run_cli_command('resetall', [])
    assert status_code == 200

if __name__ == '__main__':
    pytest.main()
