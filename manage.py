from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from Flask_Web import create_app
from exts import db
from app.cms import models as cms_models
from app.front import models as front_models
from app.models import BannerModel, BoardModel, PostModel

app = create_app()
CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPermission
FrontUser = front_models.FrontUser
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    return '用户添加成功'


@manager.option('-t', '--telephone', dest='telephone')
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_front_user(telephone, username, password):
    user = FrontUser(telephone=telephone, username=username, password=password)
    db.session.add(user)
    db.session.commit()


@manager.command
def create_role():
    guest = CMSRole(name='guest', desc='visit only')
    guest.permissions = CMSPermission.GUEST

    operator = CMSRole(name='operator', desc='modify personal info,comments,posts')
    operator.permissions = CMSPermission.GUEST | CMSPermission.POST | CMSPermission.FRONTUSER | CMSPermission.COMMENTER

    admin = CMSRole(name='admin', desc='all permissions')
    admin.permissions = CMSPermission.GUEST | CMSPermission.POST | CMSPermission.CMSUSER | CMSPermission.COMMENTER | CMSPermission.FRONTUSER | CMSPermission.BOADRER

    developer = CMSRole(name='developer', desc='developer permissions only')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([guest, operator, admin, developer])
    db.session.commit()


@manager.option('-e', '--email', dest='email')
@manager.option('-n', '--name', dest='name')
def add_user_to_role(email, name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            # print('successfully added users!')
            return 'successfully added users!'
        # print('role {} not exists.'.format(role))
        return 'role {} not exists.'.format(role)
    # print('email {} not exists.'.format(email))
    return 'email {} not exists.'.format(email)


@manager.command
def test_permission():
    user = CMSUser.query.first()
    if user.has_permission(CMSPermission.GUEST):
        # print('you has guest permissions!')
        return 'you has guest permissions!'
    # print('...')
    return '...'


@manager.command
def create_posts():
    for _ in range(1, 10):
        title = 'Flask2{!s}'.format(_)
        content = 'Flask2Content {!s}'.format(_)
        board_id = BoardModel.query.filter(BoardModel.name == 'flask').first()
        author = FrontUser.query.filter(FrontUser.username == 'Johncy').first()
        post = PostModel(title=title, content=content)
        post.boards = board_id
        post.front_users = author
        db.session.add(post)
        db.session.commit()
    print('Success!')


def make_shell_context():
    return dict(app=app, db=db, CMSUser=CMSUser)


manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
