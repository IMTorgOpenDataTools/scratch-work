
from services.workflow import domains_workflow

from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/latest')
def serve_app(path):
    """Serve the most-recent app version.
    """
    return send_from_directory('static', path)


@app.route("/domain", methods=['POST'])
def convert_domain():
    """Get domains for list of websites.  Then, convert
    the website into pdf and return to the pdf url path 
    to the user.
    """
    #get domains
    post_data = request.get_json()
    print(post_data.get('domainUrl'))

    #process domains
    processing_results = domains_workflow(post_data)

    #return pdf links
    #response = jsonify({'text': "Hello, World!"})
    print(processing_results)
    response = jsonify({'results': processing_results})
    return response


if __name__ == '__main__':
    app.run()