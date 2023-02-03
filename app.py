from flask.app import Flask, request, send_file
import cv2
import os

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hello():
    try:
        ratio_resize = request.form['ratio_resize']
    except:
        ratio_resize = 1

    request_file = request.files['file']

    if request_file:
        file_name = gen_random_string() + '.jpg'

        current_dir = os.path.dirname(os.path.abspath(__file__))

        request_file_path = os.path.join(current_dir, 'tmp/files', file_name)
        
        request_file.save(request_file_path)

        file = cv2.imread(request_file_path)

        new_width = int(file.shape[1] / ratio_resize)
        new_height = int(file.shape[0] / ratio_resize)

        resized_file = cv2.resize(file, (new_width, new_height))

        new_file_path = os.path.join(current_dir, 'tmp/resized', file_name)

        cv2.imwrite(new_file_path, resized_file)
        
        return send_file(new_file_path, mimetype='image/jpg')

    return 'No file'

def gen_random_string():
    import random
    import string
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

@app.route('/clean_up')
def clean_up():
    import os
    for file in os.listdir('./tmp/files'):
        if file.endswith('.jpg'):
            os.remove(file)
    for file in os.listdir('./tmp/resized'):
        if file.endswith('.jpg'):
            os.remove(file)

if __name__ == '__main__':
    app.run(debug=True)
