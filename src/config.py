"""
Global Financial and Operational Configuration Parameters for Customer Retention Economics.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class RetentionEconomicsConfig:
    # Portfolio Financial Metrics
    GROSS_MARGIN: float = 0.70               # Operating contribution margin (70%)
    LTV_HORIZON_MONTHS: int = 12             # Rescued customer lifetime horizon (12 months)
    
    # Campaign Operational Costs (USD)
    CONTACT_COST: float = 10.00              # Outbound success contact + omni-channel tracking
    INCENTIVE_OFFER_COST: float = 90.00      # 20% promotional discount or bundle subsidy (TechSupport/Security)
    TOTAL_INTERVENTION_COST: float = 100.00  # CONTACT_COST + INCENTIVE_OFFER_COST
    
    # Operational Effectiveness
    SAVE_RATE: float = 0.35                  # Base conversion/save rate of true churners (35%)
    
    # Portfolio Benchmarks (Telco Churn Dataset)
    AVG_CHURN_MONTHLY_CHARGE: float = 74.44  # Average MRR for churning customers
    AVG_RESCUABLE_LTV: float = 74.44 * 0.70 * 12 # ~$625.30 USD
    
    # ML & Reproducibility Settings
    RANDOM_STATE: int = 42
    TEST_SIZE: float = 0.20
    CV_FOLDS: int = 5

CONFIG = RetentionEconomicsConfig()
