"""
Domain-Specific Feature Engineering for Customer Retention Economics.
Constructs leak-free, business-grounded features compatible with scikit-learn.
"""
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class BusinessFeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Custom Transformer that generates strategic business features:
    - total_addons_count: Depth of digital ecosystem adoption [0, 6]
    - support_security_index: High switching-cost shield features [0, 4]
    - streaming_to_support_ratio: Ratio of entertainment to protection
    - historical_avg_monthly_charge: TotalCharges / max(tenure, 1)
    - price_shock_ratio: MonthlyCharges / historical_avg_monthly_charge
    - is_auto_pay: Binary flag for bank transfer / credit card auto-payments
    - unprotected_fiber_flag: Fiber optic without tech support or online security
    """
    def __init__(self):
        self.digital_addons = [
            'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
            'TechSupport', 'StreamingTV', 'StreamingMovies'
        ]
        self.shield_addons = [
            'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport'
        ]
        
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        # Create a clean working copy
        df = X.copy() if isinstance(X, pd.DataFrame) else pd.DataFrame(X)
        
        # 1. Add-on Ecosystem Adoption Counts
        addon_binary = pd.DataFrame(index=df.index)
        for col in self.digital_addons:
            if col in df.columns:
                addon_binary[col] = (df[col] == 'Yes').astype(int)
            else:
                addon_binary[col] = 0
                
        df['total_addons_count'] = addon_binary[self.digital_addons].sum(axis=1)
        df['support_security_index'] = addon_binary[self.shield_addons].sum(axis=1)
        
        # 2. Entertainment vs. Support Ratio
        streaming_count = addon_binary['StreamingTV'] + addon_binary['StreamingMovies']
        support_count = df['support_security_index']
        # Avoid division by zero: add 1 smoothing to denominator
        df['streaming_to_support_ratio'] = streaming_count / (support_count + 1.0)
        
        # 3. Unit Economics & Pricing Disruption
        tenure_safe = np.maximum(df['tenure'].values, 1)
        total_charges_safe = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(df['MonthlyCharges'])
        
        df['historical_avg_monthly_charge'] = total_charges_safe / tenure_safe
        
        # Price shock ratio (> 1.0 means recent price increase or promo roll-off)
        df['price_shock_ratio'] = df['MonthlyCharges'] / np.maximum(df['historical_avg_monthly_charge'], 1.0)
        
        # 4. Payment Friction Indicator
        if 'PaymentMethod' in df.columns:
            df['is_auto_pay'] = df['PaymentMethod'].str.contains('automatic', case=False, na=False).astype(int)
        else:
            df['is_auto_pay'] = 0
            
        # 5. Critical Vulnerability Flag: Unprotected Fiber Optic
        is_fiber = (df['InternetService'] == 'Fiber optic') if 'InternetService' in df.columns else False
        no_support = (df['TechSupport'] != 'Yes') if 'TechSupport' in df.columns else True
        no_security = (df['OnlineSecurity'] != 'Yes') if 'OnlineSecurity' in df.columns else True
        
        df['unprotected_fiber_flag'] = (is_fiber & no_support & no_security).astype(int)
        
        return df

if __name__ == "__main__":
    import os
    sample_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "telco_churn_cleaned.csv")
    if os.path.exists(sample_path):
        df_sample = pd.read_csv(sample_path).head(10)
        fe = BusinessFeatureEngineer()
        transformed = fe.transform(df_sample)
        print("Engineered features preview:")
        print(transformed[['total_addons_count', 'support_security_index', 'price_shock_ratio', 'unprotected_fiber_flag']])
