import os
import azure.cognitiveservices.speech as speechsdk
import openai

chatlist = []
def generate_response(entre):
    """
    Fonction qui génère une réponse à partir d'une requête
    """
    
    global chatlist 
    conv = "\n".join(chatlist)
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt= f"quand je dis {entre}, tu tiens compte de {conv}",
        temperature=0.3,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    chatlist.append(response.choices[0].text.strip())

    return response.choices[0].text.strip()



def keys():
    """Cette fonction enregistre les clés pour les réutiliser."""
    # Set up the OpenAI API key
    openai.api_key = "CLE_OPENAI"

    # Set up the Speech SDK config
    speech_config = speechsdk.SpeechConfig(subscription="CLE_AZURE", region="REGION")
    speech_config.speech_recognition_language = "fr-FR" # or your preferred language
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"

    return speech_config, openai.api_key

def speech_reconizer(speech_config):
    # Set up the audio input source
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    phrase_list_grammar = speechsdk.PhraseListGrammar.from_recognizer(speech_recognizer)
    phrase_list_grammar.addPhrase("Sophana")
    phrase_list_grammar.addPhrase("Simplonien")
    phrase_list_grammar.addPhrase("Simplonienne")

    print("Speak into your microphone.")

    # Start the speech recognizer and transcribe the audio input
    result = speech_recognizer.recognize_once_async().get()

    return result, audio_config

def write_words(result):
    # pour écrire ma dictée
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")


def write_answer(result):
    # génération de la réponse 
    answer = generate_response(result.text)
    print(answer)

    return answer

def reponse_vocale(answer, speech_config, audio_config):
    # synthèse vocale 
    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name='fr-FR-DeniseNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    # Synthétiser la réponse à voix haute
    return speech_synthesizer.speak_text_async(answer).get()



# speech_config, openai.api_key = keys()fl
# result, audio_config = speech_reconizer(speech_config)
# write_words(result)
# answer = write_answer(result)
# final = reponse_vocale(answer, speech_config, audio_config)

# final 
    