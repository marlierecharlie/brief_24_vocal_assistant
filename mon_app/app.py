import azure.cognitiveservices.speech as speechsdk
import openai
from flask import Flask, render_template, request, jsonify
from speech_recognition import *
import os

app = Flask(__name__)

speech_config, openai.api_key = keys()


@app.route("/")
def ecris_la_reponse():
    result, audio_config = speech_reconizer(speech_config)
    write_words(result)
    answer = write_answer(result)
    final = reponse_vocale(answer, speech_config, audio_config)
    final
    return render_template("index.html", answer=answer, result=result)

 
if __name__ == '__main__':
    app.run(debug=True)


