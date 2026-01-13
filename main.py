import json
import os
import time

from zara_checker import create_driver, check_stock_zara
from stradivarius_checker import check_stock_stradivarius
from bershka_checker import check_stock_bershka
from notifier import send_mail
from products_loader import load_products



if __name__ == "__main__":
    print("Stock check started (GitHub Actions run)")

    products = load_products()
    ZARA_PRODUCTS = products.get("zara", [])
    STRADIVARIUS_PRODUCTS = products.get("stradivarius", [])
    BERSHKA_PRODUCTS = products.get("bershka", [])


    # 🔹 ZARA
    for product in ZARA_PRODUCTS:
        url = product["url"]
        sizes = product["sizes"]

        print(f"\n Checking ZARA :\n{url}")
        driver = create_driver()

        try:
            if check_stock_zara(driver, url, sizes):
                for size in sizes:
                    print(f"🚨 ZARA in stock (Varyant: {sizes})")
                    send_mail(url)
            else:
                print(f"❌ ZARA size not in stock: {sizes}")
        finally:
            driver.quit()
            time.sleep(5)

    # 🔹 STRADIVARIUS
    for product in STRADIVARIUS_PRODUCTS:
        url = product["url"]
        sizes = product["sizes"]

        print(f"\nChecking STRADIVARIUS:\n{url}")
        driver = create_driver()

        try:
            if check_stock_stradivarius(driver, url, sizes):
                for size in sizes:
                    print(f"🚨 STRADIVARIUS in stock (Size: {', '.join(sizes)})")
                    send_mail(url)
            else:
                print(f"❌ STRADIVARIUS requested sizes are not in stock: {sizes}")
        finally:
            driver.quit()
            time.sleep(5)

    # 🔹 BERSHKA
    for product in BERSHKA_PRODUCTS:
        url = product["url"]
        sizes = product["sizes"]

        print(f"\nChecking BERSHKA:\n{url}")
        driver = create_driver()

        try:
            if check_stock_bershka(driver, url, sizes):
                for size in sizes:
                    print(f"🚨 BERSHKA in stock (Size: {', '.join(sizes)})")
                    send_mail(url)
            else:
                print(f"❌ BERSHKA requested sizes are not in stock: {sizes}")
        finally:
            driver.quit()
            time.sleep(5)

    print("\n✅ Stock check completed, workflow finished successfully.")
