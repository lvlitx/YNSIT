from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Setup the Chrome driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Open the target website
driver.get("https://biology.ucsd.edu/research/academic-departments/mb/faculty.html")
time.sleep(5)

# Find all <strong> elements or what ever u need
allLinks = driver.find_elements(By.XPATH, "//strong")
names_and_emails = {}

# Iterate over each link and perform the required actions
for i, link in enumerate(allLinks):
    try:
        # Get the name
        name = link.text.strip()
        names_and_emails[name] = None  # Initialize with None

        # Open link in a new tab using ActionChains
        action = ActionChains(driver)
        action.key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(5)  # Wait for the new page to load #dont change the time internet might be slow on ur computer

        # Find the email element (update the XPath as per the actual page structure)
        email_element = driver.find_element(By.XPATH, "//a[contains(@href, 'mailto:')]")
        email = email_element.get_attribute('href').replace('mailto:', '').strip()

        # Store the email
        names_and_emails[name] = email # for each name each email

        # Print the result
        print(f"Name: {name}, Email: {email}")

        # Close the current tab and switch back to the main tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        break

        # Re-fetch the <strong> elements, as the DOM may have changed
        allLinks = driver.find_elements(By.XPATH, "//strong")
    except Exception as e:
        print(f"Failed to process {name}: {e}")
        # Ensure we're back to the main tab in case of any error
        if len(driver.window_handles) > 1:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        allLinks = driver.find_elements(By.XPATH, "//strong")

# Print all names and emails
print(names_and_emails)

# Close the driver
driver.quit()
df = pd.DataFrame(list(names_and_emails.items()), columns=['Name', 'Email'])

# Save the DataFrame to a CSV file
df.to_csv('faculty_emails.csv', index=False)

print("Data has been saved to faculty_emails.csv")




