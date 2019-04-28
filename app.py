from flask import Flask
from slackeventsapi import SlackEventAdapter
from models import db
from slack_handler import process_incoming_message

# flask init
app = Flask(__name__)
app.config.from_object('config')

# init slack event adaptor
slack = SlackEventAdapter(app.config['SLACK_SIGNING_SECRET'], "/slack/events", app)

# init SQLAlchemy
with app.app_context():
    db.init_app(app)
    db.create_all()


from slack import slack as slack_blueprint
app.register_blueprint(slack_blueprint, url_prefix='/slack')


@slack.on("message")
def handle_message(event_data, req):
    process_incoming_message(event_data, req)


if __name__ == '__main__':
    app.run(port=3000)
