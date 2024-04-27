#!/usr/bin/env python3

import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import os
import time
import subprocess

import configparser
from tkinter import font
import pyautogui
import sys

global volume, accX, accH
volume = 50
accX = 1145
accH = 887

user_home = os.path.expanduser("~")
vastsysteem_path = os.path.join(user_home, "VASTSYSTEEM")

config = configparser.ConfigParser()
config.read(vastsysteem_path + '/settings.ini')

screen_width = config.get('Settings', 'screen_width')
colorcode = config.get('Settings', 'colorcode')
font_size = config.get('Settings', 'font_size')
font_type = config.get('Settings', 'font_type')
chrome_options = Options()

#program = 'radio1classic'
program = sys.argv[1]

def addarguments():
    # Create an instance of the WebDriver
    #chromedriver_path = '/home/meme/Documenten/chromedriver'
    #Disable automate test infobar
    chrome_options.add_argument('--disable-infobars')
    
    # Automatically accept all cookies
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--disable-site-isolation-trials')
    chrome_options.add_argument("--enable-automation")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    
    
    #chrome_options.add_argument("--app="+url)



def createbrowser(url):
        
    global driver
    driver = webdriver.Chrome(options= chrome_options)
    
    #driver = webdriver.Chrome(executable_path='/home/meme/VASTSYSTEEM/chromedriver', options=chrome_options)
    driver.maximize_window()
    
    driver.get(url)


time.sleep(2)
def vrtmaxplay():
    time.sleep(5)
   
    pyautogui.click(accX, accH) #alles accepteren
    elem = driver.find_element(By.CLASS_NAME, "SRSOVR")
    driver.execute_script("arguments[0].remove();", elem)
    elem = driver.find_element(By.CLASS_NAME, "CrD3n2")
    driver.execute_script("arguments[0].remove();", elem)
    elem = driver.find_element(By.CLASS_NAME, "skQsGK")
    driver.execute_script("arguments[0].remove();", elem)
    elem = driver.find_element(By.CLASS_NAME, "mPKpBH")
    driver.execute_script("arguments[0].remove();", elem)
    elem = driver.find_element(By.CLASS_NAME, "EobK_g")
    driver.execute_script("arguments[0].remove();", elem)
    
    
    
    elem = driver.find_element(By.CLASS_NAME, "baTnBX")
    driver.execute_script("arguments[0].remove();", elem)
    elem = driver.find_element(By.CLASS_NAME, "HL8Eec")
    driver.execute_script("arguments[0].remove();", elem)
    elem = driver.find_element(By.CLASS_NAME, "GJXJ7X")
    driver.execute_script("arguments[0].style.width = '1500px';", elem)
    driver.execute_script("arguments[0].style.height = '750px';", elem)
    driver.execute_script("arguments[0].style.position = 'fixed'; \
                           arguments[0].style.top = '50%'; \
                           arguments[0].style.left = '50%'; \
                           arguments[0].style.transform = 'translate(-50%, -50%)';", elem)
    time.sleep(2)
    pyautogui.click(955, 602) #press play


def vrtmaxkijk():
    
    time.sleep(2)
    pyautogui.click(accX, accH) #alles accepteren
    elem = driver.find_element(By.CLASS_NAME, "SRSOVR")
    driver.execute_script("arguments[0].remove();", elem)
    elem = driver.find_element(By.CLASS_NAME, "CrD3n2")
    driver.execute_script("arguments[0].remove();", elem)
    elem = driver.find_element(By.CLASS_NAME, "skQsGK")
    driver.execute_script("arguments[0].remove();", elem)
    elem = driver.find_element(By.CLASS_NAME, "mPKpBH")
    driver.execute_script("arguments[0].remove();", elem)
    elem = driver.find_element(By.CLASS_NAME, "EobK_g")
    driver.execute_script("arguments[0].remove();", elem)
    elem = driver.find_element(By.CLASS_NAME, "baTnBX")
    driver.execute_script("arguments[0].remove();", elem)
    elem = driver.find_element(By.CLASS_NAME, "HL8Eec")
    driver.execute_script("arguments[0].remove();", elem)
    elem = driver.find_element(By.CLASS_NAME, "GJXJ7X")
    driver.execute_script("arguments[0].style.width = '1700px';", elem)
    driver.execute_script("arguments[0].style.height = '950px';", elem)
    driver.execute_script("arguments[0].style.position = 'fixed'; \
                           arguments[0].style.top = '50%'; \
                           arguments[0].style.left = '50%'; \
                           arguments[0].style.transform = 'translate(-50%, -50%)';", elem)  
    time.sleep(2)
    pyautogui.click(949, 653) #press play
    
def vrtmaxluister():
    
    time.sleep(2)
    pyautogui.click(accX, accH) #alles accepteren
    
    elem = driver.find_element(By.CLASS_NAME, "SRSOVR")
    driver.execute_script("arguments[0].remove();", elem)
    elem = driver.find_element(By.CLASS_NAME, "CrD3n2")
    driver.execute_script("arguments[0].remove();", elem)
    elem = driver.find_element(By.CLASS_NAME, "skQsGK")
    driver.execute_script("arguments[0].remove();", elem)
    elem = driver.find_element(By.CLASS_NAME, "mPKpBH")
    driver.execute_script("arguments[0].remove();", elem)
    elem = driver.find_element(By.CLASS_NAME, "EobK_g")
    driver.execute_script("arguments[0].remove();", elem)
    elem = driver.find_element(By.CLASS_NAME, "baTnBX")
    driver.execute_script("arguments[0].remove();", elem)
    elem = driver.find_element(By.CLASS_NAME, "HL8Eec")
    driver.execute_script("arguments[0].remove();", elem)
    elem = driver.find_element(By.CLASS_NAME, "GJXJ7X")
    driver.execute_script("arguments[0].style.width = '1700px';", elem)
    driver.execute_script("arguments[0].style.height = '950px';", elem)
    driver.execute_script("arguments[0].style.position = 'fixed'; \
                           arguments[0].style.top = '50%'; \
                           arguments[0].style.left = '50%'; \
                           arguments[0].style.transform = 'translate(-50%, -50%)';", elem)   
    time.sleep(2)
    pyautogui.click(957, 399) #press play                     
                           
def set_volume(volume_level):
    # Calculate the volume value based on the desired level
    volume = int(volume_level)  # Range: 0-100

    # Set the volume using the 'amixer' command
    subprocess.run(["amixer", "-D", "default", "sset", "Master", f"{volume}%"])


# voeg een functie toe aan de volume_down_button
def volume_down_button_clicked():
    
     #driver.execute_script("document.querySelector('video').volume -= 0.1;")
    global volume
    if volume == 0:
        volume = 0
    else:
        volume = volume -10
        set_volume(volume)

# voeg een functie toe aan de volume_up_button
def volume_up_button_clicked():
   
    #driver.execute_script("document.querySelector('video').volume += 0.1;")
    global volume
    if volume == 100:
        volume = 100
    else:    
        volume = volume +10
        set_volume(volume)
    
def close():

    try:        
        driver.quit()
    except Exception as e:
        print(e)
        
    root.destroy()


print(program)
if program == 'canvas': 
    url = 'https://www.vrt.be/vrtnu/livestream/video/canvas/'
    addarguments()
    createbrowser(url)
    vrtmaxplay()
    
    
elif program == 'vrt1' or program == 'vrt':
    url = 'https://www.vrt.be/vrtnu/livestream/video/een/'
    addarguments()
    createbrowser(url)
    vrtmaxplay()
elif program == 'Ketnet' or program == 'ketnetgroen':
    url = 'https://www.vrt.be/vrtnu/livestream/video/ketnet/'
    addarguments()
    createbrowser(url)
    vrtmaxplay()
    
elif program == 'Ketnet-Junior':
    url = 'https://www.vrt.be/vrtnu/livestream/video/ketnet-jr/'
    addarguments()
    createbrowser(url)
    vrtmaxplay()
elif program == 'vrtnews' or program == 'VRT-NWS':
    url = 'https://www.vrt.be/vrtnu/livestream/video/vgt-journaal/'
    addarguments()
    createbrowser(url)  
    vrtmaxplay()
elif program == 'MNM':
    url = 'https://www.vrt.be/vrtnu/livestream/audio/mnm/?context=kijk'
    addarguments()
    createbrowser(url)
    vrtmaxkijk()
elif program == 'stubru':
    url = 'https://www.vrt.be/vrtnu/livestream/audio/stubru/?context=kijk'
    addarguments()
    createbrowser(url)
    vrtmaxkijk()
elif program == 'radio1':
    url = 'https://www.vrt.be/vrtnu/livestream/video/radio1/?context=kijk'
    addarguments()
    createbrowser(url)
    vrtmaxkijk()
elif program == 'radio2':
    url = 'https://www.vrt.be/vrtnu/livestream/video/radio2/?context=kijk'
    addarguments()
    createbrowser(url)
    vrtmaxkijk()
elif program == 'radio1classic':
    url = 'https://www.vrt.be/vrtnu/livestream/audio/radio1classics/'
    addarguments()
    createbrowser(url)
    vrtmaxluister()
elif program == 'lagelanden':
    url = 'https://www.vrt.be/vrtnu/livestream/audio/radio1lagelandenlijst/'
    addarguments()
    createbrowser(url)
    vrtmaxluister()
elif program == 'unwind':
    url = 'https://www.vrt.be/vrtnu/livestream/audio/radio2unwind/'
    addarguments()
    createbrowser(url)
    vrtmaxluister()
elif program == 'klara':
    url = 'https://www.vrt.be/vrtnu/livestream/audio/klara/?context=kijk'
    addarguments()
    createbrowser(url)
    vrtmaxkijk()
elif program == 'klara-continuo':
    url = 'https://www.vrt.be/vrtnu/livestream/audio/klaracontinuo/'
    addarguments()
    createbrowser(url)
    vrtmaxluister()
elif program == 'ketnethits':
    url = 'https://www.vrt.be/vrtnu/livestream/audio/ketnethits/'
    addarguments()
    createbrowser(url)
    vrtmaxluister()


elif program == 'mnmtrowback':
    url = 'https://www.vrt.be/vrtnu/livestream/audio/mnmthrowback/'
    addarguments()
    createbrowser(url)
    vrtmaxluister()
    
elif program == 'renbeats':
    url = 'https://www.vrt.be/vrtnu/livestream/audio/mnmrbeats/'
    addarguments()
    createbrowser(url)
    vrtmaxluister()
    
elif program == 'MNM-hits':
    url = 'https://www.vrt.be/vrtnu/livestream/audio/mnmhits/'
    addarguments()
    createbrowser(url)
    vrtmaxluister()
    
elif program == 'tijdloze':
    url = 'https://www.vrt.be/vrtnu/livestream/audio/tijdloze/'
    addarguments()
    createbrowser(url)
    vrtmaxluister()
    
elif program == 'stubru-vuurland':
    url = 'https://www.vrt.be/vrtnu/livestream/audio/vuurland/'
    addarguments()
    createbrowser(url)
    vrtmaxluister()
    
elif program == 'stubru-bruut':
    url = 'https://www.vrt.be/vrtnu/livestream/audio/bruut/'
    addarguments()
    createbrowser(url)
    vrtmaxluister()
    
elif program == 'stubru-untz':
    url = 'https://www.vrt.be/vrtnu/livestream/audio/untz/'
    addarguments()
    createbrowser(url)
    vrtmaxluister()
    
elif program == 'stubru-hooray':
    url = 'https://www.vrt.be/vrtnu/livestream/audio/hooray/'
    addarguments()
    createbrowser(url)
    vrtmaxluister()
    
elif program == 'Radio2-benebene':
    url = 'https://www.vrt.be/vrtnu/livestream/audio/radio2benebene/'
    addarguments()
    createbrowser(url)
    vrtmaxluister()
    


        
else:
    print('programma nog niet ingesteld')
    url = 'http://www.google.be'
print(url)









#zet vulume half in opstart
set_volume(volume)
# maak het root-venster
root = tk.Tk()
custom_font = font.Font(size=font_size, family= font_type)
# stel root venster in
root.overrideredirect(True)
root.geometry(screen_width +"x160")
# stel `always on top` in op `true`
root.wm_attributes("-topmost", True)
root.configure(bg= colorcode)

hoogte = 2

# maak de volume omlaag-knop
volume_down_button = tk.Button(root, text="Volume omlaag", font=custom_font , bg= colorcode, activebackground= colorcode, height=hoogte )
# maak de volume omhoog-knop
volume_up_button = tk.Button(root, text="Volume omhoog", font=custom_font , bg= colorcode, activebackground= colorcode, height=hoogte )
# maak de sluit-knop
close_button = tk.Button(root, text="Sluiten", font=custom_font , bg= colorcode, activebackground= colorcode, height=hoogte )



# voeg de functie toe aan de volume_down_button
volume_down_button.config(command=volume_down_button_clicked)
# voeg de functie toe aan de volume_up_button
volume_up_button.config(command=volume_up_button_clicked)
close_button.config(command=close)



# plaats de knoppen op het root-venster
volume_down_button.pack(side="left")
volume_up_button.pack(side="left")
close_button.pack(side="right")

# initialiseer het root-venster
root.mainloop()