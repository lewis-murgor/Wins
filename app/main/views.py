from flask import render_template
from . import main

# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    title = 'Wins'
    return render_template('index.html',title = title)

@main.route('/win/<int:id>')
def win(id):

    '''
    View wins page function that returns the win details page and its data
    '''
    return render_template('win.html',id = id)