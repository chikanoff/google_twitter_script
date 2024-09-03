import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from faker import Faker
import time
import openai

fake = Faker()

AUTH_TOKEN = "auth_token"

def setup_proxy_and_options(proxy_address=None, user_agent=None):
    chrome_options = Options()
    if proxy_address:
        chrome_options.add_argument(f'--proxy-server={proxy_address}')
    if user_agent:
        chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    return chrome_options

def save_data_to_csv(data, file_name='twitters.csv'):
    df = pd.DataFrame([data])
    try:
        df.to_csv(file_name, mode='a', header=False, index=False)
    except Exception as e:
        print(f"Error saving data: {e}")

def get_new_auth_token(driver, email, password):
    try:
        driver.get('https://twitter.com/login')
        
        email_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'text'))
        )
        email_input.send_keys(email)
        email_input.send_keys(u'\ue007')
        
        password_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'password'))
        )
        password_input.send_keys(password)
        password_input.send_keys(u'\ue007')
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-contents="true"]//div[@data-block="true"]'))
        )
        
        cookies = driver.get_cookies()
    
        for cookie in cookies:
            if cookie['name'] == 'auth_token':
                auth_token = cookie['value']
            
                return auth_token
        
        print("auth_token not found")
        return None
        
    finally:
        driver.quit()

def login_to_twitter(driver):
    driver.get("https://x.com/login")
    
    cookies = [
        {'name': 'auth_token', 'value': AUTH_TOKEN, 'domain': 'x.com'},
    ]

    for cookie in cookies:
        driver.add_cookie(cookie)

def post_tweet(driver, text):
    login_to_twitter(driver)
    driver.get("https://x.com/home")
    
    tweet_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//div[@data-contents="true"]//div[@data-block="true"]'))
    )
    tweet_box.click()
    tweet_box.send_keys(text)
    
    tweet_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="tweetButtonInline"]'))
    )
    
    tweet_button.click()
    time.sleep(1)
    driver.close()

def change_twitter_password(driver, current_password, new_password):
    login_to_twitter(driver)

    driver.get("https://x.com/settings/password")
    
    current_password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "current_password"))
    )
    current_password_input.send_keys(current_password)
    
    new_password_input = driver.find_element(By.NAME, "new_password")
    new_password_input.send_keys(new_password)
    
    time.sleep(0.5)
    confirm_password_input = driver.find_element(By.NAME, "password_confirmation")
    confirm_password_input.send_keys(new_password)
    confirm_password_input.send_keys(Keys.RETURN)
    
    time.sleep(0.5)
    save_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="settingsDetailSave"]'))
    )
    save_button.click()
    time.sleep(2)

def generate_tweet_text():
    openai.api_key = 'your-openai-api-key'
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Create a tweet text.",
        max_tokens=50
    )
    
    tweet_text = response.choices[0].text.strip()
    return tweet_text


def get_new_auth_token_and_save(driver, login, new_password):

    new_auth_token = get_new_auth_token(driver, login, new_password)

    data = {
        'login': login,
        'Password': new_password,
        'auth_token': new_auth_token
    }
    save_data_to_csv(data)

    driver.close()

def main():
    proxy_address = "http://my-proxy-server:port"
    user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1"
    login = "login"
    email = "email"
    current_password = "pwd"
    new_password = "new_pwd"
    
    chrome_options = setup_proxy_and_options(proxy_address, user_agent)

    try:
        
        with webdriver.Chrome(options=chrome_options) as driver:
            tweet_text = generate_tweet_text()
            post_tweet(driver, tweet_text)

        with webdriver.Chrome(options=chrome_options) as driver:
            change_twitter_password(driver, current_password, new_password)
        
        with webdriver.Chrome(options=chrome_options) as driver:
            get_new_auth_token_and_save(driver, login, new_password)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
