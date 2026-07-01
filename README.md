# Mobile Game In-App Purchase Conversion & Monetization Analytics

## 프로젝트 개요
모바일 게임 유저의 결제 행동을 분석하여 결제 전환 및 매출 구조를 이해하고,
고가치 유저를 조기에 식별하기 위한 데이터 기반 전략을 도출한 프로젝트

## 핵심 질문
"누가, 언제, 왜 결제하는가?" 
(어떤 유저가 고가치 유저가 되며, 이를 사전에 식별할 수 있는가)

## 데이터
- 파일: `data/raw/mobile_game_inapp_purchases.csv`
- 주요 컬럼: UserID, Age, Gender, Country, Device, GameGenre, SessionCount,
  AverageSessionLength, InAppPurchaseAmount, SpendingSegment,
  FirstPurchaseDaysAfterInstall, PaymentMethod

## 분석 구성
1. **EDA** - 데이터 분포 및 기초 통계
2. **퍼널 분석** - Install → Active → Engaged → Purchase
3. **코호트 분석**- 첫 결제 소요일 기반 근사 리텐션
4. **모델링** - Whale 예측(Logistic/XGBoost), LTV 예측(XGBoost)

## 핵심 인사이트
- 전체 결제 전환율 약 95% (일반 모바일 게임 대비 매우 높음 → 데이터 특성 고려 필요)
- Whale 유저는 2.2%에 불과하지만 전체 매출의 약 59% 차지 (전형적 파레토 분포)
- 보유 피처(나이/성별/디바이스/장르/세션 데이터)만으로는 Whale 여부 및 LTV를
  안정적으로 예측하기 어려움 (AUC 0.5~0.6 수준) → 추가 행동 데이터 필요

## 한계 및 향후 개선 방향
- 일자별 활동 로그 부재로 실제 D1/D7/D30 리텐션 분석 불가 (근사치로 대체)
- 결제 예측 모델 성능이 낮아, 결제 이벤트 시계열·인앱 경제 데이터 등
  추가 피처 확보가 필요

## 실행 방법
```bash
pip install -r requirements.txt
python src/preprocessing.py
python src/funnel.py
python src/cohort.py
python src/modeling.py
```

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
