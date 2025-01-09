from typing import List

from injector import singleton

from dataweave.gpt.models.product_data import ProductData
from dataweave.gpt.models.prompt_models import Prompt
from dataweave.gpt.prompt_generator import PromptGenerator


@singleton
class ProductPromptGenerator(PromptGenerator):

    def get_prompt(self, product: ProductData) -> List[Prompt]:
        system_message = (
            "You are a data processing assistant tasked with analyzing product titles for better categorization."
        )

        user_message = (
            f"Analyze the following product title and return the data in the specified format:\n"
            f"1. Extract the brand name, color, and style code from the title.\n"
            f"2. Remove unrelated words (e.g., seller's name, promotional words like 'instant', 'same day').\n"
            f"3. Provide translations for the title by country code.\n"
            f"4. If the title exceeds 60 characters, shorten it to 60 characters or fewer.\n\n"
            f"Return format:\n"
            f"{{\n"
            f"    \"product_group_id\": <int>,\n"
            f"    \"original_title\": <str>,\n"
            f"    \"filtered_title\": {{\"KR\": <str>, \"US\": <str>}},\n"
            f"    \"brand_name\": <str>,\n"
            f"    \"style_code\": <str>,\n"
            f"    \"color_in_title\": <str>,\n"
            f"    \"deleted_words\": <list>\n"
            f"}}\n\n"
            f"Input data:\n"
            f"Product Group ID: {product.product_group_id}\n"
            f"{product.product_group_name}"
        )

        metadata = {"product_group_id": product.product_group_id}

        return [Prompt(system_message, user_message, metadata)]
