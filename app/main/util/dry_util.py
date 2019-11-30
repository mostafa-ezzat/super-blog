from PIL import Image
import os
import random
import string

thumbnail_loc = os.path.join(os.path.dirname(os.path.abspath('main')),
                             'app', 'main', 'assets', 'pic')


def create_response(status, message, extra=None):
    response = {
        'status': status,
        'message': message,
    }

    # exitra is a dictionary if it exist we will
    # loop it and add it to the response
    if extra and isinstance(extra, dict):
        for key in extra:
            response[key] = extra[key]

    return response


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def thumbnail_resize(img):
    m = Image.open(img)
    r_size = (100, 100)
    m.resize(r_size)
    m_name = randomString(random.randrange(10, 15))
    filefullname = f'{thumbnail_loc}\\'
    filefullname += m_name
    filefullname += '.jpeg'
    m.save(filefullname, 'JPEG')
    return f"{m_name}.jpeg"
