# Spring Core Server Client Package

이 패키지는 Spring Core Server와의 통신을 위한 비동기 HTTP 클라이언트와 API 응답 처리 기능을 제공합니다. 이 패키지는 HTTP 요청과 응답을 처리하는 공통 로직을 캡슐화하여, 안정적이고 재사용 가능한 구조를 제공합니다.

---

## 📦 Package Features

### **주요 기능**
1. **Spring Core Server 전용 HTTP 클라이언트**:
   - `SpringCoreAsyncHttpClient`는 Spring Core Server의 API 응답 형식(`ApiResponse`)을 자동으로 처리하는 클라이언트입니다.
   - HTTP 요청 후 JSON 응답을 파싱하여 데이터(`data`)를 직접 반환합니다.

2. **API 응답 핸들링**:
   - `ApiResponseHandler`를 통해 성공적인 응답(`data`)과 오류 응답(`status`, `message`)을 분리하여 관리합니다.

3. **HTTP 요청 관리**:
   - `SpringCoreServerClient`는 HTTP 요청의 공통 로직을 캡슐화하여, 엔드포인트와 헤더, 파라미터를 기반으로 통신을 처리합니다.

4. **DTO 및 Enum 정의**:
   - 요청 및 응답 데이터를 구조화하기 위한 DTO와 Enum 클래스(`PullRequestFilterDto`, `GitType`, `ChangeType` 등)를 제공합니다.

5. **유틸리티 클래스**:
   - `SpringUtils`는 Python 객체를 JSON으로 직렬화하거나, JSON 키를 `camelCase` 형식으로 변환하는 기능을 제공합니다.

---

## 📂 Package Structure

패키지 구조는 스프링 도메인 별로 spring_core_server/ 하위에 도메인 명으로 생성 예정

```plaintext
spring_core_server/
├── git/
│   ├── models/
│   │   ├── request/
│   │   │   └── pull_request_filter.py
│   │   ├── response/
│   │   │   ├── pull_request_changed_file_response_dto.py
│   │   │   ├── pull_request_summary_dto.py
│   │   │   └── git_enums.py
│   │   └── git_fetcher.py
├── models/
│   ├── response_payload.py
│   ├── slice.py
│   ├── spring_enums.py
│   └── api_response_handler.py
├── spring_core_async_http_client.py
├── spring_core_server_client.py
├── spring_core_server_config.py
├── spring_utils.py
├── README.md
└── pyproject.toml
```

---

## 🚀 Getting Started

### **Installation**
1. 패키지를 로컬에 클론합니다.
2. `pyproject.toml`을 통해 설치:
```bash
pip install -r requirements.txt
```

**Dependencies**

pyproject.toml에서 다음 의존성을 관리합니다:
```toml
[project]
name = "spring_core_server"
version = "1.0.0"
description = "A Python client for interacting with Spring Core Server."
dependencies = [
    "aiohttp>=3.8.0",
    "injector>=0.20.1",
    "pydantic>=1.10.2"
]
requires-python = ">=3.7"

```


## 📘 Key Components
1. **SpringCoreAsyncHttpClient**
Spring Core Server의 API 응답 형식을 자동으로 처리하는 HTTP 클라이언트:

```python
response_text = await super().request(method, url, headers=headers, **kwargs)
response_json = json.loads(response_text)
api_response = ApiResponse.from_dict(response_json)
return api_response.data
```

2. **SpringCoreServerClient**
HTTP 요청 공통 로직을 캡슐화한 클래스:

```python
async def _make_request(self, method: str, endpoint: str, headers: Optional[Dict[str, str]], params: Optional[Dict[str, Any]]) -> Any:
    url = f"{self._base_url}{endpoint}"
    combined_headers = {**self._header, **(headers or {})}
    return await self._http_client.request(method, url, headers=combined_headers, params=params)

```
2. **DTO와 Enumt**

**PullRequestFilterDto**: Spring Core Server의 필터 요청을 정의.
**PullRequestSummaryResponseDto**, **PullRequestChangedFileResponseDto**: API 응답 데이터를 구조화.


3. **Utilities**
- **SpringUtils**
  - JSON 키 변환(snake_case ↔ camelCase).  Python 객체 직렬화.