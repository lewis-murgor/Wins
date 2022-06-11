from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required,current_user
from ..models import User,Win,Comment,UpVote
from .forms import UpdateProfile,WinForm, CommentForm
from .. import db,photos
import markdown2

# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    title = 'Wins'
    wins = Win.get_wins()
    return render_template('index.html',title = title,wins = wins)

@main.route('/win/<int:id>')
def win(id):

    '''
    View wins page function that returns the win details page and its data
    '''
    win = Win.query.get(id)
    title = f'{win.title}'
    comments = Comment.query.filter_by(win_id = id).all()
    return render_template('win.html',title = title,win = win,comments = comments)

@main.route('/win/new/', methods = ['GET','POST'])
@login_required
def new_win():
    '''
    Function that creates new wins
    '''
    form = WinForm()

    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        new_win= Win(title = title, text = text, user = current_user)

        new_win.save_win()
        return redirect(url_for('.index'))
    title = 'Create Win'
    return render_template('new_win.html',title = title, win_form = form)

@main.route('/delete/win/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_win(id):
    win = Win.query.get(id)

    if win is None:
        abort(404)

    db.session.delete(win)
    db.session.commit()
    return redirect (url_for('main.index'))

@main.route('/win/comment/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_comment(id):
    form = CommentForm()
    win = Win.query.get(id)

    if form.validate_on_submit():
        comment = form.comment.data
        new_comment = Comment(win_id=win.id,comment = comment, user = current_user)
        new_comment.save_comment()
        return redirect(url_for('.win',id = win.id ))

    title = f'{win.title} comment'
    return render_template('new_comment.html',title = title, comment_form=form, win = win)

@main.route('/delete/comment/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_comment(id):
    comment =Comment.query.get(id)

    if comment is None:
        abort(404)

    db.session.delete(comment)
    db.session.commit()
    return redirect (url_for('.index'))

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('.profile',uname=uname))

@main.route('/win/upvote/<int:id>', methods = ['GET', 'POST'])
@login_required
def upvote(id):
    win = Win.query.get(id)

    if win is None:
        abort(404)

    upvote = UpVote.query.filter_by(user_id=current_user.id, win_id=id).first()
    if upvote is not None:
        db.session.delete(upvote)
        db.session.commit()
        return redirect(url_for('.index'))
    
    vote = UpVote(user_id=current_user.id, win_id=id)
    db.session.add(vote)
    db.session.commit()

    return redirect(url_for('.index'))

@main.route('/comment/<int:id>')
def single_comment(id):
    comment = Comment.query.get(id)
    if comment is None:
        abort(404)
    format_comment = markdown2.markdown(comment.comment,extras=["code-friendly", "fenced-code-blocks"])
    return render_template('comment.html',comment = comment,format_comment = format_comment)

@main.route('/single/win/<int:id>')
def single_win(id):
    win = Win.query.get(id)
    if win is None:
        abort(404)
    format_win = markdown2.markdown(win.text,extras=["code-friendly", "fenced-code-blocks"])
    return render_template('single_win.html',win = win,format_win=format_win)


