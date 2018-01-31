# @dsanchezseco
import os
import json


CONFIG_FILE="config.json"

class configGenerator(object):
    def __init__(self):
        print "Welcome to the Pull List Config Generator!"
        print ""

        if os.path.isfile(CONFIG_FILE):
            print "Previous config found! Do you wanna..."
            print "1. Add new items to pull list?"
            print "2. Remove item from pull list?"
            print "3. Edit config file?"
            print "\n0. Quit"
            choice = raw_input(" >>  ")
            print
            
            os.system('clear')

            if "1" == choice:
                self.addItems()
            elif "2" == choice:
                self.removeItems()
            elif "3" == choice:
                self.editConfig()
            elif not choice or choice == "0":
                print "May the F=m*a be with you!"
            else:
                print "That functionality doesn't exist yet, bye!"
        else:
            print "No config file found! Let's create a new one..."
            self.create()
    
    def create(self):
        data = {}
        # common attributes for comics
        print "Note: to use the default values just hit INTRO"
        print

        print "download directory (default '<here>/comics')"
        data['download_directory'] = raw_input(" >> ")
        print "sorting order (default 'ascending')"
        data["sorting_order"] = raw_input("[ ascending | descending ] >> ")
        print "conversion (default 'none')"
        data["conversion"] = raw_input("[ cbz | pdf ] >> ")
        print "keep images after conversion (default 'True', forced 'True' if no conversion)"
        data["keep"] = raw_input("[ True | False ] >> ")
        print "image quality (default 'Best')"
        data["image_quality"] = raw_input("[ Best | Low ] >> ")

        # check mandatories and defaults
        if not data["sorting_order"]:
            data["sorting_order"] = "ascending"
        if not data['download_directory']:
            data['download_directory'] = "comics"
        if not data["keep"]:
            data["keep"] = "True"
        if not data["conversion"]:
            data["conversion"] = "None"
            data["keep"] = "True"
        if not data["image_quality"]:
            data["image_quality"] = "Best"


        # add comics
        os.system('clear')
        print "Now the comics :)"
        print "Remember to use the series link not the chapter/issue!"

        data["comics"] = self.genComicsObject()
        os.system('clear')

        # write config file
        json.dump(data, open(CONFIG_FILE, 'w'), indent=4)

        return

    def addItems(self):
        data = json.load(open('config.json'))

        data["comics"].update(self.genComicsObject())

        # write config file
        json.dump(data, open(CONFIG_FILE, 'w'), indent=4)
        return
    
    def editConfig(self):
        data = json.load(open('config.json'))
        while True:
            print "Select field to edit"
            options = {}
            index = 0
            # gen list to choose
            for key, value in data.items():
                options[index] = key
                if not "comics" == key:
                    print str(index)+". "+key+" (actual value: "+data[key]+")"
                    index = index + 1
            print
            choice = raw_input("leave blank to finish >> ")
            if not choice:
                break
            if not int(choice) in options:
                os.system("clear")                
                print "Bad choice, try again!"
                continue
            data[options[int(choice)]] = raw_input("Editing '"+options[int(choice)]+"': "+ data[options[int(choice)]]+" >> ")
            os.system("clear")                
            
        json.dump(data, open(CONFIG_FILE, 'w'), indent=4)
        return

    def removeItems(self):
        data = json.load(open('config.json'))
        comics = data["comics"]
        
        if comics == {}:
            print "No comics!"
            print "Add comics first!!"
            return

        while True:
            print "Select series to remove from pull list"
            options = {}
            index = 0
            # gen list to choose
            for key, value in comics.items():
                options[index] = key
                print str(index)+". "+key+" (next chapter: "+str(value["next"])+")"
                index = index + 1
            
            if not 0 in options:
                print "No more options, bye!"
                break

            print
            choice = raw_input("leave blank to finish >> ")
            if not choice:
                break
            if not int(choice) in options:
                os.system("clear")                
                print "Bad choice, try again!"
                continue
            
            del comics[options[int(choice)]]
            os.system("clear")            
        
        data["comics"] = comics
        json.dump(data, open(CONFIG_FILE, 'w'), indent=4)

    def genComicsObject(self):
        comics = {}
        while True:
            comic = {}
            print "Series link for comics (leave empty to finish)"
            comic["url"] = raw_input(" >> ")
            if not comic["url"]:
                break
            print "Next chapter to download (default 0)"
            comic["next"] = raw_input(" >> ")
            print "Page login username (leave blank if not needed)"
            comic["username"] = raw_input(" >> ")
            print "Page login password (leave blank if not needed)"
            comic["password"] = raw_input(" >> ")
            print "Comic language (default 0)"
            comic["comic_language"] = raw_input(" >> ")

            if not comic["next"]:
                comic["next"] = 0
            else:
                comic["next"] = int(comic["next"])
            if not comic["username"]:
                comic["username"] = "None"
            if not comic["password"]:
                comic["password"] = "None"
            if not comic["comic_language"]:
                comic["comic_language"] = "0"

            comics[comic["url"]] = comic
            os.system('clear')

        return comics
