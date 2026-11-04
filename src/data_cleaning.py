"""
Data Cleaning and Accounting Sanity Module for Telco Customer Churn.
Resolves whitespace TotalCharges, standardizes schema types, and outputs certified dataset.
"""
import os
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

RAW_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "WA_Fn-UseC_-Telco-Customer-Churn.csv")
PROCESSED_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "telco_churn_cleaned.parquet")
PROCESSED_CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "telco_churn_cleaned.csv")

def clean_and_certify_data(raw_path: str = RAW_DATA_PATH) -> pd.DataFrame:
    logging.info(f"Loading raw dataset from {raw_path}...")
    df = pd.read_csv(raw_path)
    initial_shape = df.shape
    logging.info(f"Loaded {initial_shape[0]} rows and {initial_shape[1]} columns.")
    
    # 1. Verify primary key uniqueness
    unique_ids = df['customerID'].nunique()
    assert unique_ids == len(df), f"Duplicate customerIDs found! {unique_ids} vs {len(df)}"
    logging.info(f"Primary key check: 100% unique customerIDs ({unique_ids}).")
    
    # 2. Accounting Audit: TotalCharges whitespace anomaly
    # IBM dataset contains ' ' for customers with tenure == 0
    whitespace_mask = df['TotalCharges'].astype(str).str.strip() == ''
    whitespace_count = whitespace_mask.sum()
    logging.info(f"Accounting Audit: Found {whitespace_count} rows with blank 'TotalCharges'.")
    
    if whitespace_count > 0:
        tenure_zero_count = (df.loc[whitespace_mask, 'tenure'] == 0).sum()
        churn_no_count = (df.loc[whitespace_mask, 'Churn'] == 'No').sum()
        logging.info(f"  - Rows with tenure == 0: {tenure_zero_count}/{whitespace_count}")
        logging.info(f"  - Rows with Churn == 'No': {churn_no_count}/{whitespace_count}")
        
        # Financial Accounting Rule:
        # Customers with tenure == 0 are onboarding accounts in their first month.
        # Impute TotalCharges = MonthlyCharges (first month charge committed).
        # Add explicit audit flag 'is_new_onboarding'.
        df['is_new_onboarding'] = 0
        df.loc[whitespace_mask, 'is_new_onboarding'] = 1
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'].replace(r'^\s*$', np.nan, regex=True))
        df.loc[whitespace_mask, 'TotalCharges'] = df.loc[whitespace_mask, 'MonthlyCharges']
    else:
        df['is_new_onboarding'] = (df['tenure'] == 0).astype(int)
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'])
        
    # 3. Standardize Binary and Target Variables
    df['Churn_Binary'] = (df['Churn'] == 'Yes').astype(int)
    
    # 4. Save certified datasets
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    try:
        df.to_parquet(PROCESSED_DATA_PATH, index=False)
        logging.info(f"Saved certified Parquet to {PROCESSED_DATA_PATH}")
    except Exception as e:
        logging.warning(f"Could not save Parquet directly: {e}")
        
    df.to_csv(PROCESSED_CSV_PATH, index=False)
    logging.info(f"Saved certified CSV to {PROCESSED_CSV_PATH}")
    
    return df

if __name__ == "__main__":
    clean_and_certify_data()
