# @Chr1st-oo

import json
import cloudscraper
import requests
import sys
import re
from bs4 import BeautifulSoup
from datetime import date

class RCOUpdater():
    def __init__ (self, link=None, name=None):
        self.BASE = "https://readcomiconline.li/Comic/"
        self.link = link

        if name:
            self.link = self.BASE + self.nameLink(str(name).strip())

        self.session = requests.session()
        self.scraper = cloudscraper.create_scraper(sess=self.session)

        self.data = ""
        try:
            self.data = json.load(open("rco-data.json", "r"))
        except Exception as e:
            print("An error occurred : {}".format(repr(e)))
            print("Download the data from {}".format("https://drive.google.com/open?id=1eOjwOQx_LHericcowyBRNIJtZZGMKlp6"))
            print("And paste it inside the comic-dl/comic_dl directory")
            sys.exit()

        if self.link:
            try:
                soup = BeautifulSoup(
                    self.scraper.get(self.link).content,
                    "html.parser"
                )

                divs = soup.find_all("div", {"class": "content space-top"})

                #TOP
                name = divs[0].find("div", {"class": "content_top red"}).text.strip()
                infos = divs[0].find("div", {"class": "col info"}).find_all("p")

                #BOTTOM
                issues = divs[1].find("ul", {"class": "list"}).find_all("li")

                print("You want to add {} in the database. Checking if it already exist.".format(name))
                cid = int(self.alreadyExists(name))

                summary = "N/A"

                try:
                    summaryBox = divs[0].find_all("div", {"class" : "section group"})[1]
                    summary = summaryBox.text.strip()
                except:
                    pass

                if cid:
                    print("{} already exists in the database. Trying to update its details...".format(name))
                    self.data["comics"][cid - 1]["name"] = name
                    self.data["comics"][cid - 1]["genres"] = self.getGenre(infos[0])
                    self.data["comics"][cid - 1]["numOfChapters"] = self.getNumOfChapters(issues)
                    self.data["comics"][cid - 1]["publisher"] = self.getPublisher(infos[1])
                    self.data["comics"][cid - 1]["writer"] = self.getWriter(infos[2])
                    self.data["comics"][cid - 1]["artist"] = self.getArtist(infos[3])
                    self.data["comics"][cid - 1]["publicationDate"] = self.getPublicationDate(infos[4]).strip()
                    self.data["comics"][cid - 1]["status"] = self.getStatus(infos[5]).strip()
                    self.data["comics"][cid - 1]["summary"] = summary
                    self.data["comics"][cid - 1]["link"] = self.link
                else:
                    cid = int(self.getLastId(name)) + 1
                    print("{} does not exist in the database. Adding it to the database...".format(name))
                    newComic = {
                        "no": cid,
                        "name": name,
                        "genres": self.getGenre(infos[0]),
                        "numOfChapters": self.getNumOfChapters(issues),
                        "publisher": self.getPublisher(infos[1]),
                        "writer": self.getWriter(infos[2]),
                        "artist": self.getArtist(infos[3]),
                        "publicationDate": self.getPublicationDate(infos[4]).strip(),
                        "status": self.getStatus(infos[5]).strip(),
                        "summary": summary,
                        "link": self.link
                    }

                    self.data["comics"].append(newComic)
                    self.data["last"] = {
                        "no": self.data["comics"][-1]["no"], "name": self.data["comics"][-1]["name"], "dateAdded": date.today().strftime("%d/%m/%Y")
                    }

                with open("rco-data.json", "w") as out:
                    json.dump(self.data, out, indent=2)

                print("Database updated successfully...")
            except Exception as e:
                print("The link is not available, perhaps you provided an invalid link or name.")
                sys.exit()

    def getLastId(self, name):
        return self.data["last"]["no"]

    def nameLink(self, name):
        return re.sub(r"[^A-Z|^a-z|\-|^0-9]", "", name.replace(" ", "-"))

    def alreadyExists(self, name):
        for datum in self.data["comics"]:
            if name == datum["name"]:
                return datum["no"]

        return False

    def getGenre(self, el):
        try:
            genres = []

            g = el.find_all("a")

            for genre in g:
                genres.append(genre.text)

            return genres
        except:
            return ["N/A"]

    def getPublisher(self, el):
        try:
            publishers = []

            p = el.find_all("a")

            for publisher in p:
                publishers.append(publisher.text)

            return publishers
        except:
            return ["N/A"]

    def getWriter(self, el):
        try:
            writers = []

            w = el.find_all("a")

            for writer in w:
                writers.append(writer.text)

            return writers
        except:
            return ["N/A"]

    def getArtist(self, el):
        try:
            artists = []

            a = el.find_all("a")

            for artist in a:
                artists.append(artist.text)

            return artists
        except:
            return ["N/A"]

    def getPublicationDate(self, el):
        try:
            return el.text.replace("Publication date:", "")
        except:
            "N/A"

    def getStatus(self, el):
        try:
            return el.text.replace("Status:", "")
        except:
            return "N/A"

    def getNumOfChapters(self, el):
        try:
            return len(el)
        except:
            return "N/A"
