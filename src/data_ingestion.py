"""
Data Ingestion Script for Telco Customer Churn Project.
Downloads official raw dataset directly from verified source and preserves it in data/raw/.
"""
import os
import urllib.request
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

RAW_URL = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "WA_Fn-UseC_-Telco-Customer-Churn.csv")

def download_raw_data(url: str = RAW_URL, dest_path: str = OUTPUT_PATH):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    if os.path.exists(dest_path):
        logging.info(f"Dataset already exists at {dest_path}. Verifying size...")
        size_kb = os.path.getsize(dest_path) / 1024
        logging.info(f"Existing file size: {size_kb:.2f} KB")
        return dest_path
    
    logging.info(f"Downloading raw dataset from {url}...")
    urllib.request.urlretrieve(url, dest_path)
    size_kb = os.path.getsize(dest_path) / 1024
    logging.info(f"Successfully downloaded to {dest_path} ({size_kb:.2f} KB)")
    return dest_path

if __name__ == "__main__":
    download_raw_data()
