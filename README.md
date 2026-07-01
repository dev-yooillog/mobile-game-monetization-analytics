# Mobile Game In-App Purchase Conversion & Monetization Analytics

## Executive Summary

Whale 유저가 전체 매출의 59%를 차지하는 구조를 확인하였으며,
유저 행동 기반 퍼널 분석과 세그먼트 분석을 통해
결제 전환 최적화 및 고가치 유저 타겟 전략을 도출한 데이터 분석 프로젝트이다.

---

## 프로젝트 개요

모바일 게임 유저의 결제 행동을 분석하여 결제 전환 및 매출 구조를 이해하고,
고가치 유저를 조기에 식별하기 위한 데이터 기반 전략을 도출하는 것을 목표로 한다.

---

## 핵심 질문

"누가, 언제, 왜 결제하는가?"
→ 어떤 유저가 고가치 유저(Whale)가 되며, 이를 사전에 식별할 수 있는가

---

## Key Performance Indicators (KPI)

* **Conversion Rate** = Purchase User / Total User
* **ARPU (Average Revenue Per User)** = Total Revenue / Total User
* **ARPPU (Average Revenue Per Paying User)** = Total Revenue / Paying User
* **Whale Detection Recall** = 실제 Whale 중 모델이 올바르게 식별한 비율

---

## 데이터

* 파일: `data/raw/mobile_game_inapp_purchases.csv`
* 주요 컬럼:

  * UserID, Age, Gender, Country
  * Device, GameGenre
  * SessionCount, AverageSessionLength
  * InAppPurchaseAmount, SpendingSegment
  * FirstPurchaseDaysAfterInstall, PaymentMethod

---

## 분석 구성

### 1. EDA

* 데이터 분포 및 기초 통계 분석
* 유저 세그먼트별 결제 패턴 확인

### 2. 퍼널 분석 (Funnel Analysis)

Install → Active → Engaged → Purchase

* Install: 앱 설치 및 유입
* Active: 1회 이상 세션 발생
* Engaged: 세션 수 ≥ 5 또는 평균 세션 시간 ≥ 20분
* Purchase: 인앱 결제 완료

(예시)
Install 100% → Active 85% → Engaged 60% → Purchase 95%

---

### 3. 코호트 분석

* 첫 결제까지 소요일 기반 근사 리텐션 분석
* 유저별 결제 전환 타이밍 분석

---

### 4. 모델링

* Whale 예측: Logistic Regression, XGBoost
* LTV 예측: XGBoost

#### 모델링 고려 사항

* Whale 비율 2.2% → **Severe Class Imbalance 문제 존재**
* 정적 피처 중심 → 행동 패턴 반영 한계
* 평가 지표: ROC-AUC, Precision-Recall AUC

---

## 핵심 인사이트

### 1. 매출 집중도

* 전체 유저의 2.2% (Whale)가 매출의 59% 차지
  → 전형적인 파레토 분포 구조

---

### 2. 데이터 편향성 (Bias)

* 전체 결제 전환율 약 95%로 비정상적으로 높음
  → 결제 유저 중심으로 샘플링된 데이터셋일 가능성 존재
  → 실제 Free-to-Play 환경 대비 전환율 과대 추정 가능
  → 실서비스 일반화 시 주의 필요

---

### 3. 모델 성능 한계

* AUC: 0.5 ~ 0.6 수준
* 정적 피처만으로 Whale 예측 어려움
  → 행동 로그 기반 피처 필요

---

## 비즈니스 전략 및 제언 (Action Items)

### 1. Whale 타겟 마케팅

* VIP 전용 프리미엄 패키지 제공
* 맞춤형 푸시 알림
* 목표: ARPU 증가

---

### 2. 결제 전환 최적화

* Funnel 이탈 구간 집중 개선
* 초보자 지원 패키지 노출
* 목표: 전환율 +5%

---

### 3. 데이터 기반 모델 고도화

* 추가 데이터 확보 필요:

  * 아이템 클릭 로그
  * 레벨업 속도
  * 이벤트 참여 여부

---

## 실험 및 검증 계획

* **VIP 패키지 전략**
  → A/B 테스트 (VIP 노출 vs 비노출)
  → KPI: ARPU, Whale 전환율

* **초보자 패키지**
  → Funnel 단계별 전환율 비교
  → KPI: Engaged → Purchase Conversion

* **모델 개선**
  → 기존 vs 행동 데이터 추가 모델 비교
  → KPI: ROC-AUC, Recall@Whale

---

## 한계 및 향후 개선 방향

* 일자별 활동 로그 부재
  → D1/D7/D30 리텐션 분석 불가 (근사치 사용)

* 향후 개선 방향:

  * 유저 행동 로그 기반 리텐션 분석
  * 시계열 결제 데이터 활용
  * 인앱 경제 시스템 데이터 반영

---

## 실행 방법

```bash
pip install -r requirements.txt
python src/preprocessing.py
python src/funnel.py
python src/cohort.py
python src/modeling.py
```

---

## 폴더 구조

```
mobile-game-iap-project/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
├── config/
├── outputs/
└── README.md
```
