import yaml
from modules.crawler.models.site_context_response import SiteContextResponse


class CrawlConfigSaver:
    @staticmethod
    def save_to_yaml(site_context: SiteContextResponse, file_path):
        site_data = {
            "siteId": site_context.site_id,
            "siteName": site_context.site_name,
            "baseUrl": site_context.base_url,
            "countryCode": site_context.country_code,
            "siteType": site_context.site_type,
            "siteProfiles": []
        }

        for profile in site_context.site_profiles:
            profile_data = {
                "mappingId": profile.mapping_id,
                "crawlSetting": {
                    "crawlFrequency": profile.crawl_setting.crawl_frequency,
                    "crawlType": profile.crawl_setting.crawl_type
                },
                "crawlAuthSetting": {
                    "authType": profile.crawl_auth_setting.auth_type,
                    "authEndpoint": profile.crawl_auth_setting.auth_endpoint,
                    "authHeaders": profile.crawl_auth_setting.auth_headers,
                    "authPayload": profile.crawl_auth_setting.auth_payload
                },
                "headers": profile.headers,
                "crawlEndpoints": []
            }

            for endpoint in profile.crawl_endpoints:
                endpoint_data = {
                    "endpointId": endpoint.endpoint_id,
                    "endPointUrl": endpoint.end_point_url,
                    "parameters": endpoint.parameters,
                    "crawlTasks": []
                }

                for task in endpoint.crawl_tasks:
                    task_data = {
                        "endpointId": task.endpoint_id,
                        "stepOrder": task.step_order,
                        "type": task.type,
                        "target": task.target,
                        "action": task.action,
                        "params": task.params,
                        "responseMapping": task.response_mapping
                    }
                    endpoint_data["crawlTasks"].append(task_data)

                profile_data["crawlEndpoints"].append(endpoint_data)

            site_data["siteProfiles"].append(profile_data)

        with open(file_path, 'w') as file:
            yaml.dump(site_data, file)
