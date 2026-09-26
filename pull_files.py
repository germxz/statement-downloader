from playwright.sync_api import sync_playwright
from pathlib import Path
import re

# Folder where the files get saved
SAVE_DIR = Path("downloads")
SAVE_DIR.mkdir(exist_ok=True)

# Statement links look like 08/31/24
DATE = re.compile(r"\d{2}/\d{2}/\d{2}")

with sync_playwright() as p:
    # Attach to your open Brave window
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]
    page = context.pages[0]
    modal = page.locator("#accountHistoryModal")

    # Collect any download that starts, on this tab or on a new tab
    downloads = []
    page.on("download", lambda d: downloads.append(d))
    context.on("page", lambda new_tab: new_tab.on("download", lambda d: downloads.append(d)))
    saved = set()
    while True:
        links = modal.locator("a").filter(has_text=DATE)
        for i in range(links.count()):
            link = links.nth(i)
            date = link.text_content().strip()      # e.g. 08/31/24
            if date in saved:
                continue

            before = len(downloads)
            link.click()

            # Wait up to 30 seconds for the download to start
            for _ in range(60):
                if len(downloads) > before:
                    break
                page.wait_for_timeout(500)
            else:
                print("No download for", date)
                continue

            # Name it like statement_2024-08-31.pdf so they sort in order
            name = f"statement_20{date[6:8]}-{date[0:2]}-{date[3:5]}.pdf"
            downloads[-1].save_as(SAVE_DIR / name)
            saved.add(date)
            print("Saved", name)

        # Go to older statements, stop when there aren't any
        prev = modal.locator("button", has_text="Previous")
        if prev.count() == 0 or prev.is_disabled():
            break
        prev.click()
        page.wait_for_timeout(1500)
        page.locator("#loadingModal").wait_for(state="hidden")

        new_dates = [l.text_content().strip() for l in modal.locator("a").filter(has_text=DATE).all()]
        if all(d in saved for d in new_dates):
            break

    print(f"Done. Saved {len(saved)} statements to {SAVE_DIR.resolve()}")