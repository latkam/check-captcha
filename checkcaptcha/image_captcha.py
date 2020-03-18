import uuid
import random
from typing import List, Tuple

from checkcaptcha.models import ImageCaptcha, Label, Image, image_captcha
from checkcaptcha import db

MAX_SELECTED = 4
TOTAL_IMAGES = 9

def create_captcha(user_hash):
    cap = ImageCaptcha(user_hash=user_hash, captcha_hash=str(uuid.uuid4()))
    
    target_label: Label = _select_random_label()
    images: List[Image] = _select_random_images(target_label)

    cap.images.extend(images)

    cap.target_label_id = target_label.id_label

    db.session.add(cap)
    db.session.commit()

    return cap

def load_captcha(captcha_hash):
    cap = ImageCaptcha.query.filter_by(captcha_hash=captcha_hash).one_or_none()
    return cap

def _select_random_label():
    row_count = Label.query.count()

    target_label = Label.query.offset(int(row_count*random.random())).first()

    return target_label

def _select_random_images(target_label) -> List[Image]:
    target_label: Label = _select_random_label()
    target_count: int = random.randrange (1, MAX_SELECTED)

    # get target images
    possible_targets = Image.query.filter(Image.labels.any(id_label=target_label.id_label))
    target_rows: int = possible_targets.count()
    selected_offsets: List[int] = random.sample(range(target_rows), target_count)
    targets = []
    target_ids = []
    for offset in selected_offsets:
        targets.append(possible_targets.offset(offset).limit(1).one())
        target_ids.append(targets[-1].id_image)

    # get non-target images
    non_target_count = TOTAL_IMAGES - target_count
    possible = Image.query.filter(~Image.id_image.in_(target_ids))
    other_rows: int = possible.count()
    other_offsets: List[int] = random.sample(range(other_rows), non_target_count)
    others = []
    for offset in other_offsets:
        others.append(possible.offset(offset).limit(1).one())

    return targets + others