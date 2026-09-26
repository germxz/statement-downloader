from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Attach to your open Brave window
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    page = browser.contexts[0].pages[0]

    # List every link/button inside the account history pop-up
    links = page.locator("#accountHistoryModal a, #accountHistoryModal button").all()
    for link in links:
        text = (link.text_content() or "").strip()
        print(repr(text), link.get_attribute("href"))