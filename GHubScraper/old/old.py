import bs4 as bs
import urllib.request
import csv
import traceback


def max_page():

    url = f"https://github.com/github?page={1}"
    sauce = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(sauce, 'html.parser')
    total_pages = soup.find('em', {'data-total-pages': [int]}).get('data-total-pages')
    return int(total_pages)


def git_scraper(page):
    url = f"https://github.com/github?page={str(page)}"

    sauce = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(sauce, 'html.parser')
    for div in soup.find_all('li', {'itemprop': ['owns']}):
        try:
            reps = []
            repo_name = div.find('a', {'itemprop': ['name codeRepository']}).text.strip()

            for r in div.find_all('a', {'class': ['topic-tag topic-tag-link f6 my-1']}):
                if r is not None:
                    reps.append(r.text.strip())

            repo_desc = div.find('p', {'itemprop': ['description']})
            if repo_desc is not None:
                repo_desc = repo_desc.text.strip()
            pr_lang = div.find('span', {'itemprop': ['programmingLanguage']})
            if pr_lang is not None:
                pr_lang = pr_lang.text.strip()

            results = [repo_name, repo_desc, pr_lang, reps]
            with open("results.csv", 'a', encoding="utf-8", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(results)

            print(" Repo name: {0}\n Short description: {1}\n Programming Language: {2}\n Repo tags: {3}\n".format(
                repo_name, repo_desc, pr_lang, reps))

        except (UnicodeEncodeError, TypeError) as e:
            traceback.print_exc()
            continue


if __name__ == '__main__':
    with open('results.csv', 'w', encoding="utf-8", newline='') as f:
        wr = csv.writer(f)
        wr.writerow(["name", "description", "language", "tags"])
    j = max_page()
    for i in range(j):
        git_scraper(i+1)
    print("\n\t ### Writing to results.csv completed.. ###")
