# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

        self.kepler_url = "https://kepler-beta.itu.edu.tr"  # Kepler URL
        self.courses = ["*****", "*****"]  # Course CRN
        self.password = "*****"  # Student Password
        self.username = "*****"  # Student Username

    def test_app_dynamics_job(self):
        driver = self.driver
        wait = WebDriverWait(driver, 5)
        driver.get(self.kepler_url)
        wait.until(lambda driver: driver.current_url != self.kepler_url)
        driver.find_element(By.ID, "ContentPlaceHolder1_tbUserName").click()
        driver.find_element(By.ID, "ContentPlaceHolder1_tbUserName").clear()
        driver.find_element(By.ID, "ContentPlaceHolder1_tbUserName").send_keys(self.username)
        driver.find_element(By.ID, "ContentPlaceHolder1_tbPassword").clear()
        driver.find_element(By.ID, "ContentPlaceHolder1_tbPassword").send_keys(self.password)
        driver.find_element(By.ID, "ContentPlaceHolder1_btnLogin").click()
        wait.until(EC.visibility_of_element_located((By.LINK_TEXT, u"Ders Kayıt İşlemleri")))
        driver.find_element(By.LINK_TEXT, u"Ders Kayıt İşlemleri").click()
        wait.until(EC.visibility_of_element_located((By.LINK_TEXT, u"Ders Kayıt")))
        driver.find_element(By.LINK_TEXT, u"Ders Kayıt").click()
        for i in range(len(self.courses)):
            driver.find_element(By.XPATH,
                                "//main[@id='page-wrapper']/div[2]/div/div/div[3]/div/form/div/div/div[" + str(
                                    i + 1) + "]/div/input").click()
            driver.find_element(By.XPATH,
                                "//main[@id='page-wrapper']/div[2]/div/div/div[3]/div/form/div/div/div[" + str(
                                    i + 1) + "]/div/input").clear()
            driver.find_element(By.XPATH,
                                "//main[@id='page-wrapper']/div[2]/div/div/div[3]/div/form/div/div/div[" + str(
                                    i + 1) + "]/div/input").send_keys(self.courses[i])

        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        driver.find_element(By.XPATH, "//div[@id='modals-container']/div/div[2]/div/div[3]/button[2]").click()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
