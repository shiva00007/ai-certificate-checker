import os
from flask import Flask, render_template, request,redirect, url_for, session
import newsapi
from newsapi import NewsApiClient

from flask_mail import Mail, Message
#import ibm_db
#import re
# init flask app
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import db


# Initialize Firebase Admin SDK with service account
cred = credentials.Certificate('hhkt-78cca-firebase-adminsdk-2wrqz-efad644446.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hhkt-78cca-default-rtdb.firebaseio.com/'
})

# Initialize Firestore database client
# db = firestore.client()

app = Flask(__name__)
app.secret_key = 'a'
#conn = ibm_db.connect("DATABASE=bludb ; HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud; PORT= 31249; SECURITY=SSL; SSLServerertificate=DigiCertGlobalRootCA.crt; UID=chy62889; PWD=jUDTX6iyU1fnu8xx;", '', '')
  
# Init news api 
newsapi = NewsApiClient(api_key='080f8b6701044c6183d75ff27aac0028')


# Get a reference to the Firestore database

  
# helper function
def get_sources_and_domains():
    all_sources = newsapi.get_sources()['sources']
    sources = []
    domains = []
    for e in all_sources:
        id = e['id']
        domain = e['url'].replace("http://", "")
        domain = domain.replace("https://", "")
        domain = domain.replace("www.", "")
        slash = domain.find('/')
        if slash != -1:
            domain = domain[:slash]
        sources.append(id)
        domains.append(domain)
    sources = ", ".join(sources)
    domains = ", ".join(domains)
    return sources, domains

#
@app.route("/", methods=['GET', 'POST'])
def home():
    # Store the news data in Firebase
    sources, domains = get_sources_and_domains()
    all_articles = newsapi.get_everything(q="",
                                          sources=sources,
                                          domains=domains,
                                          language='en',
                                          sort_by='relevancy',
                                          page_size=100)['articles']
    ref = db.reference('news')
    for i, article in enumerate(all_articles):
        ref.child(str(i)).set(article)

    if request.method == "POST":
        sources, domains = get_sources_and_domains()
        keyword = request.form["keyword"]
        related_news = newsapi.get_everything(q=keyword,
                                      sources=sources,
                                      domains=domains,
                                      language='en',
                                      sort_by='relevancy')
        no_of_articles = related_news['totalResults']
        if no_of_articles > 100:
            no_of_articles = 100
        all_articles = newsapi.get_everything(q=keyword,
                                      sources=sources,
                                      domains=domains,
                                      language='en',
                                      sort_by='relevancy',
                                      page_size = no_of_articles)['articles']


        return render_template("home.html", all_articles = all_articles, 
                               keyword=keyword)
    else:
        top_headlines = newsapi.get_top_headlines(country="in", language="en")
        total_results = top_headlines['totalResults']
        if total_results > 100:
            total_results = 100
        all_headlines = newsapi.get_top_headlines(country="in",
                                                     language="en", 
                                                     page_size=total_results)['articles']
        return render_template("home.html", all_headlines = all_headlines)
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug = True)