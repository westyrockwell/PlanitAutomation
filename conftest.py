from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

class DriverWrap:
    # driver = None
    # mandatoryFields = None    
    def __init__(self):
        #options = webdriver.ChromeOptions()
        options = Options()
        #ua = UserAgent()
        #userAgent = ua.random
        #print(userAgent)
        #options.add_argument(f'user-agent={userAgent}')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=options)        
        #self.driver = webdriver.Chrome(options=options, executable_path=r'C:\SeleniumDrivers\chromedriver.exe')
        
        self.mandatoryFields = []
        #self.driver.get("https://www.google.co.in")
        #self.driver.quit()

        