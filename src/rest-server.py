from flask import Flask
from flask_restful import Resource, Api
from riot_endpoints import Wrapper

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app)

@app.route('/<region>/username=<username>&champion=<champion>&enemy_champion=<enemy_champion>')
def RiotCall(region, username, champion, enemy_champion):
  """
  Arguments
  ---------
  region : str
    valid region to look username up in
  username : str 
    summoner league name for the user you want to look up
  champion : str
    champion the user is playing
  enemy_champion : str
    which champion the user is playing against
  
  Attributes
    info : object
      creating object for Wrapper() class

  Returns
  -------
    info.MatchBreakdown(), a json response of the Wrapper()
  """
  info = Wrapper(region, username, champion, enemy_champion)
  return info.MatchBreakdown()

if __name__ == '__main__':
  app.run(debug=True)
