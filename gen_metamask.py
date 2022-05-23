from selenium import webdriver
from win32api import GetSystemMetrics
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time, os

options = webdriver.FirefoxOptions()
options.add_argument("--headless")
options.add_argument('window-size=%dx%d'%(GetSystemMetrics(0), GetSystemMetrics(1)))

pw = '본인 비번' #메타마스크 비밀번호 (전부다 똑같음)
num_account = 299 #봇돌릴 계정 갯수 입력
mm_path = r'C:\Users\Junho\PycharmProjects\pythonProject2\metamask-10.12.4-an+fx.xpi' #본인에 맞게 수정해야함 참고로 윈도우에선 \ 이고 맥이나 우분투에선 /로 디렉토리 구분

# 웹에서 클릭버튼 누를때 쓰는 함수
def clickable(path, driver):
    driver.implicitly_wait(10)
    clk = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, path)))
    clk.click()

# 웹에서 텍스트 보낼때 쓰는 함수
def textable(path, driver):
    driver.implicitly_wait(10)
    clk = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, path)))
    return clk.text

# 웹에서 키값 보낼때 쓰는 함수
def sendable(path, keys, driver):
    driver.implicitly_wait(10)
    send = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, path)))
    send.send_keys(keys)

# 시드 / 지갑주소 / 프라이빗 키 값 저장
def save_pharse_address(seed, address, key):
    with open("./text/seed_address.txt", "w+") as f:
        f.write(seed)
        f.write(':')
        f.write(address)
        f.write(':')
        f.write(key)
        f.write("\n")

# 시드 구문 퍼즐 푸는 함수
def seed_puzzle(seed_phrase):
    seed_length = 12
    driver.implicitly_wait(5)
    seed_list = []

    for seed_idx in range(seed_length):
        instance = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[2]/div[5]/div[%d]' % (seed_idx + 1))))
        seed_list.append(instance.text)

    true_seed = seed_phrase.split(' ')

    for s_idx in range(seed_length):
        for c_idx in range(seed_length):
            if true_seed[s_idx] == seed_list[c_idx]:
                driver.implicitly_wait(5)
                clickable('/html/body/div[1]/div/div[2]/div/div/div[2]/div[5]/div[%d]' % (c_idx + 1), driver)
                # driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div/div[2]/div[5]/div[%d]' % (c_idx + 1)).click()
            else:
                pass

    driver.implicitly_wait(5)
    clickable('/html/body/div[1]/div/div[2]/div/div/div[2]/button', driver)
    clickable('/html/body/div[1]/div/div[2]/div/div/button', driver)

# 메타마스크 셋팅
def metamask_setting():
    # 메타마스크 탭 이동
    driver.implicitly_wait(10)
    last_tab = driver.window_handles[-1]

    # 화면 전체화 하고 메타마스크 비번 치고 클릭클릭 넘어감
    driver.switch_to.window(window_name=last_tab)

    clickable('/html/body/div[1]/div/div[2]/div/div/div/button', driver)
    clickable('/html/body/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/button', driver)
    clickable('/html/body/div[1]/div/div[2]/div/div/div/div[5]/div[1]/footer/button[2]', driver)
    sendable('//*[@id="create-password"]', pw, driver)
    sendable('//*[@id="confirm-password"]', pw, driver)
    clickable('/html/body/div[1]/div/div[2]/div/div/div[2]/form/div[3]/div', driver)
    clickable('/html/body/div[1]/div/div[2]/div/div/div[2]/form/button', driver)
    clickable('/html/body/div[1]/div/div[2]/div/div/div[2]/div/div[1]/div[2]/button', driver)
    clickable('/html/body/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div[5]/div[2]', driver)

    # 시드구문 복사하고 저장함
    seed_phrase = driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div[5]/div').text
    time.sleep(1)

    clickable('/html/body/div[1]/div/div[2]/div/div/div[2]/div[2]/button[2]', driver)

    # 시드구문 퍼즐 푸는 함수하고 클릭클릭
    driver.implicitly_wait(3)
    seed_puzzle(seed_phrase)

    clickable('/html/body/div[2]/div/div/section/div[1]/div/button', driver)

    # 점 세개 누르고
    clickable('/html/body/div[1]/div/div[3]/div/div/div/div[1]/button', driver)
    clickable('/html/body/div[2]/div[2]/button[2]', driver)
    
    # 주소랑 프라이빗 키 저장
    address = textable('/html/body/div[1]/div/span/div[1]/div/div/div/div[3]/div[2]/div/div/div[1]', driver)
    clickable('/html/body/div[1]/div/span/div[1]/div/div/div/button[3]', driver)
    sendable('/html/body/div[1]/div/span/div[1]/div/div/div/div[5]/input', pw, driver)
    clickable('/html/body/div[1]/div/span/div[1]/div/div/div/div[7]/button[2]', driver)
    pri_key = textable('/html/body/div[1]/div/span/div[1]/div/div/div/div[5]/div/textarea', driver)

    # 메마 접속 완료하고 시드, 주소, 프빗키 저장
    save_pharse_address(seed_phrase, address, pri_key)

if __name__ == '__main__':
    for num_idx in range(num_account):
        start = time.time()

        # Firefox 이니셜라이제이션
        driver = webdriver.Firefox(executable_path=".\geckodriver.exe", firefox_options=options)
        # driver = webdriver.Firefox(executable_path=".\geckodriver.exe")

        driver.install_addon(mm_path, temporary=True)
        driver.implicitly_wait(20)

        # 메타마스크 셋팅 함수
        metamask_setting()

        # 종료하고 담 반복문으로
        print(" [%d/%d] Metamask Setting is Completed for %.2f" %(num_idx+1, num_account, time.time()-start))

        driver.quit()