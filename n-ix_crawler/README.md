# github_crawler how-to:

This is a Github crawler which can be used to search Github
repos, issues and wikis using some keywords.

##Installation:

*git clone https://github.com/Rocckk/github_crawler.git*

*cd github_crawler/*

*pip install -r requirements.txt*


## Usage:
The crawler is used from command line and accepts input in JSON format
which is passed to it as a standard input.

The example of an input JSON file can be found in the root directory of the repo (file input.json).

Input file must contain 3 keywords to search for, valid proxies to use for the request and type of Github
entities to search through: Repositories, Issues, Wikis.

The command to start crawler is:

*python github_crawler.py < input.json*

The crawler will search through Github and output the results of search in the file result.json.

For Issues and Wikis search it returns only urls of the pages which match search criteria - for 
Repositories - the result will also show the owner of a repo and the language stats of that repo.


## Testing

The crawler can be tested and test coverage can be measured using the following commands:

*coverage run tests.py*

*coverage report -m github_crawler.py*


