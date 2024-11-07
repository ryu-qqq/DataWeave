# Dynamic Crawl DAG 설명

## 개요

이 프로젝트에서는 Airflow의 `sync_crawl_config`와 `dynamic_crawl_dag.py`를 활용하여 서버로부터 크롤링할 사이트 및 설정 정보를 동적으로 수신하고, 이를 기반으로 DAG와 태스크를 자동 생성합니다. 먼저 `sync_crawl_config` DAG가 서버로부터 설정 정보를 수신하고 config 파일로 저장한 후, `dynamic_crawl_dag.py`가 이 파일을 기반으로 DAG와 태스크를 생성하는 구조입니다.

---

## DAG 생성 흐름

### 1. **초기 설정 파일 저장 (sync_crawl_config DAG)**
   - `sync_crawl_config` DAG는 정해진 스케줄에 따라 ProductHub 서버로부터 크롤링할 사이트 목록과 각 사이트에 대한 세부 프로필을 수신합니다.
   - 이 DAG는 `fetch_and_save_config`라는 PythonOperator를 통해 서버로부터 응답을 받아 설정 파일로 저장합니다.
   - 각 사이트마다 config 파일이 생성되며, 파일 형식은 YAML로 `/usr/src/app/dags/config` 디렉토리에 저장됩니다.

   - 예시 설정 파일(`crawl_config_site_1.yaml`):
     ```yaml
     baseUrl: https://m.web.mustit.co.kr
     countryCode: KR
     siteId: 1
     siteName: MUSTIT
     siteProfiles:
       - mappingId: 1
         crawlSetting:
           crawlFrequency: 10
           crawlType: API
         crawlAuthSetting:
           authType: COOKIE
           authEndpoint: https://m.web.mustit.co.kr
           authHeaders: Authorization
           authPayload: "\"${token_type} ${token}\""
         crawlEndpoints:
           - endpointId: 75
             endPointUrl: /mustit-api/facade-api/v1/search/mini-shop-search
             parameters: sellerId=bino2345&pageNo={}&pageSize={}&order=LATEST
             crawlTasks:
               - stepOrder: 1
                 type: CRAWLING
                 target: RAW_DATA
                 action: SAVE_S3
                 params: "{}"
                 responseMapping: '{"items": "$.items[*]"}'
     ```

### 2. **크롤링 DAG 생성 (dynamic_crawl_dag.py)**
   - `dynamic_crawl_dag.py` 파일은 Airflow가 시작될 때 또는 재시작될 때 `config` 디렉토리 내의 YAML 파일들을 탐색하여 각 사이트에 대한 크롤링 DAG를 동적으로 생성합니다.
   - 각 사이트 프로필마다 별도의 DAG가 생성되며, DAG ID는 `crawl_site_{site_name}_{mapping_id}` 형식으로 지정됩니다.
   - 생성된 DAG에는 사이트별 엔드포인트와 크롤링 태스크 정보가 포함됩니다.

### 3. **태스크 구성**
   - `crawlEndpoints` 배열의 각 엔드포인트마다 여러 `crawlTasks`가 정의되며, `dynamic_crawl_dag.py`는 이 정보를 기반으로 DAG 내의 태스크를 구성합니다.
   - 예를 들어, `CRAWLING` 타입의 태스크는 크롤링 작업을 수행하고, `SAVE_S3` 액션을 통해 S3에 저장할 수 있습니다.
   - 각 태스크는 `parameters`와 `responseMapping` 설정을 통해 원하는 데이터를 정확히 가져올 수 있도록 세부 조정이 가능합니다.

---

## 코드 설명

- `sync_crawl_config.py`의 주요 기능:
  - 서버로부터 사이트와 프로필 정보를 수신합니다.
  - 수신한 정보를 YAML 형식의 config 파일로 `/usr/src/app/dags/config`에 저장합니다.

- `dynamic_crawl_dag.py`의 주요 기능:
  - Airflow 시작 시 config 디렉토리에서 YAML 파일을 읽어 각 사이트의 크롤링 DAG를 동적으로 생성합니다.
  - `crawlEndpoints`와 `crawlTasks` 배열을 기반으로 DAG 내에 태스크를 정의하고, 크롤링 작업 및 후처리 작업을 수행합니다.

---

## 결론

이 구조를 통해 Airflow는 ProductHub 서버의 정보를 기반으로 유연하게 구성되며, 사이트 정보가 변경될 때마다 별도의 DAG 수정 없이도 시스템이 이를 반영하여 크롤링 작업을 수행할 수 있습니다. `sync_crawl_config` DAG가 설정 파일을 동기화하고, `dynamic_crawl_dag.py`가 이 파일을 읽어 동적으로 DAG를 생성하는 프로세스는 데이터 업데이트에 즉각적으로 대응할 수 있도록 합니다.
