from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
import requests

class JobTracker:
    def __init__(self):
        self.job_titles = []
        self.job_company = []
        self.job_loc = []
        self.job_link = []
        self.job_date = []
        usr, pas = self.data()
        self._user = usr.strip()
        self._pas = pas.strip()

    def data(self):
        with open("layout\\user_data\\login.txt", "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            if len(lines) < 2:
                raise ValueError("Login file must contain at least two lines: username and password.")
            return lines[0], lines[1]

class JobSearcher(JobTracker):
    def __init__(self):
        super().__init__()
        options = Options()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
        options.add_argument("--disable-gpu")
        service = Service(executable_path="chromedriver.exe")
        self.driver = webdriver.Chrome(service=service, options=options)


    def scroller(self):
        start = time.time()
        initialScroll = 0
        finalScroll = 1000

        while True:
            self.driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
            initialScroll = finalScroll
            finalScroll += 1000

            time.sleep(5)

            end = time.time()

            if round(end - start) > 20:
                break

    def logging(self):

        self.driver.get("https://www.linkedin.com/login")
        time.sleep(5)
        self.driver.refresh()
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "username")))

            username = self.driver.find_element(By.CSS_SELECTOR, "username")
            password = self.driver.find_element(By.CSS_SELECTOR, "password")

            username.send_keys(self._user)
            time.sleep(5)
            password.send_keys(self._pas)
            time.sleep(5)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
            time.sleep(5)

            strr = ""

            with open("layout\\user_data\\search.txt", "r") as f:
                strr = f.readline()
                                                                                                                    #INJA#
            search_url = f"https://www.linkedin.com/jobs/search/?currentJobId=4240781587&geoId=92000000&keywords={strr}&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true"

            self.driver.get(search_url)
            self.scroller()
        except Exception as e:
            print(f"An error occurred during logging: {e}")

    def adder(self, var, lst):
        for i in var:
            lst.append(i.text.strip())

    def extractor(self):
        src = self.driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        job_opp = soup.find_all('div', {'class':'full-width artdeco-entity-lockup__title ember-view'})
        self.adder(job_opp, self.job_titles)
        job_comp = soup.find_all('div', {'class':'artdeco-entity-lockup__subtitle ember-view'})
        self.adder(job_comp, self.job_company)
        job_loc = soup.find_all('div', {'class':'artdeco-entity-lockup__caption ember-view'})
        self.adder(job_loc, self.job_loc)


    def main(self):
        self.logging()
        self.extractor()

if __name__ == "__main__":
    a = JobSearcher()
    a.main()
    print(a.job_titles)
