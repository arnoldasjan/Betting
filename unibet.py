from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options

dic = {
    'Maskvos CSKA': 'CSKA Maskva',
    'Anadolu Efes': 'Anadolu Efes',
    'Kauno Žalgiris': 'Žalgiris',
    'Olympiacos Piraeus': 'Olympiacos',
    'AX Armani Exchange Olimpia Milano': 'Milano Armani Exchange',
    'Alba Berlin': 'Alba Berlin',
    'Asvel Lyon-Villeurbanne': 'Asvel Lyon Villeurbanne',
    'FC Bayern München': 'FC Bayern Munchen',
    'Real Madrid': 'Real Madrid',
    'Kirolbet Baskonia': 'Baskonia Vitoria Gasteiz',
    'BC Zenit Saint Petersburg': 'Zenit',
    'Fenerbahçe Ülker': 'Fenerbahce',
    'KK Crvena Zvezda Belgrad': 'Crvena Zvezda',
    'Panathinaikos': 'Panathinaikos',
    'Maccabi Tel Aviv': 'Maccabi Tel Aviv',
    'BC Khimki Moscow': 'BC Khimki',
    'Valencia Basket Club': 'Valencia Basket',
    'FC Barcelona': 'Barcelona Lassa'
}

class UnibetBot:
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
        driver.get('https://lt.unibet-50.com/betting/sports/filter/basketball/nba')
        time.sleep(8)
        df = pd.DataFrame(columns=['Home Team', 'Away Team', 'Unibet HW', 'Unibet AW'])
        try:
            findedtabs = driver.find_elements_by_xpath("//div[@class='KambiBC-collapsible-container KambiBC-mod-event-group-container']")

            for tab in findedtabs:
                button = tab.find_element_by_xpath(".//header[@class='KambiBC-collapsible-header KambiBC-mod-event-group-header']")
                driver.execute_script("arguments[0].click();", button)
                time.sleep(1)

            findedrows = driver.find_elements_by_xpath("//div[@class='KambiBC-event-item__event-wrapper']")

            for row in findedrows:
                tim = row.find_element_by_xpath(".//span[@class='KambiBC-event-item__start-time--time']")
                teams = row.find_elements_by_xpath(".//div[@class='KambiBC-event-participants__name']")
                odds = row.find_elements_by_xpath(".//span[@class='KambiBC-mod-outcome__odds']")
                if len(odds) > 0:
                    df = df.append({'Home Team': teams[0].text, 'Away Team': teams[1].text,
                                    'Unibet HW': odds[0].text,
                                    'Unibet AW': odds[1].text},
                                   ignore_index=True)
            print(df)
            print('Unibet was successful')
            self.closeBrowser()
            return df
        except Exception as e:
            print("Unibet did not work:", format(e))
            self.closeBrowser()

    def scrapeEuroleague(self):
        driver = self.driver
        driver.get('https://lt.unibet-50.com/betting/sports/filter/basketball/euroleague')
        time.sleep(8)
        df = pd.DataFrame(columns=['Home Team', 'Away Team', 'Unibet HW', 'Unibet AW'])
        try:
            findedtabs = driver.find_elements_by_xpath("//div[@class='KambiBC-collapsible-container KambiBC-mod-event-group-container']")

            for tab in findedtabs:
                button = tab.find_element_by_xpath(".//header[@class='KambiBC-collapsible-header KambiBC-mod-event-group-header']")
                driver.execute_script("arguments[0].click();", button)
                time.sleep(2)

            findedrows = driver.find_elements_by_xpath("//div[@class='KambiBC-event-item__event-wrapper']")

            for row in findedrows:
                try:
                    tim = row.find_element_by_xpath(".//span[@class='KambiBC-event-item__start-time--time']")
                except:
                    continue
                teams = row.find_elements_by_xpath(".//div[@class='KambiBC-event-participants__name']")
                odds = row.find_elements_by_xpath(".//span[@class='KambiBC-mod-outcome__odds']")
                if len(odds) > 0:
                    df = df.append({'Home Team': dic[teams[0].text], 'Away Team': dic[teams[1].text],
                                    'Unibet HW': odds[0].text,
                                    'Unibet AW': odds[1].text},
                                   ignore_index=True)
            print(df)
            print('Unibet was successful')
            self.closeBrowser()
            return df
        except Exception as e:
            print("Unibet did not work:", format(e))
            self.closeBrowser()
