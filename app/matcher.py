import google.generativeai as genai
from app.schemas import Product
from app.config import GEMINI_API_KEY
from app.utils import log_message

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-pro')

async def filter_matching_products(products, query):
    matched_products = []

    log_message("info", f"Starting Gemini-based product matching for query: '{query}'")

    for product in products:
        prompt = f"Does the product '{product.productName}' exactly match the search query '{query}'? Answer Yes or No."

        try:
            response = model.generate_content(prompt)
            log_message("info", f"Gemini response: {response.text.strip()} for product: {product.productName}")

            if "yes" in response.text.lower():
                matched_products.append(product)
                log_message("info", f"Product matched: {product.productName}")

        except Exception as e:
            log_message("error", f"Error during Gemini API call: {e}")
            continue

    return matched_products
