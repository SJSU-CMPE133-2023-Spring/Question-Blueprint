# Import necessary modules
from sentence_transformers import SentenceTransformer, util

# Data Preprocessing    
def preprocess_questions(questions):
    preprocessed_questions = []
    for question in questions:
        preprocessed_question = {}
        preprocessed_question['id'] = question.id
        preprocessed_question['title'] = question.title
        preprocessed_question['content'] = question.content
        preprocessed_questions.append(preprocessed_question)
    return preprocessed_questions


# Define function to compute similarity scores between input question and set of questions
def similarity_check(question, question_set):
    # Load pre-trained model for embedding sentences
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    
    # Embed the input question using the pre-trained model
    question_embeddings = model.encode([question['title'] + ' ' + question['content']])
    
    # Embed the set of questions using the pre-trained model
    question_set_embeddings = model.encode([q['title'] + ' ' + q['content'] for q in question_set])
    
    # Compute cosine similarity scores between the input question and the set of questions
    scores = util.cos_sim(question_embeddings, question_set_embeddings)
    
    # Convert scores to list of tuples (index, score)
    results = [(i, round(float(scores[0][i].item()), 4)) for i in range(len(scores[0]))]
    
    # Sort results by descending score and return the sorted list of tuples
    return sorted(results, key=lambda x: x[1], reverse=True)



# ===========================================================

""" 
In addition to "TOXICITY", the Perspective API of Google also provides analysis for the following perspectives:

"SEVERE_TOXICITY": This represents the model's score of the input text's likelihood of being considered severely toxic or inflammatory.

"IDENTITY_ATTACK": This represents the model's score of the input text's likelihood of being an attack on the perceived identity of a group.

"INSULT": This represents the model's score of the input text's likelihood of being considered an insult.

"PROFANITY": This represents the model's score of the input text's likelihood of containing profanity.

"THREAT": This represents the model's score of the input text's likelihood of containing a threat.

"SEXUALLY_EXPLICIT": This represents the model's score of the input text's likelihood of containing sexually explicit material.

"FLIRTATION": This represents the model's score of the input text's likelihood of containing flirtatious material.

Each perspective has its own score, which ranges from 0 to 1, where 0 indicates a low likelihood of the input text containing the perspective and 1 indicates a high likelihood. """


API_KEY = 'AIzaSyAAU4tA9zRdw1Mi7aN2YPnQfOWtcJQa3AY'
from googleapiclient.discovery import build
import json


def perspective(text):
    client = build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=API_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        'comment': { 'text': text },
        'requestedAttributes': {'TOXICITY': {}, 
                                'SEVERE_TOXICITY': {},
                                'IDENTITY_ATTACK': {},
                                'INSULT': {},
                                'PROFANITY': {},
                                'THREAT': {},
                                'SEXUALLY_EXPLICIT': {},
                                'FLIRTATION': {},}
    }
    fields = ["TOXICITY", "SEVERE_TOXICITY", "IDENTITY_ATTACK", "INSULT", "PROFANITY", "THREAT", "SEXUALLY_EXPLICIT", "FLIRTATION"]
    res = {}

    response = client.comments().analyze(body=analyze_request).execute()
    
    for field in fields:
        res[field] = response['attributeScores'][field]['summaryScore']['value']
    return dict(sorted(res.items(), key=lambda item: item[1], reverse=True)) 





# ===================================================================
if __name__ == "__main__":

    question = {"title": "How to learn Python", "content": "I want to learn Python. What resources can you recommend?"}

    question_set = [
        {"id": 0, "title": "Best resources for learning Python", "content": "What are some good online resources for learning Python?"},
        {"id": 1, "title": "Learning Python for beginners", "content": "What's the best way to get started with Python for someone who has never programmed before?"},
        {"id": 2, "title": "Python tutorials for beginners", "content": "Can anyone recommend some good Python tutorials for someone who is just starting out?"},
        {"id": 3, "title": "Python programming books", "content": "What are some good books for learning Python programming?"},
        {"id": 4, "title": "Python coding challenges", "content": "What are some good coding challenges for practicing Python programming?"},
        {"id": 5, "title": "Python web development", "content": "How do I get started with web development using Python?"},
        {"id": 6, "title": "Python data science resources", "content": "Can anyone recommend some good resources for learning data science with Python?"},
        {"id": 7, "title": "Python for machine learning", "content": "What's the best way to learn Python for machine learning?"},
        {"id": 8, "title": "Python projects for beginners", "content": "Can anyone suggest some simple Python projects for beginners to practice with?"}
    ]

    # test for question similarity
    print(similarity_check(question, question_set))

    # test for perspective API
    print(perspective('your mother fucker'))




