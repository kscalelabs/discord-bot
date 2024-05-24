"""This is a script to scrape Arxiv."""

import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Any, Dict

import requests


def scrape_arxiv2() -> list[list[str]]:
    base_url = "http://export.arxiv.org/api/query"

    one_week_ago = datetime.now() - timedelta(days=3)
    # start_date_str = one_week_ago.strftime("%Y-%m-%d")
    # end_date_str = datetime.now().strftime("%Y-%m-%d")

    query_params: Dict[str, Any] = {
        "search_query": "all:cs.ro",
        "start": 0,
        "max_results": 3,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    ret_list: list[list[str]] = [[], [], [], [], []]
    response = requests.get(base_url, params=query_params)
    xml_text = response.text
    root = ET.fromstring(xml_text)
    for entry in root.findall(".//{http://www.w3.org/2005/Atom}entry"):
        if entry is None:
            continue
        authors = [""]
        link = "No link found"
        date = "No date found"
        summary = "No summary found"
        title = "No title found"
        for i in range(0, len(entry)):
            if entry[i] is None or entry[i].tag is None:
                continue
            newtag = entry[i].tag.replace("{http://www.w3.org/2005/Atom}", "").strip()
            if newtag == "published":
                curdate_nullable = entry[i].text
                if curdate_nullable is None:
                    continue
                curdate = curdate_nullable[:10]
                date = curdate
                if curdate < str(one_week_ago):
                    return ret_list
            elif newtag == "link":
                link_text = entry[i].attrib.get("href", None)
                if link_text is None:
                    continue
                new_link = link_text.replace("abs", "html", 1)
                if new_link != link_text:
                    link = new_link
            elif newtag == "author":
                author_element = entry[i].find("{http://www.w3.org/2005/Atom}name")
                if author_element is not None and author_element.text is not None:
                    authors.append(author_element.text)
            elif newtag == "summary":
                if entry[i].text is not None:
                    summary = entry[i].text or "No summary found"
            elif newtag == "title":
                if entry[i].text is None:
                    continue
                title = entry[i].text or "No title found"
        authors.pop(0)
        link = link.replace("html", "pdf", 1)
        ret_list[0].append(link.replace("\n ", "").replace("\n", ""))
        ret_list[1].append(date.replace("\n ", "").replace("\n", ""))
        ret_list[2].append(", ".join(authors).replace("\n ", "").replace("\n", ""))
        ret_list[3].append(summary.replace("\n ", "").replace("\n", ""))
        ret_list[4].append(title.replace("\n ", "").replace("\n", ""))
    return ret_list


def main() -> None:
    list = scrape_arxiv2()
    print(list)


if __name__ == "__main__":
    # python -m stompy.scrape_arxiv
    main()
