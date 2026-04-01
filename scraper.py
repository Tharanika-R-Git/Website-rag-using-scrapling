from scrapling.fetchers import Fetcher

def scrape_url(url: str) -> str:
    try:
        page = Fetcher.get(url)

        # ✅ Extract text properly
        texts = page.css("body *::text").getall()

        # Clean text
        cleaned = [t.strip() for t in texts if t.strip()]

        return " ".join(cleaned)

    except Exception as e:
        print("SCRAPING ERROR:", e)
        return ""