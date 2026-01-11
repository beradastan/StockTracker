import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import PAGE_LOAD_TIMEOUT, HUMAN_WAIT

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager




def check_stock_zara(driver, url, target_variants):
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

    # 🛒 Ekle butonu
    try:
        add_btn = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[data-qa-action='add-to-cart']")
            )
        )
        driver.execute_script("arguments[0].click();", add_btn)
        print("Ekle butonuna tıklandı")
    except TimeoutException:
        print("Ekle butonu yok → STOK YOK")
        return False

    # 📦 Varyant / seçenek listesi
    try:
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-qa-qualifier='size-selector-sizes-size-label']")
            )
        )
    except TimeoutException:
        # Varyant yoksa (tek ürün) → stokta
        print("Varyant yok ama ekle açıldı → STOKTA")
        return True

    option_labels = driver.find_elements(
        By.CSS_SELECTOR,
        "[data-qa-qualifier='size-selector-sizes-size-label']"
    )

    for label in option_labels:
        text = label.text.strip().upper()

        for variant in target_variants:
            if variant.upper() in text:
                parent = label.find_element(By.XPATH, "./ancestor::li")
                button = parent.find_element(By.TAG_NAME, "button")

                data_action = button.get_attribute("data-qa-action") or ""
                if "in-stock" in data_action or "low-on-stock" in data_action:
                    print(f"✅ ZARA VARYANT STOKTA → {text}")
                    return True
                else:
                    print(f"❌ ZARA VARYANT YOK → {text}")

    print("İstenen ZARA varyantları stokta değil")
    return False

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def create_driver():
    options = Options()

    # 🔥 KRİTİK: yeni headless (eskisi değil)
    options.add_argument("--headless=new")

    # 🛡️ Anti-bot kaçınma
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # 🖥️ Gerçek ekran gibi davran
    options.add_argument("--window-size=1920,1080")

    # 🧠 User-Agent spoof
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # navigator.webdriver = false
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => undefined
                })
            """
        }
    )

    return driver

