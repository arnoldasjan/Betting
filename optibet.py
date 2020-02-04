from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options


dic = {
    'CSKA Moscow': 'CSKA Maskva',
    'Anadolu Efes Istanbul': 'Anadolu Efes',
    'Zalgiris Kaunas': 'Žalgiris',
    'Olympiakos Pireus': 'Olympiacos',
    'Emporio Armani Milano': 'Milano Armani Exchange',
    'Alba Berlin': 'Alba Berlin',
    'ASVEL Lyon-Villeurbanne': 'Asvel Lyon Villeurbanne',
    'Bayern Munich': 'FC Bayern Munchen',
    'Real Madrid': 'Real Madrid',
    'CD Saski Baskonia': 'Baskonia Vitoria Gasteiz',
    'Zenit St Petersburg': 'Zenit',
    'Fenerbahce Ulker': 'Fenerbahce',
    'Crvena Zvezda': 'Crvena Zvezda',
    'Panathinaikos AO': 'Panathinaikos',
    'Maccabi Tel-Aviv': 'Maccabi Tel Aviv',
    'BC Khimki': 'BC Khimki',
    'Valencia BC': 'Valencia Basket',
    'FC Barcelona': 'Barcelona Lassa'
}

class OptibetBot:
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
        driver.get('https://www.optibet.lt/lt/sport/prematch/NBA-466')
        time.sleep(8)
        # df = pd.DataFrame(columns=['Time', 'Home Team', 'Away Team', 'Optibet HW', 'Optibet AW'])
        df = pd.DataFrame(columns=['Home Team', 'Away Team', 'Optibet HW', 'Optibet AW'])
        try:
            driver.switch_to.frame(driver.find_element_by_id("iFrameResizer0"))
            findedrows = driver.find_elements_by_xpath("//div[contains(@class, 'event-block-row event-block__row')]")
            for row in findedrows:
                tim = row.find_element_by_xpath(".//div[@class='event-block-row__time']")
                teams = row.find_element_by_xpath(".//div[@class='event-block-row__name']")
                odds = row.find_elements_by_xpath(".//div[@class='odd__value']")
                if len(odds) > 0:
                    # df = df.append({'Time': tim.text,
                    #                 'Home Team': teams.text.split(' - ')[0], 'Away Team': teams.text.split(' - ')[1],
                    #                 'Optibet HW': odds[0].text,
                    #                 'Optibet AW': odds[1].text},
                    #                ignore_index=True)
                    df = df.append({'Home Team': teams.text.split(' - ')[0], 'Away Team': teams.text.split(' - ')[1],
                                    'Optibet HW': odds[0].text,
                                    'Optibet AW': odds[1].text},
                                   ignore_index=True)
            print(df)
            print('Optibet was successful')
            self.closeBrowser()
            return df
        except Exception as e:
            print("Optibet did not work:", format(e))
            self.closeBrowser()

    def scrapeEuroleague(self):
        driver = self.driver
        driver.get('https://www.optibet.lt/lt/sport/prematch/Eurolyga-494')
        time.sleep(8)
        # df = pd.DataFrame(columns=['Time', 'Home Team', 'Away Team', 'Optibet HW', 'Optibet AW'])
        df = pd.DataFrame(columns=['Home Team', 'Away Team', 'Optibet HW', 'Optibet AW'])
        try:
            driver.switch_to.frame(driver.find_element_by_id("iFrameResizer0"))
            findedrows = driver.find_elements_by_xpath("//div[contains(@class, 'event-block-row event-block__row')]")
            for row in findedrows:
                # tim = row.find_element_by_xpath(".//div[@class='event-block-row__time']")
                teams = row.find_element_by_xpath(".//div[@class='event-block-row__name']")
                odds = row.find_elements_by_xpath(".//div[@class='odd__value']")
                if len(odds) > 0:
                    # df = df.append({'Time': tim.text,
                    #                 'Home Team': teams.text.split(' - ')[0], 'Away Team': teams.text.split(' - ')[1],
                    #                 'Optibet HW': odds[0].text,
                    #                 'Optibet AW': odds[1].text},
                    #                ignore_index=True)
                    df = df.append({'Home Team': dic[teams.text.split(' - ')[0]], 'Away Team': dic[teams.text.split(' - ')[1]],
                                    'Optibet HW': odds[0].text,
                                    'Optibet AW': odds[1].text},
                                   ignore_index=True)
            print(df)
            print('Optibet was successful')
            self.closeBrowser()
            return df
        except Exception as e:
            print("Optibet did not work:", format(e))
            self.closeBrowser()
