from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Defining function to get user's search keywords
def get_search_keywords():
    #Getting user input
    user_input_keywords = \
        str(input("Please type the keywords of the job title separated by a space:" + "\n")).lower().split(" ")
    return user_input_keywords
    
# Defining function to find and wait for cookie popup reject buttom to be clickable and click the buttom
def reject_cookies(browser):
    reject_cookie = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By. ID, "onetrust-reject-all-handler")))
    reject_cookie.click()

def email_popup_close(browser):
    print("Waiting for email popup...")
    email_popup_close = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By. CSS_SELECTOR, "[aria-label=schließen]")))
    # Click email form close button
    email_popup_close.click()