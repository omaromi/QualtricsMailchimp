from flask import Flask, request
import json


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.get("/")
def hello():
    """Return a friendly HTTP greeting."""
    return "This is a real mailchimp marketing app!"


@app.route("/surveysignup/", methods=['POST'])
def send_survey():
    student = request.json
    # print(x)
    # student = x
    # i am expecting the payload to look like 
    # {"firstName": "Jane",
    #  "lastName": "Doe",
    #  "email":"user@email.com",}

    from qual import create_qualtrics_contact, add_mailchimp_contact
    create_qualtrics_contact(student)
    add_mailchimp_contact(student)

    return 'Mailchimp Contact Added'

@app.route("/surveycomplete/", methods=['POST'])
def survey_complete():
    student = request.json
    from qual import add_surveycomplete_tag

    add_surveycomplete_tag(student)
    return "survey complete tag"


if __name__ == "__main__":
    # Used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host="localhost", port=8080, debug=True)
