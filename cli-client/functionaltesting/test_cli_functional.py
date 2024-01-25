import subprocess
import json
import pytest


def run_cli_command(command, args):
    try:
        result = subprocess.run(['python', '-m', 'se2305', command] + args, capture_output=True, text=True, check=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr
    except Exception as e:
        return "", str(e)

#Functional Testing

def test_newtitles_valid_input():
    args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\title.tsv']
    stdout, _ = run_cli_command('newtitles', args)
    expected_text = "status\": \"titlebasics data added"
    assert expected_text in stdout



def test_newtitles_edge_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\titles.tsv']
        stdout, _, = run_cli_command('newtitles', args)
        expected_text = "status\": \"titlebasics data added"
        assert expected_text in stdout


def test_newtitles_invalid_input1():
    args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\name.tsv']
    stdout, _ = run_cli_command('newtitles', args)
    expected_text = 'Adding new titlebasics with filename: C:\\temp\\cli-client\\functionaltesting\\name.tsv\nResponse Status Code: 500\nResponse Content: {\n    "this error": "(1054, \\"Unknown column \'nconst\' in \'field list\'\\")"\n}\n\n'
    assert expected_text in stdout

    
def test_newtitles_missing_argument():
    args = ['--filename']
    stdout, stderr = run_cli_command('newtitles', args)
    expected_error_message = 'usage: se2305.py newtitles [-h] --filename FILENAME\nse2305.py newtitles: error: argument --filename: expected one argument'
    assert expected_error_message in stderr

def test_newtitles_missing_parametre():
    args = []
    stdout, stderr = run_cli_command('newtitles', args)
    expected_error_message = 'usage: se2305.py newtitles [-h] --filename FILENAME\nse2305.py newtitles: error: the following arguments are required: --filename'
    assert expected_error_message in stderr


def test_newtitles_invalid_input2():
    args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\title.tsv']
    stdout, stderr = run_cli_command('newtitles', args)
    expected_error_message = 'Duplicate entry'
    assert expected_error_message in stdout


def test_searchtitle_valid_input():
        args = ['--titlepart','Kleb']
        stdout, _, = run_cli_command('searchtitle', args)
        
        expected_text = 'Searching for titles containing: Kleb'
        assert expected_text in stdout
        expected_text = 'titleID'
        assert expected_text in stdout
        expected_text = 'type'
        assert expected_text in stdout
        expected_text = 'originalTitle'
        assert expected_text in stdout
        expected_text = 'startYear'
        assert expected_text in stdout
        expected_text = 'endYear'
        assert expected_text in stdout
        expected_text = 'genres'
        assert expected_text in stdout
        expected_text = 'titleAkas'
        assert expected_text in stdout
        expected_text = 'akaTitle'
        assert expected_text in stdout
        expected_text = 'regionAbbrev'
        assert expected_text in stdout
        expected_text = 'principals'
        assert expected_text in stdout
        expected_text = 'nameID'
        assert expected_text in stdout
        expected_text = 'name'
        assert expected_text in stdout
        expected_text = 'category'
        assert expected_text in stdout
        expected_text = 'rating'
        assert expected_text in stdout
        expected_text = 'avRating'
        assert expected_text in stdout
        expected_text = 'nVotes'
        assert expected_text in stdout

def test_searchtitle_invalid_input():
        args = ['--titlepart','Νύχτα']
        stdout, _, = run_cli_command('searchtitle', args)
        expected_text = 'Response Content: []'
        assert expected_text in stdout

def test_title_valid_input():
        args = ['--titleID','tt0000929']
        stdout, _ = run_cli_command('title', args)
        expected_text = 'Fetching data for Title ID: tt0000929'
        assert expected_text in stdout
        expected_text = 'titleID'
        assert expected_text in stdout
        expected_text = 'type'
        assert expected_text in stdout
        expected_text = 'originalTitle'
        assert expected_text in stdout
        expected_text = 'startYear'
        assert expected_text in stdout
        expected_text = 'endYear'
        assert expected_text in stdout
        expected_text = 'genres'
        assert expected_text in stdout
        expected_text = 'titleAkas'
        assert expected_text in stdout
        expected_text = 'akaTitle'
        assert expected_text in stdout
        expected_text = 'regionAbbrev'
        assert expected_text in stdout
        expected_text = 'principals'
        assert expected_text in stdout
        expected_text = 'nameID'
        assert expected_text in stdout
        expected_text = 'name'
        assert expected_text in stdout
        expected_text = 'category'
        assert expected_text in stdout
        expected_text = 'rating'
        assert expected_text in stdout
        expected_text = 'avRating'
        assert expected_text in stdout
        expected_text = 'nVotes'
        assert expected_text in stdout

def test_title_invalid_input():
        args = ['--titleID', 'tt4444444']
        stdout, _ = run_cli_command('title', args)
        expected_text = "message\": \"Title not found"
        assert expected_text in stdout

def test_searchname_valid_input():
        args = ['--name','Ernst']
        stdout, _ = run_cli_command('searchname', args)
        expected_text = 'Searching for titles containing: Ernst'
        assert expected_text in stdout
        expected_text = 'nameID'
        assert expected_text in stdout
        expected_text = 'name'
        assert expected_text in stdout
        expected_text = 'namePoster'
        assert expected_text in stdout
        expected_text = 'birthYr'
        assert expected_text in stdout
        expected_text = 'deathYr'
        assert expected_text in stdout
        expected_text = 'profession'
        assert expected_text in stdout
        expected_text = 'nameTitles'
        assert expected_text in stdout
        expected_text = 'titleID'
        assert expected_text in stdout
        expected_text = 'category'
        assert expected_text in stdout

def test_searchname_invalid_input():
        args = ['--name','Areti']
        stdout, _, = run_cli_command('searchname', args)
        expected_text = 'Response Content: []'
        assert expected_text in stdout

def test_name_valid_input():
        args = ['--nameid','nm0066941']
        stdout, _, = run_cli_command('name', args)
        expected_text = 'Fetching data for Professional ID: nm0066941'
        assert expected_text in stdout
        expected_text = 'nameID'
        assert expected_text in stdout
        expected_text = 'name'
        assert expected_text in stdout
        expected_text = 'namePoster'
        assert expected_text in stdout
        expected_text = 'birthYr'
        assert expected_text in stdout
        expected_text = 'deathYr'
        assert expected_text in stdout
        expected_text = 'profession'
        assert expected_text in stdout
        expected_text = 'nameTitles'
        assert expected_text in stdout
        expected_text = 'titleID'
        assert expected_text in stdout
        expected_text = 'category'
        assert expected_text in stdout


def test_name_invalid_input():
        args = ['--nameid' ,'nm4444444']
        stdout, _, = run_cli_command('name', args)
        expected_text = "message\": \"Contributor not found"
        assert expected_text in stdout

def test_bygenre_valid_input():
        args = ['--genre', 'Comedy', '--min', '5', '--from', '1998', '--to', '2030']
        stdout, _, = run_cli_command('bygenre', args)
        expected_text = 'Filtering titles by genre: Comedy, min rating: 5.0, start year: 1998, end year: 2030'
        assert expected_text in stdout
        expected_text = 'titleID'
        assert expected_text in stdout
        expected_text = 'type'
        assert expected_text in stdout
        expected_text = 'originalTitle'
        assert expected_text in stdout
        expected_text = 'titlePoster'
        assert expected_text in stdout
        expected_text = 'startYear'
        assert expected_text in stdout
        expected_text = 'endYear'
        assert expected_text in stdout
        expected_text = 'genres'
        assert expected_text in stdout
        expected_text = 'titleAkas'
        assert expected_text in stdout
        expected_text = 'akaTitle'
        assert expected_text in stdout
        expected_text = 'regionAbbrev'
        assert expected_text in stdout
        expected_text = 'principals'
        assert expected_text in stdout
        expected_text = 'nameID'
        assert expected_text in stdout
        expected_text = 'name'
        assert expected_text in stdout
        expected_text = 'category'
        assert expected_text in stdout
        expected_text = 'rating'
        assert expected_text in stdout
        expected_text = 'avRating'
        assert expected_text in stdout
        expected_text = 'nVotes'
        assert expected_text in stdout


def test_bygenre_invalid_input():
        args = ['--genre', 'Comedy', '--min', '5', '--from', '2040', '--to', '2050']
        stdout, _, = run_cli_command('bygenre', args)
        expected_text = 'Response Content: []'
        assert expected_text in stdout

def test_newnames_valid_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\name.tsv']
        stdout, _, = run_cli_command('newnames', args)
        expected_text = "status\": \"namebasics data added"
        assert expected_text in stdout


def test_newnames_edge_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\names.tsv']
        stdout, _, = run_cli_command('newnames', args)
        expected_text = "status\": \"namebasics data added"
        assert expected_text in stdout

def test_newnames_invalid_input1():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\title.tsv']
        stdout, _, = run_cli_command('newnames', args)
        expected_text = 'Adding new names with filename: C:\\temp\\cli-client\\functionaltesting\\title.tsv\nResponse Status Code: 500\nResponse Content: {\n    "this error": "(1054, \\"Unknown column \'tconst\' in \'field list\'\\")"\n}\n\n'
        assert expected_text in stdout

def test_newnames_invalid_input2():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\name.tsv']
        stdout, _, = run_cli_command('newnames', args)
        expected_text = (
            f'Adding new names with filename: C:\\temp\\cli-client\\functionaltesting\\name.tsv\n'
            f'Response Status Code: 500\n'
            f'Response Content: {{\n'
            f'    "this error": "(1062, \\"Duplicate entry \'nm0000000\' for key \'PRIMARY\'\\")"\n'
            f'}}\n\n'
        )        
        assert expected_text in stdout

def test_newcrew_valid_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\crew.tsv']
        stdout, _ = run_cli_command('newcrew', args)
        expected_text = "status\": \"crew data added"
        assert expected_text in stdout

def test_newcrew_edge_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\crews.tsv']
        stdout, _ = run_cli_command('newcrew', args)
        expected_text = "status\": \"crew data added"
        assert expected_text in stdout

def test_newcrew_invalid_input1():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\title.tsv']
        stdout, _ = run_cli_command('newcrew', args)
        expected_text = 'Adding new crew with filename: C:\\temp\\cli-client\\functionaltesting\\title.tsv\nResponse Status Code: 500\nResponse Content: {\n    "this error": "(1054, \\"Unknown column \'titleType\' in \'field list\'\\")"\n}\n\n'
        assert expected_text in stdout

def test_newcrew_invalid_input2():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\crew.tsv']
        stdout, _ = run_cli_command('newcrew', args)
        expected_text = (
            f'Adding new crew with filename: C:\\temp\\cli-client\\functionaltesting\\crew.tsv\n'
            f'Response Status Code: 500\n'
            f'Response Content: {{\n'
            f'    "this error": "(1062, \\"Duplicate entry \'tt0000000\' for key \'PRIMARY\'\\")"\n'
            f'}}\n\n'
        )        
                
        assert expected_text in stdout

def test_newakas_valid_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\aka.tsv']
        stdout, _ = run_cli_command('newakas', args)
        expected_text = "status\": \"akas data added"
        assert expected_text in stdout


def test_newakas_edge_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\akas.tsv']
        stdout, _ = run_cli_command('newakas', args)
        expected_text = "status\": \"akas data added"
        assert expected_text in stdout
    
def test_newakas_invalid_input1():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\title.tsv']
        stdout, _ = run_cli_command('newakas', args)
        expected_text = 'Adding new akas with filename: C:\\temp\\cli-client\\functionaltesting\\title.tsv\nResponse Status Code: 500\nResponse Content: {\n    "this error": "(1054, \\"Unknown column \'tconst\' in \'field list\'\\")"\n}\n\n'
        assert expected_text in stdout

def test_newakas_invalid_input2():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\aka.tsv']
        stdout, _ = run_cli_command('newakas', args)
        expected_text = (
            f'Adding new akas with filename: C:\\temp\\cli-client\\functionaltesting\\aka.tsv\n'
            f'Response Status Code: 500\n'
            f'Response Content: {{\n'
            f'    "this error": "(1062, \\"Duplicate entry \'tt0000000-1\' for key \'PRIMARY\'\\")"\n'
            f'}}\n\n'
        )        
        assert expected_text in stdout
        
def test_newepisode_valid_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\episode.tsv']
        stdout, _ = run_cli_command('newepisode', args)
        expected_text = "status\": \"episode data added"
        assert expected_text in stdout

def test_newepisode_edge_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\episodes.tsv']
        stdout, _ = run_cli_command('newepisode', args)
        expected_text = "status\": \"episode data added"
        assert expected_text in stdout

def test_newepisode_invalid_input1():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\title.tsv']
        stdout, _ = run_cli_command('newepisode', args)
        expected_text = 'Adding new episodes with filename: C:\\temp\\cli-client\\functionaltesting\\title.tsv\nResponse Status Code: 500\nResponse Content: {\n    "this error": "(1054, \\"Unknown column \'titleType\' in \'field list\'\\")"\n}\n\n'
        assert expected_text in stdout

def test_newepisode_invalid_input2():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\episode.tsv']
        stdout, _ = run_cli_command('newepisode', args)
        expected_text = (
            f'Adding new episodes with filename: C:\\temp\\cli-client\\functionaltesting\\episode.tsv\n'
            f'Response Status Code: 500\n'
            f'Response Content: {{\n'
            f'    "this error": "(1062, \\"Duplicate entry \'tt0000000\' for key \'PRIMARY\'\\")"\n'
            f'}}\n\n'
        )        
        assert expected_text in stdout

def test_newratings_valid_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\rating.tsv']
        stdout, _ = run_cli_command('newratings', args)
        expected_text = "status\": \"ratings data added"
        assert expected_text in stdout

def test_newratings_edge_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\ratings.tsv']
        stdout, _ = run_cli_command('newratings', args)
        expected_text = "status\": \"ratings data added"
        assert expected_text in stdout

def test_newratings_invalid_input1():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\title.tsv']
        stdout, _ = run_cli_command('newratings', args)
        expected_text = 'Adding new ratings with filename: C:\\temp\\cli-client\\functionaltesting\\title.tsv\nResponse Status Code: 500\nResponse Content: {\n    "this error": "(1054, \\"Unknown column \'titleType\' in \'field list\'\\")"\n}\n\n'
        assert expected_text in stdout

def test_newratings_invalid_input2():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\rating.tsv']
        stdout, _ = run_cli_command('newratings', args)
        expected_text = (
            f'Adding new ratings with filename: C:\\temp\\cli-client\\functionaltesting\\rating.tsv\n'
            f'Response Status Code: 500\n'
            f'Response Content: {{\n'
            f'    "this error": "(1062, \\"Duplicate entry \'tt0000000\' for key \'PRIMARY\'\\")"\n'
            f'}}\n\n'
        )        
        assert expected_text in stdout

def test_newprincipals_valid_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\principal.tsv']
        stdout, _ = run_cli_command('newprincipals', args)
        expected_text = "status\": \"principals data added"
        assert expected_text in stdout

def test_newprincipals_edge_input():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\principals.tsv']
        stdout, _ = run_cli_command('newprincipals', args)
        expected_text = "status\": \"principals data added"
        assert expected_text in stdout

def test_newprincipals_invalid_input1():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\title.tsv']
        stdout, _ = run_cli_command('newprincipals', args)
        expected_text = 'Adding new principals with filename: C:\\temp\\cli-client\\functionaltesting\\title.tsv\nResponse Status Code: 500\nResponse Content: {\n    "this error": "(1054, \\"Unknown column \'titleType\' in \'field list\'\\")"\n}\n\n'
        assert expected_text in stdout

def test_newprincipals_invalid_input2():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\principal.tsv']
        stdout, _ = run_cli_command('newprincipals', args)
        expected_text = (
            f'Adding new principals with filename: C:\\temp\\cli-client\\functionaltesting\\principal.tsv\n'
            f'Response Status Code: 500\n'
            f'Response Content: {{\n'
            f'    "this error": "(1062, \\"Duplicate entry \'tt0000000-1\' for key \'PRIMARY\'\\")"\n'
            f'}}\n\n'
        )        
        assert expected_text in stdout

        
def run_help_command():
    result = subprocess.run(['python', 'se2305.py', '--help'], capture_output=True, text=True)
    return result.stdout, result.stderr

def test_help():
    stdout, stderr = run_help_command()
    expected_help_message = (
        'usage: se2305.py [-h] [--format {json,csv}]\n'
        '                 {newnames,newtitles,newakas,newcrew,newepisode,newprincipals,newratings,title,searchtitle,name,bygenre,searchname,top10genre,healthcheck,resetall}\n'
        '                 ...\n\n'
        'CLI for Your Application\n\n'
        'positional arguments:\n'
        '  {newnames,newtitles,newakas,newcrew,newepisode,newprincipals,newratings,title,searchtitle,name,bygenre,searchname,top10genre,healthcheck,resetall}\n'
        '                        Available scopes\n'
        '    newnames            Add new names\n'
        '    newtitles           Add new titles\n'
        '    newakas             Add new akas\n'
        '    newcrew             Add new crew\n'
        '    newepisode          Add new episodes\n'
        '    newprincipals       Add new principals\n'
        '    newratings          Add new ratings\n'
        '    title               Fetch data for a given Title ID\n'
        '    searchtitle         Search for titles\n'
        '    name                Fetch data for a given Professional ID\n'
        '    bygenre             Filter titles by genre, min rating, and optional\n'
        '                        start/end year\n'
        '    searchname          Search for professionals by part of Primary_Name\n'
        '    top10genre          Get top 10 titles in ratings for each genre\n'
        '    healthcheck         Health Check\n'
        '    resetall            Resets the database in the initial data\n\n'
        'options:\n'
        '  -h, --help            show this help message and exit\n'
        '  --format {json,csv}   Specify the output format (json/csv)\n'
    )
    assert expected_help_message in stdout

def test_healthcheck():
        stdout, _ = run_cli_command('healthcheck', [])
        expected_text = "status\": \"OK"
        assert expected_text in stdout
        expected_text = "database\": \"Connected"
        assert expected_text in stdout

def test_top10genre():
        stdout, _, = run_cli_command('top10genre', [])
        expected_text = 'Fetching the top 10 titles in ratings for each genre'
        assert expected_text in stdout
        expected_text = 'titleID'
        assert expected_text in stdout
        expected_text = 'type'
        assert expected_text in stdout
        expected_text = 'originalTitle'
        assert expected_text in stdout
        expected_text = 'titlePoster'
        assert expected_text in stdout
        expected_text = 'startYear'
        assert expected_text in stdout
        expected_text = 'endYear'
        assert expected_text in stdout
        expected_text = 'genres'
        assert expected_text in stdout
        expected_text = 'titleAkas'
        assert expected_text in stdout
        expected_text = 'akaTitle'
        assert expected_text in stdout
        expected_text = 'regionAbbrev'
        assert expected_text in stdout
        expected_text = 'principals'
        assert expected_text in stdout
        expected_text = 'nameID'
        assert expected_text in stdout
        expected_text = 'name'
        assert expected_text in stdout
        expected_text = 'category'
        assert expected_text in stdout
        expected_text = 'rating'
        assert expected_text in stdout
        expected_text = 'avRating'
        assert expected_text in stdout
        expected_text = 'nVotes'
        assert expected_text in stdout


def test_rating_topgenres():
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\newtitle.tsv']
        stdout, _ = run_cli_command('newtitles', args)
        expected_text = "status\": \"titlebasics data added"
        assert expected_text in stdout
        args = ['--filename', 'C:\\temp\\cli-client\\functionaltesting\\test_rating_top10genres.tsv']
        stdout, _ = run_cli_command('newratings', args)
        expected_text = "status\": \"ratings data added"
        assert expected_text in stdout
        stdout, _, = run_cli_command('top10genre', [])
        expected_text = 'Fetching the top 10 titles in ratings for each genre'
        assert expected_text in stdout
        expected_text = "titleID\": \"tt0000001"
        assert expected_text in stdout

def test_resetall():
    stdout, _ = run_cli_command('resetall', [])
    expected_text = "status\": \"Database repopulated successfully"
    assert expected_text in stdout

if __name__ == '__main__':
    pytest.main()
