from Bio import Entrez
from Bio.Medline import parse
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import openai
import pandas as pd
from io import StringIO
import csv
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions server-side as files
Session(app)


def fetch_pubmed_articles(query, email):
    Entrez.email = email

    # Search PubMed
    search_results = Entrez.esearch(db="pubmed", term=query, retmax=10, sort="relevance")
    record = Entrez.read(search_results)
    search_results.close()

    # Get PubMed IDs
    pubmed_ids = record["IdList"]

    # Fetch details
    handle = Entrez.efetch(db="pubmed", id=pubmed_ids, rettype="medline", retmode="text")
    records = parse(handle)

    # Extract information and create DataFrame
    data = []
    for rec in records:
        pmid = rec.get("PMID", "")
        title = rec.get("TI", "")
        authors = ", ".join(rec.get("AU", []))
        journal_citation = rec.get("SO", "")
        abstract = rec.get("AB", "")
        abstract_link = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        data.append([pmid, title, authors, journal_citation, abstract, abstract_link])

    # Create DataFrame
    df = pd.DataFrame(data, columns=['PMID', 'Title', 'Authors', 'Journal Citation', 'Abstract', 'Abstract_Link'])
    return df

def is_relevant(article, question, api_key):
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"You are a medical researching performing a systematic review. You are presented with an article and you have to determine whether the article is related to the research question and should be included in the systematic review and can only reply with relevant or not relevant to this research question: {question}"
            },
            {
                "role": "user",
                "content": article
            },
            {
                "role": "assistant",
                "content": ""
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    reply = response.choices[0].message['content']
    return reply

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        api_key = request.form['api_key']
        question = request.form['question']
        pubmed_query = request.form['pubmed_query']

        # create a df using PubMed results
        df = fetch_pubmed_articles(pubmed_query, email)

        # Create a new column for relevancy
        df['relevancy'] = ""

        # Iterate through the DataFrame and fill the relevancy column
        for index, row in df.iterrows():
            article = row['Abstract']
            relevancy = is_relevant(article, question, api_key)
            df.at[index, 'relevancy'] = relevancy

        # Convert the DataFrame to CSV and store it in a session variable
        csv_str = StringIO()
        df.to_csv(csv_str, index=False)
        csv_str.seek(0)
        session['df_csv'] = csv_str.read()

        return redirect(url_for('results'))

    return render_template('index.html')


@app.route('/results', methods=['GET'])
def results():
    print(session)  # Debugging line to print the session content
    csv_str = StringIO(session['df_csv'])
    df = pd.read_csv(csv_str)

    return render_template('results.html', df=df)

if __name__ == '__main__':
    app.run(debug=True)
