from jinja2 import Undefined
from psutil import users
from selenium import webdriver
import random
import time
import os
import pytools # note: pytools is my own python library, to use it, download it here: https://github.com/Ghostcrafter090/pytools
import sys

# Globals
class globals:
    broswer = '' # allows access to browser driver at all levels of application
    user = ""
    passwd = ""

# Sys class, contains main components
class sys:
    def start():
        globals.browser = webdriver.Firefox()

    # Used for signing in, requires user interaction in the form of verification and recapcha
    def signin(username, password):
        globals.browser.get("https://secure.indeed.com/auth?hl=en_CA&co=CA&continue=https%3A%2F%2Fca.indeed.com%2Fcmp%2FLeap-Tools-Inc.-1%2Fjobs%3Fjk%3D562c7031db35aae8%26start%3D0%26clearPrefilter%3D1&tmpl=desktop&from=gnav-util-acme--acme-webapp&_ga=2.205514322.358284476.1651172242-1342485949.1651172242")
        # Type email
        email_input = globals.browser.find_element_by_css_selector('input[name=__email]')
        email = username
        for letter in email:
            print(letter)
            email_input.send_keys(letter)
            wait_time = random.randint(0,500)/10000
            time.sleep(wait_time)
        # Click next
        next_button = globals.browser.find_elements_by_css_selector("button[type=submit]")
        time.sleep(1)
        next_button[0].click()
        time.sleep(1)
        password_input = globals.browser.find_element_by_css_selector('input[name=__password]')
        for letter in password:
            print(letter)
            password_input.send_keys(letter)
            wait_time = random.randint(0,500)/10000
            time.sleep(wait_time)
        next_button = globals.browser.find_elements_by_css_selector("button[type=submit]")
        time.sleep(1)
        next_button[0].click()
        time.sleep(1)

    # contains primary functions of the bot, main actions used based on criteria are stored here.
    class funcs:
        def apply(job):
            job.find_elements_by_css_selector("button")[0].click()
            time.sleep(2)
            try:
                test = globals.browser.find_elements_by_css_selector("a[data-tn-element=IAApplyButton]")[0].find_elements_by_css_selector("span")[0].get_attribute("innerText") != "Apply Now ✓"
            except:
                test = True
            print(test)
            try:
                if test == True:
                    globals.browser.find_elements_by_css_selector("a[data-tn-element=IAApplyButton]")[0].click()
                    time.sleep(1)
                    globals.browser.find_elements_by_css_selector("label[for=input-q_cfcd208495d565ef66e7dff9f98764da-3]")[0].click()
                    answer_two = "42"
                    two_input = globals.browser.find_element_by_css_selector('input[id=input-q_c4ca4238a0b923820dcc509a6f75849b]')
                    for letter in answer_two:
                        print(letter)
                        two_input.send_keys(letter)
                        wait_time = random.randint(0, 500) / 10000
                        time.sleep(wait_time)
                    answer_three = "O(n m**2 2**n)"
                    three_input = globals.browser.find_element_by_css_selector('input[id=input-q_c81e728d9d4c2f636f067f89cc14862c]')
                    for letter in answer_three:
                        print(letter)
                        three_input.send_keys(letter)
                        wait_time = random.randint(0, 500) / 10000
                        time.sleep(wait_time)
                    globals.browser.find_elements_by_css_selector("option[label=Other]")[0].click()
                    globals.browser.find_elements_by_css_selector("div[class=ia-pageButtonGroup]")[0].find_elements_by_css_selector("button")[1].click()
                    time.sleep(2)
                    globals.browser.find_elements_by_css_selector("div[class=ia-pageButtonGroup]")[0].find_elements_by_css_selector("button")[1].click()
                    time.sleep(2)
                    globals.browser.find_elements_by_css_selector("div[id=write-cover-letter-selection-card]")[0].click()
                    time.sleep(1)
                    text = pytools.IO.getFile('message.txt')
                    text_input = globals.browser.find_element_by_css_selector('textarea[id=coverletter-textarea]')
                    text_input.clear()
                    for letter in text:
                        print(letter)
                        text_input.send_keys(letter)
                        wait_time = random.randint(0, 500) / 10000
                        time.sleep(wait_time)
                    time.sleep(1)
                    globals.browser.find_elements_by_css_selector("div[class=ia-pageButtonGroup]")[0].find_elements_by_css_selector("button")[1].click()
                    time.sleep(2)
                    globals.browser.find_elements_by_css_selector("div[class=ia-pageButtonGroup]")[0].find_elements_by_css_selector("button")[1].click()
            except:
                pass
            return 1

    # small functions for making my life easier
    class exe:
        def goto(url):
            globals.browser.get(url)

# more general tools
class tools:
    def pause():
        os.system("pause")

# Main function
def main():
    try:
        print("Username: " + sys.argv[1])
        globals.user = sys.argv[1]
        globals.passwd = sys.argv[2]
    except:
        pass
    sys.start()
    sys.signin(globals.user, globals.passwd)
    tools.pause()
    sys.exe.goto("https://ca.indeed.com/cmp/Leap-Tools-Inc.-1/jobs?jk=562c7031db35aae8&start=0&clearPrefilter=1")
    i = 0
    while i < len(globals.browser.find_elements_by_css_selector("li[data-testid=jobListItem")):
        print(i)
        sys.exe.goto("https://ca.indeed.com/cmp/Leap-Tools-Inc.-1/jobs?jk=562c7031db35aae8&start=0&clearPrefilter=1")
        time.sleep(3)
        job = globals.browser.find_elements_by_css_selector("li[data-testid=jobListItem")[i]
        app = 0
        while app != 1:
            try:
                print(job.find_elements_by_css_selector("button")[0].get_attribute("innerText"))
                print(job.find_elements_by_css_selector("button")[0].get_attribute("innerText").find("Senior") == -1)
                print((job.find_elements_by_css_selector("button")[0].get_attribute("innerText").find("Develop") != -1) or (job.find_elements_by_css_selector("button")[0].get_attribute("innerText").find("Programmer") != -1))
                if job.find_elements_by_css_selector("button")[0].get_attribute("innerText").find("Senior") == -1:
                    if (job.find_elements_by_css_selector("button")[0].get_attribute("innerText").find("Develop") != -1) or (job.find_elements_by_css_selector("button")[0].get_attribute("innerText").find("Programmer") != -1):
                        app = sys.funcs.apply(job)
            except:
                i = i + 1  
        i = i + 1

