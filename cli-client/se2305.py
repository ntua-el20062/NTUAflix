import argparse
import csv
import mysql.connector
import codecs
import requests

BASE_URL = "http://127.0.0.1:9876//ntuaflix_api"

def healthcheck():
        response = requests.get(f"{BASE_URL}/admin/healthcheck")
    
        # Print the response status code and content
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        return response
def resetall():
        response = requests.post(f"{BASE_URL}/admin/resetall")
    
        # Print the response status code and content
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        return response 
def top10genre():
    print("Fetching the top 10 titles in ratings for each genre.")
    response = requests.get(f"{BASE_URL}/top10bygenre")
    
    # Print the response status code and content
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    return response


def searchname(args):
    print(f"Searching for professionals with Primary_Name containing: {args.name}")
    print(f"Searching for titles containing: {args.name}")
    response = requests.get(f"{BASE_URL}/searchname", params={'namePart': args.name})
    
        # Print the response status code and content
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    return response
    


def name(args):
    print(f"Fetching data for Professional ID: {args.nameid}")
    response = requests.get(f"{BASE_URL}/name/{args.nameid}")
    
        # Print the response status code and content
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    return response

   

    

def bygenre(args):
    print(f"Filtering titles by genre: {args.genre}, min rating: {args.min}, start year: {args.yrFrom}, end year: {args.yrTo}")
    # Assuming that your API endpoint for by_genre is '/bygenre'
    response = requests.get(f"{BASE_URL}/bygenre", params={
        'qgenre': args.genre,
        'minrating': args.min,
        'yrFrom': args.yrFrom,
        'yrTo': args.yrTo
    })
    
    # Print the response status code and content
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    return response
   
def searchtitle(args):
    print(f"Searching for titles containing: {args.titlepart}")
    response = requests.get(f"{BASE_URL}/searchtitle", params={'titlePart': args.titlepart})
    
        # Print the response status code and content
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    return response
    

def title(args):
    print(f"Fetching data for Title ID: {args.titleID}")
    response = requests.get(f"{BASE_URL}/title/{args.titleID}")
    
        # Print the response status code and content
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    return response

    
def newratings(args):
    print(f"Adding new ratings with filename: {args.filename}")

     # Assuming args.filename contains the path to the file or the file content
    with open(args.filename, 'r', encoding='utf-8') as file:
        tsv_data = file.read()

    # Make the POST request
    response = requests.post(f"{BASE_URL}/admin/upload/titleratings", files={"tsv_title_ratings": tsv_data})

    # Print the response status code and content
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    return response

def newprincipals(args):
    print(f"Adding new principals with filename: {args.filename}")
    
    # Assuming args.filename contains the path to the file or the file content
    with open(args.filename, 'r', encoding='utf-8') as file:
        tsv_data = file.read()

    # Make the POST request
    response = requests.post(f"{BASE_URL}/admin/upload/titleprincipals", files={"tsv_title_principal": tsv_data})

    # Print the response status code and content
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    return response

def newepisode(args):
    print(f"Adding new episodes with filename: {args.filename}")
    
    # Assuming args.filename contains the path to the file or the file content
    with open(args.filename, 'r', encoding='utf-8') as file:
        tsv_data = file.read()

    # Make the POST request
    response = requests.post(f"{BASE_URL}/admin/upload/titleepisode", files={"tsv_title_episode": tsv_data})

    # Print the response status code and content
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    return response

def newcrew(args):
    print(f"Adding new crew with filename: {args.filename}")

     # Assuming args.filename contains the path to the file or the file content
    with open(args.filename, 'r', encoding='utf-8') as file:
        tsv_data = file.read()

    # Make the POST request
    response = requests.post(f"{BASE_URL}/admin/upload/titlecrew", files={"tsv_title_crew": tsv_data})

    # Print the response status code and content
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    return response
def newakas(args):
    print(f"Adding new akas with filename: {args.filename}")

     # Assuming args.filename contains the path to the file or the file content
    with open(args.filename, 'r', encoding='utf-8') as file:
        tsv_data = file.read()

    # Make the POST request
    response = requests.post(f"{BASE_URL}/admin/upload/titleakas", files={"tsv_aka": tsv_data})

    # Print the response status code and content
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    return response
def newtitles(args):
    print(f"Adding new titlebasics with filename: {args.filename}")

     # Assuming args.filename contains the path to the file or the file content
    with open(args.filename, 'r', encoding='utf-8') as file:
        tsv_data = file.read()

    # Make the POST request
    response = requests.post(f"{BASE_URL}/admin/upload/titlebasics", files={"tsv_title_basics": tsv_data})

    # Print the response status code and content
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    return response

def newnames(args):
    print(f"Adding new names with filename: {args.filename}")
    
    # Assuming args.filename contains the path to the file or the file content
    with open(args.filename, 'r', encoding='utf-8') as file:
        tsv_data = file.read()

    # Make the POST request
    response = requests.post(f"{BASE_URL}/admin/upload/namebasics", files={"tsv_name_basics": tsv_data})

    # Print the response status code and content
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    return response
def main():
    parser = argparse.ArgumentParser(description='CLI for Your Application')
    subparsers = parser.add_subparsers(dest='scope', help='Available scopes')

    # Subparser for 'newnames' scope
    newnames_parser = subparsers.add_parser('newnames', help='Add new names')
    newnames_parser.add_argument('--filename', required=True, help='Specify filename')

     # Subparser for 'newtitles' scope
    newtitles_parser = subparsers.add_parser('newtitles', help='Add new titles')
    newtitles_parser.add_argument('--filename', required=True, help='Specify filename')

    # Subparser for 'newakas' scope
    newakas_parser = subparsers.add_parser('newakas', help='Add new akas')
    newakas_parser.add_argument('--filename', required=True, help='Specify filename')

     # Subparser for 'newcrew' scope
    newcrew_parser = subparsers.add_parser('newcrew', help='Add new crew')
    newcrew_parser.add_argument('--filename', required=True, help='Specify filename')

    # Subparser for 'newepisode' scope
    newepisode_parser = subparsers.add_parser('newepisode', help='Add new episodes')
    newepisode_parser.add_argument('--filename', required=True, help='Specify filename')

     # Subparser for 'newprincipals' scope
    newprincipals_parser = subparsers.add_parser('newprincipals', help='Add new principals')
    newprincipals_parser.add_argument('--filename', required=True, help='Specify filename')

     # Subparser for 'newratings' scope
    newratings_parser = subparsers.add_parser('newratings', help='Add new ratings')
    newratings_parser.add_argument('--filename', required=True, help='Specify filename')

    
    # Subparser for 'title' scope
    title_parser = subparsers.add_parser('title', help='Fetch data for a given Title ID')
    title_parser.add_argument('--titleID', required=True, help='Specify title_id')

    # Subparser for 'searchtitle' scope
    searchtitle_parser = subparsers.add_parser('searchtitle', help='Search for titles')
    searchtitle_parser.add_argument('--titlepart', required=True, help='Specify the search query')

    # Subparser for 'name' scope
    name_parser = subparsers.add_parser('name', help='Fetch data for a given Professional ID')
    name_parser.add_argument('--nameid', required=True, help='Specify Professional_id')  

    # Subparser for 'bygenre' scope
    bygenre_parser = subparsers.add_parser('bygenre', help='Filter titles by genre, min rating, and optional start/end year')
    bygenre_parser.add_argument('--genre', required=True, help='Specify genre')
    bygenre_parser.add_argument('--min', required=True, type=float, help='Specify minimum rating')
    bygenre_parser.add_argument('--from', dest='yrFrom', type=int, help='Specify start year (optional)')
    bygenre_parser.add_argument('--to', dest='yrTo', type=int, help='Specify end year (optional)')

    # Subparser for 'searchname' scope
    searchname_parser = subparsers.add_parser('searchname', help='Search for professionals by part of Primary_Name')
    searchname_parser.add_argument('--name', required=True, help='Specify part of Primary_Name')
    
    # Subparser for 'top10genre' scope
    top10genre_parser = subparsers.add_parser('top10genre', help='Get top 10 titles in ratings for each genre')
    
    # Subparser for 'healtcheck' scope
    healthcheck_parser = subparsers.add_parser('healthcheck', help='Health Check')

    # Subparser for 'resetall' scope
    resetall_parser = subparsers.add_parser('resetall', help='Resets the database in the initial data')
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Specify the output format (json/csv)")

    args = parser.parse_args()

    if args.scope == 'newnames':
        newnames(args)
    elif args.scope == 'newtitles':
        newtitles(args)
    elif args.scope == 'newakas':
        newakas(args)
    elif args.scope == 'newcrew':
        newcrew(args)
    elif args.scope == 'newepisode':
        newepisode(args)
    elif args.scope == 'newprincipals':
        newprincipals(args)
    elif args.scope == 'newratings':
        newratings(args)
    elif args.scope == 'title':
        title(args)
    elif args.scope == 'searchtitle':
        searchtitle(args)
    elif args.scope == 'bygenre':
        bygenre(args)
    elif args.scope == 'name':
        name(args)
    elif args.scope == 'searchname':
        searchname(args)
    elif args.scope == 'top10genre':
        top10genre(args)
    elif args.scope == 'healthcheck':
        result = healthcheck()
    elif args.scope == 'resetall':
        result = resetall()
        print(result)

if __name__ == '__main__':
    main()
