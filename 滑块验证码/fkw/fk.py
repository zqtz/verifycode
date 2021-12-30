import base64

import requests
from selenium.webdriver import Chrome, ActionChains
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import cv2
import time

url = 'https://i.fkw.com/'
while True:
    web = Chrome()
    web.get(url)
    WebDriverWait(web,4).until(ec.presence_of_element_located((By.XPATH,'//*[@id="loginCacct"]')))
    web.find_element(By.XPATH,'//*[@id="loginCacct"]').send_keys('123@qq.com')
    web.find_element(By.XPATH,'//*[@id="loginPwd"]').send_keys('123456')
    web.find_element(By.XPATH,'//*[@id="login_button"]').click()
    time.sleep(2)
    big_img_bs6_url = web.find_element(By.XPATH,'/html/body/div[4]/div/div[2]/div/div/div[3]/div/div[1]/div[1]/img[1]').get_attribute('src')
    small_img_bs6_url  = web.find_element(By.XPATH,'/html/body/div[4]/div/div[2]/div/div/div[3]/div/div[1]/div[1]/img[2]').get_attribute('src')
    print(big_img_bs6_url)
    print(small_img_bs6_url)
    big_img_url = big_img_bs6_url.split(',')[-1]
    small_img_url = small_img_bs6_url.split(',')[-1]

    big_img_url_content = base64.urlsafe_b64decode(big_img_url + '=' * (4 - len(big_img_url) % 4))
    small_img_url_content = base64.urlsafe_b64decode(small_img_url + '=' * (4 - len(small_img_url) % 4))

    with open('hb.jpg','wb')as f:
        f.write(big_img_url_content)
        f.close()
    with open('hk.jpg','wb')as f:
        f.write(small_img_url_content)
        f.close()

    big_grey = cv2.imread('hb.jpg',0)
    small_grey = cv2.imread('hk.jpg',0)
    resp = cv2.matchTemplate(big_grey,small_grey,cv2.TM_CCORR_NORMED)
    value = cv2.minMaxLoc(resp)
    print(value)
    x = value[2][0]
    actions = ActionChains(web)
    hk_ele = web.find_element(By.XPATH,'/html/body/div[4]/div/div[2]/div/div/div[3]/div/div[1]/div[1]/img[2]')
    actions.click_and_hold(hk_ele).perform()
    time.sleep(1)
    actions.drag_and_drop_by_offset(hk_ele,x,0).perform()
    time.sleep(1)
    try:
        WebDriverWait(web,10).until(ec.presence_of_element_located((By.XPATH,'/html/body/div[4]/div/div[2]/div/div/div[3]/div/div[1]/div[2]/div[1]/div/div')))
    except:
        break
        web.quit()


