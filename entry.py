# encoding: utf-8
import json
from g4f import ChatCompletion 
from flask import Flask, request, Response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


@app.route("/", methods=['GET'])
def index():  
    return "Hello I am g4f"

@app.route("/chat/completions", methods=['OPTIONS', 'POST'])
@cross_origin(origins='*')
def chat_completions():   
    req_param = json.loads(request.data)
    streaming = True
    model = req_param.get('model')
    messages = req_param.get('messages')  

    response = ChatCompletion.create(model=model, messages=messages, stream=True)
    
    if not streaming:
        while 'curl_cffi.requests.errors.RequestsError' in response:
            response = ChatCompletion.create(model=model, stream=streaming,
                                             messages=messages)
        return "data: finish_reason=stop\n\n"

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