# Main Imports
from typing import Union
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import warnings

# Configurations
from .configurations import DataConfig as config

# Creating UserAgent Object
useragent = UserAgent()


# Ignoring Warnings
warnings.filterwarnings('ignore')

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
def getHtml(term, lang, num, proxies, timeout):

    res = requests.get(
        url="https://www.google.com/search",
        headers={"User-Agent": useragent.random},
        params={
            "q": term,
            "num": num,
            "hl": lang,
        },
        proxies=proxies,
        verify=(proxies is None),
        timeout=timeout,
    )

    try:
        res.raise_for_status()
    except Exception as e:
        return {
            "success": False,
            "error": "Blocked by Captcha" if res.status_code == 429 else str(e)
        }

    return res.text


# Get Direct Google answer if Exists
def getDirectAnswers(soup: BeautifulSoup):
    """
    ## Description:
    First 3 Methods works when Google parse the Answer by them self and Show them as Answers.

    Fourth Method and onward methods will use the Observed technics which can be used to parse the Answer.
    """
    # First Method - For Direct Answer
    elements = soup.find_all(**config.answersSearchArgs_01)

    directAnswers = []
    for element in elements:
        answer = element[config.answersParseKey_01]
        directAnswers.append(answer)

    # Return if any Answer found
    if len(directAnswers) > 0:
        return directAnswers


    # Fallback for 1st Method - For Direct Answer
    elements = soup.find_all(**config.answersSearchArgs_02)

    directAnswers = []
    for element in elements:
        answer = cleanText(element.get_text())
        directAnswers.append(answer)

    # Return if any Answer found
    if len(directAnswers) > 0:
        return directAnswers

    # Fallback for 2nd Method - For Direct Answer
    elements = soup.find_all(**config.answersSearchArgs_03)

    directAnswers = []
    for element in elements:
        aTag = element.find_all("a")[0]
        answer = cleanText(aTag.get_text())
        directAnswers.append(answer)

    if len(directAnswers) > 0:
        return directAnswers


    # Fallback for 3rd Method - Observed method - 01
    # Seeks for bold tag in the First Description of Search Result. If found, than it's the / an Answer

    element = soup.find(**config.searchResultSearchArgs_01)
    if element is None:
        element = soup.find(**config.searchResultSearchArgs_02)

    if element is None:
        return directAnswers

    descElm = element.find(**config.searchResultDescriptionSearchArgs_01)
    if descElm is None:
        descElm = element.find(**config.searchResultDescriptionSearchArgs_02)

    if descElm is None:
        return directAnswers
    
    answerElms = descElm.find_all("b")
    answer = "".join([x.get_text() for x in answerElms])

    if (len(answer)):
        directAnswers.append(answer)

    return directAnswers


# From div, parse the Title, Link and Description
def parseResultContainerData(element: BeautifulSoup):
    urlElm = element.find(**config.searchResultLinkSearchArgs)
    if (urlElm is None):
        return None
    
    url = cleanUrl(urlElm[config.searchResultLinkParseKey])

    titleElm = urlElm.find(**config.searchResultTitleSearchArgs_01)
    if titleElm is None:
        titleElm = urlElm.find(**config.searchResultTitleSearchArgs_02)

    if titleElm is None:
        titleElm = urlElm

    title = cleanText(titleElm.get_text())

    descElm = element.find(**config.searchResultDescriptionSearchArgs_01)
    if descElm is None:
        descElm = element.find(**config.searchResultDescriptionSearchArgs_02)

    if descElm is not None:
        description = cleanText(descElm.get_text())
    else:
        description = None

    result = {
        "title": title,
        "url": url,
        "description": description,
    }

    return result


# Get The Search Results
def getSearchData(soup: BeautifulSoup):
    searchDataList = []

    elements = soup.find_all(**config.searchResultSearchArgs_01)
    if len(elements) < 3:
        elements += soup.find_all(**config.searchResultSearchArgs_02)
    else:
        elements = elements[1:]

    for element in elements:
        result = parseResultContainerData(element)
        if (result is not None) and (not result["url"].startswith("/search")):
            searchDataList.append(result)

    return searchDataList


# Get Peoples also Ask
def getPeoplesAlsoAsk(soup: BeautifulSoup):
    peoplesAlsoAsk = []
    elements = soup.find_all(**config.peoplesAlsoAskSearchArgs_01)

    for element in elements:
        question = element[config.peoplesAlsoAskQuestionParseKey_01]
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

    if (len(elements) > 0):
        return peoplesAlsoAsk


    elements = soup.find_all(**config.peoplesAlsoAskSearchArgs_02)
    for element in elements:
        question = element.get_text()
        peoplesAlsoAsk.append(question)
    
    return peoplesAlsoAsk


# Get Related Search Results
def getRelatedSearches(soup: BeautifulSoup):
    elements = soup.find_all(**config.relatedSearchesSearchArgs_01)
    if len(elements) == 0:
        elements = soup.find_all(**config.relatedSearchesSearchArgs_02)

    relatedSearches = []
    for element in elements:
        relatedSearch = cleanText(element.get_text())
        relatedSearches.append(relatedSearch)

    return relatedSearches


# Main Function to execute
def search(
    term: str, num_results=5, lang="en", timeout=10, proxy: Union[dict, str, None] = None
):
    """
    ## Description:
    Get Direct Google Answer of Questions, Search Results, Related Searches, Peoples also Ask Queries just by Calling a Single Function!

    ### Parameters:
        term: Your Google Search Term
        num_results: Number of results you want to Parse / Get
        lang: Your Search Language
        timeout: Request Timeout
        proxy: Give your proxy here to Bypass Captcha. You can pass proxy as: `{"https": "https://yourproxy:port.com", "http": "http://yourproxy:port.com"}` , or you can also pass only a proxy as: `https://yourproxy:port.com`. This is Optional...

    ### Note:
        If you use Proxy, try to use Bigger `timeout` number.
    
    ### Suggestion:
        For Proxy, you can use proxy from `https://oxylabs.io`. It works fine!
    
    ### Return:
        Returns a Dictionary containing Data
        If parsing is successful, the `success` will be `True`, else will be `False` and `error` will contain the Error Message
    """

    # Proxy
    proxies = None
    if type(proxy) is str:
        proxy = proxy.replace("https://", "").replace("http://", "")
        proxies = {"https": "https://" + proxy, "http": "http://" + proxy}
    elif type(proxy) is dict:
        proxies = proxy

    num = num_results + 2 # To get Accurate Result
    html = getHtml(term, lang=lang, num=num, proxies=proxies, timeout=timeout)
    if (type(html) is dict): # Error ocurred
        return html

    soup = BeautifulSoup(html, "html.parser")

    directAnswers = getDirectAnswers(soup)
    searchDataList = getSearchData(soup)
    if (len(searchDataList) > num_results):
        searchDataList = searchDataList[:num_results]
    
    relatedSearches = getRelatedSearches(soup)
    peoplesAlsoAsk = getPeoplesAlsoAsk(soup)

    finalResult = {
        "success": True,
        "answer_box": directAnswers,
        "search_results": searchDataList,
        "related_searches": relatedSearches,
        "peoples_also_ask": peoplesAlsoAsk,
    }

    return finalResult
