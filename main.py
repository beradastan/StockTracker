import time

from zara_checker import create_driver, check_stock_zara
from stradivarius_checker import check_stock_stradivarius
from bershka_checker import check_stock_bershka
from notifier import send_mail
from config import ZARA_PRODUCTS, STRADIVARIUS_PRODUCTS , BERSHKA_PRODUCTS


CHECK_INTERVAL = 60 * 60  # 1 saat




if __name__ == "__main__":
    print("🕒 Çoklu ürün + ürün bazlı beden/varyant stok takibi başladı")

    while True:




        # 🔹 ZARA
        for product in ZARA_PRODUCTS:
            url = product["url"]
            sizes = product["sizes"]

            print(f"\n🔍 ZARA kontrol ediliyor:\n{url}")
            driver = create_driver()

            try:
                if check_stock_zara(driver, url, sizes):
                    print(f"🚨 ZARA STOKTA! (Varyant: {sizes})")
                    send_mail(url)
                else:
                    print(f"❌ ZARA varyant stokta değil: {sizes}")
            finally:
                driver.quit()
                time.sleep(5)

        # 🔹 STRADIVARIUS
        for product in STRADIVARIUS_PRODUCTS:
            url = product["url"]
            sizes = product["sizes"]

            print(f"\n🔍 STRADIVARIUS kontrol ediliyor:\n{url}")
            driver = create_driver()

            try:
                if check_stock_stradivarius(driver, url, sizes):
                    print(f"🚨 STRADIVARIUS STOKTA! (Beden: {', '.join(sizes)})")
                    send_mail(url)
                else:
                    print(f"❌ İstenen bedenler stokta değil: {sizes}")
            finally:
                driver.quit()
                time.sleep(5)


        # 🔹 BERSHKA
        for product in BERSHKA_PRODUCTS:
            url = product["url"]
            sizes = product["sizes"]

            print(f"\n🔍 BERSHKA kontrol ediliyor:\n{url}")
            driver = create_driver()

            try:
                if check_stock_bershka(driver, url, sizes):
                    print(f"🚨 BERSHKA STOKTA! (Beden: {', '.join(sizes)})")
                    send_mail(url)
                else:
                    print(f"❌ BERSHKA istenen bedenler stokta değil: {sizes}")
            finally:
                driver.quit()
                time.sleep(5)






        print("\n⏳ Tüm ürünler kontrol edildi. 1 saat bekleniyor...\n")
        time.sleep(CHECK_INTERVAL)
