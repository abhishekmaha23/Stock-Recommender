import requests
# import base64
import json
import pandas as pd


def credentials(encodeValue, authorizationType):
    lHead = {'Authorization': authorizationType + ' ' + encodeValue}
    return lHead


def url_site(website):
    lUrl = ''
    if website == 'Twitter':
        lUrl = 'https://api.twitter.com/oauth2/token?grant_type=client_credentials'
    elif website == 'Alpha Vantage':
        lUrl = 'https://www.alphavantage.co/query'
    elif website == 'Quandl':
        lUrl = 'https://www.quandl.com/api/v3/datasets/WIKI/'
    elif website == 'NewsApi':
        lUrl = 'https://newsapi.org/v2/'
    else:
        raise Exception('!!Site Not Found!!')
    return lUrl


def access_token(head, website):
    lApiUrl = url_site(website)
    r = requests.post(lApiUrl, headers=head)
    lTokenJson = json.loads(r.text)
    lAccessToken = lTokenJson['access_token']
    return lAccessToken


def access_url(website):
    lAccessUrl = ''
    if website == 'Twitter':
        lAccessUrl = 'https://api.twitter.com/1.1/search/tweets.json'
    else:
        raise Exception('!!Site Not Found!!')
    return lAccessUrl


def dataExtractWithToken(website, encodeValue, authorizationType, tokenType, query):
    lAccessUrl = access_url(website)
    lHead = credentials(encodeValue, authorizationType)
    lAccessToken = access_token(lHead, website)
    lHeader = {'Authorization': tokenType + ' ' + lAccessToken}
    lParam = {'q': query}
    data = requests.get(lAccessUrl, headers=lHeader, params=lParam)
    return data


def dataExtractWithCredentials(website, encodeValue, authorizationType, tokenType, query):
    lAccessUrl = access_url(website)
    lHead = credentials(encodeValue, authorizationType)
    lParam = {'q': query}
    data = requests.get(lAccessUrl, headers=lHead, params=lParam)
    return data


def dataExtractionWithQuery(url, query):
    lParam = query
    data = requests.get(url, params=lParam)
    print(data.url)
    return data


# def Data_Report(data, reqColsName):
#     dataset = pd.DataFrame(data)
#     dataset.columns = reqCols
#     for colNum in range(0, len(reqCols)):
#         colName = reqCols[colNum]
#         dataset.colName = dataset.colName.apply(
#             lambda colName: np.nan if len(colName) == 0 else colName)
#     return dataset


def Twitter(query):
    content = []
    tweetData = dataExtractWithToken('Twitter',
                                     'SllWYVhYa25tRzRMUFNRcDFFYjl6UlpGQTo1QWN6Tng4Nnd3cDVUcDNYT2FaUXk0VVdjR3ZtQldjcVpUYmk5YUpXVGNWVkpOWjVmZA==',
                                     'Basic',
                                     'Bearer',
                                     query)
    tweetTextJson = json.loads(tweetData.text)
    return tweetData.text


def Alpha_Vantage(function, symbol, outputSize, interval):
    url = url_site('Alpha Vantage')
    if function == 'TIME_SERIES_INTRADAY':
        query = {'function': function, 'symbol': symbol, 'outputsize': outputSize, 'interval': interval + 'mins',
                 'apikey': 'PTEGOCHNAABHYBIL'}
    else:
        query = {'function': function, 'symbol': symbol,
                 'outputsize': outputSize, 'apikey': 'PTEGOCHNAABHYBIL'}
    lData = dataExtractionWithQuery(url, query)
    return lData


def Quandl(company, startDate, endDate, order='desc'):
    url = url_site('Quandl')
    urlSeek = url + company + '.json'
    query = {'start_date': startDate, 'end_date': endDate,
             'order': order, 'apikey': 'WrstrSAi289CAATv4x-E'}
    lData = dataExtractionWithQuery(urlSeek, query)
    return lData


def NewsApi(news_type, sources, company):
    url = url_site('NewsApi')
    urlSeek = url + news_type
    query = {'sources': sources, 'q': company,
             'apiKey': '9ad90e41f4404cb7a510213dbe93875f'}
    lData = dataExtractionWithQuery(urlSeek, query)
    return lData
