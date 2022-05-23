import argparse
import random
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

parser = argparse.ArgumentParser()

parser.add_argument('--port', default=9223, type=int)
parser.add_argument('--min_len', default=3, type=int)
parser.add_argument('--max_len', default=5, type=int)
parser.add_argument('--word', default=True, type=str)
parser.add_argument('--xpath', default=None, type=str)
parser.add_argument('--interval', default=60, type=int)

args = parser.parse_args()

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:%d"%(args.port))
chrome_driver = ".\chromedriver.exe"
driver = webdriver.Chrome(chrome_driver, options=chrome_options)

def sendable(path, keys):
    driver.implicitly_wait(10)
    send = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, path)))
    send.send_keys(keys)
    send.send_keys(Keys.RETURN)

def word_sentence():
    r_list = ['으아', 'ㅎ', 'ㅋㅋ', '3렙', '7렙', '초대도?', '달라', '챗굴', '화이팅', '헛둘',
              '가즈아', '화이팅', '행운아', '밤새부러', '언제되냐', '가보자', '다와간다', '언제 렙업...',
              '화리', '드가보자', '한국방', '초대', '랜덤', '아무말이나', '되보자', '느프트', '화력',
              '또 해보자', '되는건가', '새로운', '스테픈', '이건', '빡셉니다', '추가', 'Wen', '졸업',
              '프로젝트', '코인웤', '아직도..', '챗굴 가즈아', '희망회로', '굴려봅니다',
              '아무말', '대잔치', '똑같은게', '졸리다..', '힘들다..', '빡센챗굴', '레벨업', 'LFG']
    if args.word:
        r_len = random.randint(args.min_len, args.max_len + 1)
        r_select = random.sample(r_list, r_len)
    else:
        r_select = random.sample(r_list, 1)

    r_select = str(r_select).replace(',', '').replace("'", '')[1:-1]

    return r_select

if __name__ == '__main__':
    discord_tab = driver.window_handles[0]
    driver.switch_to.window(window_name=discord_tab)

    while True:
        sentence = word_sentence()
        sendable(args.xpath, sentence)
        time.sleep(args.interval)