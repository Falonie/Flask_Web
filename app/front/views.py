from io import BytesIO
from flask import Blueprint, views, redirect, url_for, g, session, render_template, make_response, request, abort
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy.sql import func
from utils.captcha import Captcha
from exts import db, alidayu
from .forms import SignupForm, SigninForm, AddPostForm, AddCommentForm
from .models import FrontUser
from ..models import BannerModel, BoardModel, PostModel, Comment, HighlightPost
from .decorators import login_required_
from utils import restful, safeutils
import config

bp = Blueprint('front', __name__)


@bp.route('/')
def index():
    board_id = request.args.get('bd', type=int, default=None)
    # print('board_id: {}'.format(board_id))
    banners = BannerModel.query.filter().limit(4)
    boards = BoardModel.query.filter().all()
    # posts = PostModel.query.filter().all()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    sort = request.args.get('st', type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    total=0
    query_obj = None
    if sort == 1:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 2:
        query_obj = db.session.query(PostModel).outerjoin(HighlightPost).order_by(HighlightPost.create_time.desc(), PostModel.create_time.desc())
    elif sort == 3:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 4:
        query_obj = db.session.query(PostModel).outerjoin(Comment).group_by(PostModel).order_by(
            func.count(Comment.id).desc(), PostModel.create_time.desc())
    if board_id:
        query_obj = query_obj.filter(PostModel.board_id==board_id)
        # posts = PostModel.query.slice(start, end)
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    else:
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    # pagination = Pagination(bs_version=3, page=page, total=PostModel.query.count(), outer_window=0, inner_window=1)
    current_sort=sort
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=1)
    # context = {'pagination': pagination}
    return render_template('front/front_index.html', banners=banners, boards=boards, posts=posts, pagination=pagination,current_sort=current_sort,current_board=board_id)
    # return render_template('front/front_index.html', banners=banners, boards=boards, current_sort=current_sort,posts=PostModel.query.all(),current_board=board_id)
    # return render_template('front/front_test.html')
    # return 'front index'


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('.index'))


@bp.route('/article/<article_id>')
def article(article_id):
    post = PostModel.query.filter_by(id=article_id).first()
    if not post:
        abort(404)
    # comments = Comment.query.filter().all()
    return render_template('front/front_article.html', post=post)
    # return render_template('front/front_article.html', post=post, comments=comments)


# @bp.route('/comments/',methods=['GET','POST'])
# @bp.route('/comments/')
@bp.route('/comments/', methods=['POST'])
@login_required_
def comments():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.comment_content.data
        post_id = form.post_id.data
        # post_id = request.form.get('post_id')
        print(post_id)
        post = PostModel.query.filter_by(id=post_id).first()
        if post:
            comment = Comment(content=content)
            comment.post = post
            comment.front_users = g.front_user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
            # return redirect(url_for('.article',article_id=post_id))
        return restful.params_error(message='没有这个帖子')
    return restful.params_error(message=form.get_error())


@bp.route('/aposts/', methods=['GET', 'POST'])
@login_required_
def apost():
    form = AddPostForm(request.form)
    if form.validate():
        title = form.title.data
        content = form.content.data
        board_id = form.board_id.data
        board = BoardModel.query.filter_by(id=board_id).first()
        if not board:
            return restful.params_error(message='没有这个板块')
        post = PostModel(title=title, content=content)
        post.boards = board
        post.front_users = g.front_user
        db.session.add(post)
        db.session.commit()
        return restful.success()
    # return restful.params_error(message=form.get_error())
    # boards = BoardModel.query.filter().all()
    boards = BoardModel.query.all()
    return render_template('front/front_apost.html', boards=boards)


# @bp.route('/captcha/')
# def graph_captcha():
#     text, image = Captcha.gene_graph_captcha()
#     out = BytesIO()
#     image.save(out, 'png')
#     out.seek(0)
#     resp = make_response(out.read())
#     resp.content_type = 'image/png'
#     return resp


@bp.route('/sms_captcha/')
def sms_captcha():
    result = alidayu.send_sms('18516630543', code='1234')
    if result:
        return '发送成功'
    return '发送失败'


class SignupView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            return render_template('front/front_signup.html', return_to=return_to)
        return render_template('front/front_signup.html')

    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data
            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        print(form.get_error())
        return restful.params_error(message=form.get_error())


class SigninView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and return_to != url_for('front.signup') and safeutils.is_safe_url(
                return_to):
            print(True)
            return render_template('front/front_signin.html', return_to=return_to)
        print(False)
        return render_template('front/front_signin.html')

    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember_me = form.remember.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.verify_password(password=password):
                # if user:
                print(user)
                session[config.FRONT_USER_ID] = user.id
                if remember_me:
                    session.permanent = True
                    return restful.success()
            return restful.params_error(message='手机号码或密码错误')
        return restful.params_error(message=form.get_error())


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
bp.add_url_rule('/signin/', view_func=SigninView.as_view('signin'))
