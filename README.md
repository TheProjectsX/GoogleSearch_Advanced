# Google Search Advanced

Advanced version of Google Search

## Workflow:

- Parse google search HTML from Web
- Use bs4 to Parse the required Data

## Installations:

```bash script
pip install git+https://github.com/TheProjectsX/GoogleSearch_Advanced.git
```

## Uses:

```python
from googlesearch_advanced import search

searchResults = search("What is the latest version of Node JS?")
print(searchResults)
```

### Parameters:

There are several Parameters of the `search` function. You can View them by Hovering in the function from any advanced Code Editor.

## Result:

Returns a Dictionary.

- success: `True` | `False`
- error: If error Happens Error Message will be here
- answer_box: The Direct answers given by Google. If no answer found, Empty List will be returned.
- search_results: The actual search Results. Contains:
  - title: Result Title
  - url: Result URL
  - description: Result Description
- related_searches: Searches Related to given Search Term
- peoples_also_ask: Similar Questions Peoples also Ask

## About:

This Module uses Multiple Parsing Queries to get the Result Accurately.
Uses Single Request Method to Get Results in One Request.

## Motivation:

Wanted to create a Google Searcher which can not only parse the search results, but also the Answer directly given by Google!
