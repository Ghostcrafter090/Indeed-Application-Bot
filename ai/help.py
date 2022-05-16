import pytools
from selenium import webdriver
import os

class globals:
    browser = ""
    exit = False

class sys:
    def start():
        globals.browser = webdriver.Firefox()
    
    class exe:
        def goto(url):
            globals.browser.get(url)

def main():
    sys.start()
    fols = os.listdir(".\\ai\\brain")
    for fol in fols:
        sys.exe.goto("file:///C:/Users/joshp/Desktop/auto_leaptools_apply/ai/brain/" + fol + "/image.jpg")
        json = pytools.IO.getJson(".\\ai\\brain\\" + fol + "\\info.json")
        if (str(json).find(' = -1') == -1) and (str(json).find(': -2') == -1):
            for type in json:
                err = True
                while err:
                    try:
                        conf = "no"
                        while conf != "yes":
                            out = input(type + " is correct? ")
                            conf = "yes"
                            if out == "exit":
                                globals.exit = True
                                exit()
                        if out == "yes":
                            out = -1
                        elif out == "no":
                            out = -2
                        elif out == "1":
                            out = -1
                        elif out == "2":
                            out = -2
                        else:
                            out = int(out)
                        err = False
                    except:
                        if globals.exit:
                            exit()
                        pass
                json[type] = out
            pytools.IO.saveJson(".\\ai\\brain\\" + fol + "\\info.json", json)

main()