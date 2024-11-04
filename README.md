# DataWeave

DataWeave는 웹 크롤링을 통해 다양한 데이터 소스를 수집하고 가공하며, 이를 활용하여 사용자 정의된 데이터 워크플로우를 자동화하는 프로젝트입니다. 이 프로젝트는 **ConneXt 프로젝트의 일환**으로, Airflow와 Python 기반의 크롤링 모듈을 사용하여 데이터 파이프라인을 손쉽게 관리하고 확장 가능한 아키텍처를 제공합니다.
> **주의**: 본 프로젝트는 **타인에게 피해를 주지 않도록** 신중하게 개발되었습니다. 모든 크롤링 작업은 천천히 진행되며, 웹사이트에 과부하를 주지 않기 위해 최대한 신중하게 설정되었습니다. **상업적인 용도로 사용하는 것은 지양**해 주시고, 프로젝트는 개인적인 흥미와 학습 목적으로만 활용되길 권장드립니다.

## 주요 기능

- **데이터 수집 및 크롤링**: 설정된 웹 소스에서 주기적으로 데이터를 크롤링하여 최신 정보를 수집합니다.
- **Airflow 기반 파이프라인 관리**: Airflow를 활용하여 데이터 수집, 가공, 저장 작업을 자동화하고 워크플로우를 효율적으로 관리합니다.
- **데이터 가공 및 저장**: 수집한 데이터를 정제하고 구조화하여 데이터 분석 또는 머신러닝 모델 학습에 적합한 형태로 저장합니다.
- **LLM 통합** (예정): 대형 언어 모델(LLM)과 통합하여 수집된 데이터를 기반으로 한 자연어 응답 기능을 제공할 예정입니다.

## 설치 및 설정

### 1. 클론 및 가상환경 설정
```bash
git clone https://github.com/ryu-qqq/DataWeave.git
cd DataWeave
python3 -m venv .venv
source .venv/bin/activate
```

### 2. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```
### 3. Docker Compose 설정

Docker Compose를 사용하여 Airflow, MySQL, Redis 등의 필요한 서비스를 컨테이너로 실행합니다. docker-compose.yml 파일을 실행하여 환경을 설정할 수 있습니다.
```bash
docker-compose up -d
```

이 명령어를 사용하면 Airflow 웹서버가 8080 포트에서 실행되며, MySQL과 Redis가 백엔드로 설정됩니다. Airflow 웹 UI에 접속하려면 브라우저에서 http://localhost:8080을 입력하세요.
참고: Docker가 설치되어 있어야 하며, .env.local 파일에서 필요한 환경 변수를 설정해야 합니다.


### 4. 크롤링 모듈 설정

dataweave 폴더에서 크롤링 모듈을 설정하고 데이터 수집 로직을 구현합니다.

### 프로젝트 구조

```
DataWeave/
├── .venv/                 # Python 가상환경 폴더
├── dataweave/             # 크롤링 및 데이터 처리 모듈
├── dags/                  # Airflow DAG 폴더
├── requirements.txt       # Python 패키지 목록
├── README.md              # 프로젝트 설명
├── docker-compose.yml     # Docker Compose 설정 파일
└── .env.local             # 환경 변수 설정 파일
```


### 사용법
#### 1. 크롤링 작업 실행: Airflow의 DAG를 통해 주기적으로 크롤링 작업을 실행합니다.
#### 2. LLM 통합 (예정): 추후 통합 예정인 LLM을 통해 데이터 기반의 자연어 응답을 받을 수 있습니다.


### 기여 방법
프로젝트에 기여하고 싶으신 분들은 이슈나 PR을 열어 자유롭게 의견을 나누고 새로운 기능을 추가해주시면 감사하겠습니다.

### 노션 링크
https://www.notion.so/DataWeave-12f72e942a1680f3a2f8d33ee7332eac