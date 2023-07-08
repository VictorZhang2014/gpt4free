# encoding: utf-8
import json
from g4f import ChatCompletion, Provider, Model
from flask import Flask, request, Response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


@app.route("/", methods=['GET'])
def index():  
    return "Hello I am ChatGPT for FREE."


@app.route("/chat/completions", methods=['OPTIONS', 'POST'])
@cross_origin(origins='*')
def chat_completions():    
    req_param = json.loads(request.data) 
    streaming = True if req_param.get('streaming') == 'true' else False
    model = req_param.get('model')
    messages = req_param.get('messages')   
    
    if not streaming: 
        return ChatCompletion.create(model=model, provider=Provider.DeepAi, messages=messages) 
    else:
        response = ChatCompletion.create(model=model, messages=messages, stream=True)
        def stream():  
            for token in response: 
                yield 'data: {}\n\n'.format(token) 
        return app.response_class(stream(), mimetype='text/event-stream')


if __name__ == '__main__':
    config = {
        'host': '0.0.0.0',
        'port': 9011,
        'debug': False
    } 
    app.run(**config) 


# Run with gunicorn 
# gunicorn entry:app --bind 0.0.0.0:9011 --daemon

# lsof -i :9011 

