"""
End-to-End Pipeline Builder with scikit-learn.
Combines BusinessFeatureEngineer, ColumnTransformer, and Models into unified pipelines.
Prevents any data leakage and exposes get_preprocessor().
"""
import sys
import os
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

# Add project root to sys.path for absolute and relative imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.feature_engineering import BusinessFeatureEngineer
from src.config import CONFIG

def get_preprocessor():
    """
    Constructs the ColumnTransformer for the Telco dataset after feature engineering.
    """
    # 1. Numeric features to standardize
    numeric_features = [
        'tenure', 'MonthlyCharges', 'TotalCharges', 
        'total_addons_count', 'support_security_index',
        'streaming_to_support_ratio', 'historical_avg_monthly_charge', 
        'price_shock_ratio'
    ]
    
    # 2. Ordinal features
    ordinal_features = ['Contract']
    contract_order = [['Month-to-month', 'One year', 'Two year']]
    
    # 3. Categorical / Nominal features to One-Hot Encode
    categorical_features = [
        'gender', 'SeniorCitizen', 'Partner', 'Dependents',
        'PhoneService', 'MultipleLines', 'InternetService',
        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
        'TechSupport', 'StreamingTV', 'StreamingMovies',
        'PaperlessBilling', 'PaymentMethod',
        'is_new_onboarding', 'is_auto_pay', 'unprotected_fiber_flag'
    ]
    
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    ordinal_transformer = Pipeline(steps=[
        ('ordinal', OrdinalEncoder(categories=contract_order, handle_unknown='use_encoded_value', unknown_value=-1))
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(drop='if_binary', handle_unknown='ignore', sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_transformer, numeric_features),
        ('ord', ordinal_transformer, ordinal_features),
        ('cat', categorical_transformer, categorical_features)
    ])
    
    # Wrap with custom domain feature engineer
    full_pipeline = Pipeline(steps=[
        ('feature_engineer', BusinessFeatureEngineer()),
        ('col_transform', preprocessor)
    ])
    
    return full_pipeline

def get_train_test_splits(data_path: str = None):
    """
    Loads certified clean data and performs stratified train/test split.
    Guarantees strict featurization ordering (split BEFORE fitting).
    """
    if data_path is None:
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "telco_churn_cleaned.parquet")
        
    df = pd.read_parquet(data_path)
    
    # Target and features
    y = df['Churn_Binary']
    X = df.drop(columns=['Churn', 'Churn_Binary']) # customerID is preserved for scoring reference if needed
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=CONFIG.TEST_SIZE, 
        stratify=y, 
        random_state=CONFIG.RANDOM_STATE
    )
    
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    X_train, X_test, y_train, y_test = get_train_test_splits()
    print(f"Train set: {X_train.shape[0]} rows (Churn rate: {y_train.mean():.4f})")
    print(f"Test set: {X_test.shape[0]} rows (Churn rate: {y_test.mean():.4f})")
    
    pipe = get_preprocessor()
    X_train_trans = pipe.fit_transform(X_train)
    X_test_trans = pipe.transform(X_test)
    print(f"Transformed train shape: {X_train_trans.shape}")
    print(f"Transformed test shape: {X_test_trans.shape}")
