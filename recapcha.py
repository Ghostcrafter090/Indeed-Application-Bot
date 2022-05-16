import re, csv
from time import sleep, time
from random import uniform, randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pytools
import sys
import os

def write_stat(loops, time):
    with open('stat.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([loops, time])       
    
def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
    
def wait_between(a,b):
    rand=uniform(a, b) 
    sleep(rand)
    
# ***** main procedure to identify and submit picture solution
class solve:
    def processImage(url, text):
        os.system('mkdir temp')
        pytools.net.download(url, ".\\temp\\test.jpg", 1)
        imageA = pytools.IO.getBytes(".\\temp\\test.jpg")
        fols = os.listdir(".\\ai\\brain")
        i = 0
        notExists = True
        corr = False
        while i < len(fols):
            try:
                if pytools.IO.getBytes(".\\ai\\brain\\" + fols[i] + "\\image.jpg") == imageA:
                    json = pytools.IO.getJson(".\\ai\\brain\\" + fols[i] + "\\info.json")
                    try:
                        json[text]
                        if json[text] > -1:
                            json[text] = json[text] + 1
                        corr = json
                        imgNum = fols[i]
                        notExists = False
                    except:
                        json[text] = 1
                    pytools.IO.saveJson(".\\ai\\brain\\" + fols[i] + "\\info.json", json)
            except:
                pass
            i = i + 1
        if notExists:
            os.system('mkdir .\\ai\\brain\\' + str(len(fols)))
            json = {}
            json[text] = 1
            pytools.IO.saveJson(".\\ai\\brain\\" + str(len(fols)) + "\\info.json", json)
            os.system('copy /y .\\temp\\test.jpg .\\ai\\brain\\' + str(len(fols)) + '\\image.jpg')
            os.system('del ".\\temp\\test.jpg" /f /s /q')
            imgNum = len(fols)
        out = [True, False, ".\\ai\\brain\\" + str(imgNum) + "\\info.json"]
        if corr != False:
            n = 0
            f = 0
            l = True
            for key in corr.keys():
                if l:
                    if n > -1:
                        if corr[key] > n:
                            n = corr[key]
                            f = key
                if corr[key] == -1:
                    n = -1
                    f = key
                    l = False
                if corr[key] == -2:
                    n = -2
                    f = key
                    l = False
            if f == text:
                if n == -1:
                    out[1] = True
                elif n != -2:
                    if randint(1, 10) < 5:
                        out[1] = True
                    else:
                        out[1] = False
        else:
            out[0] = False
        return out

    def images(driver):
        print(By.ID)
        imagesf = [[True, False, ""], [True, False, ""], [True, False, ""], [True, False, ""], [True, False, ""], [True, False, ""], [True, False, ""], [True, False, ""], [True, False, ""], ""]
        print("Grabbing image html...")
        images = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "task-image")))
        print("Grabbing prompt text...")
        promptText = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "prompt-text")))[0].get_attribute('innerText')
        imagesf[9] = promptText
        i = 0
        while i < len(images):
            print("Processing image " + str(i))
            imageURL = images[i].find_element(By.CLASS_NAME, "image").get_attribute('style').split('url("')[1].split('") no-')[0]
            check = solve.processImage(imageURL, promptText)
            imagesf[i][2] = check
            print("Statement   ::::   " + str(check))
            if check[0]:
                print("I am smart!")
                if check[1]:
                    images[i].click()
                    imagesf[i][0] = False
                    print("Criteria Matches!")
                else:
                    print("Criteria doesn't match.")
            else:
                print("I am dumb!!!")
                if randint(0, 10) > 5:
                    images[i].click()
                    imagesf[i][1] = True
                else:
                    imagesf[i][0] = False
            i = i + 1
        print("Clicking next...")
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME ,"button-submit")))[0].click()
        except:
            pass
        return imagesf

    def main(driver, status):
        print("imagesf")
        imagesf = solve.images(driver)
        print('imagesn')
        imagesn = solve.images(driver)
        out = True
        sleep(3)
        try:
            if WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME ,"button-submit")))[0].get_attribute('innerText') != 'Skip':
                if status.get_attribute('style').find('display: none') != -1:
                    out = False
                    solve.correctImages(imagesf)
                    solve.correctImages(imagesn)
                    print("I AM SMART BOIIIIISSSS!!!!")
            else:
                print("I done fucked up.")
        except:
            if status.get_attribute('style').find('display: none') != -1:
                out = False
                solve.correctImages(imagesf)
                solve.correctImages(imagesn)
                print("I AM SMART BOIIIIISSSS!!!!")
        return out
    
    def correctImages(imagesf):
        print("correcting images...")
        i = 0
        print(imagesf)
        while i < (len(imagesf) - 1):
            print(imagesf[i])
            json = pytools.IO.getJson(imagesf[i][2][2])
            if (imagesf[i][2][1]):
                json[imagesf[9]] = -1
            else:
                json[imagesf[9]] = -2
            pytools.IO.saveJson(imagesf[i][2][2], json)
            i = i + 1

def main(driver):
    driver.switch_to.default_content()
    start = time()

    mainWin = driver.current_window_handle  

    # move the driver to the first iFrame 
    driver.switch_to.frame(driver.find_elements_by_css_selector("iframe")[0])

    # *************  locate CheckBox  **************
    CheckBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID ,"checkbox")))

    # *************  click CheckBox  ***************
    wait_between(0.5, 0.7)  
    # making click on captcha CheckBox 
    CheckBox.click() 
    
    #***************** back to main window **************************************
    driver.switch_to.window(mainWin)  

    wait_between(2.0, 2.5)

    # ************ switch to the second iframe by tag name ******************
    driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])
    i = 1
    out = True
    try:
        while (i < 130) and (out):
            print('\n\r{0}-th loop'.format(i))
            # ******** check if checkbox is checked at the 1st frame ***********
            driver.switch_to.window(mainWin)   
            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME , 'iframe')))
            wait_between(1.0, 2.0)
            if check_exists_by_xpath(driver, '//span[@aria-checked="true"]'):
                write_stat(i, round(time()-start) - 1 ) # saving results into stat file
                break
            driver.switch_to.window(mainWin)   
            # ********** To the second frame to solve pictures *************
            wait_between(0.3, 1.5)
            
            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME , 'iframe')))
            status = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID ,"status")))[0]
            driver.switch_to.window(mainWin)
            driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[1])
            out = solve.main(driver, status)
            driver.switch_to.window(mainWin)
            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME , 'iframe')))
            try:
                if status.get_attribute('style').find('display: none') == -1:
                    CheckBox.click()
                    out = True
            except:
                pass
            i = i + 1
    except:
        print("Unexpected main error:", sys.exc_info())
        return True
    return out

def run(driver):
    solvef = True
    while solvef:
        try:
            solvef = main(driver)
        except:
            print("Unexpected main error:", sys.exc_info())
            solvef = True