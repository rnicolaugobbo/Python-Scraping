from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from threading import Thread

# Initialization of the WebDriver
browser = webdriver.Chrome()

# Getting the target webpage
browser.get("https://de.indeed.com/")

# Finding the right fields to be filled in the website
search_form_job = browser.find_element(By.ID, "text-input-what")
search_form_location = browser.find_element(By.ID, "text-input-where")

# Sending input to the website and submiting the search form
search_form_job.send_keys("python")
search_form_location.send_keys("berlin")
search_form_job.submit()

# Finding and waiting for cookie popup reject buttom to be clickable and clicking the buttom
reject_cookie = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By. ID, "onetrust-reject-all-handler")))
reject_cookie.click()

# Initializing empty results dictionary to hold our search results
results = {}

# Initializing page counter
current_page = 1

# Initializing variable so the user can stop the application before it's done
stop_input = False

# Initializing list to hold the keywords that are going to be searched in the website's results page
extra_filters = ["python", "test", "developer"]

# Defining a function to get user input to stop the application
def get_user_input():
    global stop_input
    input("Press enter to stop.")
    stop_input = True

# Initializing multithreading to wait for user input while the rest of the application continues running
input_thread = Thread(target = get_user_input)
input_thread.start()

# Main application logic
while not stop_input:
    # Wait until all the job results are loaded
    WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "mosaic-zone")))
    print("Page loaded.")

    # Initializing variable to hold the results from the website
    job_listings = browser.find_elements(By.CLASS_NAME, "mosaic-zone")

    for job in job_listings:
        try:
            # Try to find page element jobTitle
            job_title_element = job.find_element(By. CLASS_NAME, "jobTitle")
            # Convert jobTitle element to text and to lower case
            job_title = job_title_element.text.lower()
            print(job_title)
            # Check if job_title has any of the keywords present in extra_filters. If it does, save the job_title as a key and the job_url as a value of our results dictionary
            if any(filter_word in job_title for filter_word in extra_filters):
                job_url = job.find_element(By.CLASS_NAME, "jobTitle").find_element(By.TAG_NAME, "a").get_attribute("href")
                results[job_title] = job_url
        # If the try block wasn't able to execute, continue the loop
        except:
            continue
    print("Scanning pages...")
    print("Number of URLs collected: " + str(len(results)) + "...")
        
    try:
        # Try to find and wait for the next page button to be clickable
        next_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By. CSS_SELECTOR, "[data-testid=pagination-page-next]")))
        print("Next page found.")
        # Click next page button
        next_button.click()
        # Increment page counter by 1
        current_page += 1
        print(current_page)
        # If page counter is equal to 2, wait for the email form close button to be clickable
        if current_page == 2:
            print("Waiting for email popup...")
            email_popup_close = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By. CSS_SELECTOR, "[aria-label=schließen]")))
            # Click email form close button
            email_popup_close.click()
        print("Button clicked.")
    # If try block wasn't able to execute, there are no more pages. Prompt the user to press Enter to generate CSV file and break out of the loop
    except:
        print("No more pages found.")
        print("Press Enter to generate CSV file.")
        break

# Wait for thread to terminate
input_thread.join()

# Generate CSV file from the results dictionary
with open("results.csv", "w", newline = "") as results_csv:
    w = csv.writer(results_csv)
    w.writerow(["Job Title", "Job Link"])
    for job_title, job_link in results.items():
        w.writerow([job_title, job_link])