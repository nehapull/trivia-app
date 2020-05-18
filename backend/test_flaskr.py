import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for
    expected errors.
    """

    def test_retrieve_all_categories(self):
        """Test get request for listing out all categories"""

        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_404_cannot_retrieve_categories(self):
        """Test 404 error for get request to page that does not exist"""

        res = self.client().get('/categories?page=500')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'request not found')

    def test_retrieve_questions_list(self):
        """Test get request for listing out all questions"""

        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), QUESTIONS_PER_PAGE)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_404_cannot_get_questions(self):
        """Test 404 error for get request to page that does not exist"""

        res = self.client().get('/questions?page=10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'request not found')

    """
    def test_delete_question(self):
        Test deleting a question from questions list
        res = self.client().delete('/questions/11')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(Question.query.filter(Question.id == 3))
        self.assertEqual(data['total_questions'])
        self.assertTrue(len(data['categories']))
    """

    def test_404_cannot_delete_question(self):
        """Test 404 error for an invalid question ID for deleting
           question"""

        res = self.client().delete('/questions/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'request not found')

    def test_post_a_question(self):
        """Test posting a new question"""

        res = self.client().post(
            '/questions',
            json={
                'question':
                'In what year was the first ever Wimbledon Championship held?',
                'answer': 1877,
                'difficulty': 3,
                'category': 6})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_422_cannot_post_question(self):
        """Test 422 error for post request with no request data"""

        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'cannot process request')

    def test_search_question_by_substring_with_results(self):
        """Test retrieving questions using a search term which should give back
        results"""

        res = self.client().post('/questions', json={'searchTerm': 'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_search_question_by_substring_without_results(self):
        """Test retrieving questions using a search term with no results"""

        res = self.client().post('/questions', json={'searchTerm': 'blah'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)
        self.assertTrue(len(data['categories']))

    def test_retrieve_questions_by_category(self):
        """Test retreiving questions based on category selected"""

        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        questions = Question.query.filter(Question.category == 2)
        formatted_questions = [question.format() for question in questions]
        total_questions = len(formatted_questions)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['total_questions'], total_questions)
        self.assertTrue(len(data['categories']))

    def test_404_cannot_retrieve_questions_by_category(self):
        """Test 404 error for a category ID that does not exist"""

        res = self.client().get('/categories/10/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'request not found')

    def test_play_quiz(self):
        """Test playing quiz given category and prev questions"""

        res = self.client().post(
            '/quizzes',
            json={
                'quiz_category': {
                    'type': 'Science',
                    'id': 1},
                'previous_questions': []})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_bad_parameters_for_quiz(self):
        """Test 422 error for wrong parameters for playing quiz"""

        res = self.client().post('/quizzes',
                                 json={
                                     'quiz_category': {
                                         'type': 'Blah',
                                         'Science': 100},
                                     'previous_questions': {}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'cannot process request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
