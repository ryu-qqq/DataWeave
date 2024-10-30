# DataWeave

DataWeave는 웹 크롤링을 통해 다양한 데이터 소스를 수집하고 가공하며, 이를 활용하여 사용자 정의된 데이터 워크플로우를 자동화하는 프로젝트입니다. 이 프로젝트는 Airflow와 Python 기반의 크롤링 모듈을 사용하여 데이터 파이프라인을 손쉽게 관리하고 확장 가능한 아키텍처를 제공합니다.

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
python3 -m venv dataweave-env
source dataweave-env/bin/activate
```

### 2. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```
### 3. Airflow 설정

Airflow 초기화 및 웹서버/스케줄러를 설정합니다. 필요한 경우 .env 파일에서 환경 변수를 설정합니다.

```bash
airflow db init
airflow webserver --port 8080 &
airflow scheduler &
```

### 4. 크롤링 모듈 설정

dataweave 폴더에서 크롤링 모듈을 설정하고 데이터 수집 로직을 구현합니다.

### 프로젝트 구조

```
DataWeave/
├── dataweave-env/        # Python 가상환경 폴더
├── dataweave/            # 크롤링 및 데이터 처리 모듈
├── dags/                 # Airflow DAG 폴더
├── requirements.txt      # Python 패키지 목록
├── README.md             # 프로젝트 설명
└── .env                  # 환경 변수 설정 파일 (예정)
```


### 사용법
크롤링 작업 실행
Airflow의 DAG를 통해 주기적으로 크롤링 작업을 실행합니다.
LLM 통합 (예정)
추후 통합 예정인 LLM을 통해 데이터 기반의 자연어 응답을 받을 수 있습니다.




### 기여 방법
프로젝트에 기여하고 싶으신 분들은 이슈나 PR을 열어 자유롭게 의견을 나누고 새로운 기능을 추가해주시면 감사하겠습니다.