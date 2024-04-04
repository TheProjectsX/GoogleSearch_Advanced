from urllib.parse import unquote
import re


# From HTML find the First Search Result
def findFirstResult(tag):
    return (tag.name == "div") and (
        tag.find("div", attrs={"data-attrid": "wa:/description"}) is not None
    )


# From HTML find the Related Search Texts
def findRelatedSearches(tag):
    if not (tag.name == "a"):
        return False

    if not (tag.get("href", "").startswith("/search")):
        return False

    if tag.has_attr("aria-hidden"):
        return False

    if tag.find("img") or tag.find("g-img"):
        return False

    if not (
        any(
            (
                (
                    child.has_attr("class")
                    and ("aXBZVd" in child["class"] or "unhzXb" in child["class"])
                )
                if hasattr(child, "has_attr")
                else False
            )
            for child in tag.children
        )
    ):
        return False

    cleaned_text = re.sub(r"\s+", " ", tag.get_text()).strip()
    if cleaned_text == "":
        return

    if not (cleaned_text.replace(" ", "+") in unquote(tag.get("href", "").lower())):
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
    """

    ### Answer Searching Configs
    answersSearchArgs = {"attrs": {"data-tts": "answers"}}
    answersParseKey = "data-tts-text"

    ### Secondary Answer searching Configs
    # Sometimes google gives answer by parsing webpage and sometimes it gives answer via it's AI. The above config is for the Website parsed Answers. And below is of AI answer.
    # How do I know? I just know!
    secondaryAnswersSearchArgs = {"name": "div", "attrs": {"class": "vk_bk"}}
    secondaryAnswersParseKey = "element.get_text()"
    """
    Cannot use Directly as a Parse Key. Can be used as hint!
    """

    ### Tertiary Answer searching Configs
    # I have no Idea how they create this Answer. Obviously using AI, but....
    tertiaryAnswersSearchArgs = {"name": "div", "attrs": {"class": "kp-header"}}
    tertiaryAnswersParseKey = "element.get_text()"
    """
    Cannot use Directly as a Parse Key. Can be used as hint!
    """

    ### Search Data Configs
    # Sometimes when There is direct answer, the top Result's style be different, so using another Rule for that
    searchResultSearchArgs = {"name": "div", "attrs": {"lang": True, "class": "g"}}

    # searchResultSearchArgs = {"name": "div", "attrs": {"lang": True, "class": "g"}}
    secondarySearchResultSearchArgs = {
        "name": "div",
        "attrs": {"data-dsrp": True, "lang": True},
    }

    # the Link
    searchResultLinkSearchArgs = {"name": "a", "href": True}
    searchResultLinkParseKey = "href"

    # the Title
    # If the a contains any h3, than it is the title
    primarySearchResultTitleSearchArgs = {"name": "h3"}
    # The First results sometimes has different format, that's why we are using Top one, which contains the structure of the First Result
    searchResultTitleTopSearchArgs = "a (current)"
    """
    Cannot use Directly as a Search Args. Can be used as hint!
    """
    searchResultTitleSearchArgs = {"name": "div", "attrs": {"role": "link"}}
    searchResultTitleParseKey = "element.get_text()"
    """
    Cannot use Directly as a Parse Key. Can be used as hint!
    """

    # the Description
    # The First results sometimes has different format, that's why we are using Top one, which contains the structure of the First Result
    searchResultDescriptionTopSearchArgs = {
        "name": "span",
        "attrs": {"class": "hgKElc"},
    }

    searchResultDescriptionSearchArgs = {
        "name": "div",
        "attrs": {"data-snf": "nke7rc", "data-sncf": "1"},
    }

    searchResultDescriptionParseKey = "element.get_text()"
    """
    Cannot use Directly as a Parse Key. Can be used as hint!
    """

    ### Related Searches Configs
    relatedSearchesSearchArgs = {"name": findRelatedSearches}
    secondaryRelatedSearchesSearchArgs = {
        "name": "div",
        "attrs": {"class": "qR29te", "role": "listitem"},
    }

    relatedSearchesParseKey = "element.get_text()"
    """
    Cannot use Directly as a Parse Key. Can be used as hint!
    """

    ### Peoples Also Ask Configs
    peoplesAlsoAskSearchArgs = {"attrs": {"data-q": True}}
    secondaryPeoplesAlsoAskSearchArgs = {
        "name": "div",
        "attrs": {"class": "dnXCYb", "role": "button"},
    }
    peoplesAlsoAskQuestionParseKey = "data-q"

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
