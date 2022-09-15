from flask import Flask, jsonify, request
from flask_cors import CORS
from db_utils import find_ht,min_max_time
import base64

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

posts_cursor = None


@app.route('/posts', methods=['POST'])
def get_posts():

    global posts_cursor

    response_object = {'status': 'success'}

    req = request.get_json()
    ht = req.get('ht', '')
    t1 = req.get('t1', 0)
    t2 = req.get('t2', 0)
    posts_cursor = find_ht(ht, t1, t2)

    initial_posts = get_post_batch()

    response_object.update({'posts': initial_posts})

    return jsonify(response_object)


@app.route('/loadposts', methods=['GET', 'POST'])
def load_posts():

    response_object = {'status': 'success'}
    initial_posts = get_post_batch()

    response_object.update({'posts': initial_posts})

    return jsonify(response_object)

@app.route('/minmax',methods=['GET'])
def ht_min_max():

    return jsonify(min_max_time())

def get_post_batch():

    global posts_cursor

    result = []
    for i in range(9):

        post = next(posts_cursor, None)

        if post is not None:
            img_bin = post.get('img_bin')
            img_string = base64.encodebytes(img_bin).decode('ascii')
            scraped_timestamp = post.get('scraped_timestamp')
            post.update({'scraped_timestamp':int(scraped_timestamp)})
            post.update({'img_bin': img_string})
            result.append(post)
        else:
            break

    return result


if __name__ == '__main__':
    app.run(debug=True)

# curl -X POST http://localhost:5000/posts -d \ '{"ht": "kfarkama"}' \ -H 'Content-Type: application/json'

# curl -X POST http://localhost:5000/posts -H 'Content-Type: application/json' -d '{"ht":"kfarkama"}'
