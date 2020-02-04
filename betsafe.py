from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options


class BetsafeBot:
    def __init__(self):
        WINDOW_SIZE = "1920,1080"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        self.driver = webdriver.Chrome(chrome_options=chrome_options)


    def closeBrowser(self):
        self.driver.close()
        self.driver.quit()


    def scrapeNba(self):
        driver = self.driver
        driver.get('https://betsafe.lt/betting-categories/nba')
        time.sleep(8)
        # df = pd.DataFrame(columns=['Time', 'Home Team', 'Away Team', 'Olybet HW', 'Olybet AW'])
        df = pd.DataFrame(columns=['Home Team', 'Away Team', 'Betsafe HW', 'Betsafe AW'])
        try:
            findedlinks = driver.find_elements_by_xpath("//a[@class='icon text']")
            for link in findedlinks:
                if int(link.text[1:]) > 0:
                    script = "window.open('{}');".format(link.get_attribute('href'))
                    driver.execute_script(script)
                    time.sleep(2)
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(2)
                    try:
                        block = driver.find_element_by_xpath("//div[@id='odds-1_0']")
                    except:
                        continue
                    teams = driver.find_elements_by_xpath("//h3")
                    odds = block.find_elements_by_xpath(".//span")
                    df = df.append({'Home Team': teams[0].text.lower().title(), 'Away Team': teams[1].text.lower().title(),
                                    'Betsafe HW': odds[-2].text,
                                    'Betsafe AW': odds[-1].text},
                                   ignore_index=True)
                    time.sleep(2)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(2)
            print(df)
            print('Betsafe was successful')
            self.closeBrowser()
            return df
        except Exception as e:
            print("Betsafe did not work:", format(e))
            self.closeBrowser()

    def scrapeEuroleague(self):
        driver = self.driver
        driver.get('https://betsafe.lt/krepsinis/europa/euroleague')
        time.sleep(8)
        # df = pd.DataFrame(columns=['Time', 'Home Team', 'Away Team', 'Olybet HW', 'Olybet AW'])
        df = pd.DataFrame(columns=['Home Team', 'Away Team', 'Betsafe HW', 'Betsafe AW'])
        try:
            findedlinks = driver.find_elements_by_xpath("//a[@class='icon text']")
            for link in findedlinks:
                if int(link.text[1:]) > 0:
                    script = "window.open('{}');".format(link.get_attribute('href'))
                    driver.execute_script(script)
                    time.sleep(2)
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(2)
                    try:
                        block = driver.find_element_by_xpath("//div[@id='odds-1_0']")
                    except:
                        continue
                    teams = driver.find_elements_by_xpath("//h3")
                    odds = block.find_elements_by_xpath(".//span")
                    df = df.append({'Home Team': teams[0].text.lower().title(), 'Away Team': teams[1].text.lower().title(),
                                    'Betsafe HW': odds[-2].text,
                                    'Betsafe AW': odds[-1].text},
                                   ignore_index=True)
                    time.sleep(2)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(2)
            print(df)
            print('Betsafe was successful')
            self.closeBrowser()
            return df
        except Exception as e:
            print("Betsafe did not work:", format(e))
            self.closeBrowser()
