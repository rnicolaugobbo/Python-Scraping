from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# opts = Options()

browser = webdriver.Chrome()

browser.get("https://de.indeed.com/")

search_form_job = browser.find_element(By.ID, "text-input-what")
search_form_location = browser.find_element(By.ID, "text-input-where")
search_form_job.send_keys("python")
search_form_location.send_keys("berlin")
search_form_job.submit()

reject_cookie = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By. ID, "onetrust-reject-all-handler")))
reject_cookie.click()

results = {}
current_page = 1

while True:
    WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "mosaic-zone")))
    print("Page loaded.")

    job_listings = browser.find_elements(By.CLASS_NAME, "mosaic-zone")

    for job in job_listings:
        try:
            if "developer" in job.text.lower():
                job_url = job.find_element(By.CLASS_NAME, "jobTitle").find_element(By.TAG_NAME, "a").get_attribute("href")
                job_title = job.find_element(By. CLASS_NAME, "jobTitle").text
                results[job_title] = job_url
        except:
            job_listings = browser.find_elements(By.CLASS_NAME, "mosaic-zone")
            continue

        print("Number of URLs collected:" + str(len(results)))
        
    try:
        next_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By. CSS_SELECTOR, "[data-testid=pagination-page-next]")))
        print("Next page found.")
        # browser.implicitly_wait(100)
        next_button.click()
        current_page += 1
        print(current_page)
        if current_page == 2:
            print("Waiting for email popup...")
            email_popup_close = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By. CSS_SELECTOR, "[aria-label=schließen]")))
            email_popup_close.click()
        # browser.implicitly_wait(100)
        print("Button clicked.")
    except:
        print("No more pages found.")
        break

print(results)