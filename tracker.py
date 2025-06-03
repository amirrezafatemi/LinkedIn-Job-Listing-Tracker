from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import time

class JobTracker:

    def __init__(self):
        usr, pas = JobTracker.data()
        self._user = usr
        self._pas = pas

    def data():
        with open("layout\\user_data\\login.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                yield line

class JobSearcher(JobTracker):

    def __init__(self):
        super().__init__()
        self.driver = webdriver.Chrome()

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

        time.sleep(4)

        username = self.driver.find_element(By.ID, "username")
        password = self.driver.find_element(By.ID, "password")


        username.send_keys(self.user)
        password.send_keys(self.pas)

        time.sleep(4)

        sign_in_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(4)

        search_url = f"https://www.linkedin.com/jobs/search/?currentJobId=4231607675&f_C=3536&geoId=92000000&origin=COMPANY_PAGE_JOBS_CLUSTER_EXPANSION&originToLandingJobPostings=3756663036%2C4204888095%2C4231607675%2C3983400564%2C4228369169%2C3892351862%2C4189393103%2C4190374191%2C4235056922&trk=d_flagship3_company"

        self.driver.get(search_url)
        JobSearcher.scroller(self)



    def extractor(self):

        src = self.driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        intro = soup.find('div', {'class': 'jobs-search__job-details--container'})
        print(intro)

    def main(self):
        if __name__ == "__main__":
            self.logging()
            self.scroller()
            self.extractor()











a = JobSearcher()
a.main()