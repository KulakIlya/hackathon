from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import pickle
import undetected_chromedriver as uc
import os
import cv2
import selenium

def Login(driver):
    driver.get("https://chatgpt.com/")
    time.sleep(5)
    buttons = driver.find_elements(By.CLASS_NAME, "btn")
    for bttn in buttons:
        print(bttn.text)
        if bttn.text == "Log in":
            bttn.click()
            break
    time.sleep(5)
    driver.find_element(By.CLASS_NAME, "email-input").send_keys(email)
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "continue-btn").click()
    time.sleep(5)
    driver.find_element(By.NAME, "password").send_keys(password)
    actions = driver.find_elements(By.NAME, "action")
    for action in actions:
        if action.text == "Continue":
            action.click()
            break
    time.sleep(5)

# def Image_prompt(driver):
#     prompt_area = driver.find_element(By.ID, "prompt-textarea")
#     prompt = "What the movie this image from?(answer only the name of movie or the most predicted movie)"
#     prompt_area.send_keys(prompt)
#     time.sleep(1)
#     driver.find_element(By.XPATH,
#                         '//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[2]/div[1]/div/form/div/div[2]/div/div/div/input').send_keys(
#         "D:\Work(coding)\Movie Shazam\image2.png")
#     time.sleep(5)
#     driver.find_element(By.XPATH,
#                         '//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[2]/div[1]/div/form/div/div[2]/div/button').click()
#     time.sleep(5)
#     counter = 1
#     answer = driver.find_elements(By.CLASS_NAME, "text-message")[counter]
#     return answer.text

def Get_title(driver, description=None, photo=None, video=None, text_counter=1):
    if video != None:
        vidcap = cv2.VideoCapture(video)
        frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        seconds = round(frames / fps)
        print("VIDEO DURATION: " + str(seconds))
        times = round(seconds / 3)
        if times > 5:
            times = 5
        success, image = vidcap.read()
        count = 0
        for s in range(times):
            vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * 3000))
            cv2.imwrite("image%d.jpg" % count, image)  # save frame as JPEG file
            success, image = vidcap.read()
            count += 1

        counter = 2
        prompt_area = driver.find_element(By.ID, "prompt-textarea")
        if description != None:
            prompt = "What the movie this image from?(answer only the name of movie or the most predicted movie, write the title in quotation marks), Description of film by myself - " + str(description)
        else:
            prompt = "What the movie this image from?(answer only the name of movie or the most predicted movie)"
        prompt_area.send_keys(prompt)
        time.sleep(1)
        for i in range(times):
            driver.find_element(By.XPATH,
                                '//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[2]/div[1]/div/form/div/div[2]/div/div/div/input').send_keys(
                f"D:\Work(coding)\Movie Shazam\image{i}.jpg")
            time.sleep(3)
            if (i > 0):
                for x in range(i):
                    driver.find_element(By.XPATH,
                                        f'//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[2]/div[1]/div/form/div/div[2]/div/div[1]/div[{counter}]/button').click()
                counter += 1
    elif (photo != None) and (video == None):
        prompt_area = driver.find_element(By.ID, "prompt-textarea")
        if description != None:
            prompt = "What the movie this image from?(answer only the name of movie or the most predicted movie, write the title in quotation marks), Description of film by myself - " + str(
                description)
        else:
            prompt = "What the movie this image from?(answer only the name of movie or the most predicted movie)"
        prompt_area.send_keys(prompt)
        time.sleep(1)
        driver.find_element(By.XPATH,
                            '//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[2]/div[1]/div/form/div/div[2]/div/div/div/input').send_keys(
            f"D:\Work(coding)\Movie Shazam\{photo}")
        time.sleep(3)
    else:
        prompt_area = driver.find_element(By.ID, "prompt-textarea")
        prompt = "What the movie i speak about?(answer only the name of movie or the most predicted movie, write the title in quotation marks), Description of film by myself - " + str(
            description)
        prompt_area.send_keys(prompt)
        time.sleep(1)
    driver.find_element(By.XPATH,
                        '//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[2]/div[1]/div/form/div/div[2]/div/button').click()
    time.sleep(10)
    answer = driver.find_elements(By.CLASS_NAME, "text-message")[text_counter]
    try:
        title = '"' + answer.text.split('"')[1] + '"'
    except:
        title = answer.text
    print("TITLE: " + str(title))
    return title

# def Try_another(driver, title, counter, additional_text):
#     prompt_area = driver.find_element(By.ID, "prompt-textarea")
#     prompt = "Its not " + str(title) + " , try another guess. Additional message: " + str(additional_text) + "(answer only the name of movie or the most predicted movie, write the title in brackets)"
#     prompt_area.send_keys(prompt)
#     time.sleep(1)
#     driver.find_element(By.XPATH,
#                         '//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[2]/div[1]/div/form/div/div[2]/div/button').click()
#     time.sleep(5)
#     answer = driver.find_elements(By.CLASS_NAME, "text-message")[counter+1]
#     print("TRY ANOTHER TEXT " + str(answer.text))
#     try:
#         title = '"' + answer.text.split('"')[1] + '"'
#     except:
#         title = answer.text
#     print("TITLE: " + str(title))

def Imdb_data(driver, title):
    driver.get("https://www.imdb.com/?ref_=nv_home")
    time.sleep(4)
    driver.find_element(By.CLASS_NAME, "imdb-header-search__input").send_keys(title)
    time.sleep(2)
    link = driver.find_element(By.CLASS_NAME, "searchResult--const").get_attribute("href")
    driver.get(link)
    main_photo = driver.find_element(By.CLASS_NAME, "ipc-lockup-overlay").get_attribute("href")
    about = driver.find_element(By.CLASS_NAME, "ipc-html-content-inner-div").text
    rating = driver.find_element(By.CLASS_NAME, "sc-bde20123-2").text.replace("\n", "")
    print("IMDB RATING " + str(rating))
    print("ABOUT " + str(about))
    return [main_photo, rating, about]

def main(description=None, photo=None, video=None):
    email = "chatgpt@sych.moe"
    password = "H@rrrd_Passwd"

    while True:
        try:
            driver = uc.Chrome()
            driver_imdb = uc.Chrome()
            Login(driver)
            break
        except:
            driver.close()
            driver_imdb.close()
    counter = 4
    title = Get_title(driver=driver, description=description, photo=photo, video=video)
    while True:
        try:
            data = Imdb_data(driver_imdb, title)
            break
        except:
            pass
    return data
    # while True:
    #     result = input("Is it that?")
    #     if result == "Yes":
    #         break
    #     else:
    #         description = "Its not " + str(title) + " , try another guess. Additional message: " + str(result) + "(answer only the name of movie or the most predicted movie, write the title in quotation marks)"
    #         title = Get_title(driver, description=description, text_counter=counter)
    #         while True:
    #             try:
    #                 data = Imdb_data(driver_imdb, title)
    #                 break
    #             except:
    #                 pass
    #         counter += 2