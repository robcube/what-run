from flask import Flask, request, jsonify
import openai
import os
import numpy as np

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Example dictionary
dictionary = {
    'politics': 'The activities associated with the governance of a country or area.',
    'exercise': 'Activity requiring physical effort, carried out to sustain or improve health and fitness.',
    'office': 'A room, set of rooms, or building used as a place for commercial, professional, or bureaucratic work. This is not in reference to politics nor campaigning.',
    'nose': 'When you are referring to liquids coming out of your nose or bodily orficies.',
    'engine': 'This is in reference to an engine or a motor of a car, truck, or any other moving vehicles.',
    'overflow': 'When water or any other liquids cannot be contained, this happens.',
    'unknown': 'If you do not know the answer, use this.',
}

@app.route('/ask_context', methods=['POST'])
def ask_context():
    data = request.json
    sentence = data.get('sentence', '')
    
    if 'run' in sentence:
        context_response = get_context(sentence)
        relevant_entries, top_entry = query_dictionary(context_response)
        made_up_url = generate_url(top_entry)
        return jsonify({'context': context_response, 'relevant_entries': relevant_entries, 'url': made_up_url}) 
    else:
        return jsonify({'context': 'The word "run" is not in the sentence.'})

def get_context(sentence):
    prompt = f"Explain the context of the word 'run' in this sentence: '{sentence}'"
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=500
    )
    return response.choices[0].text.strip()

def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        engine="text-embedding-3-small"  # Choose the appropriate model
    )
    return response['data'][0]['embedding']

def query_dictionary(context):
    context_embedding = get_embedding(context)
    similarities = []

    for word, definition in dictionary.items():
        word_embedding = get_embedding(definition)
        similarity = np.dot(context_embedding, word_embedding) / (np.linalg.norm(context_embedding) * np.linalg.norm(word_embedding))
        similarities.append((word, similarity))

    # Sort entries by similarity in descending order
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    top_entry = similarities[0][0]

    # Return top N relevant entries
    top_n = 1
    relevant_entries = {word: dictionary[word] for word, _ in similarities[:top_n]}
    return relevant_entries, top_entry

def generate_url(entry):
    base_url = "https://robcube.github.io/assets/"
    return base_url + entry.replace(' ', '_') + ".mp4"

if __name__ == '__main__':
    app.run(port=5001, debug=True)
