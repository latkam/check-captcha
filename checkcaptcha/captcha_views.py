import click
from flask import Blueprint, render_template, url_for, request
from flask.cli import with_appcontext
from checkcaptcha import image_captcha, db
from checkcaptcha.image_captcha import Label, Image

bp = Blueprint('captcha', __name__)

@bp.route('/api/generate/<user_hash>')
def captcha_generate(user_hash):
    # retrive images form DB
    # imgs = [url_for('static', filename="cat0{}.jpg".format(x)) for x in range(1, 10)]
    # imgs_data = _get_images()
    
    # save captcha to db
    # captcha_id = conn.create_captcha(imgs_data['answer'], imgs_data['target']['id'])
    cap = image_captcha.create_captcha(user_hash)

    # return captcha.render()
    imgs = [{
        'path': url_for('static', filename='images/{}'.format(img.path)),
        'id_image': img.id_image,
    } for img in cap.images]

    return render_template('resp.html', 
        imgs=imgs,
        captcha_hash=cap.captcha_hash, 
        query='Select {}(s)'.format(cap.label.name)
        )
    # return 'foo'

@bp.route('/api/answer/<captcha_hash>', methods=['POST'])
def captcha_answer(captcha_hash):
    answer = request.form.getlist('answers[]')

    captcha = image_captcha.load_captcha(captcha_hash)

    if not captcha:
        return {'correct': False, 'hash': None}

    

    correct_answer = captcha.is_correct(answer)
    # update db
    pass

    if correct_answer:
        return {
            'correct': True,
            # 'hash': some_hash
        }

    else:
        pass
        return {
            'correct': False,
            # 'hash': None
        }
    
@bp.route('/api/verify/<captcha_hash>')
def captcha_verify(captcha_hash):
    captcha = image_captcha.load_captcha(captcha_hash)
    # load from db
    loaded = {
        'valid': True,
        'user_id': 'foobar.cz'
    }
    if loaded:
        return jsonify(loaded)
    else:
        return jsonify({
            'valid': False,
            'user_id': None
        })

@bp.route('/')
def hello_world():
    return render_template('form_new.html')

@bp.route('/send')
def send():
    return render_template('success.html')