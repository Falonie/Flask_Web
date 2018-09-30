import string, random
from flask import Blueprint, views, render_template, request, redirect, url_for, session, g, jsonify
from flask_mail import Message
from .forms import LoginForm, ResetpwdForm, ResetEmailForm, AddBannerForm, UpdateBannerForm, AddBoardForm, \
    UpdateBoardForm
from .models import CMSUser, CMSPermission
from ..models import BannerModel, BoardModel, PostModel, HighlightPost
from .decorators import login_required_, permission_required
from exts import db, mail
from utils import restful, zlcache
from tasks import send_mail
import config

bp = Blueprint('cms', __name__, url_prefix='/cms')


@bp.route('/')
@login_required_
def index():
    return render_template('cms/cms_index.html')


@bp.route('/logout/')
def logout():
    # session.clear()
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


@bp.route('/profile/')
@login_required_
def profile():
    return render_template('cms/cms_profile.html')


@bp.route('/email_captcha/')
def email_captcha():
    email = request.args.get('email')
    if not email:
        return '请传递邮箱参数'
    source = list(string.ascii_letters)
    source.extend(str(_) for _ in range(0, 10))
    captcha = ''.join(random.sample(source, 6))
    # message = Message(subject='Python', recipients=[email], body='验证码：{}'.format(captcha))
    # try:
    #     mail.send(message)
    # except:
    #     return restful.server_error()
    send_mail.delay('Python', [email], '验证码：{}'.format(captcha))
    zlcache.set(email, captcha)
    return restful.success()


@bp.route('/email/')
def send_email():
    # message = Message(subject='this is first mail.', recipients=['541002901@qq.com'], body='this is content.')
    message = Message(subject='this is first mail.', recipients=['541002901@qq.com'], body='this is content.')
    mail.send(message)
    return 'success.'


@bp.route('/posts/')
@permission_required(CMSPermission.POST)
@login_required_
def posts():
    post_list = PostModel.query.filter_by().all()
    return render_template('cms/cms_posts.html', post_list=post_list)


@bp.route('/highlightposts/', methods=['POST'])
@permission_required(CMSPermission.POST)
@login_required_
def hpost():
    post_id = request.form.get('post_id')
    if post_id:
        post = PostModel.query.filter_by(id=post_id).first()
        if post:
            highlightpost = HighlightPost()
            highlightpost.posts = post
            db.session.add(highlightpost)
            db.session.commit()
            return restful.success()
        return restful.params_error(message='没有这个帖子')
    return restful.params_error(message='请输入帖子id')


@bp.route('/unhighlightposts/', methods=['POST'])
@permission_required(CMSPermission.POST)
@login_required_
def upost():
    post_id = request.form.get('post_id')
    if post_id:
        post = PostModel.query.filter_by(id=post_id).first()
        if post:
            # highlightpost = post.highlight_post
            highlightpost = HighlightPost.query.filter_by(post_id=post_id).first()
            highlightpost.posts = post
            db.session.delete(highlightpost)
            db.session.commit()
            return restful.success()
        return restful.params_error(message='没有这个帖子')
    return restful.params_error(message='请输入帖子id')


@bp.route('/comments/')
@login_required_
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')


@bp.route('/boards/')
@login_required_
@permission_required(CMSPermission.BOADRER)
def boards():
    board = BoardModel.query.filter().all()
    return render_template('cms/cms_boards.html', board=board)


@bp.route('/aboard/')
@login_required_
@permission_required(CMSPermission.BOADRER)
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    return restful.params_error(message=form.get_error())


@bp.route('/uboard/')
@login_required_
@permission_required(CMSPermission.BOADRER)
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.filter_by(board_id=board_id).first()
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        return restful.params_error(message='没有这个板块')
    return restful.params_error(message=form.get_error())


@bp.route('/dboard/')
@login_required_
@permission_required(CMSPermission.BOADRER)
def dboard():
    board_id = request.form.get('board_id')
    if not board_id:
        return restful.params_error(message='请传入板块id')
    board = BoardModel.query.filter_by(board_id=board_id).first()
    if not board_id:
        return restful.params_error(message='没有这个板块')
    db.session.delete(board_id)
    db.session.commit()
    return restful.success()


@bp.route('/fusers/')
@login_required_
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    return render_template('cms/cms_frontusers.html')


@bp.route('/cusers/')
@login_required_
@permission_required(CMSPermission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')


@bp.route('/croles/')
@login_required_
@permission_required(CMSPermission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_croles.html')


@bp.route('/banners/')
@login_required_
def banners():
    banners = BannerModel.query.filter_by().all()
    # banners = BannerModel.query.all()
    return render_template('cms/cms_banners.html', banners=banners)


# @bp.route('/abanner/', methods=['GET', 'POST'])
@bp.route('/abanner/', methods=['POST'])
@login_required_
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        print(banner)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    return restful.params_error(message=form.get_error())


@bp.route('/upbanner/', methods=['POST'])
@login_required_
def update_banner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        return restful.params_error(message='没有这个轮播图')
    return restful.params_error(message=form.get_error())


@bp.route('/dbanner/', methods=['POST'])
@login_required_
def delete_banner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message='请传入轮播图id')
    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.params_error(message='没有这个轮播图')
    db.session.delete(banner)
    db.session.commit()
    return restful.success()


class LoginViews(views.MethodView):
    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            print(user)
            if user and user.verify_password(password):
                # if user:
                # session['user_id'] = user.id
                session[config.CMS_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return redirect(url_for('.index'))
            return self.get('email or password incorrect')
        print(form.errors)
        # print(form.errors.popitem())
        # return self.get('表单验证错误')
        # return self.get(form.errors.popitem()[1][0])
        message = form.errors.get('password')[0]
        return self.get(form.errors.get('password')[0])


class ResetPwd(views.MethodView):
    decorators = [login_required_]

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            print('....')
            if user.verify_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # return jsonify({"code": 200, "message": ""})
                print('密码修改成功！')
                return restful.success()
            # return jsonify({"code": 400, "message": "旧密码错误!"})
            return restful.params_error('旧密码错误')
        message = form.get_error()
        # return jsonify({"code": 400, "message": message})
        return restful.params_error(message)


class ResetEmailView(views.MethodView):
    decorators = [login_required_]

    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            print('邮箱修改成功！')
            return restful.success()
        print(form.errors)
        return restful.params_error(form.get_error())


bp.add_url_rule('/login/', view_func=LoginViews.as_view('login'))

bp.add_url_rule('/resetpwd/', view_func=ResetPwd.as_view('resetpwd'))

bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
