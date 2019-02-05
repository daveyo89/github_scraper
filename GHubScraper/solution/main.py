import bs4 as bs
import urllib.request
import requests
import csv
import traceback
from tqdm import tqdm
import time
import argparse
import os
import sys

"""The code is heavily commented due to it being a "homework" and all. If something is still not clear, don't worry,
    it is obviously my fault. For manual testing besides the default github scraping I used mine, I encourage you,
    to try it on yours as well. If I did well here, it is harder to produce an error than a result. 
    Enjoy! """


class Main:
    # Get number of pages at initialisation (was not part of task, but no errors with valid github page.)
    # I know __init__ is a bit too long like this, but I choose this solution to make the class ready-to-use as soon as
    # it is instantiated.

    # If you don't want to use defaults, give github username to url parameter like so: Main(url="githubusername")
    # or url=https://github.com/githubusername.
    def __init__(self, username="github", output_file="results.csv"):

        if username is not None and len(str(username)) > 1:
            self.username = username.strip()
        # Check if user comes from python console:
        if ap.prog != os.path.basename(__file__) and args['name'] is None:
            args['name'] = "github"
            # On win cmd this puts the results to solution/GHubScraper/results/
            self.file_path = os.getcwd() + "/GHubScraper/solution/results/"
        elif ap.prog != os.path.basename(__file__):
            self.file_path = os.getcwd() + "/GHubScraper/solution/results/"

        else:
            self.file_path = os.getcwd() + "/results/"

        # If we have a name from argparse or default.
        if args['name'] is not None:
            self.username = args['name'].strip()

        # Get arg or default.
        if args['file'] is not None:
            self.output_file = args['file'].strip()
        else:
            self.output_file = output_file
        # Init total pages here to silence minor errors on the side.
        self.total_pages = 1

    def __str__(self):
        # In case someone is deeply curious.
        return f"Getting info from the repositories of this user: {str(self.username)}, saving them to " \
            f"{str(self.output_file)}"

    def __repr__(self):
        return f"Default user: github\nCurrent user: {str(self.username)}\nCurrent target filename: {self.output_file}"

    def check_url(self):
        url = f"https://github.com/{str(self.username)}?page=1"

        # In case of a non-existent user or a bad url we ask for new input.
        if self.username is None or requests.head(url).status_code >= 300:
            while requests.head(url).status_code >= 300:
                # Get new username by input.
                new_username = str(input("Enter valid username or leave blank for default. (github/github)")).strip()
                if new_username == "":
                    new_username = "github"
                url = "https://github.com/" + new_username + "?page=1"
                # Preparing multi page compatibility with given username.
            self.username = url[:-1]
            return url
        else:
            # Preparing multi page comp. with url.
            self.username = url[:-1]
            return url

    def get_first_page(self):
        # Url we get back will surely be valid github url.
        url = self.check_url()
        output_file = self.output_file

        # Read url.
        sauce = urllib.request.urlopen(url).read()

        # Couldn't think of a better, or more efficient way to get max page number,
        #     however task was only for github/github so it could've been 10.
        total_pages = bs.BeautifulSoup(sauce, 'html.parser').find('em', {'data-total-pages': [int]})

        if total_pages is not None:
            # If target user has less than two pages of repositories, data-total-pages will be non-existent in html.
            self.total_pages = int(total_pages.get('data-total-pages'))
        else:
            # Github pages work with github/"username?page=1" even if there is only 1 page.
            self.total_pages = 1
        # Make sure output file has .csv extension.
        if self.output_file[-4:] != ".csv":
            self.output_file += ".csv"

        os.makedirs(self.file_path, exist_ok=True)
        # Excessive use of utf-8 encoding prevents encoding errors.
        # Also had to change pycharm default encoding settings to utf-8, but it's a windows only thing as far as I know.
        with open(f"{self.file_path}{self.output_file}", 'w', encoding="utf-8", newline='') as f:
            wr = csv.writer(f)
            # Make sure we delete existing results plus adding column names in first row.
            wr.writerow(["name", "description", "language", "tags"])

        print("\nGit scraper initialised, ready for duty!")
        print(f"URL: {url}\nTotal pages: {self.total_pages}\nOutput filename: {output_file}\n")
        # Little time so the user can read printed info.
        time.sleep(1.5)

    def scraping(self):
        print("Scraping sequence activated...\n")

        # Progress bar because it's fancy and useful. I Love Progressbar.
        for i in tqdm(range(self.total_pages)):
            if self.total_pages == 1:
                # Take away ?page= from url to replace it with repositories seen below.
                url = self.username[:-5] + "tab=repositories"
            else:
                # Or adding ?page=n to url.
                url = self.username + f"{str(i + 1)}"

            # Scraping starts here with the prepared url.
            sauce = urllib.request.urlopen(url).read()
            soup = bs.BeautifulSoup(sauce, 'html.parser')
            # Get all repository blocks and iterate by divs.
            for div in soup.find_all('li', {'itemprop': ['owns']}):
                try:
                    tags = []
                    # In each div we look for the info we need.
                    repo_name = div.find('a', {'itemprop': ['name codeRepository']}).text.strip()

                    for tag in div.find_all('a', {'class': ['topic-tag topic-tag-link f6 my-1']}):
                        if tag is not None:
                            tags.append(tag.text.strip())
                        else:
                            tags.append(" ")

                    repo_desc = div.find('p', {'itemprop': ['description']})
                    if repo_desc is not None:
                        repo_desc = repo_desc.text.strip()
                    else:
                        repo_desc = " "

                    repo_lang = div.find('span', {'itemprop': ['programmingLanguage']})
                    if repo_lang is not None:
                        repo_lang = repo_lang.text.strip()
                    else:
                        repo_lang = " "
                    # Put findings in a list.
                    results = [repo_name, repo_desc, repo_lang, tags]
                    # Then write it as a line.
                    with open(f"{self.file_path}{self.output_file}", 'a', encoding="utf-8", newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(results)
                    # Using 'with' statement makes sure we close resources after use.

                    # Uncomment to see data flowing in on console.
                    # print(
                    #     f"\n Repo name: {repo_name}\n Short description: {repo_desc}\n"
                    #     f" Programming Language: {repo_lang}\n Tags: {tags}\n")

                except (UnicodeEncodeError, TypeError) as e:
                    traceback.print_exc(e)
                    continue


while True:
    # Argparse catches given arguments within cmd/terminal, also "ap.prog" will equal given parameter from python shell,
    # making it losing its name "main". I couldn't find an elegant workaround yet, so I use it now as an indicator
    # that someone is trying to give arguments through shell commands.. Please contact me if you have a solution.
    ap = argparse.ArgumentParser()

    ap.add_argument("-n", "--name", required=False,
                    help="Github username.")
    ap.add_argument("-f", "--file", required=False,
                    help="Output filename.")

    args, unknown = ap.parse_known_args()
    args = vars(args)

    # args = vars(ap.parse_args())
    # input("Press Enter to start David's github scraper : ")
    print("Starting scraper....\n")
    time.sleep(2.0)

    main = Main()
    main.get_first_page()
    main.scraping()
    print(f"\nScraping finished, please find your results in \"{main.output_file}\"")
    time.sleep(1.5)
    break
