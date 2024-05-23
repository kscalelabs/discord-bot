"""Defines a code which scrapes the cs.RO tag on Arxiv and parses the titles from XML."""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import List


def scrape_arxiv2() -> List[List[str]]:

    base_url = "http://export.arxiv.org/api/query"

    one_week_ago = datetime.now() - timedelta(weeks=1)
    start_date_str = one_week_ago.strftime("%Y-%m-%d")
    end_date_str = datetime.now().strftime("%Y-%m-%d")

    query_params = {
        "search_query": "all:humanoid",
        "start": 0,
        "max_results": 10,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    list = [[], [], [], [], []]
    response = requests.get(base_url, params=query_params)
    xml_text = response.text
    root = ET.fromstring(xml_text)
    for entry in root.findall(".//{http://www.w3.org/2005/Atom}entry"):
        authors = []
        link = date = summary = title = ""
        for i in range(0, len(entry)):
            newtag = entry[i].tag.replace("{http://www.w3.org/2005/Atom}", "")
            newtag.strip()
            if newtag == "published":
                curdate = entry[i].text[:10]
                date = curdate
                if curdate < str(one_week_ago):
                    return list
            elif newtag == "link":
                link_text = entry[i].attrib.get("href", None)
                new_link = link_text.replace("abs", "html", 1)
                if new_link != link_text:
                    link = new_link
            elif newtag == "author":
                authors.append(entry[i].find("{http://www.w3.org/2005/Atom}name").text)
            elif newtag == "summary":
                summary = entry[i].text
            elif newtag == "title":
                title = entry[i].text
        list[0].append(link.replace("\n ", "").replace("\n", ""))
        list[1].append(date.replace("\n ", "").replace("\n", ""))
        list[2].append(",".join(authors).replace("\n ", "").replace("\n", ""))
        list[3].append(summary.replace("\n ", "").replace("\n", ""))
        list[4].append(title.replace("\n ", "").replace("\n", ""))
    return list


def main() -> None:
    list = scrape_arxiv2()
    print(list)


if __name__ == "__main__":
    # python -m stompy.scrape_arxiv
    main()
