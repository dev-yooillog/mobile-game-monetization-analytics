import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import yaml

def load_config(config_path="config/config.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_raw_data(path):
    df = pd.read_csv(path)
    print(f"로드 완료: {df.shape[0]}행 x {df.shape[1]}열")
    return df

# 결제 여부 플래그 생성
def add_purchase_flag(df):
    df = df.copy()
    df["HasPurchased"] = df["InAppPurchaseAmount"].notna().astype(int)
    return df

# Whale 여부 플래그 생성
def add_whale_flag(df):
    df = df.copy()
    df["is_whale"] = (df["SpendingSegment"] == "Whale").astype(int)
    return df

def bin_session_count(df, bins, labels):
    df = df.copy()
    df["session_bin"] = pd.cut(df["SessionCount"], bins=bins, labels=labels)
    return df

def bin_age_group(df):
    df = df.copy()
    df["age_group"] = pd.cut(
        df["Age"],
        bins=[12, 17, 24, 34, 44, 55],
        labels=["13-17", "18-24", "25-34", "35-44", "45-54"],
    )
    return df

def encode_categoricals(df, categorical_cols):
    df = df.copy()
    encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[f"{col}_enc"] = le.fit_transform(df[col].fillna("Unknown"))
        encoders[col] = le
    return df, encoders

def build_feature_set(df, numeric_cols, categorical_cols):
    df_enc, encoders = encode_categoricals(df, categorical_cols)
    feature_cols = numeric_cols + [f"{c}_enc" for c in categorical_cols]
    df_enc[feature_cols] = df_enc[feature_cols].fillna(df_enc[feature_cols].median(numeric_only=True))
    return df_enc, feature_cols, encoders

# 전체 전처리 파이프라인 실행
def run_preprocessing_pipeline(config_path="config/config.yaml"):
    cfg = load_config(config_path)
    df = load_raw_data(cfg["data"]["raw_path"])

    df = add_purchase_flag(df)
    df = add_whale_flag(df)
    df = bin_session_count(
        df,
        cfg["segmentation"]["session_bins"],
        cfg["segmentation"]["session_labels"],
    )
    df = bin_age_group(df)

    df.to_csv(cfg["data"]["processed_path"], index=False)
    print(f"전처리 완료. 경로: {cfg['data']['processed_path']}")
    return df


if __name__ == "__main__":
    run_preprocessing_pipeline()