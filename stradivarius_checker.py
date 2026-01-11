import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import PAGE_LOAD_TIMEOUT, HUMAN_WAIT


def check_stock_stradivarius(driver, url, target_sizes):
    wait = WebDriverWait(driver, PAGE_LOAD_TIMEOUT)
    driver.get(url)

    try:
        wait.until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        ).click()
    except TimeoutException:
        pass

    time.sleep(HUMAN_WAIT)

    try:
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button.size-item")
            )
        )
    except TimeoutException:
        print("Sizes did not load → OUT OF STOCK")
        return False

    size_buttons = driver.find_elements(By.CSS_SELECTOR, "button.size-item")

    for btn in size_buttons:
        class_attr = btn.get_attribute("class") or ""

        try:
            label_el = btn.find_element(By.CSS_SELECTOR, "p.size-name")
            size_text = (label_el.get_attribute("data-text") or label_el.text).strip().upper()
        except Exception:
            continue

        if size_text not in [s.upper() for s in target_sizes]:
            continue

        print(f"🔍 {size_text} found")

        if "size-no-stock" in class_attr:
            print(f"❌ Size {size_text} out of stock (size-no-stock)")
            continue

        # ✅ STOKTA
        print(f"✅ Size {size_text} si in stock")
        return True

    print("None of the requested sizes are in stock")
    return False
