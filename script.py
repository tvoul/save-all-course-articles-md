import requests
import datetime

articles = []
skip = 0

def getArticles(skip):
    url = f'https://devop.lms.nodehill.com/api/articles?skip={skip}&klass=devop&admin=&category='
    response = requests.get(url)
    responsejson = response.json()
    for i in range (0, len(responsejson)):
        slug = responsejson[i]['slug']
        url = 'https://devop.lms.nodehill.com/rest/Article?body={"properties":{"slug":"' + slug + '"}}'
        r = requests.get(url)
        rjson = r.json()
        article = []
        article.append(rjson[0]['slug'])
        timestamp = rjson[0]['publishedAt']
        date = convertDate(timestamp)
        article.append(date)
        article.append(rjson[0]['title'])
        article.append(rjson[0]['content'])
        articles.append(article)
    if(len(responsejson) != 0):
        skip += 40
        getArticles(skip)

def writeArticles(articles):
    for item in articles:
        with open(f'articles/{item[0]}.md', 'a', encoding='utf-8') as file:
            file.write('###### ' + str(item[1]) + '\n')
            file.write('# ' + str(item[2]) + '\n')
            file.write('\n' + str(item[3]))

def convertDate(ms):
    date = datetime.datetime.fromtimestamp(int(ms / 1000)).strftime('%Y-%m-%d %H:%M:%S')
    return date

getArticles(skip)
writeArticles(articles)
