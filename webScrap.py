# import required modules
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# set up the web driver
PATH = "/home/okori/Downloads/ChromeDriver/chromedriver_linux64/chromedriver" #Reconfigure
driver = webdriver.Chrome(PATH)

# set up the product search and get the web page
product = "Samsung"
driver.get("https://jumia.ug/")
search = driver.find_element_by_name("q")
search.send_keys(product)
search.send_keys(Keys.RETURN)

# set up the CSV file for writing the results
filename = "jumia_products1.csv"
with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Product", "Price", "Shipped_from_abroad"])

    # loop through all pages and extract data
    while True:
        try:
            # wait for page to load
            main = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "jm"))
            )

            # extract data for each product on the page
            articles = main.find_elements_by_tag_name("article")
            for article in articles:
                try:
                    # extract product name and price
                    product_name = article.find_element_by_class_name("name")
                    product_price = article.find_element_by_class_name("prc")
                    shipped_from_abroad = "No"
                    if article.find_elements_by_css_selector("div.bdg._glb._xs"):
                        shipped_from_abroad = "Yes"

                    print("Product: " + product_name.text + "\nPrice: " + product_price.text + "\nShipped from abroad: " + shipped_from_abroad + "\n\n")

                    # write product name and price to CSV file
                    writer.writerow([product_name.text, product_price.text, shipped_from_abroad])

                except:
                    pass

            # check if there is a next page
            next_button = driver.find_elements_by_css_selector("a.pg[aria-label='Next Page']")
            if next_button:
                """next_button.click()
                time.sleep(5)"""
                next_page_url = next_button[0].get_attribute('href')
                driver.get(next_page_url)
                time.sleep(5)

            else:
                break  # no more pages, exit loop

        except:
            break  # error loading page, exit loop

# quit the web driver
driver.quit()
