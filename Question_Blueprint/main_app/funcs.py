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


if __name__ == "__main__":

    def test(question, question_set):
        res = similarity_check(question, question_set)
        print(res)


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

    test(question, question_set)