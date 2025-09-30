import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def scraper(url):
    # ---------- Selenium Setup ----------
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        time.sleep(3)  # wait for page to load

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Grab all <h2> tags
        titles = [h2.get_text(strip=True) for h2 in soup.find_all("h2")]
        cleaned_titles = list(dict.fromkeys(titles))  # remove duplicates

        # Grab meta description
        meta_desc = None
        meta_tag = soup.find("meta", attrs={"name": "description"})
        if meta_tag and meta_tag.get("content"):
            meta_desc = meta_tag["content"].strip()

        # Grab visible <p> tags (first few paragraphs usually matter most)
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
        cleaned_paragraphs = " ".join(
            paragraphs[:3]) if paragraphs else None  # take first 3 paragraphs

        # Combine description sources
        description = meta_desc if meta_desc else cleaned_paragraphs

        return {
            "Titles": "; ".join(cleaned_titles) if cleaned_titles else None,
            "Description": description
        }

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return {"Titles": None, "Description": None}

    finally:
        driver.quit()


# ---------- Main ----------
df = pd.read_csv("FRurl.csv")

# Apply scraper to each row
results = df["Organization Website"].apply(scraper)

# Convert results (dicts) into separate columns
df["Scraped Titles"] = results.apply(lambda x: x["Titles"])
df["Scraped Description"] = results.apply(lambda x: x["Description"])

# Save back to CSV
df.to_csv("FRurl_with_data2.csv", index=False, encoding="utf-8")

print("✅ Finished scraping titles & descriptions. Data saved to FRurl_with_data.csv")
