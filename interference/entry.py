# encoding: utf-8
import json
from g4f import Model, ChatCompletion, Provider
from flask import Flask, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/chat/completions", methods=['POST'])
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

