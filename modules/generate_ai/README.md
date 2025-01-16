# OpenAI Client Package

`openAi`는 OpenAI API와 상호작용하기 위한 Python 패키지로, 배치 작업과 실시간 대화를 지원하는 클라이언트를 제공합니다.

---

## 🚀 Features

- **Batch Operations**:
  - 파일 업로드 및 배치 작업 생성
  - 배치 상태 조회 및 결과 다운로드
  - 최근 배치 작업 목록 조회

- **Real-Time Interactions**:
  - 실시간 AI 대화 생성
  - 다양한 모델(GPT-4 등)과 온도 조정 지원

- **Reviewer & Tester**:
  - 코드를 리뷰하는 리뷰어 와 테스터가 존재.
  - 현재는 Java 리뷰어 와 Junit 5의 단위 테스터만 존재
  - 향후 통합 테스터 및 Python 언어도 지원할 예정

- **Configuration**:
  - `.env` 파일을 통한 API 키 및 환경 설정 관리

---


# Code Review & Test Generate PipeLine

시스템은 **리뷰어(Reviewer)**와 **테스터(Tester)**라는 두 가지 핵심 추상화를 기반으로 하며, 
언어별 기능을 구현하여 확장 가능하고 유지보수 가능한 코드 관리가 가능하도록 합니다.

## 아키텍처

### 추상화

1. **리뷰어(Reviewer)**
   - 코드 리뷰를 수행하기 위한 핵심 추상화입니다.
   - 언어별 리뷰어(Java, Python 등)를 필요에 따라 구현할 수 있습니다.
   - 현재 구현:
     - **JavaReviewer**: 객체지향적 클린코드 원칙에 중점을 두고 Java 코드를 리뷰합니다.

2. **테스터(Tester)**
   - 단위 테스트 생성을 위한 핵심 추상화입니다.
   - 언어별 테스터(Java, Python 등)를 필요에 따라 구현할 수 있습니다.
   - 현재 구현:
     - **JavaTester**: JUnit5를 활용하여 Java 코드에 대한 단위 테스트를 작성합니다.

### 구현 세부사항

- **JavaReviewer**: `review_code` 메서드를 구현하여 Java 코드를 리뷰하고, 클린코드 피드백을 제공합니다.
- **JavaTester**: `write_tests` 메서드를 구현하여 JUnit5를 활용한 Java 단위 테스트를 생성합니다.

### 사용 예시

다음은 파이프라인이 동작하는 간단한 예시입니다:

```python
from abc import ABC, abstractmethod

# 추상 클래스
class Reviewer(ABC):
    @abstractmethod
    def review_code(self, code: str) -> str:
        pass

class Tester(ABC):
    @abstractmethod
    def write_tests(self, code: str) -> str:
        pass

# Java 구현
class JavaReviewer(Reviewer):
    def review_code(self, code: str) -> str:
        return "객체지향적 클린코드 원칙에 따라 Java 코드를 리뷰합니다."

class JavaTester(Tester):
    def write_tests(self, code: str) -> str:
        return "JUnit5를 사용하여 Java 코드의 단위 테스트를 작성합니다."

# 실행 예제
if __name__ == "__main__":
    java_reviewer = JavaReviewer()
    java_tester = JavaTester()

    sample_code = "public class Example { }"

    # 리뷰 및 테스트 수행
    review_feedback = java_reviewer.review_code(sample_code)
    test_feedback = java_tester.write_tests(sample_code)

    print(f"리뷰 피드백: {review_feedback}")
    print(f"테스트 피드백: {test_feedback}")
```

### 출력 예시

```
리뷰 피드백: 객체지향적 클린코드 원칙에 따라 Java 코드를 리뷰합니다.
테스트 피드백: JUnit5를 사용하여 Java 코드의 단위 테스트를 작성합니다.
```

## 확장성

이 시스템은 새로운 언어 지원을 쉽게 확장할 수 있도록 설계되었습니다. 새로운 언어를 추가하려면:
1. 해당 언어에 맞는 `Reviewer` 클래스를 구현합니다.
2. 해당 언어에 맞는 `Tester` 클래스를 구현합니다.
3. 새로운 구현을 파이프라인에 통합합니다.

### 예시: Python 지원 추가
Python 관련 기능을 추가하려면:
- `PythonReviewer` 클래스를 `Reviewer`에서 상속받아 구현합니다.
- `PythonTester` 클래스를 `Tester`에서 상속받아 구현합니다.

```python
class PythonReviewer(Reviewer):
    def review_code(self, code: str) -> str:
        return "PEP 8 준수를 중점으로 Python 코드를 리뷰합니다."

class PythonTester(Tester):
    def write_tests(self, code: str) -> str:
        return "pytest를 사용하여 Python 코드의 단위 테스트를 작성합니다."
```

## 앞으로의 작업

- Python 및 기타 언어에 대한 지원 추가
- Airflow와 통합하여 자동화된 작업 스케줄링 구현
- AI 기반 추천을 포함한 리뷰 및 테스트 생성 로직 향상

## 기여 방법

기여를 환영합니다! 새로운 기능을 추가하거나 기존 기능을 개선하려면, 이 저장소를 포크하고 풀 리퀘스트를 제출해 주세요.

