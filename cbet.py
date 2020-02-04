from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options


dic = {
    'CSKA Moscow': 'CSKA Maskva',
    'Anadolu Efes': 'Anadolu Efes',
    'Žalgiris': 'Žalgiris',
    'Olympiacos': 'Olympiacos',
    'EA7 Emporio Armani': 'Milano Armani Exchange',
    'ALBA Berlin': 'Alba Berlin',
    'Asvel Villeurbanne': 'Asvel Lyon Villeurbanne',
    'Bayern Munich': 'FC Bayern Munchen',
    'Real Madrid': 'Real Madrid',
    'Baskonia': 'Baskonia Vitoria Gasteiz',
    'B.C. Zenit Saint Petersburg': 'Zenit',
    'Fenerbahce': 'Fenerbahce',
    'Crvena Zvezda': 'Crvena Zvezda',
    'Panathinaikos': 'Panathinaikos',
    'Maccabi Tel Aviv': 'Maccabi Tel Aviv',
    'BC Khimki': 'BC Khimki',
    'Valencia Basket': 'Valencia Basket',
    'Barcelona': 'Barcelona Lassa'
}

class CbetBot:
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
        driver.get('https://cbet.lt/sportas/NBA')
        time.sleep(8)
        df = pd.DataFrame(columns=['Home Team', 'Away Team', 'Cbet HW', 'Cbet AW'])
        # df = pd.DataFrame(columns=['Time', 'Home Team', 'Away Team', 'Cbet HW', 'Cbet AW'])
        try:
            findedrows = driver.find_elements_by_xpath("//div[@class='d-flex flex-row flex-grow-1 mr-0']")
            for row in findedrows:
                tim = row.find_element_by_xpath(".//span[@class='h6 m-0']")
                teams = row.find_elements_by_xpath(".//span[@class='inplay-team-name mr-auto']")
                odds = row.find_elements_by_xpath(".//div[@class='odd order-1 order-sm-2']")
                if len(odds) > 0:
                    # df = df.append({'Time': tim.text[:-1] + '0',
                    #                 'Home Team': teams[0].text, 'Away Team': teams[1].text,
                    #                 'Cbet HW': odds[0].text,
                    #                 'Cbet AW': odds[1].text},
                    #                ignore_index=True)
                    df = df.append({'Home Team': teams[0].text, 'Away Team': teams[1].text,
                                    'Cbet HW': odds[0].text,
                                    'Cbet AW': odds[1].text},
                                   ignore_index=True)
            print(df)
            print('Cbet was successful')
            self.closeBrowser()
            return df
        except Exception as e:
            print("Cbet did not work", format(e))
            self.closeBrowser()

    def scrapeEuroleague(self):
        driver = self.driver
        driver.get('https://cbet.lt/sportas/Eurolyga')
        time.sleep(8)
        df = pd.DataFrame(columns=['Home Team', 'Away Team', 'Cbet HW', 'Cbet AW'])
        # df = pd.DataFrame(columns=['Time', 'Home Team', 'Away Team', 'Cbet HW', 'Cbet AW'])
        try:
            findedrows = driver.find_elements_by_xpath("//div[@class='d-flex flex-row flex-grow-1 mr-0']")
            for row in findedrows:
                tim = row.find_element_by_xpath(".//span[@class='h6 m-0']")
                teams = row.find_elements_by_xpath(".//span[@class='inplay-team-name mr-auto']")
                odds = row.find_elements_by_xpath(".//div[@class='odd order-1 order-sm-2']")
                if len(odds) > 0:
                    # df = df.append({'Time': tim.text[:-1] + '0',
                    #                 'Home Team': teams[0].text, 'Away Team': teams[1].text,
                    #                 'Cbet HW': odds[0].text,
                    #                 'Cbet AW': odds[1].text},
                    #                ignore_index=True)
                    df = df.append({'Home Team': dic[teams[0].text], 'Away Team': dic[teams[1].text],
                                    'Cbet HW': odds[0].text,
                                    'Cbet AW': odds[1].text},
                                   ignore_index=True)
            print(df)
            print('Cbet was successful')
            self.closeBrowser()
            return df
        except Exception as e:
            print("Cbet did not work", format(e))
            self.closeBrowser()
