"""
코호트 분석 - Day 1/7/30 리텐션 및 결제 전환 추적

주의: 현재 데이터셋에는 일자별 로그인 로그가 없음,
FirstPurchaseDaysAfterInstall을 기준으로 한 근사 코호트 분석을 수행.
실제 리텐션 분석을 위해서는 일별 활동 로그(install_date, activity_date)가 필요
"""

import pandas as pd
import numpy as np

def approximate_retention_proxy(df, retention_days=[1, 7, 30]):
    total_users = len(df)
    results = {}
    for d in retention_days:
        retained = (
            (df["FirstPurchaseDaysAfterInstall"].notna())
            & (df["FirstPurchaseDaysAfterInstall"] <= d)
        ).sum()
        results[f"day_{d}_purchase_retention_proxy_pct"] = round(
            retained / total_users * 100, 2
        )
    return pd.Series(results)


def cohort_by_install_period(df, date_col=None):
    if date_col is None or date_col not in df.columns:
        print(
            "[WARN] 설치일자 컬럼이 없어 코호트(가입 월/주차별) 분석을 수행할 수 없음 "
            "데이터 수집 시 install_date 컬럼 추가를 권장."
        )
        return None

    df = df.copy()
    df["install_period"] = pd.to_datetime(df[date_col]).dt.to_period("M")
    cohort = df.groupby("install_period").agg(
        users=("UserID", "count"),
        purchasers=("HasPurchased", "sum"),
        revenue=("InAppPurchaseAmount", "sum"),
    )
    cohort["cvr_pct"] = (cohort["purchasers"] / cohort["users"] * 100).round(1)
    return cohort

# 세그먼트(Whale/Dolphin/Minnow)별 결제까지 걸린 기간 비교
def segment_retention_comparison(df, segment_col="SpendingSegment"):
    grp = df.groupby(segment_col)["FirstPurchaseDaysAfterInstall"].agg(
        ["mean", "median", "count"]
    )
    return grp.round(1)


if __name__ == "__main__":
    from preprocessing import run_preprocessing_pipeline

    df = run_preprocessing_pipeline()
    print(approximate_retention_proxy(df))
    print(segment_retention_comparison(df))