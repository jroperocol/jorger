import os
import requests
from flask import Flask, request, jsonify
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator

app = Flask(__name__)

os.environ["OPENAI_API_KEY"] = "sk-proj-Md1Au3ZEGVsjQqE5ka11T3BlbkFJdLhqnubJTr7DBwvqjSQo"

file_id = '1wd14YRQ4OXu4bJjjhgEkbyTO0LUqOpuS'
download_url = f"https://drive.google.com/uc?id={file_id}"
response = requests.get(download_url)

with open("data.txt", "wb") as file:
    file.write(response.content)

with open("data.txt", "r") as file:
    text_data = file.read()

file_path = 'data.txt'
__loader__ = TextLoader(file_path)
index = VectorstoreIndexCreator().from_loaders([__loader__])

embeddings = OpenAIEmbeddings()

@app.route('/query', methods=['POST'])
def query_index():
    try:
        data = request.get_json()
        default_query = data['query']
        result = index.query(default_query)
        return jsonify({"query": default_query, "result": result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
