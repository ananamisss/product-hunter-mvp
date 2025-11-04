from pytrends.request import TrendReq

def top_queries(kw_list=["gadgets"]):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(kw_list, timeframe='now 7-d')
    return pytrends.related_queries()

if __name__ == "__main__":
    print(top_queries(["mini workout"]))
