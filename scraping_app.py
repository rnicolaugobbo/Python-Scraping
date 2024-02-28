from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from threading import Thread

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
stop_input = False

def get_user_input():
    global stop_input
    input("Press enter to stop.")
    stop_input = True

extra_filters = ["python", "test", "developer"]

input_thread = Thread(target = get_user_input)
input_thread.start()

while not stop_input:
    WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "mosaic-zone")))
    print("Page loaded.")

    job_listings = browser.find_elements(By.CLASS_NAME, "mosaic-zone")

    for job in job_listings:
        try:
            job_title_element = job.find_element(By. CLASS_NAME, "jobTitle")
            job_title = job_title_element.text.lower()
            print(job_title)
            if any(filter_word in job_title for filter_word in extra_filters):
                job_url = job.find_element(By.CLASS_NAME, "jobTitle").find_element(By.TAG_NAME, "a").get_attribute("href")
                results[job_title] = job_url
        except:
            continue
    print("Scanning pages...")
    print("Number of URLs collected: " + str(len(results)) + "...")
        
    try:
        next_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By. CSS_SELECTOR, "[data-testid=pagination-page-next]")))
        print("Next page found.")
        next_button.click()
        current_page += 1
        print(current_page)
        if current_page == 2:
            print("Waiting for email popup...")
            email_popup_close = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By. CSS_SELECTOR, "[aria-label=schließen]")))
            email_popup_close.click()
        print("Button clicked.")
    except:
        print("No more pages found.")
        print("Press Enter to generate CSV file.")
        break

input_thread.join()

with open("results.csv", "w", newline = "") as results_csv:
    w = csv.writer(results_csv)
    w.writerow(["Job Title", "Job Link"])
    for job_title, job_link in results.items():
        w.writerow([job_title, job_link])