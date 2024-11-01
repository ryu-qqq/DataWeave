import unittest
import json

from dataweave.crawler.parser.api_response_parser import ApiResponseParser


class TestApiResponseParser(unittest.TestCase):
    def setUp(self):
        response_mapping = "{\"brands\": \"$.english.*[*]\"}"
        self.parser = ApiResponseParser(response_mapping)

    def test_parse_response(self):
        response_data = json.dumps({
            "english": {
                "A": [
                    {
                        "brandNo": 2406,
                        "brandNameEng": "A BETTER FEELING",
                        "brandNameKor": "베터 필링",
                        "keyword": []
                    },
                    {
                        "brandNo": 2342,
                        "brandNameEng": "A DICIANNOVEVENTITRE",
                        "brandNameKor": "디시아노베베니트레",
                        "keyword": []
                    },
                    {
                        "brandNo": 1226,
                        "brandNameEng": "A-COLD-WALL",
                        "brandNameKor": "어콜드월",
                        "keyword": [
                            "A-COLD-WALL",
                            "어콜드월"
                        ]
                    }
                ]
            }
        })

        expected_output = {
            "brands": [
                {
                    "brandNo": 2406,
                    "brandNameEng": "A BETTER FEELING",
                    "brandNameKor": "베터 필링"
                },
                {
                    "brandNo": 2342,
                    "brandNameEng": "A DICIANNOVEVENTITRE",
                    "brandNameKor": "디시아노베베니트레"
                },
                {
                    "brandNo": 1226,
                    "brandNameEng": "A-COLD-WALL",
                    "brandNameKor": "어콜드월"
                }
            ]
        }

        parsed_output = self.parser.parse_response(response_data)

        filtered_output = {
            "brands": [
                {key: brand[key] for key in ["brandNo", "brandNameEng", "brandNameKor"]}
                for brand in parsed_output["brands"]
            ]
        }

        self.assertEqual(filtered_output, expected_output)

if __name__ == "__main__":
    unittest.main()
