#!/usr/bin/env python

import re
import requests

from bs4 import BeautifulSoup


def collect_categories(num_pages):
    categories = set()

    for page in range(1, num_pages + 1):
        res = requests.get("https://github.com/showcases?page=%d" % page)
        categories.update(re.findall(r"\/showcases\/([a-z0-9-]+)", res.text))

    return categories


def collect_showcases(category):
    res = requests.get("https://github.com/showcases/%s" % category)
    soup = BeautifulSoup(res.text, "html.parser")

    for item in soup.find_all(class_="repo-list-item"):
        repo = "https://github.com{0}".format(item.find("h3").find("a").get("href"))

        lang_item = item.find(itemprop="programmingLanguage")
        lang = lang_item.text.strip() if lang_item else "?"

        stars = int(item.find(href=re.compile("stargazers")).text.strip().replace(",", ""))

        forks_item = item.find(href=re.compile("network"))
        forks = int(forks_item.text.strip().replace(",", "")) if forks_item else 0

        yield repo, lang, stars, forks


if __name__ == "__main__":
    categories = collect_categories(4)
    repos = set()

    print("url", "lang", "stars", "forks", sep="\t")

    for category in categories:
        for repo, lang, stars, forks in collect_showcases(category):
            if repo not in repos:
                repos.add(repo)
                print(repo, lang, stars, forks, sep="\t")
