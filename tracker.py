from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time

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
    def __init__(self, jbsearch):
        super().__init__()
        self.jbsearch = jbsearch
        # options = Options()
        # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
        # options.add_argument("--disable-gpu")
        # options.add_argument("--ignore-certificate-error")
        # options.add_argument("--allow-insecure-localhost")
        # service = Service(executable_path="chromedriver.exe")
        self.driver = webdriver.Chrome()  # options=options, service=service


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
        # self.driver.refresh()
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
            # WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, "username")))

            username = self.driver.find_element(By.ID, "username")
            password = self.driver.find_element(By.ID, "password")

            username.send_keys(self._user)
            time.sleep(3)
            password.send_keys(self._pas)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
            time.sleep(5)
                                                                                                                  #INJA#
            search_url = f"https://www.linkedin.com/jobs/search/?currentJobId=4240781587&geoId=92000000&keywords={self.jbsearch}&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true"

            self.driver.get(search_url)

            self.scroller()

            src = self.driver.page_source
            soup = BeautifulSoup(src, 'lxml')
            job_opp = soup.find_all('div', {'class':'full-width artdeco-entity-lockup__title ember-view'})
            self.adder(job_opp, self.job_titles)
            job_comp = soup.find_all('div', {'class':'artdeco-entity-lockup__subtitle ember-view'})
            self.adder(job_comp, self.job_company)
            job_loc = soup.find_all('div', {'class':'artdeco-entity-lockup__caption ember-view'})
            self.adder(job_loc, self.job_loc)

        except Exception as e:
            print(f"An error occurred during logging: {e}")

    def adder(self, var, lst):
        for i in var:
            lst.append(i.text.strip())

    def main(self):
        self.logging()

if __name__ == "__main__":
    a = JobSearcher("C%20programmer")
    a.main()
    print(a.job_titles)
