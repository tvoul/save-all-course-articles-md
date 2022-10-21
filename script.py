import requests
import datetime

#array to store articles
articles = []

#the api retrieves 40 articles at a time, by skipping multipliers of 40
#skip will therefore increase by 40 for every request
skip = 0

def getArticles(skip):

    #url with dynamic skip
    #0 the first time and will increment by 40 before its called again
    url = f'https://devop.lms.nodehill.com/api/articles?skip={skip}&klass=devop&admin=&category='
    
    #fetch group of articles and transform it to json
    response = requests.get(url)
    responsejson = response.json()

    #loop for the number of responses
    for i in range (0, len(responsejson)):

        #from the json response, extract the slug
        slug = responsejson[i]['slug']

        #combine the slug with the url to fetch a single article
        url = 'https://devop.lms.nodehill.com/rest/Article?body={"properties":{"slug":"' + slug + '"}}'

        #fetch article and transform it to json
        r = requests.get(url)
        rjson = r.json()

        #array to store different parts of the article
        article = []

        #slug will be used as the filename
        article.append(rjson[0]['slug'])

        #timestamp is Unix time (ms)
        timestamp = rjson[0]['publishedAt']

        #convert timestamp to human readable format
        date = convertDate(timestamp)

        #date and time published will be included in the file
        article.append(date)

        #save title to write it to file
        article.append(rjson[0]['title'])

        #save article content to write it to file
        article.append(rjson[0]['content'])

        #save this article to an array of articles
        articles.append(article)

    #execute this function again if there were any responses last time
    #it will therefore run once with zero articles as a response, skipped "too many"
    #and then break
    if(len(responsejson) != 0):
        #increase skip by 40 to fetch the next batch
        skip += 40
        getArticles(skip)

#convert timestamp to human readable format
def convertDate(ms):
    #use the imported datetime module
    #JavaScript uses milliseconds
    #datetime expects seconds, so divide ms by 1000
    #convert to year-month-day hour-minute-second
    date = datetime.datetime.fromtimestamp(int(ms / 1000)).strftime('%Y-%m-%d %H:%M:%S')
    return date

#write each article into a file in the folder articles
def writeArticles(articles):
    for article in articles:
        #'w' to overwrite copies if run as an automated script (cronjob)
        #use slug as the filename
        with open(f'articles/{article[0]}.md', 'w', encoding='utf-8') as file:
            #write date at top of file, in small format
            file.write('###### ' + str(article[1]) + '\n')
            #write the title as a header
            file.write('# ' + str(article[2]) + '\n')
            #write the content
            file.write('\n' + str(article[3]))


#populate the articles array
getArticles(skip)

#write the articles array into files
writeArticles(articles)
