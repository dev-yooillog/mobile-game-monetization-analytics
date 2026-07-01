"""
퍼널 분석 (Install -> Active -> Engaged -> Purchase)

퍼널 단계별 유저 수 집계
Install: 전체 유저
Active: SessionCount >= 1
Engaged: AverageSessionLength >= threshold
Purchase: HasPurchased == 1
"""
import pandas as pd

def build_funnel(df, engaged_threshold_minutes=20):
    install = len(df)
    active = (df["SessionCount"] >= 1).sum()
    engaged = (df["AverageSessionLength"] >= engaged_threshold_minutes).sum()
    purchase = df["HasPurchased"].sum()

    funnel = pd.DataFrame(
        {
            "stage": ["Install", "Active", "Engaged", "Purchase"],
            "users": [install, active, engaged, purchase],
        }
    )
    funnel["pct_of_install"] = (funnel["users"] / install * 100).round(1)
    funnel["step_conversion"] = (
        funnel["users"] / funnel["users"].shift(1) * 100
    ).round(1)
    return funnel

# 세그먼트별 결제 전환율 및 ARPU
def conversion_by_segment(df, segment_col="GameGenre"):
    grp = df.groupby(segment_col).agg(
        total=("UserID", "count"),
        purchasers=("HasPurchased", "sum"),
        revenue=("InAppPurchaseAmount", "sum"),
    )
    grp["cvr_pct"] = (grp["purchasers"] / grp["total"] * 100).round(1)
    grp["arpu"] = (grp["revenue"] / grp["total"]).round(1)
    return grp.sort_values("cvr_pct", ascending=False)

# 첫 결제까지 걸린 일수 분포
def first_purchase_distribution(df):
    fp = df["FirstPurchaseDaysAfterInstall"].dropna()
    cuts = pd.cut(
        fp,
        bins=[-0.1, 0, 3, 7, 14, 30],
        labels=["당일", "1-3일", "4-7일", "8-14일", "15-30일"],
    )
    dist = cuts.value_counts().sort_index()
    summary = {
        "mean_days": round(fp.mean(), 1),
        "median_days": round(fp.median(), 1),
        "distribution": dist,
    }
    return summary


if __name__ == "__main__":
    from preprocessing import run_preprocessing_pipeline

    df = run_preprocessing_pipeline()
    print(build_funnel(df))
    print(conversion_by_segment(df))
    print(first_purchase_distribution(df))