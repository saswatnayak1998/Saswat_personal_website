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

# instantiate Flask app and database
app = Flask(__name__)
CORS(app) 

def chatbot(question):
    pickle_path = 'retrieval_chain.pkl'
    if os.path.exists(pickle_path):
        with open(pickle_path, 'rb') as file:
            retrieval_chain = pickle.load(file)
            print("WORKS")
            response = retrieval_chain.invoke({"input": question})
            return response["answer"]

    else:
        llm = Ollama(model="llama2")
        output_parser = StrOutputParser()
        
        loader = WebBaseLoader("http://127.0.0.1:5500/about.html")

        docs = loader.load()

        embeddings = OllamaEmbeddings()
        text_splitter = RecursiveCharacterTextSplitter()
        documents = text_splitter.split_documents(docs)
        vector = FAISS.from_documents(documents, embeddings)

        prompt = ChatPromptTemplate.from_template("""you are Saswat, i.e. the person in the text. Answer questions like saswat will answer. He respects people and is funny sometimes.Never mention that you are an AI. 

        <context>
        {context}
        </context>

        Question: {input}""")

        document_chain = create_stuff_documents_chain(llm, prompt)

        retriever = vector.as_retriever()
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        response = retrieval_chain.invoke({"input": question})
        with open(pickle_path, 'wb') as file:
            pickle.dump(retrieval_chain, file)
            print("Fuckin_Works")

            return response["answer"]

@app.route("/ask", methods=['POST'])
def askme():

    # access data submitted with HTTP request
    qinfo = request.json

    question=qinfo['question']


    answer = chatbot(question)
    return jsonify({'answer': answer})


if __name__ == "__main__":
    app.run(debug=True)

