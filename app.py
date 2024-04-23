from flask import Flask, render_template, request, jsonify
import langchain
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from flask_cors import CORS
import os
import dill as pickle
from newsapi import NewsApiClient
from newsapi.newsapi_client import NewsApiClient
from datetime import datetime, timedelta
from textblob import TextBlob



# instantiate Flask app and database
app = Flask(__name__)
CORS(app) 

def chatbot(question):
    pickle_path = 'retrieval_chain.pkl'
    if os.path.exists(pickle_path):
        with open(pickle_path, 'rb') as file:
            retrieval_chain = pickle.load(file)
            response = retrieval_chain.invoke({"input": question})
            return response["answer"]

    else:

        llm = Ollama(model="llama2")
        
        loader = WebBaseLoader("http://127.0.0.1:5500/about.html")

        docs = loader.load()

        embeddings = OllamaEmbeddings()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=10
        )
        documents = text_splitter.split_documents(docs)
        vector = FAISS.from_documents(documents, embeddings)

        prompt = ChatPromptTemplate.from_template("""NEVER MENTION THAT YOU ARE AN AI. You are Saswat, i.e. the person in the text. Answer questions like Saswat will answer. He respects people and answers questions like he is in an interview. 

        <context>
        {context}
        </context>

        Question: {input}""")

        document_chain = create_stuff_documents_chain(llm, prompt)
 
        retriever = vector.as_retriever(search_kwargs={"k":2})
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        response = retrieval_chain.invoke({"input": question})
        print("Frickin works")
        with open(pickle_path, 'wb') as file:
            pickle.dump(retrieval_chain, file)

            return response["answer"]

@app.route("/ask", methods=['POST'])
def askme():

    # access data submitted with HTTP request
    qinfo = request.json

    question=qinfo['question']


    answer = chatbot(question)
    return jsonify({'answer': answer})

@app.route("/news", methods=['POST'])
def stock_news():

    # access data submitted with HTTP request

    info = request.json

    about=info['question']
    today_date = datetime.now()
    dates = [today_date - timedelta(days=i) for i in range(5)]

    # Format dates as strings in Year-Month-Day format
    formatted_dates = [date.strftime("%Y-%m-%d") for date in dates]

    newsapi = NewsApiClient(api_key='c96d36fa06c842a084ddfe6ef02f127c')

    # /v2/top-headlines
    all_articles = newsapi.get_everything(q=about,
                                        sources='bbc-news,the-verge',
                                        from_param=formatted_dates[0],
                                        to=formatted_dates[2],
                                        language='en',
                                        sort_by='relevancy',
                                        page=1)
    sentiment_score = 0
    for news in all_articles['articles']:
        text = news['description']
        blob = TextBlob(text)
        sentiment_score = sentiment_score + blob.sentiment.polarity
    return jsonify({'answer': sentiment_score})


if __name__ == "__main__":
    app.run(debug=True)

