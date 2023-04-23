

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



