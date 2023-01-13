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
        article.append(', '.join(responsejson[i]['categories'])) 
        article.append(rjson[0]['title'])
        article.append(rjson[0]['content'])
        articles.append(article)
    if(len(responsejson) != 0):
        skip += 40
        getArticles(skip)

def convertDate(ms):
    date = datetime.datetime.fromtimestamp(int(ms / 1000)).strftime('%Y-%m-%d %H:%M:%S')
    return date

def writeArticles(articles):
    for article in articles:
        with open(f'articles/{article[0]}.md', 'w', encoding='utf-8') as file:
            file.write('###### ' + str(article[1]) + '\n')
            file.write('##### ' + str(article[2]) + '\n')
            file.write('# ' + str(article[3]) + '\n')
            file.write('\n' + str(article[4]))

getArticles(skip)
writeArticles(articles)