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

#### 환경 변수 설정

`.env.local.example` 파일을 참고하여 `.env.local` 파일을 생성하고, 필요한 API 키와 IP 주소를 설정하세요.

```bash
cp .env.local.example .env.local
# .env.local 파일을 열고 필요한 값을 설정합니다
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

dataweave 폴더에서 크롤링 모듈을 설정하고 데이터 수집 로직을 구현합니다. ProductHub 레포지토리의 스프링 서버를 먼저 가동해야 하며, 서버가 동작 중일 때 ProductHub로부터 크롤링 대상 정보를 받아 작업할 수 있습니다.

AWS S3 설정
크롤링한 데이터를 AWS S3에 저장하려면 아래의 설정이 필요합니다:

AWS 커넥션 정보를 Airflow UI에서 설정합니다. AWS에 대한 **접근 키(Access Key)**와 **비밀 키(Secret Key)**를 설정하고, 연결 이름을 aws_default로 지정합니다.
Airflow UI의 변수(Variables) 메뉴에서 bucket_name이라는 변수 이름으로 S3 버킷 이름을 지정해야 합니다.
또한 DAG 실패시 알람을 받기 위해선 Variables 또는 env파일에 slack_webhook_url을 추가해야합니다.


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
#### 1. sync_crawl_config DAG로 설정 파일 동기화
sync_crawl_config DAG를 통해 ProductHub 서버로부터 크롤링 대상과 설정 정보를 수신하여 /usr/src/app/dags/config 디렉토리에 YAML 형식의 설정 파일로 저장합니다. 설정 파일은 각 사이트에 대한 크롤링 정보를 담고 있습니다.

#### 2. dynamic_crawl_dag.py를 통한 DAG 및 태스크 생성
dynamic_crawl_dag.py는 위의 config 파일들을 기반으로 각 사이트의 크롤링을 수행할 DAG를 동적으로 생성합니다.
설정된 AWS 커넥션과 S3 버킷 정보에 따라 크롤링한 데이터를 저장하거나, 필요한 데이터 가공 작업을 수행합니다.

#### 3. 크롤링 작업 관리
Airflow의 UI에서 생성된 DAG를 확인하고, DAG가 정의한 스케줄에 따라 크롤링 작업이 실행됩니다.



### 기여 방법
프로젝트에 기여하고 싶으신 분들은 이슈나 PR을 열어 자유롭게 의견을 나누고 새로운 기능을 추가해주시면 감사하겠습니다.

### 노션 링크
https://www.notion.so/DataWeave-12f72e942a1680f3a2f8d33ee7332eac