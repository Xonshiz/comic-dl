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
            print "2. Edit config file?"
            print "\n0. Quit"
            choice = raw_input(" >>  ")
            print "TODO!"
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
        print "keep images after conversion (default 'True')"
        data["keep"] = raw_input("[ True | False ] >> ")
        print "image quality (default 'Best')"
        data["image_quality"] = raw_input("[ Best | Low ] >> ")

        # check mandatories and defaults
        if not data["sorting_order"]:
            data["sorting_order"] = "ascending"
        if not data['download_directory']:
            data['download_directory'] = os.path.join(os.getcwd(), "comics")
        if not data["conversion"]:
            data["conversion"] = "None"
        if not data["keep"]:
            data["keep"] = "True"
        if not data["image_quality"]:
            data["image_quality"] = "Best"

        # TODO: add comics

        # write config file
        json.dump(data, open(CONFIG_FILE, 'w'), indent=4)

        return
        


# data["comics"]
# el = data["comics"][elKey]
# el["next"]
# el["url"].strip()
# el["username"]
# el["password"],
# el["comic_language"]