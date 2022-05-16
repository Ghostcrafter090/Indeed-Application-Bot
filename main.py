from jinja2 import Undefined
from psutil import users
from selenium import webdriver
import random
import time
import os
import pytools # note: pytools is my own python library, to use it, download it here: https://github.com/Ghostcrafter090/pytools
import sys as sysn

# Globals
class globals:
    broswer = '' # allows access to browser driver at all levels of application
    user = ""
    passwd = ""
    questions = {}

# Sys class, contains main components
class sys:
    def start():
        globals.browser = webdriver.Firefox()

    # Used for signing in, requires user interaction in the form of verification and recapcha
    def signin(username, password):
        globals.browser.get("https://secure.indeed.com/auth?hl=en_CA&co=CA&continue=https%3A%2F%2Fca.indeed.com%2Fcmp%2FLeap-Tools-Inc.-1%2Fjobs%3Fjk%3D562c7031db35aae8%26start%3D0%26clearPrefilter%3D1&tmpl=desktop&from=gnav-util-acme--acme-webapp&_ga=2.205514322.358284476.1651172242-1342485949.1651172242")
        time.sleep(1)

    # contains primary functions of the bot, main actions used based on criteria are stored here.
    class funcs:
        def apply(jobf):
            sys.exe.goto(jobf.get_attribute('href'))
            time.sleep(3)
            try:
                test = globals.browser.find_element_by_css_selector("button[id=indeedApplyButton]").get_attribute("innerText") != "Apply Now ✓"
            except:
                test = True
            print(test)
            try:
                if test == True:
                    globals.browser.find_elements_by_css_selector("button[id=indeedApplyButton]")[0].click()
                    time.sleep(3)
                    out = 1
                    fnl = 0
                    while (out != 0) and (fnl < 100):
                        try:
                            out = pageAction()
                        except:
                            print("Unexpected apply error:", sysn.exc_info())
                            fnl = fnl + 1
                    return 1
            except:
                pass
            return 0

        class questions:
            def checkQuestions(question):
                answer = input("Answer (yes/*) ? ")
                confirm = False
                while confirm == False:
                    if answer == "yes":
                        final = input("Response: ")
                        globals.questions[question] = final
                    else:
                        globals.questions[question] = "?ask"
                    sure = input("Are you sure (yes/*) ? ")
                    if sure == "yes":
                        confirm = True
                print(globals.questions)
                pytools.IO.saveJson("questions.json", globals.questions)

            # https://ca.indeed.com/jobs?q=Junior%20Developer&l=Canada&lang=en&taxo1=EHPW9&remotejob=032b3046-06a3-4876-8dfd-474eb5e7ed11&vjk=89a07d50778ecdc7

            def answerQuestions():
                globals.questions = pytools.IO.getJson("questions.json")
                yes = True
                n = 0
                while yes:
                    try:
                        noError = False
                        quest = globals.browser.find_element_by_css_selector('div[id=q_' + str(n) + ']')
                        try:
                            box = quest.find_elements_by_css_selector('[id=' + quest.find_elements_by_css_selector('label')[0].get_attribute('for') + ']')[0]
                            noError = True
                        except:
                            tools.pause()
                        if noError:
                            boxType = "new"
                            if box.tag_name == "textarea":
                                boxType = "textarea"
                            elif box.tag_name == "select":
                                boxType = "select"
                            elif box.tag_name == "input":
                                if box.get_attribute('type') == "number":
                                    boxType = "input-number"
                                if box.get_attribute('type') == "text":
                                    boxType = "input-text"
                                if box.get_attribute('type') == "date":
                                    boxType = "input-date"
                                if box.get_attribute('type') == "tel":
                                    boxType = "input-tel"
                            elif box.tag_name == "fieldset":
                                    boxType = "fieldset"
                            quest = globals.browser.find_element_by_css_selector('div[id=q_' + str(n) + ']')
                            try:
                                tools.dummy(globals.questions[quest.get_attribute('innerText') + "_" + boxType])
                            except:
                                print(quest.get_attribute('innerText') + "_" + boxType)
                                sys.funcs.questions.checkQuestions(quest.get_attribute('innerText') + "_" + boxType)
                            if globals.questions[quest.get_attribute('innerText') + "_" + boxType] == "?ask":
                                confirm = False
                                while confirm == False:
                                    answer = input("Response: ")
                                    check = input("Are you sure (yes/*) ? ")
                                    if check == "yes":
                                        confirm = True
                            else:
                                answer = globals.questions[quest.get_attribute('innerText') + "_" + boxType]
                            quest.find_elements_by_css_selector('[id=' + quest.find_elements_by_css_selector('label')[0].get_attribute('for') + ']')[0]
                            box = quest.find_elements_by_css_selector('[id=' + quest.find_elements_by_css_selector('label')[0].get_attribute('for') + ']')[0]
                            if box.tag_name == "textarea":
                                box.clear()
                                for letter in answer:
                                    print(letter)
                                    box.send_keys(letter)
                                    wait_time = random.randint(0, 500) / 10000
                                    time.sleep(wait_time)
                            elif box.tag_name == "select":
                                box.find_elements_by_css_selector('option')[int(answer)].click()
                            elif box.tag_name == "input":
                                box.clear()
                                if box.get_attribute('type') == "number":
                                    for letter in answer:
                                        print(letter)
                                        box.send_keys(letter)
                                        wait_time = random.randint(0, 500) / 10000
                                        time.sleep(wait_time)
                                if box.get_attribute('type') == "text":
                                    for letter in answer:
                                        print(letter)
                                        box.send_keys(letter)
                                        wait_time = random.randint(0, 500) / 10000
                                        time.sleep(wait_time)
                                if box.get_attribute('type') == "date":
                                    if answer == "today":
                                        globals.browser.execute_script('document.getElementById("' + box.get_attribute('id') + '").valueAsDate = new Date()')
                                    else:
                                        dateArray = pytools.clock.getDateTime()
                                        globals.browser.execute_script('document.getElementById("' + box.get_attribute('id') + '").valueAsDate = new Date("' + answer.split("-")[0] + '-' + answer.split("-")[1] + '-' + answer.split("-")[2] + '")')
                                    tools.pause()
                                if box.get_attribute('type') == "tel":
                                    for letter in answer:
                                        print(letter)
                                        box.send_keys(letter)
                                        wait_time = random.randint(0, 500) / 10000
                                        time.sleep(wait_time)
                            elif box.tag_name == "fieldset":
                                quest.find_elements_by_css_selector('label[for=' + quest.find_elements_by_css_selector('label')[0].get_attribute('for') + '-' + str(answer) + ']')[0].click()
                            elif box.tag_name == 'div':
                                box.find_elements_by_css_selector('label[for=' + box.find_elements_by_css_selector('input')[int(answer)].get_attribute('id') + ']')[0].find_elements_by_css_selector('span')[0].click()
                    except:
                        print("Unexpected error:", sysn.exc_info())
                        yes = False
                    n = n + 1
                globals.browser.find_elements_by_css_selector("div[class=ia-pageButtonGroup]")[0].find_elements_by_css_selector("button")[1].click()
            
            def forward():
                globals.browser.find_elements_by_css_selector("div[class=ia-pageButtonGroup]")[0].find_elements_by_css_selector("button")[1].click()

            def jobExpo():
                globals.browser.find_elements_by_css_selector('div[role=radio]')[0].click()
                globals.browser.find_elements_by_css_selector("div[class=ia-pageButtonGroup]")[0].find_elements_by_css_selector("button")[1].click()

            def coverLetter(f):
                globals.browser.find_elements_by_css_selector("div[id=write-cover-letter-selection-card]")[f].click()
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
                        
            def addResume():
                globals.browser.find_elements_by_css_selector('div[id=ia-IndeedResumeSelect-headerButton]')[0].click()
                globals.browser.find_elements_by_css_selector("div[class=ia-pageButtonGroup]")[0].find_elements_by_css_selector("button")[1].click()

            def yesImSmart():
                globals.browser.find_elements_by_css_selector('div[class=ia-InterventionActionButtons]')[0].find_elements_by_css_selector('button')[0].click()
                        

    # small functions for making my life easier
    class exe:
        def goto(url):
            globals.browser.get(url)

# more general tools
class tools:
    def pause():
        os.system("pause")

    def dummy(inf):
        return inf == inf

# Main function
def main():

    nameCrit = {
        "containsOr": [
            "Develop",
            "Programmer",
            "Software"
            "Java "
        ],
        "containsAnd": [],
        "!contains": [
            "Senior",
            "Sales",
            "Analytics"
        ]
    }

    try:
        print("Username: " + sysn.argv[1])
        globals.user = sysn.argv[1]
        globals.passwd = sysn.argv[2]
    except:
        pass
    sys.start()
    sys.signin(globals.user, globals.passwd)
    tools.pause()
    sys.exe.goto("https://ca.indeed.com/jobs?q=Developer&l=Canada&jt=fulltime&sort=date&fromage=7&lang=en&taxo2=EHPW9&remotejob=032b3046-06a3-4876-8dfd-474eb5e7ed11")
    while True:
        add = 0
        i = 0
        while i < len(globals.browser.find_elements_by_css_selector("a")):
            print(i)
            sys.exe.goto("https://ca.indeed.com/jobs?q=Developer&l=Canada&jt=fulltime&sort=date&fromage=7&lang=en&taxo2=EHPW9&remotejob=032b3046-06a3-4876-8dfd-474eb5e7ed11")
            time.sleep(3)
            app = 0
            while app != 1:
                fn = True
                while fn and (i < len(globals.browser.find_elements_by_css_selector("a"))):
                    print(i)
                    try:
                        jobf = globals.browser.find_elements_by_css_selector("a")[i]
                        job = jobf.find_elements_by_css_selector("td[class=resultContent]")[0]
                        fn = False
                    except:
                        pass
                    i = i + 1
                containsAnd = True
                containsOr = False
                notContains = True
                try:
                    print(job.find_elements_by_css_selector("h2")[0].get_attribute("innerText"))
                    try:
                        for crit in nameCrit["containsAnd"]:
                            if job.find_elements_by_css_selector("h2")[0].get_attribute("innerText").find(crit) == -1:
                                containsAnd = False
                    except:
                        pass
                    for crit in nameCrit["containsOr"]:
                        if job.find_elements_by_css_selector("h2")[0].get_attribute("innerText").find(crit) != -1:
                            containsOr = True
                    for crit in nameCrit["!contains"]:
                        if job.find_elements_by_css_selector("h2")[0].get_attribute("innerText").find(crit) != -1:
                            notContains = False
                    print("contains requirements: " + str(containsAnd))
                    print("contains one opt requirement: " + str(containsOr))
                    print("doesn't contain blacklist requirements: " + str(notContains))
                    add = add + 1
                    if (containsAnd) and (containsOr) and (notContains):
                        app = sys.funcs.apply(jobf)
                        add = 0
                        sys.exe.goto("https://ca.indeed.com/jobs?q=Developer&l=Canada&jt=fulltime&sort=date&fromage=7&lang=en&taxo2=EHPW9&remotejob=032b3046-06a3-4876-8dfd-474eb5e7ed11")
                        time.sleep(3)
                    if add > 100:
                        i = 0
                        add = 0
                        sys.exe.goto("https://ca.indeed.com/jobs?q=Developer&l=Canada&jt=fulltime&sort=date&fromage=7&lang=en&taxo2=EHPW9&remotejob=032b3046-06a3-4876-8dfd-474eb5e7ed11")
                        time.sleep(3)
                except:
                    print("Unexpected main error:", sysn.exc_info())
                    sys.exe.goto("https://ca.indeed.com/jobs?q=Developer&l=Canada&jt=fulltime&sort=date&fromage=7&lang=en&taxo2=EHPW9&remotejob=032b3046-06a3-4876-8dfd-474eb5e7ed11")
                    time.sleep(3)
                i = i + 1

def pageAction():
    h1 = globals.browser.find_element_by_css_selector('h1').get_attribute('innerText')
    out = 0
    if h1 == 'Add a resume for the employer':
        sys.funcs.questions.forward()
        out = 1
    elif h1 == 'Select a past job that shows relevant experience':
        sys.funcs.questions.jobExpo()
        out = 2
    elif h1 == 'Consider adding supporting documents':
        try:
            sys.funcs.questions.coverLetter(0)
        except:
            sys.funcs.questions.coverLetter(1)
        out = 3
    elif h1.find('Questions from') != -1:
        sys.funcs.questions.answerQuestions()
        out = 4
    elif h1 == 'Please review your application':
        sys.funcs.questions.forward()
        out = 5
    elif h1.find('Add a resume') != -1:
        sys.funcs.questions.addResume()
        out = 6
    elif h1.find('Do you have these qualifications') != -1:
        sys.funcs.questions.yesImSmart()
        out = 7
    elif h1.find('Want to include any supporting documents?'):
        try:
            sys.funcs.questions.coverLetter(1)
        except:
            sys.funcs.questions.coverLetter(0)
        out = 8
    return out

