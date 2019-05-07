# @Christ-oo

import json
import sys

class ReadComicOnline():
    def __init__ (self):
        self.data = ""

        #Check if rco-data.json exists
        try:
            with open("rco-data.json", "r") as f:
                self.data = json.load(f)
                #data = f.read()
        except Exception as e:
            print("An error occurred : {}".format(e))
            print("Download the data from {}".format("https://drive.google.com/open?id=1eOjwOQx_LHericcowyBRNIJtZZGMKlp6"))
            print("And paste it inside the comic-dl/comic_dl directory")

    def comicSearch(self, search_query):
        search_query = str(search_query).strip()
        results = []

        for i in self.data["comics"]:
            if str(search_query) in str(i["name"]):
                results.append({
                    "id": i["no"], "name": i["name"]
                })
        
        if results:
            print("Search results for {}. Found {} results.".format(search_query, len(results)))
            print("\nComic ID\tComic Name")
            print("----------------------------------------------------------")

            for result in results:
                print("{}\t\t{}".format(result["id"], result["name"]))
            
            print("----------------------------------------------------------")
        else:
            print("No comic found with that name or id.")
            print("If you are inputting an ID, use -comic-search <QUERY> to determine the id.")
            print("If you are inputting a name, you must input the exact name of the comic for ")

    def comicLink(self, query):
        result = ""

        if str(query).isdigit():
            print("You inputted a Comic ID")

            comic_id = int(str(query).strip())
            for i in self.data["comics"]:
                if comic_id == i["no"]:
                    result = i["link"]
                    break
        else:
            print("You inputted a Comic Name")

            comic_name = str(query).strip()
            for i in self.data["comics"]:
                if comic_name == i["name"]:
                    result = i["link"]
                    break
        
        if result:
            return result
        else:
            return None

    def comicInfo(self, query):
        result = {}

        if str(query).isdigit():
            print("You inputted a Comic ID")

            comic_id = int(str(query).strip())
            for i in self.data["comics"]:
                if comic_id == i["no"]:
                    result = i
                    break
        else:
            print("You inputted a Comic Name")

            comic_name = query.strip()
            for i in self.data["comics"]:
                if comic_name == i["name"]:
                    result = i
                    break
         
        if result:
            print("Comic Information------------------------------------------")
            print("""Information gathered from readcomiconline.to as of {}
ID                  :   {}
Name                :   {}
Genres              :   {}
Publisher           :   {}
Writer(s)           :   {}
Artist(s)           :   {}
Publication Date    :   {}
Status              :   {}
No. of Issues       :   {}
Link                :   {}
Summary
{}
                """.format(
                self.data["dateCreated"],
                result["no"],
                result["name"],
                ", ".join(result["genres"]),
                ", ".join(result["publisher"]),
                ", ".join(result["writer"]),
                ", ".join(result["artist"]),
                result["publicationDate"],
                result["status"],
                result["numOfChapters"],
                result["link"],
                result["summary"],
            ))
        else:
            print("No comic found with that name or id.")
            print("If you are inputting an ID, use -comic-search <QUERY> to determine the id.")
            print("If you are inputting a name, you must input the exact name of the comic for ")
