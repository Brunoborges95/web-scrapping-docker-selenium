from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
from datetime import datetime
import pandas as pd


def handler(event=None, context=None):
    options = webdriver.ChromeOptions()
    service = webdriver.ChromeService("/opt/chromedriver")

    options.binary_location = '/opt/chrome/chrome'
    options.add_argument("--headless=new")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")

    driver = webdriver.Chrome(options=options, service=service)
    url = 'https://br.investing.com/stock-screener/?sp=country::32|sector::a|industry::a|equityType::a|exchange::a%3Ceq_market_cap;1'
    driver.get(url)
    time.sleep(5)
    list_df = []
    c = True
    i=0
    while c:
        try:
            table_element = driver.find_element(By.XPATH, '//*[@id="resultsTable"]')
            table_html = table_element.get_attribute('outerHTML')
            list_df.append(pd.read_html(table_html, index_col=0, thousands='.', decimal=',', na_values=['-'])[0].reset_index(drop=True))
            driver.find_element(By.XPATH, '//*[@id="paginationWrap"]/div[3]/a').click()
            time.sleep(5)
            i+=1
            print('página', i)
        except Exception as e:
            # Trate o erro aqui, se necessário
            print(f"Número de páginas alcançadas: {e}")
            # Encerre o loop após o erro
            c = False
    bucket_name = 'bbs-datalake'
    today = datetime.now().strftime("%Y-%m-%d")
    object_name = f'SourceZone/stock_info/{today}/df_stocks_info.csv'
    df = pd.concat(list_df)
    df = df.iloc[:,:-1]
    df.to_csv(f's3://{bucket_name}/{object_name}', index=False)

    return {
        'statusCode': 200,
        'body': f'The csv file can be found in s3://{bucket_name}/{object_name}'
    }

