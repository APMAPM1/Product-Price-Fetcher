from fastapi import APIRouter
from app.schemas import SearchRequest, SearchResponse
from app.scraper import scrape_websites
from app.matcher import filter_matching_products
from app.utils import log_message

router = APIRouter()

@router.post("/search", response_model=SearchResponse)
async def search_product(request: SearchRequest):
    log_message("info", f"Received request: Country={request.country}, Query='{request.query}'")

    scraped_products = await scrape_websites(request.country, request.query)
    log_message("info", f"Scraped {len(scraped_products)} products from websites.")

    matched_products = await filter_matching_products(scraped_products, request.query)
    log_message("info", f"{len(matched_products)} products matched after Gemini filtering.")

    sorted_products = sorted(matched_products, key=lambda x: x.price)
    log_message("info", f"Returning {len(sorted_products)} products to client.")

    return {"results": sorted_products}
