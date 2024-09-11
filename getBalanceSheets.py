import fmpsdk # for getting balance sheets
import xlrd # for extracting tickers from official NYSE data
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv('MY_API_KEY')

''' get all tickers that are listed on the NYSE
        open the first (and only) sheet in the document
        get number of rows
'''

book = xlrd.open_workbook("data/NYSE_and_NYSE_MKT_Trading_Units_Daily_File.xls")
sh = book.sheet_by_index(0)
nrows = sh.nrows

# get balance sheets 
for n in range(nrows - 1):
    balance_sheet = fmpsdk.balance_sheet_statement(key, sh.cell_value(rowx=n, colx=1), period="quarter")
    print(balance_sheet)
    # TODO: connect to mongoDB to save balance sheets there and fully implement getBalanceSheets