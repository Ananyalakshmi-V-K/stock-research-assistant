import yfinance as yf #yahoo finance ibrary to fetch real stock data for free

def get_stock_fundamentals(ticker : str) -> dict:
    """
    This function takes a stock ticker symbol and returns key financial data.
    A ticker is the short code for a company's stock- like AAPL for Apple,
    TSLA for Tesla, RELIANCE.NS for Reliance Industries (Indian stocks need . NS)

    Args:
        ticker: Stock ticker symbol as a string
    Returns: 
        Dictionary containing key financial metrics
    """

    try:
        #create a ticker obj - this is yfinance's way of representing a stock
        #No API call happens here yet, just creating the object
        stock = yf.Ticker(ticker)

        #.info gives us a big dictionary of all available data about the stock
        #This is where the actual API call to Yahoo Finance happens
        info = stock.info

        #We pick only the fields we need from the big info dictionary
        # .get("field_name", "N/A") means - get this field, but if it doesn't 
        #exist return "N/A" instaead of crashing
        return {
            "lticker" : ticker,

            #company's full official name
            "company_name" : info.get("longName", "N/A"),

            #Current trading price of one share
            "current_price" : info.get("currentPrice", "N/A"),

            #Total value of the company (price x total shares)
            'market_cap' : info.get("marketCap", "N/A"),

            #Price to Earnings ratio - how expensive the stock is relative to earnings
            #lower PE can mean undervalued, higher PE can mean overvalued
            "pe_ratio" : info.get("trailingPE", "N/A"),

            #Earnings Per share - how much profit the company makes per share
            "eps" : info.get("trailingEps", "N/A"),

            #Highest price the stock reached in the last 52 weeks
            "52_week_high" : info.get("fiftyTwoWeekHigh", "N/A"),

            #lowest price the stock reached in the last 52 weeks
            "52_week_low" : info.get("fiftyTwoWeekLow", "N/A"),

            #Total revenue the company earned
            "revenue" : info.get("totalRevenue", "N/A"),

            #What percentage of revenue is actual profit (0.2 means 20% profit margin)
            "profit_margin" : info.get("profitMargins", "N/A"),

            #How much debt the company has cmpared to its equity
            #lower is generally safer
            "debt_to_equity" : info.get("debtToEquity", "N/A"),

            #Annual dividend as a percentage of stock price
            #Some companies pay dividends (share of profits) to shareholder
            "dividend_yield" : info.get("dividendYield", "N/A"),

            #which sector the company belongs to (Technology, Healthcare etc)
            "sector" : info.get("sector", "N/A"),

            #More specific industry within the sector
            "industry" : info.get("industry", "N/A"),

            #A paragraph describing what the company does
            "summary" : info.get("longBusinessSummary", "N/A")
        }
    except Exception as e:
        #If  anything goes wrong(network issue, invalid ticker etc)
        #return an error message instead of crashing the whole program
        return {"error" : f"Failed to fetch data for {ticker} : {str(e)}"}