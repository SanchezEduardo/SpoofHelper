from flask import Flask
from flask_restful import Resource, Api
from riot_endpoints import Wrapper

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app)

@app.route('/<region>/username=<username>&champion=<champion>&enemy_champion=<enemy_champion>')
def RiotCall(region, username, champion, enemy_champion):
  info = Wrapper(region, username, champion, enemy_champion)
  response = info.MatchBreakdown()
  return response

if __name__ == '__main__':
  app.run(debug=True)
