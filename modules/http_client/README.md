# HTTP Client Package

이 패키지는 동기 및 비동기 HTTP 요청을 관리하기 위한 재사용 가능하고 모듈화된 HTTP 클라이언트 구현체를 제공합니다. 세션 관리, 프록시 처리, 커스텀 예외 처리를 지원하여 다양한 HTTP 기반 통합 작업에 적합합니다.

---

## Features

- **동기 및 비동기 HTTP 클라이언트:**:
  - `SyncHttpClient`: 동기 HTTP 요청을 처리하기 위한 클라이언트.
  - `AsyncHttpClient`: aiohttp를 사용한 비동기 HTTP 요청을 처리하기 위한 클라이언트.
  
- **Session Management**:
  - `SyncSessionManager` 및 `AsyncSessionManager` 를 통해 HTTP 세션을 효율적으로 관리.

- **Proxy Management**:
  - `ProxyManager` 인터페이스를 사용한 유연한 프록시 처리..

- **Custom Exceptions**:
  - 자주 발생하는 HTTP 오류 (`UnauthorizedException`, `ForbiddenException`, `TooManyRequestException`, etc.) 에 대한 명확한 예외 정의.

- **Cookie Management**:
  - HTTP 응답에서 쿠키를 가져오고 파싱하기 위한 유틸리티 제공.

---
