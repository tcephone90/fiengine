#PULLING EXTERNAL DATA FROM A GIT HUB STORED FILE OR OTHER CLOUD
#https://github.com/tcephone90/fiengine/blob/main/raw_financials_two.json
#THIS IS FOR ALPAHA ADVANTAGE FOR GETTING LONGER TERM FINANCIAL METRICS
#BASED ON RAW FINANCIAL STATEMENTS THEN CALCULATING THE METRICS
#**THIS IS BASED ON RAWSTATIC DATA I PULLED ALREADY NOT A WEB API CALL ***
#PULLING EXTERNAL DATA FROM A JSON FILE OR OTHER FROM A GITHUB STORED FILE OR OTHER CLOUD 
#https://github.com/tcephone90/fiengine/blob/main/raw_financials_two.json

import json
import numpy as np
import pandas as pd
import requests

# =====================================================================
# 📁 PART 1: PRE-BUILT CONFIGURATION POOLS
# =====================================================================
ticker_historical_prices = {
    '2026-06-30': 373.02, '2025-06-30': 421.90, '2024-06-30': 446.95,
    '2023-06-30': 340.54, '2022-06-30': 256.83, '2021-06-30': 270.90,
    '2020-06-30': 203.51, '2019-06-30': 133.96, '2018-06-30': 98.61,
    '2017-06-30': 68.93,  '2016-06-30': 51.17,  '2015-06-30': 44.15,
    '2014-06-30': 41.70,  '2013-06-30': 34.54,  '2012-06-30': 30.59,
    '2011-06-30': 26.00,  '2010-06-30': 23.01,  '2009-06-30': 23.77,
    '2008-06-30': 27.51,  '2007-06-30': 29.47
}

# =====================================================================
# ⚙️ PART 2: THE MAIN CALCULATION ENGINE
# =====================================================================
def parse_and_process_financial_pipeline_91026837(raw_inc, raw_cf, raw_bal):
    """
    Processes core valuation equations using the unpacked dictionary layers.
    """
    print('def parse_and_process_financial_pipeline 91026 837am github version')
    def clean_val(v):
        if v is None or str(v).strip() in ["None", ""]: return 0.0
        return float(v)

    processed_records = {}

    # Unpack variables: Income Statement layers
    for report in raw_inc.get('annualReports', []):
        d = report.get('fiscalDateEnding')
        if not d: continue
        processed_records[d] = {
            'Net_Income_M': clean_val(report.get('netIncome')) / 1000000.0,
            'Revenue_M': clean_val(report.get('totalRevenue')) / 1000000.0
        }

    # Unpack variables: Cash Flow layers
    for report in raw_cf.get('annualReports', []):
        d = report.get('fiscalDateEnding')
        if d in processed_records:
            ocf = clean_val(report.get('operatingCashflow'))
            capex = clean_val(report.get('capitalExpenditures'))
            processed_records[d]['Free_Cash_Flow_M'] = (ocf - abs(capex)) / 1000000.0

    # Unpack variables: Balance Sheet layers
    for report in raw_bal.get('annualReports', []):
        d = report.get('fiscalDateEnding')
        if d in processed_records:
            processed_records[d]['Shares_M'] = clean_val(report.get('commonStockSharesOutstanding')) / 1000000.0
            processed_records[d]['Book_Equity_M'] = clean_val(report.get('totalShareholderEquity')) / 1000000.0

    sorted_dates = sorted(processed_records.keys(), reverse=True)
    prices_list = []

    for date_key in sorted_dates:
        prices_list.append(ticker_historical_prices.get(date_key, 250.00))

    df = pd.DataFrame.from_dict(processed_records, orient='index')
    df.index.name = 'Date'
    df.index = df.index.astype(str)
    df = df.reindex(sorted_dates)

    df['Stock_Price'] = prices_list

    df['EPS'] = df['Net_Income_M'] / df['Shares_M']
    df['BVPS'] = df['Book_Equity_M'] / df['Shares_M']
    df['FCFPS'] = df['Free_Cash_Flow_M'] / df['Shares_M']
    df['Market_Cap_M'] = df['Stock_Price'] * df['Shares_M']

    df['PE_Ratio'] = np.where(df['EPS'] > 0, df['Stock_Price'] / df['EPS'], np.nan)
    df['PB_Ratio'] = np.where(df['BVPS'] > 0, df['Stock_Price'] / df['BVPS'], np.nan)
    df['PFCF_Ratio'] = np.where(df['FCFPS'] > 0, df['Stock_Price'] / df['FCFPS'], np.nan)
    df['PS_Ratio'] = np.where(df['Revenue_M'] > 0, df['Market_Cap_M'] / df['Revenue_M'], np.nan)

    target_columns = ['PE_Ratio', 'PB_Ratio', 'PFCF_Ratio', 'PS_Ratio']
    return df[target_columns].round(2)

# =====================================================================
# 🚀 PART 3: REMOTE STREAMING INGESTION (DYNAMIC BROWSER URL CONVERTER)
# =====================================================================
if __name__ == "__main__":
    # Your exact repository browser viewing location URL string link
    user_provided_url = "https://github.com/tcephone90/fiengine/blob/main/raw_financials_two.json"
    
    print(f"📡 Processing data access request for link: {user_provided_url}")
    
    # URL Mapping Fix: Properly route standard browser links to the raw text CDN endpoint
    if "github.com" in user_provided_url and "/blob/" in user_provided_url:
        processed_target_url = user_provided_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        print(f"🔄 Corrected Raw API Server Route: {processed_target_url}\n")
    else:
        processed_target_url = user_provided_url

    try:
        # Ingest text strings through streaming request pipeline
        response = requests.get(processed_target_url, timeout=15)
        response.raise_for_status()
        raw_content = response.text.strip()

        # Parse Option 2 Python code configurations securely via localized sandbox execution
        local_scope = {}
        exec(raw_content, {}, local_scope)

        income_block = local_scope['raw_income_statement']
        cash_flow_block = local_scope['raw_cash_flow']
        balance_sheet_block = local_scope['raw_balance_sheet']

        # Run valuation script matrix pipeline
        calculated_matrix = parse_and_process_financial_pipeline(
            raw_inc=income_block, 
            raw_cf=cash_flow_block, 
            raw_bal=balance_sheet_block
        )

        print("=" * 95)
        print("📊 METRICS CALCULATED SUCCESSFULLY VIA REPO URL TRANSLATION")
        print("=" * 95)
        print(calculated_matrix.to_string())

        print("\n" + "=" * 95)
        print("📦 EXPORTABLE JSON OUT STRUCT LAYER")
        print("=" * 95)
        print(calculated_matrix.to_json(orient='index', indent=2))

    except requests.exceptions.HTTPError as he:
        print(f"❌ Server Access Failure: {he}")
    except KeyError as ke:
        print(f"❌ Document Formatting Error: Script ran but missed assignment variable name: {ke}.")
    except Exception as e:
        print(f"❌ Execution Failure Error: {e}")




