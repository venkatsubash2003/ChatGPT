from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
import os
import openai


openai.api_key = "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"








app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://venkatsubash2003:srinivas123@chatgpt.urwaxot.mongodb.net/chatgpt"
mongo = PyMongo(app)

@app.route('/')
def home():
    chats = mongo.db.chats.find({})
    mychats = [chat for chat in chats]
    print(mychats)
    return render_template("index.html", mychats = mychats)


data = {"result": "Hey I am Chat GPT I can do many things."}


@app.route('/api', methods=["POST", "GET"])
def qa():
    if request.method == "POST":
        print(request.json)
        question = request.json.get("question")
        chat = mongo.db.chats.find_one({"question":question})
        print(chat)
        if chat:
            data = {"question":question,"answer":f"{chat['answer']}"}
            return jsonify(data)
        else:
            
            response = openai.Completion.create(
            model="text-davinci-003",
            prompt=question,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
            print(response)
            data = {"question":question, "answer":response["choices"][0]["text"]}
            mongo.db.chats.insert_one({"question":question,"answer":response["choices"][0]["text"]})
            return jsonify(data)
            
        
    


app.run(debug=True)
