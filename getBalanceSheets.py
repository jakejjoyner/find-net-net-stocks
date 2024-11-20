# Import modules
import requests
import pandas as pd

# Create request header
headers = {'User-agent': "jakejoyner9@gmail.com"}

def get_cik_by_index(index, headers=headers):
        # Get all company names/CIK keys
        companyTickers = requests.get(
                "https://www.sec.gov/files/company_tickers.json",
                headers=headers
                )

        # Change from dictionary into dataframe
        companyData = pd.DataFrame.from_dict(companyTickers.json(), orient='index')

        # Add leading zeroes to CIKs
        companyData['cik_str'] = companyData['cik_str'].astype(str).str.zfill(10)

        # Get the CIK at the inputted index
        cik = companyData[index:index+1].cik_str[0]

        return cik

def get_submission_data_by_index(index, only_filings_df=False, headers=headers):
        cik = get_cik_by_index(index)
        url = f'https://data.sec.gov/submissions/CIK{cik}.json'
        company_json = requests.get(url, headers=headers).json()
        if only_filings_df:
                return pd.DataFrame(company_json['filings']['recent'])
        return company_json

def get_filtered_filings(index, ten_k=True, just_accesion_numbers=False, headers=headers):
    company_filings_df = get_submission_data_by_index(index, only_filings_df=True, headers=headers)
    if ten_k:
        df = company_filings_df[company_filings_df['form'] == '10-K']
    else:
        df = company_filings_df[company_filings_df['form'] == '10-Q']
    if just_accesion_numbers:
        df = df.set_index['reportDate']
        accession_df = df['accessionNumber']
        return accession_df
    else:
        return df

def get_facts(index, headers=headers):
      cik = get_cik_by_index(index)
      url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
      company_facts = requests.get(url, headers).json()
      return company_facts

def fact_df(index, headers=headers):
        data = get_facts(index, headers=headers)
        us_gaap_data = data['facts']['us-gaap']
        df_data = []
        for fact, details in us_gaap_data.items():
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
        labels_dict = {fact: details["label"] for fact, details in us_gaap_data.items()}
        return df, labels_dict

def annual_facts(index, headers=headers):
      accession_nums = get_filtered_filings(
            index, ten_k=True, just_accesion_numbers=True
        )
      df, label_dict = fact_df(index, headers)
      ten_k = df[df["accn"].isin(accession_nums)]
      ten_k = ten_k[ten_k.index.isin(accession_nums.index)]
      pivot = ten_k.pivot_table(values="val", columns="fact", index="end")
      pivot.rename(columns=label_dict, inplace=True)
      