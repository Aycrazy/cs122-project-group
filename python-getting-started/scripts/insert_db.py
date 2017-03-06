from newsapp.models import ArticlesManager, Article
import re
import glob, os

def run():
    os.chdir("scripts")
    print(os.getcwd())
    for file in glob.glob("*.csv"):
        print(file)
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            print('hellos')
            for row in reader:
                print(row[0])
                article = Article.object.create_article(article=row[0],pub_date=row[1],\
                    nltk_score=row[2],source = row[3])
                article.save()
