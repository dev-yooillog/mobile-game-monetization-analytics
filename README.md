# Mobile Game In-App Purchase Conversion & Monetization Analytics

## 프로젝트 개요
모바일 게임 유저의 결제 행동을 분석하여 결제 전환 및 매출 구조를 이해하고,
고가치 유저를 조기에 식별하기 위한 데이터 기반 전략을 도출한 프로젝트

## 핵심 질문
"누가, 언제, 왜 결제하는가?" 
(어떤 유저가 고가치 유저가 되며, 이를 사전에 식별할 수 있는가)

## Key Performance Indicators (KPI)
Conversion Rate: 유저 유입부터 최종 구매까지의 전환 효율
ARPU / ARPPU: 유저당 평균 결제액 및 결제 유저당 평균 결제액
Whale Detection Recall: 고가치 유저 식별 모델의 재현율

## 데이터
- 파일: `data/raw/mobile_game_inapp_purchases.csv`
- 주요 컬럼: UserID, Age, Gender, Country, Device, GameGenre, SessionCount,
  AverageSessionLength, InAppPurchaseAmount, SpendingSegment,
  FirstPurchaseDaysAfterInstall, PaymentMethod

## 비즈니스 전략 및 제언 (Action Items)
분석 결과를 바탕으로 다음과 같은 비즈니스 최적화 전략을 제언

* **고가치 유저(Whale) 타겟 마케팅:** - 전체 매출의 59%를 차지하는 상위 2.2% 유저를 위해 'VIP 전용 프리미엄 패키지' 구성 및 맞춤형 푸시 알림 시행 (ARPU 증대 목표).
* **결제 전환 최적화 (Funnel Optimization):** - 이탈이 빈번한 구간을 식별하여 해당 구간에서의 '초보자 지원 패키지' 노출을 통해 결제 전환율 5% 개선 목표.
* **모델 성능 고도화를 위한 데이터 확보:** - 현재 피처만으로는 예측력의 한계가 명확함. 향후 유저별 '게임 내 아이템 클릭 로그', '레벨업 속도', '이벤트 참여 여부' 등 행동 지표를 피처로 추가하여 Whale 조기 식별 정확도 향상 추진.

## 분석 구성
1. **EDA** - 데이터 분포 및 기초 통계
2. **퍼널 분석** - Install → Active → Engaged → Purchase
- Install: 앱 설치 및 유입
- Active: 1회 이상 세션 발생
- Engaged: 세션 시간 20분 이상 또는 세션 수 5회 이상
- Purchase: 인앱 결제 완료
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
