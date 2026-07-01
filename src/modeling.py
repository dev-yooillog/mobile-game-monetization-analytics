"""
목적 1: 결제(Whale) 여부 예측 - Logistic Regression, XGBoost
목적 2: LTV(구매액) 예측 - Regression
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    roc_auc_score,
    mean_absolute_error,
    r2_score,
)
from xgboost import XGBClassifier, XGBRegressor

#결제 여부(Whale) 예측
def train_logistic_regression(X_train, y_train):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_train)
    model = LogisticRegression(class_weight="balanced", random_state=42)
    model.fit(X_scaled, y_train)
    return model, scaler


def train_xgb_classifier(X_train, y_train):
    scale = (y_train == 0).sum() / max((y_train == 1).sum(), 1)
    model = XGBClassifier(
        scale_pos_weight=scale,
        max_depth=4,
        n_estimators=200,
        random_state=42,
        eval_metric="logloss",
    )
    model.fit(X_train, y_train)
    return model

def evaluate_classifier(model, X_test, y_test, scaler=None, model_name="model"):
    if scaler is not None:
        X_test = scaler.transform(X_test)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_prob)

    print(f"\n=== {model_name} 평가 결과 ===")
    print(classification_report(y_test, y_pred, target_names=["Non-Whale", "Whale"]))
    print(f"ROC-AUC: {auc:.3f}")

    if auc < 0.6:
        print(
            "[WARN] AUC가 0.6 미만, 현재 피처셋만으로는 결제 행동을 "
            "안정적으로 설명하지 못함. 피처 추가 또는 데이터 수집 전략 "
            "재검토 필요."
        )
    return {"auc": auc, "y_pred": y_pred, "y_prob": y_prob}

def get_feature_importance(model, feature_names, model_type="logistic"):
    if model_type == "logistic":
        importance = np.abs(model.coef_[0])
    else:
        importance = model.feature_importances_
    return pd.Series(importance, index=feature_names).sort_values(ascending=False)

# LTV(구매액) 예측
def train_ltv_regressor(X_train, y_train):
    model = XGBRegressor(max_depth=4, n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    return model


def evaluate_regressor(model, X_test, y_test, model_name="LTV model"):
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"\n=== {model_name} 평가 결과 ===")
    print(f"MAE: {mae:.2f}")
    print(f"R2: {r2:.3f}")
    print(f"실제 평균 구매액: {y_test.mean():.2f} / 예측 평균: {y_pred.mean():.2f}")

    if r2 < 0:
        print(
            "[WARN] R2가 음수. 현재 모델이 단순 평균값 예측보다도 "
            "성능이 낮음. 피처셋 재검토를 권장."
        )
    return {"mae": mae, "r2": r2, "y_pred": y_pred}

def run_purchase_prediction_pipeline(df, feature_cols, target_col="is_whale", test_size=0.2, random_state=42):
    X = df[feature_cols]
    y = df[target_col]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    lr_model, scaler = train_logistic_regression(X_train, y_train)
    lr_result = evaluate_classifier(lr_model, X_test, y_test, scaler, "Logistic Regression")
    lr_importance = get_feature_importance(lr_model, feature_cols, "logistic")

    xgb_model = train_xgb_classifier(X_train, y_train)
    xgb_result = evaluate_classifier(xgb_model, X_test, y_test, None, "XGBoost")
    xgb_importance = get_feature_importance(xgb_model, feature_cols, "xgboost")

    return {
        "logistic": {"model": lr_model, "scaler": scaler, **lr_result, "importance": lr_importance},
        "xgboost": {"model": xgb_model, **xgb_result, "importance": xgb_importance},
    }


def run_ltv_prediction_pipeline(df, feature_cols, target_col="InAppPurchaseAmount", test_size=0.2, random_state=42):
    ltv_df = df.dropna(subset=[target_col])
    X = ltv_df[feature_cols]
    y = ltv_df[target_col]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    model = train_ltv_regressor(X_train, y_train)
    result = evaluate_regressor(model, X_test, y_test, "XGBoost LTV Regressor")
    importance = get_feature_importance(model, feature_cols, "xgboost")

    return {"model": model, **result, "importance": importance}


if __name__ == "__main__":
    from preprocessing import run_preprocessing_pipeline, build_feature_set, load_config

    cfg = load_config()
    df = run_preprocessing_pipeline()
    df_enc, feature_cols, encoders = build_feature_set(
        df, cfg["features"]["numeric"][:1] + ["SessionCount", "AverageSessionLength"],
        cfg["features"]["categorical"],
    )

    purchase_results = run_purchase_prediction_pipeline(df_enc, feature_cols)
    ltv_results = run_ltv_prediction_pipeline(df_enc, feature_cols)