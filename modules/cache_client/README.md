# Cache Client

`cache_client`는 Redis를 기반으로 하는 비동기 캐싱 클라이언트입니다. Redis와의 연결을 관리하며, 일반적인 캐싱 작업을 위한 인터페이스를 제공합니다.

---

## 🚀 Features

- **비동기 캐싱**:
  - `CacheManager`: 기본 캐싱 인터페이스를 정의.
  - `RedisCacheManager`: Redis와 통합된 비동기 캐싱 구현체.

- **Redis 연결 관리**:
  - `RedisClient`: Redis 연결을 관리하는 객체.

- **구성 관리**:
  - `RedisConfig`: `.env` 파일을 사용하여 Redis 설정을 로드.

- **주요 기능**:
  - 데이터 조회 (`get`)
  - 데이터 저장 및 만료 시간 설정 (`set`)
  - 키 존재 여부 확인 (`exists`)
  - 키 삭제 (`delete`)
  - 값 증가 (`increment`)
  - 만료 시간 설정 (`set_expire`)
  - 키 패턴 검색 (`scan`)

---

