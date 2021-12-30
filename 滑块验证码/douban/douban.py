import requests
from selenium.webdriver import Chrome, ActionChains
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import cv2
import time

while True:
    web = Chrome()
    web.get('https://www.douban.com/')
    time.sleep(3)
    web.switch_to.frame(web.find_element(By.XPATH,'//*[@id="anony-reg-new"]/div/div[1]/iframe'))
    web.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]').click()
    web.find_element_by_xpath('//*[@id="username"]').send_keys('15916142395')
    web.find_element_by_xpath('//*[@id="password"]').send_keys('123456')
    web.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[5]/a').click()
    time.sleep(8)
    web.switch_to.frame(web.find_element_by_xpath('//*[@id="tcaptcha_iframe"]'))
    big_image_url = web.find_element_by_xpath('//*[@id="slideBg"]').get_attribute('src')
    small_image_url = web.find_element_by_xpath('//*[@id="slideBlock"]').get_attribute('src')
    big_imge_resp = requests.get(big_image_url)
    small_image_resp = requests.get(small_image_url)
    with open('hb.jpg','wb')as f:
        f.write(big_imge_resp.content)
        f.close()
    with open('hk.jpg','wb')as f:
        f.write(small_image_resp.content)
        f.close()

    big_grey = cv2.imread('hb.jpg',0)
    small_grey = cv2.imread('hk.jpg',0)
    resp = cv2.matchTemplate(big_grey,small_grey,cv2.TM_CCORR_NORMED)
    value = cv2.minMaxLoc(resp)
    print(value)
    # 原图的像素(680*390),缩放的像素(283*162)
    x = value[2][0]
    x = x*283/680
    py = int(38-27*283/680)
    x1 = x-py
    print(x1)
    actions = ActionChains(web)
    hk_ele = web.find_element(By.XPATH,'//*[@id="slideBlock"]')
    actions.click_and_hold(hk_ele).perform()
    actions.drag_and_drop_by_offset(hk_ele,x1,0).perform()
    time.sleep(2)
    try:
        WebDriverWait(web,10).until(ec.presence_of_element_located((By.XPATH,'//*[@id="reload"]/div')))
    except:
        web.quit()
        break










