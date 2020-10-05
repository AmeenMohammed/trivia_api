import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, all_questions):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in all_questions]

  return questions[start:end]

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)

  setup_db(app)
  CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                          'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                          'GET,PUT,POST,DELETE,OPTIONS')
    return response

  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()

    if len(categories) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'categories': {category.id: category.type for category in categories}
    })


  @app.route('/questions')
  def get_questions():
    questions = Question.query.all()
    current_questions = paginate_questions(request, questions)

    categories = Category.query.all()

    if len(current_questions) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(questions),
        'categories': {category.id: category.type for category in categories},
        'current_category': None
    })

  @app.route("/questions/<question_id>", methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)
      question.delete()
      return jsonify({
          'success': True,
          'deleted': question_id
      })
    except:
      abort(422)

      
  @app.route("/questions", methods=['POST'])
  def new_question():
    data = request.get_json()
    
    question = data['question']
    answer = data['answer']
    difficulty = data['difficulty']
    category = data['category']
    
    if (question == "" or answer == "" or difficulty == "" or category == ""):
      abort(404)

    try:
      question = Question(question=question, answer=answer,
                          difficulty=difficulty, category=category)
      question.insert()

      return jsonify({
          'success': True,
          'created': question.id,
      })

    except:
      abort(422)


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    