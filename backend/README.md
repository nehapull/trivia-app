# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

### Endpoint Library
#### GET '/categories'
Returns a list of all available categories, and a success value.
Sample curl: curl http://localhost:5000/categories
{
 "categories":[
 	"Science",
	"Art",
	"Geography",
	"History",
	"Entertainment",
	"Sports"
  ],

  "success": true
}

#### GET '/questions'
Returns a list of all available questions objects, success value, total number of questions, and a list of all categories.
The results are paginated in groups of 10, and a page can be accessed by including a request argument in the request.
Sample curl: curl http://localhost:5000/questions?page=1
{
    "categories": [
        "Science",
        "Art",
        "Geography",
        "History",
        "Entertainment",
        "Sports"
    ],
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
	{
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
     ],
	"success": true,
    	"total_questions": 18
}

#### DELETE '/questions/{question_id}'
Deletes a question object corresponding to a given question ID if it exists. 
Returns a success value, list of available questions, total number of questions, and list of categories. Results are paginated in groups of 10.
Sample curl: curl -X DELETE http://localhost:5000/questions/5

#### POST '/questions'
Inserts a new question with user-provided question, answer, category, and difficulty. Returns a success value, list of questions, total number of
questions, and a list of categories. Results are paginated in groups of 10.
Sample curl: curl http://localhost:5000/questions?page=2 -X POST -H "Content-Type: application/json" -d '{"question":"How many soccer players should each team have on the field at the start of each match?", "answer":"11", "category":"6", "difficulty": 1}'
{
   "categories": [
   	"Science",
	"Art",
	"Geography",
	"History",
	"Entertainment",
	"Sports"],

   "questions":[
   	{
	  "answer":"11",
	  "category":6,
	  "difficulty":1,
	  "id":36,
	  "question":"How many soccer players should each team have on the field at the start of each match?"
	}
     ],
	  "success":true,
	  "total_questions":19
}

This endpoint is also used to return a list of questions based on a given search term.
Sample curl: curl http://localhost:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}'

#### GET '/categories/{category_id}/questions'
Returns a list of questions that belong to a category corresponding to category ID, if the ID is valid and there are questions available in the category. Also 
returns success value, total number of questions, and a list of categories.
Sample curl: curl http://localhost:5000/categories/2/questions
{
    "categories": [
        "Science",
        "Art",
        "Geography",
        "History",
        "Entertainment",
        "Sports"
    ],
    "questions": [
   	{
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
	{
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "success": true,
    "total_questions": 3
}

#### POST '/quizzes'
Returns a random question given a category and a list of previous questions that have already been used. Also returns a success value.
Sample curl: curl -X POST '/quizzes' -H "Content-Type: application/json" -d '{{"Science": 1}, [] }' 

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
