import click
import flask
from flask.cli import with_appcontext
from sqlalchemy import Table, Integer, Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from checkcaptcha import db

image_captcha = Table(
    'captcha_image', 
    db.Model.metadata,
    Column('image_id', ForeignKey('image.id_image'), primary_key=True),
    Column('captcha_id', ForeignKey('image_captcha.id_captcha'), primary_key=True),
    # Column('order', Integer, nullable=True),
    # Column('correct', Boolean, nullable=True)
    # extend_existing=True
    )

class ImageCaptcha(db.Model):
    id_captcha = Column(Integer, primary_key=True)
    captcha_hash = Column(String(255), unique=True, nullable=False)
    # answer = Column(String(255), nullable=False)
    target_label_id = Column(Integer, ForeignKey('label.id_label'), nullable=False)
    user_hash = Column(String(255), nullable=True)

    images = relationship(
        'Image',
        secondary=image_captcha,
        back_populates='captchas'
    )
    label = relationship(
        'Label'
    )

    def is_correct(self, answer):
        try:
            ans = set([int(x) for x in answer])
        except ValueError as err:
            print('invalid conversion', err)
            return False
        img_ids = set([im.id_image for im in self.images])
        
        # does answer contain additional (incorrect) images?
        if ans.difference(img_ids):
            print('additional answer', ans, img_ids)
            return False
        
        # any images missing?
        for im in self.images:
            labels_id = [label.id_label for label in im.labels]
            if self.target_label_id in labels_id and im.id_image not in ans:
                print('missing answer')
                return False
        
        return True

image_label = Table(
    'image_label', 
    db.Model.metadata,
    Column('image_id', ForeignKey('image.id_image'), primary_key=True),
    Column('label_id', ForeignKey('label.id_label'), primary_key=True),
    )


class Label(db.Model):
    id_label = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    images = relationship(
        'Image',
        secondary=image_label,
        back_populates='labels'
    )

    def __init__(self, name):
        self.name = name


class Image(db.Model):
    id_image = Column(Integer, primary_key=True)
    path = Column(String(255), nullable=False)

    labels = relationship(
        'Label',
        secondary=image_label,
        back_populates='images',
        # lazy='dynamic'
    )
    captchas = relationship(
        'ImageCaptcha',
        secondary=image_captcha,
        back_populates='images'
    )

    def __init__(self, path):
        self.path = path


@click.command("init-db")
@click.option('--debug/--no-debug', default=False)
@with_appcontext
def init_db_command(debug):
    """Clear existing data and create new tables."""
    original_config = flask.current_app.config['SQLALCHEMY_ECHO']
    if debug:
        flask.current_app.config['SQLALCHEMY_ECHO'] = True

    db.drop_all()
    db.create_all()

    import os

    imgs_root = os.path.join(flask.current_app.static_folder, 'images')
    if not os.path.exists(imgs_root):
        click.echo('Couldn\'t find root directory for images: {}'.format(imgs_root))
        return

    with os.scandir(imgs_root) as it:
        for category in it:
            if category.name == 'categories.txt':
                continue
            if not category.is_dir():
                click.echo('Unexpected file {}'.format(category))
                continue

            label = Label(category.name)
            for img_path in os.listdir(category.path):
                im = Image(path='{}/{}'.format(category.name, img_path))
                im.labels.append(label)
                db.session.add(im)

    db.session.commit()
    
    flask.current_app.config['SQLALCHEMY_ECHO'] = original_config
    
    click.echo("Initialized the database.")