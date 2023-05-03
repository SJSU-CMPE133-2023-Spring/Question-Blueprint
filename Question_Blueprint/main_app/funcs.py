# Import necessary modules
from nltk.tokenize import word_tokenize
from gensim import corpora, models, similarities

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
    # Create a list of all questions
    questions =  [q['title'] + ' ' + q['content'] for q in question_set]
    
    # Tokenize the questions
    tokenized_questions = [word_tokenize(question.lower()) for question in questions]
    
    # Create a dictionary and bag of words representation for the questions
    dictionary = corpora.Dictionary(tokenized_questions)
    corpus = [dictionary.doc2bow(tokenized_question) for tokenized_question in tokenized_questions]
    
    # Create a similarity index using the bag of words representation
    similarity_index = similarities.SparseMatrixSimilarity(corpus, num_features=len(dictionary))
    
    # Compute similarity scores between the input question and the set of questions
    query_bow = dictionary.doc2bow(word_tokenize((question.title + ' ' + question.content).lower()))
    scores = similarity_index[query_bow]
    
    # Convert scores to list of tuples (index, score)
    results = [(question_set[i]['id'], round(float(score), 4)) for i, score in enumerate(scores)]
    
    res = None

    print(len(sorted(results, key=lambda x: x[1], reverse=True)))
    # Sort results by descending score and return the sorted list of tuples
    if len(sorted(results, key=lambda x: x[1], reverse=True)) > 0 :
        res = sorted(results, key=lambda x: x[1], reverse=True)[0]
        print(res)
    return res



if __name__ == '__main__':
    # Define a list of example questions
    questions = [
        {'id': 1, 'title': 'What is Python?', 'content': 'Python is a popular programming language.'},
        {'id': 2, 'title': 'What are the benefits of using Python?', 'content': 'Python is easy to learn, has a large community, and is highly versatile.'},
        {'id': 3, 'title': 'What is machine learning?', 'content': 'Machine learning is a subset of artificial intelligence that involves training algorithms to make predictions based on data.'},
        {'id': 4, 'title': 'What is deep learning?', 'content': 'Deep learning is a subset of machine learning that involves training neural networks to make predictions based on large datasets.'},
        {'id': 5, 'title': 'What is natural language processing?', 'content': 'Natural language processing is a field of study that involves developing algorithms to understand and generate human language.'}
    ]

    # Preprocess the questions
    preprocessed_questions = preprocess_questions(questions)

    # Test the similarity_check function
    input_question = {'id': 6, 'title': 'What is Python used for?', 'content': 'I am interested in learning Python and want to know more about its applications.'}
    results = similarity_check(input_question, preprocessed_questions)

    # Print the results
    print('Input Question:', input_question['title'], input_question['content'])
    print(results)
    for result in results:
        question = questions[result[0]-1]
        print('Question ID:', question['id'], 'Title:', question['title'], 'Content:', question['content'], 'Similarity Score:', result[1])
