import asyncio

from dataweave.api_client.google_search_api_client import google_search_api_client
from dataweave.api_client.product_hub_api_client import product_hub_api_client

if __name__ == "__main__":
    asyncio.run(product_hub_api_client.fetch_sites(site_type="CRAWL", cursor_id=None, page_size=20))

