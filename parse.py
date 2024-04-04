# Main Imports
from typing import Union

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re

from configurations import DataConfig as config


useragent = UserAgent()


###### Utility Functions ######
# Clean the Text of Useless Spaces
def cleanText(text: str):
    cleanedText = re.sub(r"\s+", " ", text).strip()
    return cleanedText


# Clean the URL from #:~:text
def cleanUrl(url: str):
    cleanedUrl = url.split("#")[0]
    return cleanedUrl


# Get Search Page HTML
def getHtml(term, lang, proxies, timeout):
    resp = requests.get(
        url="https://www.google.com/search",
        headers={"User-Agent": useragent.random},
        params={
            "q": term,
            "hl": lang,
        },
        proxies=proxies,
        timeout=timeout,
    )

    resp.raise_for_status()
    open("temp.html", "w", encoding="utf-8").write(resp.text)
    return resp.text
    resp = open("temp.html", "r", encoding="utf-8").read()
    return resp


# Get Direct Google answer if Exists
def getDirectAnswers(soup: BeautifulSoup):
    elements = soup.find_all(**config.answersSearchArgs)

    directAnswers = []
    for element in elements:
        answer = element[config.answersParseKey]
        directAnswers.append(answer)

    # If any Answer found, return it. But if not found, we will try to parse the Secondary answer
    if len(directAnswers) > 0:
        return directAnswers

    # Secondary Answers
    elements = soup.find_all(**config.secondaryAnswersSearchArgs)

    directAnswers = []
    for element in elements:
        answer = cleanText(element.get_text())
        directAnswers.append(answer)

    # If any Answer found, return it. But if not found, we will try to parse the Tertiary answer
    if len(directAnswers) > 0:
        return directAnswers

    # Secondary Answers
    elements = soup.find_all(**config.tertiaryAnswersSearchArgs)

    directAnswers = []
    for element in elements:
        aTag = element.find_all("a")[0]
        answer = cleanText(aTag.get_text())
        directAnswers.append(answer)

    if len(directAnswers) > 0:
        return directAnswers

    # And Lastly, if none of them work, we will try to parse it from First Search Result
    elements = soup.find_all(**config.searchResultSearchArgs)
    if len(elements) == 0:
        elements = soup.find_all(**config.secondarySearchResultSearchArgs)

    if len(elements) == 0:
        return directAnswers

    descElm = elements[0].find_all(**config.searchResultDescriptionSearchArgs)
    if len(descElm) == 0:
        descElm = elements[0].find_all(**config.searchResultDescriptionTopSearchArgs)
    if len(descElm) > 0:
        answerElm = descElm[0].find_all("b")

        if len(answerElm) > 0:
            answer = "".join([x.get_text() for x in answerElm])
            directAnswers.append(answer)
            return directAnswers

    return directAnswers


# From div, parse the Title, Link and Description
def parseTitleUrlDesc(element: BeautifulSoup):
    urlElm = element.find_all(**config.searchResultLinkSearchArgs)
    url = cleanUrl(urlElm[0][config.searchResultLinkParseKey])

    titleElm = urlElm[0].find_all(**config.primarySearchResultTitleSearchArgs)
    if len(titleElm) == 0:
        titleElm = urlElm[0].find_all(**config.searchResultTitleSearchArgs)

    if len(titleElm) == 0:
        titleElm = urlElm

    title = cleanText(titleElm[0].get_text())

    descElm = element.find_all(**config.searchResultDescriptionSearchArgs)
    if len(descElm) == 0:
        descElm = element.find_all(**config.searchResultDescriptionTopSearchArgs)

    if len(descElm) > 0:
        description = cleanText(descElm[0].get_text())
    else:
        description = None

    result = {
        "title": title,
        "url": url,
        "description": description,
    }

    return result


# Get The Search Results
def getSearchData(soup: BeautifulSoup, num_results: int):
    searchDataList = []
    # First Check for Top Result
    elements = soup.find_all(**config.searchResultSearchArgs)
    if len(elements) > 0:
        result = parseTitleUrlDesc(elements[0])
        if not result["url"].startswith("/search"):
            searchDataList.append(result)

    elements = soup.find_all(**config.secondarySearchResultSearchArgs)
    if len(elements) < 3:
        elements = soup.find_all(**config.searchResultSearchArgs)

    for element in elements:
        result = parseTitleUrlDesc(element)
        if not result["url"].startswith("/search"):
            searchDataList.append(result)

    return searchDataList


# Get Peoples also Ask
def getPeoplesAlsoAsk(soup: BeautifulSoup):
    peoplesAlsoAsk = []
    elements = soup.find_all(**config.peoplesAlsoAskSearchArgs)

    for element in elements:
        question = element[config.peoplesAlsoAskQuestionParseKey]
        peoplesAlsoAsk.append(question)

        """
        # Below code is used to parse the `Peoples Also Ask` section's Title, Link and Descriptions. But when we don't directly visit the Google and Drop Down the questions, the title, descriptions does not render.
        # So, We can't get them, Yet...
        # But no problem, blue print is ready. We just need to find a way to parse the Full HTML, that's all!


        
        urlElm = element.find_all(**config.peoplesAlsoAskLinkSearchArgs)
        url = urlElm[0][config.peoplesAlsoAskLinkParseKey]


        titleElm = urlElm[0].find_all(**config.peoplesAlsoAskTitleSearchArgs)
        title = cleanText(titleElm[0].get_text())


        descElm = element.find_all(**config.peoplesAlsoAskDescSearchArgs)
        description = cleanText(descElm[0].get_text())

        result = {
            "question": question,
            "title": title,
            "url": url,
            "description": description,
        }

        peoplesAlsoAsk.append(result)
        """

    return peoplesAlsoAsk


# Get Related Search Results
def getRelatedSearches(soup: BeautifulSoup):
    elements = soup.find_all(**config.relatedSearchesSearchArgs)
    if len(elements) == 0:
        elements = soup.find_all(**config.secondaryRelatedSearchesSearchArgs)

    relatedSearches = []
    for element in elements:
        relatedSearch = cleanText(element.get_text())
        relatedSearches.append(relatedSearch)

    return relatedSearches


# Main Function to execute
def search(
    term: str, num_results=5, lang="en", timeout=10, proxy: Union[None, str] = None
):
    # Proxy
    proxies = None
    if proxy:
        proxy = proxy.replace("https://", "").replace("http://", "")
        proxies = {"https": "https://" + proxy, "http": "http://" + proxy}

    html = getHtml(term, lang=lang, proxies=proxies, timeout=timeout)
    soup = BeautifulSoup(html, "html.parser")

    directAnswers = getDirectAnswers(soup)
    searchDataList = getSearchData(soup, num_results=num_results)
    relatedSearches = getRelatedSearches(soup)
    peoplesAlsoAsk = getPeoplesAlsoAsk(soup)

    finalResult = {
        "answer_box": directAnswers,
        "search_results": searchDataList,
        "related_searches": relatedSearches,
        "peoples_also_ask": peoplesAlsoAsk,
    }

    return finalResult


# Test The Module
def main():
    import sys

    try:
        query = sys.argv[1]
    except:
        query = input("Enter Search Query:> ")

    print("\n")
    searchResults = search(query)
    if len(searchResults["answer_box"]) > 0:
        print("Direct Ans:", searchResults["answer_box"][0])

    print("\n------------- Search Results -------------\n")
    for result in searchResults["search_results"]:
        print("\nURL:", result["url"])
        print("Title:", result["title"])
        print("Desc:", result["description"][:200])

    print("\n------------- Related Searches -------------\n")
    print(" || ".join(searchResults["related_searches"]))

    print("\n------------- Peoples Also Ask -------------\n")
    print(" || ".join(searchResults["peoples_also_ask"]))


if __name__ == "__main__":
    main()
    # print(search(""))
