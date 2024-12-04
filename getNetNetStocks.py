import getBalanceSheets as edgar # Get the edgar data

# 10K DATA

# Annual facts
annual = edgar.annual_facts(0)

# Get current assets for all filings
assets_row = annual.loc["Assets, Current"]

# Get the most recent 10K filing's current assets
current_assets = assets_row.iloc[-1]

print(current_assets)




















# Apple's NCAV
# $4,488,000,000

# Apple's NCAV per share
# $6.9152...