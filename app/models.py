from datetime import datetime
from exts import db


class BannerModel(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Banner {}>'.format(self.name)


class BoardModel(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    posts = db.relationship('PostModel', backref='boards')

    def __repr__(self):
        return '<Board {}>'.format(self.name)


class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    # boards = db.relationship('BoardModel', backref='posts')
    author_id = db.Column(db.String(100), db.ForeignKey('front_user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post')
    # highlight_post = db.relationship('HighlightPost', bakcref='post')

    def __repr__(self):
        return '<PostTitle {}>'.format(self.title)


class HighlightPost(db.Model):
    __tablename__ = 'highlight_post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    posts = db.relationship('PostModel', backref='highlight_post')

    def __repr__(self):
        return '<HighlightPost {}>'.format(self.id)


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    author_id = db.Column(db.String(100), db.ForeignKey('front_user.id'), nullable=False)

    def __repr__(self):
        return '<CommentContent {}>'.format(self.content)
