import asyncio

from dataweave.api_client.google_search_api_client import google_search_api_client
from dataweave.api_client.product_hub_api_client import product_hub_api_client

if __name__ == "__main__":
    asyncio.run(google_search_api_client.fetch_search_word_results("아디다스 스포츠 변색 선글라스 미러 투명 라이딩 사이클 야구 SP0041 02U"))
