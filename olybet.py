from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options

dic = {
    'PBC CSKA Moscow': 'CSKA Maskva',
    'Anadolu Efes SK': 'Anadolu Efes',
    'BC Zalgiris': 'Žalgiris',
    'Olympiacos Piraeus BC': 'Olympiacos',
    'Olimpia Milano': 'Milano Armani Exchange',
    'Alba Berlin': 'Alba Berlin',
    'Asvel Lyon-Villeurbanne': 'Asvel Lyon Villeurbanne',
    'Bayern Munich': 'FC Bayern Munchen',
    'Real Madrid': 'Real Madrid',
    'Saski Baskonia': 'Baskonia Vitoria Gasteiz',
    'Zenit Saint Petersburg': 'Zenit',
    'Fenerbahce': 'Fenerbahce',
    'KK Crvena Zvezda': 'Crvena Zvezda',
    'Panathinaikos BC': 'Panathinaikos',
    'Maccabi Tel Aviv': 'Maccabi Tel Aviv',
    'BC Khimki': 'BC Khimki',
    'Valencia Basket': 'Valencia Basket',
    'FC Barcelona Basquet': 'Barcelona Lassa'
}

class OlybetBot:
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
        driver.get('https://www.olybet.lt/sports?competition=756&game=15994052&region=50003&type=0&sport=3&')
        time.sleep(8)
        # df = pd.DataFrame(columns=['Time', 'Home Team', 'Away Team', 'Olybet HW', 'Olybet AW'])
        df = pd.DataFrame(columns=['Home Team', 'Away Team', 'Olybet HW', 'Olybet AW'])
        try:
            driver.switch_to.frame(driver.find_element_by_id("bcsportsbookiframe"))

            findedteams = driver.find_elements_by_xpath("//div[@class='aic-team-names']")
            findedtimes = driver.find_elements_by_xpath("//div[@class='time-game-v3']")

            for i in range(1, len(findedtimes)+1):
                upperi = i * 2 - 1
                loweri = upperi - 1
                driver.execute_script("arguments[0].click();", findedtimes[i-1])
                time.sleep(3)
                if len(driver.find_elements_by_xpath("//div[@class='single-events-b-v3 blocked']")) == 0:
                    findedodds = driver.find_elements_by_xpath("//b[@class='p-v ']")
                    if len(findedodds) > 0:
                        realodds = []
                        while len(realodds) <= 1:
                            for odd in findedodds:
                                if odd.text != '' and odd.get_attribute('class') != 'p-v  ng-hide down-1':
                                    realodds.append(odd.text)
                        # df = df.append({'Time': findedtimes[i-1].text,
                        #                 'Home Team': findedteams[upperi].text, 'Away Team': findedteams[loweri].text,
                        #                 'Olybet HW': realodds[1],
                        #                 'Olybet AW': realodds[0]},
                        #                ignore_index=True)
                        df = df.append({'Home Team': findedteams[upperi].text, 'Away Team': findedteams[loweri].text,
                                        'Olybet HW': realodds[1],
                                        'Olybet AW': realodds[0]},
                                       ignore_index=True)
            print(df)
            print('Olybet was successful')
            self.closeBrowser()
            return df
        except Exception as e:
            print("Olybet did not work:", format(e))
            self.closeBrowser()

    def scrapeEuroleague(self):
        driver = self.driver
        driver.get('https://www.olybet.lt/sports')
        time.sleep(8)
        # df = pd.DataFrame(columns=['Time', 'Home Team', 'Away Team', 'Olybet HW', 'Olybet AW'])
        df = pd.DataFrame(columns=['Home Team', 'Away Team', 'Olybet HW', 'Olybet AW'])
        try:
            driver.switch_to.frame(driver.find_element_by_id("bcsportsbookiframe"))
            element = driver.find_element_by_xpath("//span[contains(text(), 'Eurolyga')]")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(3)
            findedrows = driver.find_elements_by_xpath("//table[starts-with(@class, 'aic-hdp-row')]")
            for row in findedrows:
                if row.text != '':
                    driver.execute_script("arguments[0].click();", row)
                    time.sleep(5)
                    # if len(driver.find_elements_by_xpath("//div[@class='single-events-b-v3 blocked']")) == 0:
                    teams = row.find_elements_by_xpath(".//div[@class='aic-team-names']")
                    tim = row.find_element_by_xpath(".//div[@class='time-game-v3']")
                    block = driver.find_element_by_xpath("//div[@class='market-ciew-v3']")
                    title = block.find_element_by_xpath(".//div[@class='market-title-v3']")
                    if 'Rungtynių nugalėtojas' in title.get_attribute('data-title'):
                        odds = row.find_elements_by_xpath("//b[starts-with(@class, 'p-v')]")
                        if len(odds) > 0:
                            realodds = []
                            while len(realodds) <= 1:
                                for odd in odds:
                                    if odd.text != '' and odd.get_attribute('class') != 'p-v  ng-hide down-1':
                                        realodds.append(odd.text)
                            # df = df.append({'Time': tim.text,
                            #                 'Home Team': teams.text.split(' - ')[0], 'Away Team': teams.text.split(' - ')[1],
                            #                 'Optibet HW': odds[0].text,
                            #                 'Optibet AW': odds[1].text},
                            #                ignore_index=True)
                            df = df.append({'Home Team': dic[teams[0].text], 'Away Team': dic[teams[1].text],
                                            'Olybet HW': realodds[0],
                                            'Olybet AW': realodds[1]},
                                           ignore_index=True)
            print(df)
            print('Olybet was successful')
            self.closeBrowser()
            return df
        except Exception as e:
            print("Olybet did not work:", format(e))
            self.closeBrowser()
