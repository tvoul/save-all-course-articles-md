from requests_html import HTMLSession

session = HTMLSession()
articles = []

def getArticles(skip):
    url = f'https://devop.lms.nodehill.com/api/articles?skip={skip}&klass=devop&admin=&category='
    response = session.get(url)
    responsejson = response.json()
    for i in range (0, len(responsejson)):
        slug = responsejson[i]['slug']
        url = 'https://devop.lms.nodehill.com/rest/Article?body={"properties":{"slug":"' + slug + '"}}'
        r = session.get(url)
        rjson = r.json()
        article = []
        article.append(rjson[0]['slug'])
        article.append(rjson[0]['title'])
        article.append(rjson[0]['content'])
        articles.append(article)
        print(len(responsejson))

def writeArticles(articles):
    for item in articles:
        with open(f'articles/{item[0]}.md', 'a', encoding='utf-8') as file:
            file.write(str(item[1]) + '\n')
            file.write(str(item[2]))

skip = 0
for i in range(0, 8):
    getArticles(skip)
    skip += 40

writeArticles(articles)