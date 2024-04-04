from urllib.parse import unquote
import re


# From HTML find the First Search Result
def findFirstResult(tag):
    return (tag.name == "div") and (
        tag.find("div", attrs={"data-attrid": "wa:/description"}) is not None
    )


# From HTML find the Related Search Texts
def findRelatedSearches(tag):
    if (
        tag.name != "a"
        or not tag.get("href", "").startswith("/search")
        or tag.has_attr("aria-hidden")
        or tag.find("img")
        or tag.find("g-img")
        or not any(
            child.has_attr("class")
            and ("aXBZVd" in child["class"] or "unhzXb" in child["class"])
            if hasattr(child, "has_attr")
            else False
            for child in tag.children
        )
    ):
        return False

    cleaned_text = re.sub(r"\s+", " ", tag.get_text()).strip()
    if ((cleaned_text == "") or (cleaned_text.replace(" ", "+") not in unquote(
        tag.get("href", "").lower()
    ))):
        return False

    return True



class DataConfig:
    """
    # Description:
    This Object contains the DataConfigs of the Parsing process.
    There are many Parsing rules, we can't add everything in the main file, it will be messy!
    So, we use this Class to store the parsing Rules.

    Why didn't we used Dictionary?
    Cause we can't Access using `config.propertyName` and Get Suggestions of the names when we use Dictionary....

    ## Variables Naming Descriptions:
    - xxxxxxxSearchArgs_connected_N :
        When there is `_connected_` in the variable name, it means with this Search Arg, should be used it's corresponding ParseKey
        Example:
            `answersSearchArgs_connected_01`, with this Search Arg, should be used `answersParseKey_connected_01` this ParseKey
    
    - xxxxxxxSearchArgs_N :
        When a Variable has this format, it means it's
    """

    #### Direct Answer Parsing Configs ####
    answersSearchArgs_01 = {"attrs": {"data-tts": "answers"}}
    """
    It's corresponding ParseKey can be used
    """
    answersParseKey_01 = "data-tts-text"


    answersSearchArgs_02 = {"name": "div", "attrs": {"class": "vk_bk"}}
    """
    It's corresponding ParseKey cannot be used. Need to use `element.get_text()` technic
    """
    answersParseKey_02 = "element.get_text()"


    answersSearchArgs_03 = {"name": "div", "attrs": {"class": "kp-header"}}
    """
    It's corresponding ParseKey cannot be used. Need to use `element.get_text()` technic
    """
    answersParseKey_03 = "element.get_text()"


    #### Search Data Configs ####
    searchResultSearchArgs_01 = {"name": "div", "attrs": {"lang": True, "class": "g"}}
    """
    This does not have any ParseKey, as it searches for the Container Element
    """
    searchResultSearchArgs_02 = {
        "name": "div",
        "attrs": {"data-dsrp": True, "lang": True},
    }
    """
    This does not have any ParseKey, as it searches for the Container Element
    """


    # the Link
    searchResultLinkSearchArgs = {"name": "a", "href": True}
    searchResultLinkParseKey = "href"

    # the Title
    # primarySearchResultTitleSearchArgs = {"name": "h3"}
    searchResultTitleSearchArgs_01 = {"name": "h3"}
    """
    It's corresponding ParseKey cannot be used. Need to use `element.get_text()` technic
    """

    searchResultTitleSearchArgs_02 = {"name": "div", "attrs": {"role": "link"}}
    """
    It's corresponding ParseKey cannot be used. Need to use `element.get_text()` technic
    """

    searchResultTitleSearchArgs_03 = "a (current)"
    """
    Cannot use Directly as a Search Args. Can be used as hint!
    It's corresponding ParseKey cannot be used. Need to use `element.get_text()` technic
    """

    # For Each and every TitleSearchArgs
    searchResultTitleParseKey_all = "element.get_text()"


    # the Description
    searchResultDescriptionSearchArgs_01 = {
        "name": "div",
        "attrs": {"data-snf": "nke7rc", "data-sncf": "1"},
    }
    """
    It's corresponding ParseKey cannot be used. Need to use `element.get_text()` technic
    """

    searchResultDescriptionSearchArgs_02 = {
        "name": "span",
        "attrs": {"class": "hgKElc"},
    }
    """
    It's corresponding ParseKey cannot be used. Need to use `element.get_text()` technic
    """

    searchResultDescriptionParseKey_all = "element.get_text()"


    #### Related Searches Configs ####
    relatedSearchesSearchArgs_01 = {"name": findRelatedSearches}
    """
    It's corresponding ParseKey cannot be used. Need to use `element.get_text()` technic
    """
    relatedSearchesSearchArgs_02 = {
        "name": "div",
        "attrs": {"class": "qR29te", "role": "listitem"},
    }
    """
    It's corresponding ParseKey cannot be used. Need to use `element.get_text()` technic
    """

    relatedSearchesParseKey_all = "element.get_text()"



    ### Peoples Also Ask Configs
    peoplesAlsoAskSearchArgs_01 = {"attrs": {"data-q": True}}
    peoplesAlsoAskQuestionParseKey_01 = "data-q"

    peoplesAlsoAskSearchArgs_02 = {
        "name": "div",
        "attrs": {"class": "dnXCYb", "role": "button"},
    }
    """
    It's corresponding ParseKey cannot be used. Need to use `element.get_text()` technic
    """
    peoplesAlsoAskQuestionParseKey_02 = "element.get_text()"
    

    # the Link
    peoplesAlsoAskLinkSearchArgs = {"name": "a", "href": True}
    peoplesAlsoAskLinkParseKey = "href"

    # the Title
    peoplesAlsoAskTitleSearchArgs = {"name": "h3"}
    peoplesAlsoAskTitleParseKey = "element.get_text()"
    """
    Cannot use Directly as a Parse Key. Can be used as hint!
    """

    # the Description
    peoplesAlsoAskDescSearchArgs = {"attrs": {"data-attrid": "wa:/description"}}
    peoplesAlsoAskDescParseKey = "element.get_text()"
    """
    Cannot use Directly as a Parse Key. Can be used as hint!
    """
