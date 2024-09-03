import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from faker import Faker
import time

fake = Faker()

def setup_proxy_and_options(proxy_address=None, user_agent=None):
    chrome_options = Options()
    if proxy_address:
        chrome_options.add_argument(f'--proxy-server={proxy_address}')
    if user_agent:
        chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    return chrome_options

def save_data_to_csv(data, file_name='gmails.csv'):
    df = pd.DataFrame([data])
    try:
        df.to_csv(file_name, mode='a', header=False, index=False)
    except Exception as e:
        print(f"Error saving data: {e}")

def change_google_password(email, current_password, new_password, proxy, user_agent):
    chrome_options = setup_proxy_and_options(proxy, user_agent)
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get("https://accounts.google.com/")

    email_input = driver.find_element(By.ID, "identifierId")
    email_input.send_keys(email)
    email_input.send_keys(Keys.RETURN)

    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "Passwd"))
    )
    password_input.send_keys(current_password)
    password_input.send_keys(Keys.RETURN)

    security_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/c-wiz/c-wiz/div/div[1]/div[3]/c-wiz/nav/ul/li[4]/a'))
    )
    security_btn.click()

    change_password_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='signinoptions/password?continue=https%3A%2F%2Fmyaccount.google.com%2Fsecurity']"))
    )
    change_password_btn.click()

    new_password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    new_password_input.send_keys(new_password)
    confirm_password_input = driver.find_element(By.NAME, "confirmation_password")
    confirm_password_input.send_keys(new_password)
    confirm_password_input.send_keys(Keys.RETURN)

    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='mUIrbf-LgbsSe mUIrbf-LgbsSe-OWXEXe-dgl2Hf' and @data-mdc-dialog-action='ok']"))
    )
    button.click()

    time.sleep(2)

    driver.quit()

def change_google_name(email, current_password, proxy, user_agent):
    chrome_options = setup_proxy_and_options(proxy, user_agent)
    driver = webdriver.Chrome(options=chrome_options)
    
    new_first_name = fake.first_name()
    new_last_name = fake.last_name()
    
    driver.get("https://accounts.google.com/")

    email_input = driver.find_element(By.ID, "identifierId")
    email_input.send_keys(email)
    email_input.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "Passwd"))
    )
    password_input = driver.find_element(By.NAME, "Passwd")
    password_input.send_keys(current_password)
    password_input.send_keys(Keys.RETURN)

    personal_info = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/c-wiz/c-wiz/div/div[1]/div[3]/c-wiz/nav/ul/li[2]/a'))
    )
    personal_info.click()

    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.RlFDUe[href*='profile/name']"))
    )
    element.click()

    edit_name_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.pYTkkf-Bz112c-mRLv6[href*='profile/name/edit']"))
    )
    edit_name_btn.click()

    first_name_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="i7"]'))
    )
    first_name_input.clear()
    first_name_input.send_keys(new_first_name)

    last_name_input = driver.find_element(By.XPATH, '//*[@id="i12"]')
    last_name_input.clear()
    last_name_input.send_keys(new_last_name)

    save_btn = driver.find_element(By.CSS_SELECTOR, "button span.UywwFc-vQzf8d")
    save_btn.click()

    time.sleep(2)

    driver.quit()

    data = {
        'Email': email,
        'Password': current_password,
        'First Name': new_first_name,
        'Last Name': new_last_name
    }
    save_data_to_csv(data)

def main():
    proxy = "http://my-proxy-server:port"
    user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1"

    email = "example@gmail.com"
    current_password = "current_password"
    new_password = "new_password"

    change_google_password(email, current_password, new_password, proxy, user_agent)
    change_google_name(email, new_password, proxy, user_agent)

if __name__ == "__main__":
    main()
