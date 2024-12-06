# Import modules
import requests
import pandas as pd

# Create request header
headers = {'User-agent': "jakejoyner9@gmail.com"}

# FORMAT DATA FROM THE EDGAR DATABASE

def get_cik_by_ticker(ticker, headers=headers):
        # Get all company names/CIK keys
        company_json = requests.get(
                "https://www.sec.gov/files/company_tickers.json",
                headers=headers
                ).json()
        for company in company_json.values():
                if company["ticker"] == ticker:
                      cik = str(company["cik_str"]).zfill(10)
                      return cik

def get_submission_data_by_ticker(ticker, only_filings_df=False, headers=headers):
        cik = get_cik_by_ticker(ticker)
        url = f'https://data.sec.gov/submissions/CIK{cik}.json'
        company_json = requests.get(url, headers=headers).json()
        if only_filings_df:
                # Only return the filings dataframe
                return pd.DataFrame(company_json['filings']['recent'])
        return company_json

# Filter filings by either 10K or 10Q only
# If just_accesion_numbers, only return the accession numbers w/ the report date
def get_filtered_filings(ticker, ten_k=False, twenty_f=False, just_accesion_numbers=False, headers=headers):
    company_filings_df = get_submission_data_by_ticker(ticker, only_filings_df=True, headers=headers)
    if ten_k:
        df = company_filings_df[company_filings_df['form'] == '10-K']
    elif twenty_f:
        df = company_filings_df[company_filings_df['form'] == '20-F']
    else:
        df = company_filings_df[company_filings_df['form'] == '10-Q']
    if just_accesion_numbers:
        df = df.set_index('reportDate')
        accession_df = df['accessionNumber']
        return accession_df
    else:
        return df

# Get the company facts
def get_facts(ticker, headers=headers):
      cik = get_cik_by_ticker(ticker)
      url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
      company_facts = requests.get(url, headers=headers).json()
      return company_facts

# Get the facts into a dataframe
# Return the dataframe and a labels dictionary with the human readable fact names
def fact_df(ticker, headers=headers):
        data = get_facts(ticker, headers=headers)
        if(data['facts'].keys() == {'dei', 'ifrs-full'}):
                # For internatinal companies
                us_gaap_ifrs_data = data['facts']['ifrs-full']
        else:
                us_gaap_ifrs_data = data['facts']['us-gaap']
        df_data = []
        for fact, details in us_gaap_ifrs_data.items():
            for unit in details["units"]:
                for item in details["units"][unit]:
                        row = item.copy()
                        row["fact"] = fact
                        df_data.append(row)
        df = pd.DataFrame(df_data)
        df["end"] = pd.to_datetime(df["end"])
        df["start"] = pd.to_datetime(df["start"])
        df = df.drop_duplicates(subset=["fact","end", "val"])
        df.set_index("end", inplace=True)
        # Only use the labels dict if dealing with us-gaap data. Otherwise we have to use the camelCase labels
        # because the human readable names are missing from non us-gaap data
        if(not(data['facts'].keys() == {'dei', 'ifrs-full'})):
                labels_dict = {fact: details["label"] for fact, details in us_gaap_ifrs_data.items()}
        else:
                labels_dict = {"":""}
        return df, labels_dict

# Returns a pivot table with end date of filing period, company facts,
# and the labels as the human readable fact names
def annual_facts(ticker, headers=headers):
      isInternationalData = True
      data = get_facts(ticker, headers=headers)
      #accession_nums = pd.DataFrame()
      # Filter for 20-Fs
      if(data['facts'].keys() >= {'dei', 'ifrs-full'}):
        accession_nums = get_filtered_filings(ticker, ten_k=False, twenty_f=True, just_accesion_numbers=True)
      # Otherwise get 10-Ks
      elif(data['facts'].keys() >= {'dei', 'us-gaap'}):
        accession_nums = get_filtered_filings(ticker, ten_k=True, twenty_f=False, just_accesion_numbers=True)
      df, label_dict = fact_df(ticker, headers)
      ten_k = df[df["accn"].isin(accession_nums)]
      accession_nums_index_inDateTime = pd.to_datetime(accession_nums.index) # Explicitly cast to make the compiler happy
      ten_k = ten_k[ten_k.index.isin(accession_nums_index_inDateTime)]
      pivot = ten_k.pivot_table(values="val", columns="fact", index="end")
      # Only rename columns if dealing with us-gaap data
      if(not(data['facts'].keys() == {'dei', 'ifrs-full'})):
        pivot.rename(columns=label_dict, inplace=True)
        isInternationalData = False
      return pivot.T, isInternationalData