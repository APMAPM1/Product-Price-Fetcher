from typing import List
from app.schemas import Product
import httpx
from httpx import ReadTimeout
from bs4 import BeautifulSoup
from app.utils import log_message

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

async def scrape_websites(country: str, query: str) -> List[Product]:
    log_message("info", f"Starting scrape for country: {country} and query: {query}")

    if country.strip().lower() in ["in", "india"]:
        return await scrape_amazon_in(query)
    elif country.strip().lower() in ["us", "usa", "united states"]:
        return await scrape_amazon_us(query)
    else:
        log_message("warning", f"No supported websites found for country: {country}")
        return []

async def scrape_amazon_in(query: str) -> List[Product]:
    search_url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"
    log_message("info", f"Scraping Amazon India: {search_url}")
    return await scrape_amazon(search_url, currency="INR")

async def scrape_amazon_us(query: str) -> List[Product]:
    search_url = f"https://www.amazon.com/s?k={query.replace(' ', '+')}"
    log_message("info", f"Scraping Amazon US: {search_url}")
    return await scrape_amazon(search_url, currency="USD")

async def scrape_amazon(search_url: str, currency: str) -> List[Product]:
    products = []
    async with httpx.AsyncClient(timeout=15) as client:
        try:
            response = await client.get(search_url, headers=HEADERS)
            log_message("info", f"Fetched {search_url} with status code {response.status_code}")
        except ReadTimeout:
            log_message("error", f"Timeout while fetching {search_url}")
            return []
        except Exception as e:
            log_message("error", f"Unexpected error while fetching {search_url}: {e}")
            return []

        if response.status_code != 200:
            log_message("error", f"Failed to fetch {search_url}")
            return []

        with open("debug_amazon.html", "w", encoding="utf-8") as f:
            f.write(response.text)
            log_message("info", "Saved Amazon response to debug_amazon.html")

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select('div.s-main-slot div[data-component-type="s-search-result"]')

        log_message("info", f"Found {len(items)} product listings on Amazon page.")

        for item in items[:5]:
            try:
                print("----- RAW ITEM HTML -----")
                print(item.prettify())

                # Title
                title_elem = item.select_one('h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal span')

                # Link
                link_elem = item.select_one('a.a-link-normal.a-text-normal')
                        
                price_whole = item.select_one('span.a-price-whole')
                price_fraction = item.select_one('span.a-price-fraction')

                if not title_elem:
                    log_message("warning", "Missing product title.")
                if not price_whole:
                    log_message("warning", "Missing product price.")
                if not link_elem:
                    log_message("warning", "Missing product link.")

                if title_elem and price_whole and link_elem:
                    product_name = title_elem.text.strip()
                    price = float(price_whole.text.replace(",", "") + "." + (price_fraction.text if price_fraction else "00"))
                    link = "https://www.amazon.in" + link_elem['href'] if "amazon.in" in search_url else "https://www.amazon.com" + link_elem['href']

                    products.append(Product(
                        link=link,
                        price=price,
                        currency=currency,
                        productName=product_name
                    ))

                    log_message("info", f"Scraped product: {product_name} at price {price} {currency}")

            except Exception as e:
                log_message("error", f"Error parsing product: {e}")
                continue

    return products
