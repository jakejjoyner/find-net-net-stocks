# Find Net-Net Stocks

This project provides tools to calculate the **Net Current Asset Value (NCAV)** and the **Net Current Asset Value per Share (NCAV per Share)** of publicly traded companies using financial data retrieved from the SEC’s EDGAR database. The goal is to identify undervalued stocks based on the NCAV formula, a strategy popularized by Benjamin Graham.

---

## Features

- Retrieve and analyze financial data (e.g., current assets, total liabilities, weighted average shares outstanding) for various companies.
- Support for both domestic (US-GAAP) and international (IFRS) reporting standards.
- Calculation of:

  - **Net Current Asset Value (NCAV):**  $\text{NCAV} = \text{Current Assets} - \text{Total Liabilities}$

  - **NCAV per Share:**  $\text{NCAV}_{\text{per share}} = \frac{\text{NCAV}}{\text{Weighted Average Shares Outstanding}}$
- Support for filtering **10-K** and **20-F** filings.

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/jakejjoyner/find-net-net-stocks.git
cd find-net-net-stocks
```

### 2. Install Dependancies
Make sure you have Python 3.8+ installed, then run:
```bash
pip install -r requirements.txt
```

---

## Usage

### 1. Import the getBalanceSheets Module
This module interacts with the SEC EDGAR API to fetch financial data for specifric companies
```python
import getBalanceSheets as edgar
```

### 2. Calculate NCAV for a Specific Company
The project provides an example script (getNetNetStocks.py) for calculating NCAV.

**Example Script:**
```bash
python getNetNetStocks.py
```

**Key Outputs:**
- Total Liabilities
- Current Assets
- Net Current Asset Value (NCAV)
- NCAV per Share

### 3. Example Workflow

**NCAV Calvulation for a Domestic Company:**
```python
annual, isInternationalData = edgar.annual_facts('AAPL')

if not isInternationalData:
    current_assets = annual.loc["Assets, Current"].iloc[-1]
    total_liabilities = annual.loc["Liabilities"].iloc[-1]
    wanosod = annual.loc["Weighted Average Number of Shares Outstanding, Diluted"].iloc[-1]

    ncav = current_assets - total_liabilities
    ncav_per_share = ncav / wanosod
    print(f"NCAV per share: {ncav_per_share}")
```

## Key Concepts
**Net Current Asset Value (NCAV)**

The NCAV formula identifies stocks that are undervalued based on their balance sheet.

*NCAV* = Current Assets - Total Liabilities

*Net Current Asset Value Per Share:* NCAV divided by the number of outstanding shares.

---

## Files and Directories

- getNetNetStocks.py:
    - Main script for calculating NCAV and related metrics.
- getBalanceSheets.py:
    - Utility module for fetching and processing financial data from the SEC EDGAR database.
- facts.ipynb:
	- Jupyter notebook for exploratory analysis and debugging.
- requirements.txt:
    - List of required Python libraries.

---

## Dependencies

- pandas: For data manipulation and analysis.
- numpy: For numerical computations.
- requests: For making HTTP requests to the SEC EDGAR API.
- jupyter: For running .ipynb files (optional).

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## TODOs

- Add 10-Q support
- Improve support for international companies (IFRS-specific data extraction).
- Enhance error handling for missing financial data.
- Add more examples and tests for different industries.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contributions
Contributions are welcome! Feel free to fork this repository, make changes, and submit a pull request.

---

## Contact
For questions or suggestions, please contact jakejoyner9@gmail.com.