import csv

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def click(element: WebElement, driver: WebDriver):
    action = ActionChains(driver)
    action.move_to_element(element).perform()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(element))
    element.click()


def main():
    driver = webdriver.Chrome()

    driver.get("https://www.schulen-online.at/sol/oeff_suche_schulen.jsf")

    driver.find_element(By.ID, "myform1:schulart").click()
    dropdown = driver.find_element(By.ID, "myform1:schulart")
    dropdown.find_element(
        By.XPATH, "//option[. = 'Allgemein bildende höhere Schule']"
    ).click()

    driver.find_element(
        By.CSS_SELECTOR, "#myform1\\3Aschulart > option:nth-child(8)"
    ).click()
    driver.find_element(By.ID, "myform1:anz").click()
    dropdown = driver.find_element(By.ID, "myform1:anz")
    dropdown.find_element(By.XPATH, "//option[. = '50']").click()

    driver.find_element(
        By.CSS_SELECTOR, "#myform1\\3A anz > option:nth-child(3)"
    ).click()
    driver.find_element(By.ID, "myform1:j_id_1x").click()
    prev_skz_top_id = None

    with open("schulen.csv", "w", newline="") as csvfile:
        fieldnames = ["name", "email"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        while True:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ergebnisTable"))
            )

            skzs = driver.find_elements(By.XPATH, "//div[@class='skz']")
            skz_top_id = skzs[0].find_element(By.XPATH, "a").text

            if skz_top_id == prev_skz_top_id:
                break

            for i_skz in range(len(skzs)):
                # for i_skz in [len(skzs) - 1]:
                skz = driver.find_elements(By.XPATH, "//div[@class='skz']")[i_skz]
                link = skz.find_element(By.XPATH, "a")
                click(link, driver)

                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "anzeigefeld_rechts")
                    )
                )

                emails = driver.find_elements(
                    By.XPATH,
                    "//h5[contains(., 'E-Mail Pädagogik')]/"
                    "following-sibling::div/"
                    "a[contains(@href, 'mailto')]",
                )

                if emails:
                    email = emails[0]
                else:
                    email = driver.find_element(
                        By.XPATH, "//div/a[contains(@href, 'mailto')]"
                    )

                title = driver.find_element(
                    By.XPATH, "//h5[contains(., 'Titel')]/following-sibling::div"
                )

                school = {"name": title.text, "email": email.text}
                writer.writerow(school)
                print(school)

                driver.find_element(By.LINK_TEXT, "Ergebnis").click()

                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ergebnisTable"))
                )

            prev_skz_top_id = skz_top_id
            driver.find_element(By.ID, "j_id_20:next").click()

    driver.quit()


if __name__ == "__main__":
    main()
