from selenium import webdriver
import pandas as pd
import time
from datetime import datetime
from selenium.webdriver.chrome.options import Options


class TOPsportBot:
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
        driver.get('https://www.topsport.lt/krepsinis/nba')
        time.sleep(8)
        df = pd.DataFrame(columns=['Report Time', 'Time', 'Home Team', 'Away Team', 'TOPsport HW', 'TOPsport AW'])
        try:
            element = driver.find_element_by_xpath("//*[contains(text(), 'Rungtynių nugalėtojas')]")
            driver.execute_script("arguments[0].click();", element)
            element2 = driver.find_element_by_xpath('//button[@id="list_filter_filter"]')
            driver.execute_script("arguments[0].click();", element2)

            findedrows = driver.find_elements_by_xpath("//div[@class='js-prelive-event-row row h-gutter1 h-gutter2-md']")
            rtime = datetime.now().strftime('%Y-%m-%d %H:%M')

            for row in findedrows:
                tim = row.find_element_by_xpath(".//span[@class='prelive-event-date h-fs11']")
                teams = row.find_elements_by_xpath(".//div[@class='prelive-list-league-choice-title d-flex align-items-center']")
                odds = row.find_elements_by_xpath(".//span[@class='prelive-list-league-rate ml-1 h-font-secondary h-fs17 h-fw500']")
                if len(odds) > 0:
                    df = df.append({'Report Time': rtime,
                                    'Time': tim.text.split(' ')[-1],
                                    'Home Team': teams[0].text, 'Away Team': teams[1].text,
                                    'TOPsport HW': odds[0].text.replace(',', '.'),
                                    'TOPsport AW': odds[1].text.replace(',', '.')},
                                   ignore_index=True)
            print(df)
            print('TOPsport was successful')
            self.closeBrowser()
            return df
        except Exception as e:
            print("TOPsport did not work:", format(e))
            self.closeBrowser()

    def scrapeEuroleague(self):
        driver = self.driver
        driver.get('https://www.topsport.lt/krepsinis/eurolyga')
        time.sleep(8)
        df = pd.DataFrame(columns=['Report Time', 'Time', 'Home Team', 'Away Team', 'TOPsport HW', 'TOPsport AW'])
        try:
            element = driver.find_element_by_xpath("//*[contains(text(), 'Rungtynių nugalėtojas')]")
            driver.execute_script("arguments[0].click();", element)
            element2 = driver.find_element_by_xpath('//button[@id="list_filter_filter"]')
            driver.execute_script("arguments[0].click();", element2)

            findedrows = driver.find_elements_by_xpath("//div[@class='js-prelive-event-row row h-gutter1 h-gutter2-md']")
            rtime = datetime.now().strftime('%Y-%m-%d %H:%M')

            for row in findedrows:
                tim = row.find_element_by_xpath(".//span[@class='prelive-event-date h-fs11']")
                teams = row.find_elements_by_xpath(".//div[@class='prelive-list-league-choice-title d-flex align-items-center']")
                odds = row.find_elements_by_xpath(".//span[@class='prelive-list-league-rate ml-1 h-font-secondary h-fs17 h-fw500']")
                if len(odds) > 0:
                    df = df.append({'Report Time': rtime,
                                    'Time': tim.text,
                                    'Home Team': teams[0].text, 'Away Team': teams[1].text,
                                    'TOPsport HW': odds[0].text.replace(',', '.'),
                                    'TOPsport AW': odds[1].text.replace(',', '.')},
                                   ignore_index=True)
            print(df)
            print('TOPsport was successful')
            self.closeBrowser()
            return df
        except Exception as e:
            print("TOPsport did not work:", format(e))
            self.closeBrowser()
