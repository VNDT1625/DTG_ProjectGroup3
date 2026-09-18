"""
Huấn luyện Mô hình Phân loại (Model Trainer Module).
Phụ trách: Văn Đức Cường
"""
import joblib
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

def train_and_export_pipeline(preprocessor, selector, X_train, y_train, output_path: str):
    """Huấn luyện và đóng gói pipeline thành file .joblib duy nhất."""
    model = XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        eval_metric="logloss"
    )
    
    full_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("selector", selector),
        ("classifier", model)
    ])
    
    full_pipeline.fit(X_train, y_train)
    joblib.dump(full_pipeline, output_path)
    print(f"Đã xuất pipeline thành công: {output_path}")
    return full_pipeline
