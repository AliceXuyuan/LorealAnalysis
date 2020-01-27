from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import csv
import re
import time

driver = webdriver.Chrome()

driver.get("https://www.lorealparisusa.com/products/makeup/lip-color/lipstick/rouge-signature-lightweight-matte-colored-ink-high-pigment.aspx?shade=450-adored")
review_button = driver.find_element_by_xpath('//*[@id="BVRRSummaryContainer"]/div/div/div/div/div/div/dl/dt/a/span[2]')
review_button.click()

csv_file = open('lipstain_reviews.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)

index = 1
while True:
    try:
        print("Scraping Page number " + str(index))
        index = index + 1
        # Find all the reviews on the page
        wait_review = WebDriverWait(driver, 10) ## wait until condition is satisfies or 10 seconds
        reviews = wait_review.until(EC.presence_of_all_elements_located((By.XPATH,
                                    '//*[@id="BVRRContainer"]/div/div/div/div/ol/li[@class="bv-content-item bv-content-top-review bv-content-review"]')))
        # print(" HERE 1 ")
        for review in reviews:
            # Initialize an empty dictionary for each review
            review_dict = {}

            # driver.execute_script("arguments[0].scrollIntoView();", review)

            # username
            try:
                username = review.find_element_by_xpath('./div[@class="bv-author-profile"]/div/div[@class="bv-author-avatar"]/div/div/h2').text
            except: 
                try:
                    username = review.find_element_by_xpath('./div[@class="bv-author-profile"]/div/div[@class="bv-author-avatar"]/div/div/button/h3').text
                except:
                    username = None
            # region
            try:
                region = review.find_element_by_xpath('./div[1]/div/div[2]/div[2]/span').text
            except:
                region = None

            # age
            try:
                age = review.find_element_by_xpath('./div[1]/div/div[2]/div[4]/ul/li[1]/span[2]').text
            # //*[@id="BVRRContainer"]/div/div/div/div/ol/li[2]/div[1]/div/div[2]/div[4]/ul/li[1]/span[2]
            except:
                age = None

            # gender
            try:
                gender = review.find_element_by_xpath('./div[1]/div/div[2]/div[4]/ul/li[2]/span[2]').text
            except:
                gender = None

            # haircolor
            try:
                haircolor = review.find_element_by_xpath('./div[1]/div/div[2]/div[4]/ul/li[4]/span[2]').text
            except:
                haircolor = None

            # complexion
            try:
                complexion = review.find_element_by_xpath('./div[1]/div/div[2]/div[4]/ul/li[5]/span[2]').text
            except:
                complexion = None

            # undertone
            try:
                undertone = review.find_element_by_xpath('./div[1]/div/div[2]/div[4]/ul/li[6]/span[2]').text
            except:
                undertone = None

            # eyecolor
            try:
                eyecolor = review.find_element_by_xpath('./div[1]/div/div[2]/div[4]/ul/li[3]/span[2]').text
            except:
                eyecolor = None

            # rating
            try:
                rating = review.find_element_by_xpath('./div[2]/div[1]/div/div[1]/div/div[@class="bv-content-header-meta"]/span/span/abbr[2]').get_attribute('title')
            #//*[@id="BVRRContainer"]/div/div/div/div/ol/li[11]/div[2]/div[1]/div/div[1]/div/div[1]/span/span/abbr[2]
            except:
                rating = None

            # time
            try:
                review_time = review.find_element_by_xpath('./div[2]/div[1]/div/div[1]/div/div[@class="bv-content-header-meta"]/div/div/div/div/span[2]').text
            except:
                review_time = None

            # quality_rating
            try:
                quality_rating = len(review.find_elements_by_xpath('./div[2]/div[1]/div/div[3]/div/dl/dd[1]/span/ul/li'))
            except:
                quality_rating = None

            # value_rating
            try:
                value_rating = len(review.find_elements_by_xpath('./div[2]/div[1]/div/div[3]/div/dl/dd[2]/span/ul/li'))
            except:
                value_rating = None

            # title
            try:
                title = review.find_element_by_xpath('./div[2]/div[1]/div/div[1]/div/div[3]/h3').text
            except:
                title = None

            # content
            try:
                content = review.find_element_by_xpath('./div[2]/div[1]/div/div[2]/div/div/div[1]/p').text
            except:
                content = None

            # received sample/points for this review
            try:
                review_benefit = review.find_element_by_xpath('./div[2]/div[1]/div/div[2]/div/div/div[2]/div[1]/dl[1]/dd').text
            except:
                review_benefit = None

            # purchase_again
            try:
                purchase_again = review.find_element_by_xpath('./div[2]/div[1]/div/div[2]/div/div/div[2]/div[1]/dl[2]/dd').text
            except:
                purchase_again = None

            # recommand
            try:
                recommand = review.find_element_by_xpath('./div[2]/div[1]/div/div[2]/div/div/div[2]/dl/dt/span[2]').text
            except:
                recommand = None

            review_dict['username'] = username
            review_dict['region'] = region
            review_dict['age'] = age
            review_dict['gender'] = gender
            review_dict['haircolor'] = haircolor
            review_dict['complexion'] = complexion
            review_dict['undertone'] = undertone
            review_dict['eyecolor'] = eyecolor
            review_dict['overall_rating'] = rating
            review_dict['review_time'] = review_time
            review_dict['quality_rating'] = quality_rating
            review_dict['value_rating'] = value_rating
            review_dict['title'] = title
            review_dict['content'] = content
            review_dict['recieved_sample_points'] = review_benefit
            review_dict['purchase_again'] = purchase_again
            review_dict['recommand'] = recommand


            # review_dict['age'] = age
            # review_dict['eyecolor'] = eyecolor

            writer.writerow(review_dict.values())

        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Locate the next button on the page.
        # time.sleep(5)
        # inputElement = driver.find_element_by_class_name('bv-content-btn bv-content-btn-pages bv-content-btn-pages-last bv-focusable bv-content-btn-pages-active')
        # inputElement.send_keys("\n")

        time.sleep(3)
        #print(" HERE 2 ")
        element = driver.find_element_by_xpath('//*[@id="BVRRContainer"]/div/div/div/div/div[@class="bv-content-pagination"]/div/ul/li[@class="bv-content-pagination-buttons-item bv-content-pagination-buttons-item-next"]/a')
        #print(" HERE 3 ")
        driver.execute_script("arguments[0].click();", element)
        # wait_button = WebDriverWait(driver, 10)
        # next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,
        #                             '//*[@id="BVRRContainer"]/div/div/div/div/div[@class="bv-content-pagination"]/div/ul/li[@class="bv-content-pagination-buttons-item bv-content-pagination-buttons-item-next"]/a')))
        # next_button.click()
        #print(" HERE 4 ")

    except Exception as e:
        print(e)
        csv_file.close()
        driver.close()
        break


