import unittest

from dataweave.api_client.models.site_profile_reponse import SiteProfileResponse

MOCK_PROFILE_DATA = {
    "crawlSetting": {
        "crawlFrequency": 10,
        "crawlType": "BEAUTIFUL_SOUP"
    },
    "crawlAuthSetting": {
        "authType": "TOKEN",
        "authEndpoint": "www.set-of.net",
        "authHeaders": "Authorization",
        "authPayload": "Bearer "
    },
    "crawlEndpoints": [
        {
            "endPointUrl": "/api/v1/product",
            "crawlTasks": [
                {
                    "endpointId": 1,
                    "stepOrder": 1,
                    "taskType": "API_CALL",
                    "actionTarget": "",
                    "actionType": "EXTRACT",
                    "params": "{}",
                    "responseMapping": "{\"brands\": \"$.english.*[*].{'brandNo': brandNo, 'brandNameEng': brandNameEng, 'brandNameKor': brandNameKor}\"}"
                }
            ]
        }
    ]
}


class TestSiteProfileResponse(unittest.TestCase):
    def test_site_profile_from_dict(self):
        site_profile = SiteProfileResponse.from_dict(MOCK_PROFILE_DATA)

        # crawlSetting 확인
        self.assertEqual(site_profile.crawl_setting.crawl_frequency, 10)
        self.assertEqual(site_profile.crawl_setting.crawl_type, "BEAUTIFUL_SOUP")

        # crawlAuthSetting 확인
        self.assertEqual(site_profile.crawl_auth_setting.auth_type, "TOKEN")
        self.assertEqual(site_profile.crawl_auth_setting.auth_endpoint, "www.set-of.net")
        self.assertEqual(site_profile.crawl_auth_setting.auth_headers, "Authorization")
        self.assertEqual(site_profile.crawl_auth_setting.auth_payload, "Bearer ")

        # crawlEndpoints 확인
        self.assertEqual(len(site_profile.crawl_endpoints), 1)
        self.assertEqual(site_profile.crawl_endpoints[0].end_point_url, "/api/v1/product")

        # crawlTasks 확인
        self.assertEqual(len(site_profile.crawl_endpoints[0].crawl_tasks), 1)
        task = site_profile.crawl_endpoints[0].crawl_tasks[0]
        self.assertEqual(task.endpoint_id, 1)
        self.assertEqual(task.step_order, 1)
        self.assertEqual(task.task_type, "API_CALL")
        self.assertEqual(task.action_target, "")
        self.assertEqual(task.action_type, "EXTRACT")
        self.assertEqual(task.params, "{}")
        self.assertEqual(task.response_mapping,
                         "{\"brands\": \"$.english.*[*].{'brandNo': brandNo, 'brandNameEng': brandNameEng, 'brandNameKor': brandNameKor}\"}")


if __name__ == "__main__":
    unittest.main()
