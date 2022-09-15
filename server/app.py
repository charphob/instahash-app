from flask import Flask, jsonify, request
from flask_cors import CORS
from db_utils import find_ht,min_max_time
import base64

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

"""
Global variable to store cursor returned from DB query.

This is done so that we could iterate over it with the pagination and keep the state of the cursor updated for each pagination call.
"""
posts_cursor = None

@app.route('/posts', methods=['POST'])
def get_posts():

    global posts_cursor

    response_object = {'status': 'success'} # should be used for checking

    req = request.get_json() # request result from POST method by AXIOS
    ht = req.get('ht', '')
    t1 = req.get('t1', 0)
    t2 = req.get('t2', 0)
    posts_cursor = find_ht(ht, t1, t2) # the cursor

    initial_posts = get_post_batch() # this gets an initial 3X3=9 batch of posts

    response_object.update({'posts': initial_posts}) # add to response object

    return jsonify(response_object)


@app.route('/loadposts', methods=['GET', 'POST'])
def load_posts():
    """ 
    Similar to get_posts(), this uses get_post_batch() to receive another new batch of 3X3=9 posts.
    """

    response_object = {'status': 'success'}
    initial_posts = get_post_batch()

    response_object.update({'posts': initial_posts})

    return jsonify(response_object)

@app.route('/minmax',methods=['GET'])
def ht_min_max():

    """ 
    Route for ht list, min and max timestamps from db query method, activated on page creation  by AXIOS
    """

    return jsonify(min_max_time())

def get_post_batch():

    """
    Keeps global posts cursor alive, advancing it by 9 steps over each time it is called by get_posts() or load_posts()
    """

    global posts_cursor

    result = []

    for i in range(9):

        # advances 1 step at a time, if ended return None, which breaks loop
        post = next(posts_cursor, None)

        if post is not None:

            # during scraping, image was encoded as binary, it is encoded as a string to be able to send it over inside a JSON.
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

""" curl commands to test server from terminal """

# curl -X POST http://localhost:5000/posts -H 'Content-Type: application/json' -d '{"ht":"kfarkama"}'
