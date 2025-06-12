from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

import csv
import time

def opss():
    with open("layout\\user_data\\search.txt", "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        if len(lines) < 2:
            raise ValueError("Saerch file must contain at least two lines: search title and results'number.")
        return lines[0], lines[1]

title_job, results_number = opss()

LINK = f"https://www.linkedin.com/jobs/search/?keywords={title_job}&location=Worldwide"

class JobTracker:
    def __init__(self):
        usr, pas = self.data()
        self._user = usr.strip()
        self._pas = pas.strip()

    def data(self):
        with open("layout\\user_data\\login.txt", "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            if len(lines) < 2:
                raise ValueError("Login file must contain at least two lines: username and password.")
            return lines[0].strip(), lines[1].strip()

class JobSearcher(JobTracker):
    def __init__(self):
        super().__init__()
        # options = Options()
        # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
        # options.add_argument("--disable-gpu")
        # options.add_argument("--ignore-certificate-error")
        # options.add_argument("--allow-insecure-localhost")
        # service = Service(executable_path="chromedriver.exe")
        # options = Options()
        # options.add_argument("--disable-gpu")
        # options.add_argument("--no-sandbox")
        # options.add_argument("--ignore-certificate-error")
        # options.add_argument("--allow-insecure-localhost")
        # options.add_argument("--enable-unsafe-swiftshader")
        # options.add_argument("--headless")
        # options = Options()
        # options.add_argument("--start-maximized")
        # options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome()

#########################################################################

    # def scroller(self):
    #     start = time.time()
    #     initialScroll = 0
    #     finalScroll = 1000

    #     while True:
    #         self.driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
    #         initialScroll = finalScroll
    #         finalScroll += 1000

    #         time.sleep(5)

    #         end = time.time()

    #         if round(end - start) > 20:
    #             break

##########################################################################

    def scroller(self):
        scroll_pause_time = 2
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def logging(self):

        self.driver.get("https://www.linkedin.com/login")
        try:

            # username = WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.ID, "username"))
            # )

            username = self.driver.find_element(By.ID, "username")

            username.send_keys(self._user)

            # password = WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.ID, "password"))
            # )

            password = self.driver.find_element(By.ID, "password")
            password.send_keys(self._pas)
            password.send_keys(Keys.RETURN)

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "global-nav-search"))
            )

            # submit_btn = WebDriverWait(self.driver, 10).until(
            #     EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            # )

            # profile_icon = WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt='Profile']"))
            # )
            # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
            # # WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, "username")))

            # username = self.driver.find_element(By.ID, "username")
            # password = self.driver.find_element(By.ID, "password")

            # username.send_keys(self._user)
            # time.sleep(3)
            # password.send_keys(self._pas)
            # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
            # time.sleep(5)
            #                                                                                                       #INJA#
            # search_url = f"https://www.linkedin.com/jobs/search/?currentJobId=4240781587&geoId=92000000&keywords={self.jbsearch}&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true"

            # self.driver.get(search_url)

            # src = self.driver.page_source
            # soup = BeautifulSoup(src, 'lxml')
            # job_opp = soup.find_all('div', {'class':'full-width artdeco-entity-lockup__title ember-view'})
            # self.adder(job_opp, self.job_titles)
            # job_comp = soup.find_all('div', {'class':'artdeco-entity-lockup__subtitle ember-view'})
            # self.adder(job_comp, self.job_company)
            # job_loc = soup.find_all('div', {'class':'artdeco-entity-lockup__caption ember-view'})
            # self.adder(job_loc, self.job_loc)

        except Exception as e:
            print(f"An error occurred during logging: {e}")
            self.driver.quit()
            return False
        return True

    def scraping(self):

        self.driver.get(LINK)
        time.sleep(5)
        self.scroller()

        job_elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//li[@data-occludable-job-id]"))
        )

        c = 0

        fname = "jobOutput.csv"
        with open(fname, mode='+w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["ID", "Link", "Title", "Company", "Location", "Salary"])

            for job in job_elements:
                try:
                    id_search = job.get_attribute("data-occludable-job-id")
                    title_search = job.find_element(By.XPATH, ".//a[contains(@class, 'job-card-container__link')]").text.strip()
                    loc_search = job.find_element(By.XPATH, ".//div[contains(@class, 'artdeco-entity-lockup__caption')]//li").text.strip()
                    link_search = job.find_element(By.XPATH, ".//div[contains(@class, 'artdeco-entity-lockup__title')]//a").get_attribute("href").text.strip()
                    company_search = job.find_element(By.XPATH, ".//div[contains(@class, 'artdeco-entity-lockup__subtitle')]").text.strip()
                    try:
                        salary = job.find_element(By.XPATH, ".//div[contains(@class, 'artdeco-entity-lockup__metadata')]//li")
                        salary = salary.text.strip()
                    except:
                        salary = "None"

                    writer.writeheader(
                        id_search,
                        f"https://www.linkedin.com/jobs/view/{link_search}/",
                        title_search,
                        company_search,
                        loc_search,
                        salary
                    )

                    if c > results_number: 
                        break
                    c += 1

                except Exception as e:
                    print(f"An error occurred while scraping a job: {e}")

    def main(self):
        if self.logging():
            self.scraping()
        self.driver.quit()

if __name__ == "__main__":
    a = JobSearcher()
    a.main()
