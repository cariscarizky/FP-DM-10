import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
url = 'https://www.olx.co.id/jakarta-selatan_g4000030/properti_c88'
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get(url)

for i in range(100) :
  time.sleep(2)
  try:
    WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, "div._38O09 > button"))
    ).click()
    time.sleep(2)
  except NoSuchElementException:
    print("Tidak ada tombol lagi untuk di klik, berhenti.")
    break
  except Exception as e:
    print(f"Error saat mencoba klik tombol: {e}")
    break
time.sleep(3)

product=[]
soup = BeautifulSoup(driver.page_source, "html.parser")
for item in soup.findAll('li', class_='_1DNjI'):
  try:
    properti_name = item.find('span', class_='_2poNJ').text
    price = item.find('span', class_='_2Ks63').text
    lokasi = item.find('span', class_='_2VQu4').text
    detail = item.find('span', class_='YBbhy').text
    product.append(
      (properti_name, price, lokasi, detail))
  except AttributeError:
    print("Ada elemen yang tidak lengkap, dilewati.")
    continue

    

df = pd.DataFrame(product, columns=['Properti_Name', 'Price', 'Lokasi', 'Detail'])
print(df)

df.to_excel('OLX Selenium Bs4.xlsx', index=False)
driver.close()