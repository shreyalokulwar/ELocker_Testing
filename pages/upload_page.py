from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UploadPage:
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-page='upload']"))
        ).click()

    def fill_form(self, name, category, issuer, date, file_path, description):
        self.driver.find_element(By.ID, "certName").send_keys(name)
        self.driver.find_element(By.ID, "certCategory").send_keys(category)
        self.driver.find_element(By.ID, "certIssuer").send_keys(issuer)
        self.driver.find_element(By.ID, "certDate").send_keys(date)
        self.driver.find_element(By.ID, "certFile").send_keys(file_path)
        self.driver.find_element(By.ID, "certDescription").send_keys(description)

    def submit(self):
        self.driver.find_element(By.XPATH, "//button[text()='Upload Certificate']").click()

    def handle_alert(self):
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        print("✅ Alert:", alert.text)
        alert.accept()
