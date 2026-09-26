# statement-downloader

A small Python script that downloads every statement PDF from an online account's history pop-up, page by page, and saves them with sortable names.

Built for one specific site, so the page selectors will need changing for others (see **Adapting it** below).

## How it works

Instead of logging in itself, the script attaches to a browser you already have open and signed in. It then:

1. Finds every link in the account history pop-up that looks like a date (e.g. `08/31/24`)
2. Clicks each one and catches the download, even if it opens in a new tab
3. Saves it as `statement_2024-08-31.pdf` so files sort by date
4. Clicks **Previous** to load older statements, and stops when there are none left

No passwords or account details are stored in the code.

## Requirements

- Python 3.9+
- Playwright

```
pip install playwright
```

- A Chromium-based browser (Brave, Chrome, Edge)

## Usage

**1. Start your browser with remote debugging turned on.** Close it fully first, then run (Windows, Brave):

```
& "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" --remote-debugging-port=9222 --user-data-dir="C:\temp\brave-debug"
```

This opens a separate browser profile, so you'll need to sign in there.

**2. Sign in and open the statements / account history pop-up.**

**3. Run the script:**

```
python pull_files.py
```

Statements are saved to a `downloads/` folder next to the script.

## Adapting it to another site

These parts of `pull_files.py` are specific to the original site:

| What | Where in the code |
|---|---|
| Pop-up container | `#accountHistoryModal` |
| Date format of the links | `DATE` regex (`MM/DD/YY`) |
| Button for older statements | `"Previous"` |
| Loading spinner to wait on | `#loadingModal` |

`peek.py` helps you find the right values: with your browser open on the page, run it to print every link and button inside the pop-up.

## Privacy

Downloaded statements go in `downloads/`, which is listed in `.gitignore`. Never commit them.

## Disclaimer

For downloading your own records only. Some sites' terms of service restrict automated access, so check before using it elsewhere.
