import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import PAGE_LOAD_TIMEOUT, HUMAN_WAIT


def check_stock_bershka(driver, url, target_sizes):
    wait = WebDriverWait(driver, PAGE_LOAD_TIMEOUT)
    driver.get(url)

    # 🍪 Cookie kabul
    try:
        wait.until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        ).click()
    except TimeoutException:
        pass

    time.sleep(HUMAN_WAIT)

    # 📏 Beden butonlarını bekle
    try:
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button[data-qa-anchor='sizeListItem']")
            )
        )
    except TimeoutException:
        print("Bershka bedenler yüklenmedi → STOK YOK")
        return False

    size_buttons = driver.find_elements(
        By.CSS_SELECTOR, "button[data-qa-anchor='sizeListItem']"
    )

    for btn in size_buttons:
        # beden adı
        try:
            size_text = btn.find_element(
                By.CSS_SELECTOR, "span.text__label"
            ).text.strip().upper()
        except Exception:
            continue

        if size_text not in [s.upper() for s in target_sizes]:
            continue

        print(f"🔍 {size_text} bedeni bulundu")

        class_attr = btn.get_attribute("class") or ""
        aria_disabled = btn.get_attribute("aria-disabled")
        aria_desc = btn.get_attribute("aria-description")
        disabled_attr = btn.get_attribute("disabled")

        # ❌ STOK YOK (KESİN)
        if (
            aria_disabled == "true"
            or disabled_attr is not None
            or "is-disabled" in class_attr
            or (aria_desc and "tükendi" in aria_desc.lower())
        ):
            print(f"❌ {size_text} bedeni stokta değil")
            continue

        # ✅ STOKTA
        print(f"✅ {size_text} BEDENİ STOKTA")
        return True

    print("İstenen bedenlerin hiçbiri stokta değil")
    return False
