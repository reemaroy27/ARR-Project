CURRENCY_RATES = {
    "USD": 1,
    "EUR": 1.1,
    "GBP": 1.27,
    "JPY": 1 / 150
}

INVALID_REVENUE_VALUES = {
    "",
    "N/A",
    "NA",
    "Not disclosed",
    "Undisclosed",
    None
}

CATEGORY_MAPPING = {

    # AI
    "Artificial Intelligence": "AI_ML",
    "AI & ML": "AI_ML",
    "AI/ML": "AI_ML",
    "Machine Learning": "AI_ML",

    # Cloud
    "Cloud": "CLOUD",
    "Cloud Computing": "CLOUD",
    "Cloud Services": "CLOUD",

    # Finance
    "FinTech": "FINTECH",
    "Financial Technology": "FINTECH",
    "Finance": "FINTECH",

    # Data
    "Analytics": "DATA_ANALYTICS",
    "Data Analytics": "DATA_ANALYTICS",
    "Big Data": "DATA_ANALYTICS",

    # Software
    "Software": "SOFTWARE",
    "Enterprise Software": "SOFTWARE",
    "SaaS": "SOFTWARE",

    # Security
    "Security": "CYBERSECURITY",
    "Cybersecurity": "CYBERSECURITY",
    "InfoSec": "CYBERSECURITY"
}

COMPANY_ALIASES = {

    # OpenAI
    "Open AI": "OpenAI",
    "OpenAI Inc.": "OpenAI",

    # AWS
    "AWS": "Amazon Web Services",
    "Amazon Web Services (AWS)": "Amazon Web Services",

    # DeepMind
    "DeepMind": "Google DeepMind",
    "Google Deepmind": "Google DeepMind",

    # Meta
    "Facebook AI Research": "Meta AI",
    "Meta AI Research": "Meta AI",

    # NVIDIA
    "Nvidia": "NVIDIA",
    "NVIDIA Corporation": "NVIDIA",

    # MongoDB
    "Mongo DB": "MongoDB",

    # DataRobot
    "Data Robot": "DataRobot",

    # Palantir
    "Palantir Technologies": "Palantir",

    # Snowflake
    "Snowflake Inc.": "Snowflake",

    # Databricks
    "Databricks Inc.": "Databricks",

    # Stripe
    "Stripe Inc.": "Stripe",

    # Azure
    "Azure": "Microsoft",
    "Microsoft Azure": "Microsoft",

    # SpaceX
    "The Boring Company / SpaceX": "SpaceX",

    #Cloudflare
    "CloudFlare": "Cloudflare"
}
