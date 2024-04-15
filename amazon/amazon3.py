# input: book name data csv
# output: book prices in different formats but without "rank"
# need to scrape url, too

import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service #
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException #

driver_path = "chromedriver.exe" #
brave_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe" #

book_title_df = pd.read_csv('C:/Users/葉/Desktop/amazon/amazon-crawler/book_title.csv', index_col=0)
book_title = book_title_df['book_title'].tolist()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = brave_path


# def try_operation(target, operation_list):
#     for index, operation in enumerate(operation_list):
#         try:
#             print(f"{target} operation {index+1} successful")
#             return operation()
#         except:
#             print(f"Error in {target} operation {index+1}")
#     return None

outcomes = pd.DataFrame(columns=['title', 'publication_date', 'KINDLE', 'KINDLE_BASE', 'AUDIO_DOWNLOAD', 'HARDCOVER', 'HARDCOVER_BASE', 'PAPERBACK'])
for item in book_title[1:10]:
    print("==================================")
    print("item: ", item)
    item_string = '+'.join(item.split())
    # item_string = '%'.join(item.split())
    url = "https://www.amazon.com/s?k=" + item_string
    print('url: ', url)
    s = Service(driver_path)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    #driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options) #
    driver.get(url)
    time.sleep(1)
    driver.refresh()
    time.sleep(1)

    try:
        input = driver.find_element(By.ID, "e")
        input.send_keys(item)
        button = driver.find_element(By.ID, "f")
        button.click()
    except:
        pass

    title = driver.find_element(By.CLASS_NAME, 'a-size-mini.a-spacing-none.a-color-base.s-line-clamp-2').find_element(By.TAG_NAME, 'a')
    title.click()
    time.sleep(1)
    driver.refresh()


    # publication date
    print("----------------------------------")
    publication_date = None
    try:
        publication_date = driver.find_element(By.ID, 'rpi-attribute-book_details-publication_date') \
            .find_elements(By.TAG_NAME, 'div')[2] \
            .find_element(By.TAG_NAME, 'span') \
            .get_attribute('innerHTML').strip()
        print("publication_date operation 1 successful")
    except:
        print("Error in publication_date operation 1")
    try:
        publication_date = driver.find_element(By.ID, 'rpi-attribute-audiobook_details-release-date') \
            .find_elements(By.TAG_NAME, 'div')[2] \
            .find_element(By.TAG_NAME, 'span') \
            .get_attribute('innerHTML').strip()
        print("publication_date operation 2 successful")
    except:
        print("Error in publication_date operation 2")
    print("publication_date: ", publication_date)
    

    # Kindle
    print("----------------------------------")
    driver.find_element(By.ID, 'formats').find_element(By.ID, 'tmm-grid-swatch-KINDLE').click()
    time.sleep(1)
    form = driver.find_element(By.ID, 'priceBlock-outsideOfForm_feature_div')

    # KINDLE_BASE
    KINDLE_BASE = None
    try:
        KINDLE_BASE = form \
            .find_element(By.ID, 'basis-price') \
            .get_attribute('innerHTML').lstrip().rstrip(' <!-- Omnibus - More Information Tooltip -->\n')
        print("KINDLE_BASE operation 1 successful")
    except:
        print(f"Error in KINDLE_BASE operation 1")
    print("KINDLE_base: ", KINDLE_BASE)

    # KINDLE
    KINDLE = None
    try:
        KINDLE = form \
            .find_element(By.ID, 'kindle-price') \
            .get_attribute('innerHTML').strip()
        print("KINDLE operation 1 successful")
    except:
        print(f"Error in KINDLE operation 1")
    print("KINDLE: ", KINDLE)
    
    
    # Hardcover
    print("----------------------------------")
    driver.find_element(By.ID, 'formats').find_element(By.ID, 'tmm-grid-swatch-HARDCOVER').click()
    time.sleep(1)

    # HARDCOVER
    HARDCOVER = None
    try:
        HARDCOVER = driver.find_element(By.ID, 'booksHeaderSection') \
            .find_element(By.ID, 'price').get_attribute('innerHTML').strip()
        print("HARDCOVER operation 1 successful")
    except:
        print(f"Error in HARDCOVER operation 1")
    try:
        HARDCOVER = driver.find_element(By.CLASS_NAME, 'a-box-inner.a-accordion-row-container') \
            .find_element(By.CLASS_NAME, 'a-offscreen') \
            .find_element(By.ID, 'price').get_attribute('innerHTML').strip()
        print("HARDCOVER operation 2 successful")
    except:
        print(f"Error in HARDCOVER operation 2")
    print("HARDCOVER: ", HARDCOVER)

    # HARDCOVER_BASE
    HARDCOVER_BASE = None
    try:
        HARDCOVER_BASE = driver.find_element(By.CLASS_NAME, 'a-accordion-inner.accordion-row-content') \
            .find_element(By.ID, 'listPrice') \
            .get_attribute('innerHTML').strip()
        print("HARDCOVER_BASE operation 1 successful")
    except:
        print(f"Error in HARDCOVER_BASE operation 1")
    try:
        HARDCOVER_BASE = driver.find_element(By.ID, 'booksAdditionalPriceInfoContainer') \
            .find_element(By.ID, 'listPrice') \
            .get_attribute('innerHTML').strip()
        print("HARDCOVER_BASE operation 2 successful")
    except:
        print(f"Error in HARDCOVER_BASE operation 2")
    print("HARDCOVER_BASE: ", HARDCOVER_BASE)


    # AUDIODOWNLOAD
    print("----------------------------------")
    AUDIO_DOWNLOAD = None
    try:
        AUDIO_DOWNLOAD = driver.find_element(By.ID, 'formats') \
            .find_element(By.ID, 'tmm-grid-swatch-AUDIO_DOWNLOAD') \
            .find_element(By.CLASS_NAME, 'slot-price') \
            .find_element(By.TAG_NAME, 'span') \
            .find_element(By.TAG_NAME, 'span') \
            .get_attribute('innerHTML').strip()
        print("AUDIO_DOWNLOAD operation 1 successful")
    except:
        print(f"Error in AUDIO_DOWNLOAD operation 1")
    print("AUDIO_DOWNLOAD: ", AUDIO_DOWNLOAD)


    # Paperback
    print("----------------------------------")
    PAPERBACK = None
    try:
        PAPERBACK = driver.find_element(By.ID, 'formats') \
            .find_element(By.ID, 'tmm-grid-swatch-PAPERBACK') \
            .find_element(By.CLASS_NAME, 'slot-price') \
            .find_element(By.TAG_NAME, 'span') \
            .get_attribute('innerHTML').strip()
        print("PAPERBACK operation 1 successful")
    except:
        print(f"Error in PAPERBACK operation 1")
    print("PAPERBACK: ", PAPERBACK)


    # AUDIOBOOK
    print("----------------------------------")
    AUDIOBOOK = None
    try:
        AUDIOBOOK = driver.find_element(By.ID, 'formats') \
            .find_element(By.ID, 'tmm-grid-swatch-AUDIOBOOK') \
            .find_element(By.CLASS_NAME, 'slot-price') \
            .find_element(By.TAG_NAME, 'span') \
            .find_element(By.TAG_NAME, 'span') \
            .get_attribute('innerHTML').strip()
        print("AUDIOBOOK operation 1 successful")
    except:
        print(f"Error in AUDIOBOOK operation 1")
    print("AUDIOBOOK: ", AUDIOBOOK)
   

    driver.quit()
    # time.sleep(1)
    # PAPERBACK = driver.find_element(By.)
    # target = driver.find_element(By.ID, 'formats')
    # try:
    #     a = target.find_element(By.ID, 'tmm-grid-swatch-KINDLE').find_element(By.CLASS_NAME, 'slot-price').find_element(By.TAG_NAME, 'span').get_attribute('innerHTML').strip()
    #     KINDLE = a[a.index('US$'):].strip(' </span>')
    # except:
    #     KINDLE = None
    # try:
    #     a = target.find_element(By.ID, 'tmm-grid-swatch-AUDIO_DOWNLOAD').find_element(By.CLASS_NAME, 'slot-price').find_element(By.TAG_NAME, 'span').find_element(By.TAG_NAME, 'span').get_attribute('innerHTML').strip()
    #     AUDIO_DOWNLOAD = a[a.index('US$'):].strip(' </span>')
    # except:
    #     AUDIO_DOWNLOAD = None
    # try:
    #     a = target.find_element(By.ID, 'tmm-grid-swatch-HARDCOVER').find_element(By.CLASS_NAME, 'slot-price').get_attribute('innerHTML').strip()
    #     HARDCOVER = a[a.index('US$'):].strip(' </span>')
    #     # .find_element(By.TAG_NAME, 'a-size-base.a-color-price.a-color-price')
    # except:
    #     HARDCOVER = None
    # try:
    #     a = target.find_element(By.ID, 'tmm-grid-swatch-PAPERBACK').find_element(By.CLASS_NAME, 'slot-price').get_attribute('innerHTML').strip()
    #     PAPERBACK = a[a.index('US$'):].strip(' </span>')
    #     # .find_element(By.TAG_NAME, 'a-size-base.a-color-price.a-color-price').get_attribute('innerHTML').strip()
    # except:
    #     PAPERBACK = None
    # try:
    #     a = target.find_element(By.ID, 'tmm-grid-swatch-AUDIOBOOK').find_element(By.CLASS_NAME, 'slot-price').get_attribute('innerHTML').strip()
    #     AUDIOBOOK = a[a.index('US$'):].strip(' </span>')
    #     # .find_element(By.TAG_NAME, 'a-size-base.a-color-secondary').get_attribute('innerHTML').strip()
    # except:
    #     AUDIOBOOK = None



    new_outcome = pd.DataFrame({
        'title': [item],
        'publication_date': [publication_date],
        'KINDLE':[KINDLE],
        'KINDLE_BASE':[KINDLE_BASE],
        'AUDIO_DOWNLOAD':[AUDIO_DOWNLOAD],
        'HARDCOVER_BASE':[HARDCOVER_BASE],
        'PAPERBACK':[PAPERBACK],
        'AUDIOBOOK': [AUDIOBOOK]
    })
    outcomes = pd.concat([outcomes, new_outcome])

print(outcomes)
outcomes.to_csv('output2.csv')