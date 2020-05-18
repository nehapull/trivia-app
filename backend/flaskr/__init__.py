import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
TOTAL_CATEGORIES = 6


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  Set up CORS. Allow '*' for origins. Delete the sample route after completing
  the TODOs
  '''
    CORS(app)
    '''
  Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS')

        return response

    '''
  Paginate questions
  '''
    def paginate_questions(request, questions):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        paginated_questions = questions[start:end]

        return paginated_questions

    '''
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories', methods=['GET'])
    def retrieve_categories():

        # Check if request arguments are passed in the URL
        if request.args:
            abort(404)

        try:
            categories = Category.query.all()
            formatted_categories = [category.format()['type']
                                    for category in categories]

            return jsonify({
                'success': True,
                'categories': formatted_categories
            })

        except BaseException:
            abort(404)

    '''
  Create an endpoint to handle GET requests for questions, including pagination
  (every 10 questions).  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application you should see questions
  and categories generated, ten questions per page and pagination at the bottom
  of the screen for three pages.  Clicking on the page numbers should update
  the questions.
  '''
    @app.route('/questions', methods=['GET'])
    def show_questions_paginated():

        try:
            questions = Question.query.order_by(Question.id).all()

            formatted_questions = [question.format() for question in questions]
            paginated_questions = paginate_questions(
                request, formatted_questions)
            categories = Category.query.all()
            formatted_categories = [category.format()['type']
                                    for category in categories]

            if len(paginated_questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': paginated_questions,
                'total_questions': len(formatted_questions),
                'current_category': None,
                'categories': formatted_categories
            })

        except BaseException:
            abort(404)

    '''
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be
  removed.  This removal will persist in the database and when you refresh the
  page.
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            questions = Question.query.order_by(Question.id).all()

            if len(questions) == 0:
                abort(404)

            formatted_questions = [question.format() for question in questions]
            paginated_questions = paginate_questions(
                request, formatted_questions)
            categories = Category.query.all()
            formatted_categories = [category.format()['type']
                                    for category in categories]

            return jsonify({
                'success': True,
                'questions': paginated_questions,
                'total_questions': len(formatted_questions),
                'current_category': None,
                'categories': formatted_categories
            })

        except BaseException:
            abort(404)

    '''
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.

  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    @app.route('/questions', methods=['POST'])
    def add_new_question():

        body = request.get_json()

        if body is None:
            abort(422)

        new_question = body.get('question')
        new_answer = body.get('answer')
        new_category = body.get('category')
        new_difficulty = body.get('difficulty')
        search_term = body.get('searchTerm')

        try:
            if search_term:
                questions = Question.query.order_by(Question.id).filter(
                    Question.question.ilike('%{}%'.format(search_term)))
                formatted_questions = [question.format()
                                       for question in questions]
                paginated_questions = paginate_questions(
                    request, formatted_questions)
                categories = Category.query.all()
                formatted_categories = [
                    category.format()['type'] for category in categories]

                return jsonify({
                    'success': True,
                    'questions': paginated_questions,
                    'total_questions': len(formatted_questions),
                    'current_category': None,
                    'categories': formatted_categories
                })

            else:
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    category=new_category,
                    difficulty=new_difficulty)
                question.insert()
                questions = Question.query.order_by(Question.id).all()
                formatted_questions = [question.format()
                                       for question in questions]
                paginated_questions = paginate_questions(
                    request, formatted_questions)
                categories = Category.query.all()
                formatted_categories = [
                    category.format()['type'] for category in categories]

                return jsonify({
                    'success': True,
                    'questions': paginated_questions,
                    'total_questions': len(formatted_questions),
                    'current_category': None,
                    'categories': formatted_categories
                })

        except BaseException:
            abort(422)

    '''
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def retrieve_questions_filteredBy_category(category_id):
        try:
            if category_id > TOTAL_CATEGORIES:
                abort(404)

            questions = Question.query.order_by(
                Question.id).filter(
                Question.category == category_id)
            formatted_questions = [question.format() for question in questions]
            paginated_questions = paginate_questions(
                request, formatted_questions)
            categories = Category.query.all()
            formatted_categories = [category.format()['type']
                                    for category in categories]

            return jsonify({
                'success': True,
                'questions': paginated_questions,
                'total_questions': len(formatted_questions),
                'current_category': None,
                'categories': formatted_categories
            })

        except BaseException:
            abort(404)

    '''
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random question within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
    @app.route('/quizzes', methods=['POST'])
    def retrieve_questions_for_quiz():
        body = request.get_json()

        if body:
            quiz_category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')

        else:
            abort(422)

        try:
            # Get questions from the given quiz category
            current_questions = None
            if quiz_category['id'] == 0:
                current_questions = Question.query.all()
            else:
                current_questions = Question.query.filter(
                    Question.category == quiz_category['id']).all()

            current_questions = [question.format() for question in
                                 current_questions if question.id not in
                                 previous_questions]

            random_question = None
            if len(current_questions) == 0:
                random_question = None
            # Get random question from those available
            else:
                random_question = random.choice(current_questions)

            return jsonify({
                'success': True,
                'question': random_question
            })

        except BaseException:
            abort(422)

    '''
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'request not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'cannot process request'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request, try again'
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500
    return app
