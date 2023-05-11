# Question-Blueprint
[![asciicast](https://asciinema.org/a/GOtFjxHGSPVDe8pyki78WxVd6.svg)](https://asciinema.org/a/GOtFjxHGSPVDe8pyki78WxVd6)
# Team 1 -  Question Blueprint

Question Blueprint is a web application where user can ask, answers question and also have some interactions with them. 

## Table of Contents

- [Question Blueprint](#question-blueprint)
  - [Table of Contents](#table-of-contents)
  - [About the Project](#about-the-project)
    - [Built With](#built-with)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
  - [Roadmap](#roadmap)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)
  - [Acknowledgements](#acknowledgements)

## About the Project

- Question Blueprint is a web-based application that enables users to post questions, answers, and upvote content they find helpful. The app provides a platform for users to seek and share knowledge, while fostering a community that promotes learning and collaboration.

- This app solves the problem of users struggling to find accurate and relevant answers to their questions on various topics. By providing a platform for users to ask questions and receive answers from a community of experts and enthusiasts, the app helps users save time and effort in finding the information they need.

- Question Blueprint is designed for anyone seeking knowledge on various topics, whether it's a student looking for help with homework, a professional seeking advice on a specific topic, or someone simply curious about a subject. It is also suitable for individuals who are knowledgeable in a particular area and want to share their expertise with others.



### Built With

  - [Django](https://www.djangoproject.com/)
  - [Python](https://www.python.org/)
  - [HTML5](https://html.spec.whatwg.org/)
  - [CSS](https://www.w3.org/Style/CSS/)
  - [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
  - [sqlite](https://www.sqlite.org/index.html)

  Some other libraries/technologies:
  - [gensim](https://pypi.org/project/gensim/): Python library for topic modeling and document similarity analysis
  - [gTTS](https://pypi.org/project/gTTS/): Google Text-to-Speech library for Python, allowing you to easily generate speech from text in multiple languages.
  - [Google Authentication](https://developers.google.com/identity): A service provided by Google that allows users to authenticate their identities and access various Google services and APIs securely.
  - [Perspective API](https://www.perspectiveapi.com/): An API provided by Jigsaw, a subsidiary of Google, that uses machine learning models to analyze the content of text and provide feedback on its perceived level of toxicity, aggression, and other traits. The Perspective API can be used to moderate online content and improve online conversations.



## Getting Started

### Prerequisites

List any dependencies or prerequisites required to run the project. Be sure to include version numbers if applicable.

- Python version [3.9](https://www.python.org/downloads/release/python-390/) or higher, but lower than [3.11](https://www.python.org/downloads/release/python-311/)

### Installation

1. Clone the repo

  ```sh
   git clone git@github.com:SJSU-CMPE133-2023-Spring/Question-Blueprint.git
  ```
  OR
  ``` sh
   git clone https://github.com/SJSU-CMPE133-2023-Spring/Question-Blueprint.git
  ```

2. (Optional) Create a virtual environment

  ```sh
    pip install virtualenv
    virtualenv venv
  ```

  ``` sh
    source venv/bin/activate (for Mac & Linux)
  ```

    

  ``` sh
  or
    venv\Scripts\activate (for Window)
  ```

3. Install dependencies

  Navigate to the folder that contains requirements.txt:

  ```sh
    cd Question_Blueprint/Question_Blueprint/
  ```
  
  Install the dependencies:

   ```sh
   pip install -r requirements.txt
   ```
   >**Note**: While running it on mac OS, if there is issue installing gensim, remove the gensim dependency from requirements.txt file and manually intall it using the command: 
   ```sh 
   pip install gensim
   ```

4. Run the application:
  > **Note:** Make sure you are in the folder contains the file called "manage.py"

  ```sh
    python manage.py runserver
  ```

### Usage

  App's Features:
  - Login/Logout/Register
  - User profile
  - Customize user profile
  - Create questions/answers
  - Update and Delete questions
  - Vote for questions/answers
  - Search questions
  - Sort questions/answers by created date or #vote

  Limitations:
   - Speed: Depending on the size and complexity of the project, there may be limitations in terms of how quickly the application can process requests or perform certain tasks. This could be due to factors such as limited processing power, network latency, or the volume of data being processed.

   - API usage: If the project relies on external APIs, there may be limitations in terms of how often requests can be made or how much data can be processed per request. Some APIs may also require authentication or payment to access, which can further impact the project's functionality.

### Roadmap

 1. Implement a user authentication system
 2. Google authentication
 3. Creating UI for user 
 4. User's profile
 5. Create, read, update and delete for question
 6. Answer feature
 7. Vote feature
 8. Search feature
 9. Question recommendation feature
 10. Text to speech feature
 11. Inappropriate Language Checker

### Contributing

  Team 1 Members:
  - Hunter Adam
  - Tan Dao
  - Vivekanand Koya
  - Yohannes Habtemariam
  - Sahiti Hibane

### License

This project is licensed under the MIT License - see the LICENSE file for details.

### Contact

  - Hunter Adam: 
  - Tan Dao: tankhanhdao@gmail.com
  - Vivekanand Koya: 
  - Yohannes Habtemariam:
  - Sahiti Hibane:

### Acknowledgements

We would like to acknowledge the invaluable contributions of Hunter Adam, Tan Dao, Vivekanand Koya, Yohannes Habtemariam, and Sahiti Hibane to this project. Their dedication, expertise, and collaborative spirit have been instrumental in the success of this endeavor.

# Documentation
![UML   Sequence Diagrams1024_4](https://user-images.githubusercontent.com/67130044/231318279-82462275-7cae-4a80-8628-20926ff07fa1.png)
![UML   Sequence Diagrams1024_6](https://user-images.githubusercontent.com/67130044/231318309-93351d7e-9316-404f-987e-8caae1e51ef3.png)
![UML   Sequence Diagrams1024_7](https://user-images.githubusercontent.com/67130044/231318323-572ad1d8-f823-4962-9c65-cf02f9439df5.png)
![UML   Sequence Diagrams1024_8](https://user-images.githubusercontent.com/67130044/231318333-a512d5ec-2650-4417-94cd-d76348feb065.png)
![UML   Sequence Diagrams1024_9](https://user-images.githubusercontent.com/67130044/231318340-2fb7210a-c518-423c-a1b8-d60763fef824.png)
![UML   Sequence Diagrams1024_10](https://user-images.githubusercontent.com/67130044/231318353-4c2ec017-6837-4cbe-8537-58506676bbd7.png)




