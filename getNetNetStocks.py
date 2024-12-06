import getBalanceSheets as edgar # Get the edgar data

# 10K DATA

# Annual facts
annual, isInternationalData = edgar.annual_facts('GM')

if(isInternationalData):
    # Get current assets for all filings
    assets_row = annual.loc["CurrentAssets"]

    # Get the most recent 10K filing's current assets
    current_assets = assets_row.iloc[-1]

    # Get most recent total liabilities for the firm
    equity_and_liabilities_row = annual.loc["EquityAndLiabilities"]
    equity_and_liabilities = equity_and_liabilities_row.iloc[-1]

    equity_row = annual.loc["Equity"]
    equity = equity_row.iloc[-1]
    
    total_liabilities = equity_and_liabilities - equity

    # Net current asset value
    ncav = current_assets - total_liabilities

    # Get weighted number of shares outstanding
    wanosod_row = annual.loc["WeightedAverageShares"]
    # Get the most recent filing
    wanosod = wanosod_row.iloc[-1]
else:
    # Get current assets for all filings
    assets_row = annual.loc["Assets, Current"]

    # Get the most recent 10K filing's current assets
    current_assets = assets_row.iloc[-1]

    # Get most recent total liabilities for the firm
    total_liabilities_row = annual.loc["Liabilities"]
    total_liabilities = total_liabilities_row.iloc[-1]

    # Net current asset value
    ncav = current_assets - total_liabilities

    # Get weighted number of shares outstanding, diluted
    wanosod_row = annual.loc["Weighted Average Number of Shares Outstanding, Diluted"]
    # Get the most recent filing
    wanosod = wanosod_row.iloc[-1]

# NCAV per Share
ncav_per_share = ncav / wanosod

# Print to console
print(f"Total Liabilities: {total_liabilities}")
print(f"Current Assets:    {current_assets}")
print(f"Net current asset value: {ncav}")
print(f"Weighted number of shares outstanding, diluted: {wanosod}")
print(f"Net current asset value per share: {ncav_per_share}")



















# Apple's NCAV
# $4,488,000,000

# Apple's NCAV per share
# $6.9152...