import os
import requests
import time
from static_files.perks_dict import perks_dict
from static_files.items_dict import items_dict
from static_files.champions_dict import champions, champions_inv
from static_files.status_codes import status_codes
from static_files.runes_dict import runes_dict
from static_files.summoners_dict import summoners_dict
from dotenv import load_dotenv
from collections import OrderedDict
import requests_cache
requests_cache.install_cache('wrapper_cache', backend='sqlite', expire_after=86400)

load_dotenv()

class Wrapper():
  def __init__(self, region, summoner, champion, enemy_champion):
    self.rate = 20
    self.per = 1
    self.totalT = 0
    
    self.rate2 = 100
    self.per2 = 120
    self.totalT2 = 0
    self.wait = 0

    self.region = region
    self.summoner = summoner
    self.champion = champion.capitalize()
    self.enemy_champion = enemy_champion.capitalize()

    self.key = os.getenv('API_KEY')
    self.regions = ['br1', 'eun1', 'euw1', 'jp1', 'kr', 'la1', 'la2', 'na1', 'oc1', 'ru', 'tr1'];
    self.hostname = f'{self.region}.api.riotgames.com'

    self.status = 0 
    self.status_codes = status_codes
    self.champion_id = champions.get(self.champion)
    self.enemy_champion_id = champions.get(self.enemy_champion)
  
  def CheckValidRegion(self):
    return self.region in self.regions

  def SummonerData(self):
    print('Initializing request to SummonerV4...')
    print('Validating region...')
    if self.CheckValidRegion() == False:
      self.status = 400
      print('False region...')
      print(f'Status code: {self.status}, {self.status_codes.get(self.status)}...')
      return self.status

    else: 
      print('Valid region, attempting request to SummonerV4...')

      url = f'https://{self.hostname}/lol/summoner/v4/summoners/by-name/{self.summoner}?api_key={self.key}'
      start = time.time()
      response = requests.get(url)
      headers = response.headers['X-App-Rate-Limit-Count']
      headers = headers.replace(',', ' ').replace(':',' ').split(' ')
      headers = [int(i) for i in headers]
      passed = time.time() - start
      self.totalT += passed
      self.totalT2  += passed

      print(f'Checking Rate Limits...{headers}')
      if(self.totalT > self.per):
        print('1 second has passed... here 1')
      
      if(self.totalT2 > self.per2):
        print('120 seconds have passed... here 1')
      
      if(headers[0] == self.rate and self.totalT > self.per):
        self.wait = 5
        print(f'condition 1 met: Reached request limit, too many requests in {self.per} seconds... setting throttle. Waiting {self.wait} seconds to continue... here 1\n')
        self.totalT = 0
        time.sleep(self.wait)
      
      if(headers[0] >= self.rate and self.totalT < self.per):
        self.wait = self.per - self.totalT
        print(f'condition 2 met: Reached request limit... setting throttle. Waiting {self.wait} seconds to continue... here 1\n')
        self.totalT = 0
        time.sleep(self.wait)
      
      if(headers[2] == self.rate2 and self.totalT2 > self.per2):
        self.wait = self.per2 - self.totalT2
        print(f'condition 3 met: Reached request limit... setting throttle. Waiting {self.wait} seconds to continue... here 1\n')
        self.totalT2 = 0
        time.sleep(self.wait)
      
      if(headers[2] > self.rate2 and self.totalT2 < self.per2):
        self.wait = self.per2 - self.totalT2
        print(f'condition 3 met: Reached request limit... setting throttle. Waiting {self.wait} seconds to continue... here 1\n')
        self.totalT2 = 0
        time.sleep(self.wait)

      print('Checking response code to SummonerV4...')
      if response.status_code != 200:
        self.status = response.status_code
        print(f'Status code: {self.status}, {self.status_codes.get(self.status)}...')
        return self.status
    
      else:
        print('Sucessful response to SummonerV4!')
        self.status = response.status_code
        account_id = response.json()['accountId']
        username = response.json()['name']
        headers = response.headers['X-App-Rate-Limit-Count']
        headers = headers.replace(',', ' ').replace(':',' ').split(' ')
        headers = [int(i) for i in headers]
        print(f'Username = {username}, Account Id = {account_id}...')
        print(f'Current limit: {headers[0]} request(s) / {headers[1]} second | {headers[2]} request(s) / {headers[3]} seconds...')
        return username, account_id, self.status, headers

  def MatchInfo(self):
    print('Initializing request to MatchV4...')
    print('Getting summoner information, calling SummonerV4...\nChecking response code before continuing with MatchV4...')
    start = time.time()
    summoner_info = self.SummonerData()
    headers = summoner_info[3]
    passed = time.time() - start
    self.totalT += passed
    self.totalT2 += passed

    print(f'Checking Rate Limits...{headers}')
    if(self.totalT > self.per):
      print('1 second has passed... here 2')
    
    if(self.totalT2 > self.per2):
      print('120 seconds have passed... here 2')
    
    if(headers[0] == self.rate and self.totalT > self.per):
      self.wait = 5
      print(f'condition 1 met: Reached request limit, too many requests in {self.per} seconds... setting throttle. Waiting {self.wait} seconds to continue... here 2\n')
      self.totalT = 0
      time.sleep(self.wait)
    
    if(headers[0] >= self.rate and self.totalT < self.per):
      self.wait = self.per - self.totalT
      print(f'condition 2 met: Reached request limit... setting throttle. Waiting {self.wait} seconds to continue... here 2\n')
      self.totalT = 0
      time.sleep(self.wait)
    
    if(headers[2] == self.rate2 and self.totalT2 > self.per2):
      self.wait = self.per2 - self.totalT2
      print(f'condition 3 met: Reached request limit... setting throttle. Waiting {self.wait} seconds to continue... here 2\n')
      self.totalT2 = 0
      time.sleep(self.wait)
    
    if(headers[2] > self.rate2 and self.totalT2 < self.per2):
      self.wait = self.per2 - self.totalT2
      print(f'condition 3 met: Reached request limit... setting throttle. Waiting {self.wait} seconds to continue... here 2\n')
      self.totalT2 = 0
      time.sleep(self.wait)

    if self.status != 200:
      self.status = summoner_info
      return self.status

    else:
      print('Successful response for SummonerV4...')
      queue_id = 420
      username = summoner_info[0]
      account_id = summoner_info[1]
      url = f'https://{self.hostname}/lol/match/v4/matchlists/by-account/{account_id}?champion={self.champion_id}&queue={queue_id}&api_key={self.key}'
      start = time.time()
      response = requests.get(url)
      headers = response.headers['X-App-Rate-Limit-Count']
      headers = headers.replace(',', ' ').replace(':',' ').split(' ')
      headers = [int(i) for i in headers]
      passed = time.time() - start
      self.totalT += passed
      self.totalT2 += passed

      print(f'Checking Rate Limits...{headers}')
      if(self.totalT > self.per):
        print('1 second has passed... here 3')
      
      if(self.totalT2 > self.per2):
        print('120 seconds have passed...here 3')
      
      if(headers[0] == self.rate and self.totalT > self.per):
        self.wait = 5
        print(f'condition 1 met: Reached request limit, too many requests in {self.per} seconds... setting throttle. Waiting {self.wait} seconds to continue... here 3\n')
        self.totalT = 0
        time.sleep(self.wait)
      
      if(headers[0] >= self.rate and self.totalT < self.per):
        self.wait = self.per - self.totalT
        print(f'condition 2 met: Reached request limit... setting throttle. Waiting {self.wait} seconds to continue... here 3\n')
        self.totalT = 0
        time.sleep(self.wait)
      
      if(headers[2] == self.rate2 and self.totalT2 > self.per2):
        self.wait = self.per2 - self.totalT2
        print(f'condition 3 met: Reached request limit... setting throttle. Waiting {self.wait} seconds to continue... here 3\n')
        self.totalT2 = 0
        time.sleep(self.wait)
      
      if(headers[2] > self.rate2 and self.totalT2 < self.per2):
        self.wait = self.per2 - self.totalT2
        print(f'condition 3 met: Reached request limit... setting throttle. Waiting {self.wait} seconds to continue... here 3\n')
        self.totalT2 = 0
        time.sleep(self.wait)

      print('Checking response code to MatchV4...')
      if response.status_code != 200:
        self.status = response.status_code
        print(f'Status code: {self.status}, {self.status_codes.get(self.status)}...')
        return self.status

      else:
        print('Successful response to MatchV4...')
        return response.json()

  def MatchBreakdown(self):
    print('Creating object for MatchInfo()...')
    match_info = self.MatchInfo()
    match_dict = OrderedDict()
    
    if self.status != 200:
      self.status = match_info
      return self.status
    
    else:
      print('Sucessful response for MatchV4, continuing match breakdown...')
      match_id_list = []

      for match_id in match_info['matches']:
        match_id_list.append(match_id['gameId'])

      match_id_list = match_id_list[:50]
      
      for match_id in match_id_list:
        url = f'https://{self.hostname}/lol/match/v4/matches/{match_id}?api_key={self.key}'
        start = time.time()
        response = requests.get(url)
        headers = response.headers['X-App-Rate-Limit-Count']
        headers = headers.replace(',', ' ').replace(':',' ').split(' ')
        headers = [int(i) for i in headers]
        passed = time.time() - start
        self.totalT += passed
        self.totalT2 += passed

        print(f'Checking Rate Limits...{headers}')
        if(self.totalT > self.per):
          print('1 second has passed... here 4')
        
        if(self.totalT2 > self.per2):
          print('120 seconds have passed... here 4')
        
        if(headers[0] == self.rate and self.totalT > self.per):
          self.wait = 5
          print(f'condition 1 met: Reached request limit, too many requests in {self.per} seconds... setting throttle. Waiting {self.wait} seconds to continue... here 4\n')
          self.totalT = 0
          time.sleep(self.wait)
        
        if(headers[0] >= self.rate and self.totalT < self.per):
          self.wait = self.per - self.totalT
          print(f'condition 2 met: Reached request limit... setting throttle. Waiting {self.wait} seconds to continue... here 4\n')
          self.totalT = 0
          time.sleep(self.wait)
        
        if(headers[2] == self.rate2 and self.totalT2 > self.per2):
          self.wait = self.per2 - self.totalT2
          print(f'condition 3 met: Reached request limit... setting throttle. Waiting {self.wait} seconds to continue... here 4\n')
          self.totalT2 = 0
          time.sleep(self.wait)
        
        if(headers[2] > self.rate2 and self.totalT2 < self.per2):
          self.wait = self.per2 - self.totalT2
          print(f'condition 3 met: Reached request limit... setting throttle. Waiting {self.wait} seconds to continue... here 4\n')
          self.totalT2 = 0
          time.sleep(self.wait)

        game_id = response.json()['gameId']
        date = response.json()['gameCreation']/1000

        if response.status_code != 200:
          self.status = response.status_code
          print(f'Status code: {self.status}, {self.status_codes.get(self.status)}...')
          return self.status

        else:
          champion_dict = {}
          data = response.json()['participants']
          usernames = response.json()['participantIdentities']

          for x in response.json()['participants']:
            info_list = [x['teamId'], x['participantId']]
            champion_dict.update({x['championId']:info_list})

          if self.champion_id in champion_dict.keys() and self.enemy_champion_id in champion_dict.keys() and champion_dict.get(self.champion_id)[0] != champion_dict.get(self.enemy_champion_id)[0]:
            print(f'Found {self.champion} and {self.enemy_champion} in gameId {game_id}')

            participants = {participant['championId']:participant for participant in data}
            participants_identities = {participant['participantId']:participant['player']['summonerName'] for participant in usernames}
            user1 = participants_identities[participants[self.champion_id]['participantId']]
            user2 = participants_identities[participants[self.enemy_champion_id]['participantId']]

            match = {
              game_id: {
                'date': date,
                champions_inv.get(self.champion_id): {
                  'username': user1,
                  'teamId': participants[self.champion_id]['teamId'],
                  'win': participants[self.champion_id]['stats']['win'],
                  'kills': participants[self.champion_id]['stats']['kills'],
                  'deaths': participants[self.champion_id]['stats']['deaths'],
                  'assists': participants[self.champion_id]['stats']['assists'],
                  'championId': self.champion_id,
                  'spell1': summoners_dict.get(participants[self.champion_id]['spell1Id']),
                  'spell2': summoners_dict.get(participants[self.champion_id]['spell2Id']),
                  'item0': items_dict.get(str(participants[self.champion_id]['stats']['item0'])),
                  'item1': items_dict.get(str(participants[self.champion_id]['stats']['item1'])),
                  'item2': items_dict.get(str(participants[self.champion_id]['stats']['item2'])),
                  'item3': items_dict.get(str(participants[self.champion_id]['stats']['item3'])),
                  'item4': items_dict.get(str(participants[self.champion_id]['stats']['item4'])),
                  'item5': items_dict.get(str(participants[self.champion_id]['stats']['item5'])),
                  'item6': items_dict.get(str(participants[self.champion_id]['stats']['item6'])),
                  'perk0': runes_dict.get(str(participants[self.champion_id]['stats']['perk0'])),
                  'perk1': runes_dict.get(str(participants[self.champion_id]['stats']['perk1'])),
                  'perk2': runes_dict.get(str(participants[self.champion_id]['stats']['perk2'])),
                  'perk3': runes_dict.get(str(participants[self.champion_id]['stats']['perk3'])),
                  'perk4': runes_dict.get(str(participants[self.champion_id]['stats']['perk4'])),
                  'perk5': runes_dict.get(str(participants[self.champion_id]['stats']['perk5'])),
                  'statPerk0': perks_dict.get(participants[self.champion_id]['stats']['statPerk0']),
                  'statPerk1': perks_dict.get(participants[self.champion_id]['stats']['statPerk1']),
                  'statPerk2': perks_dict.get(participants[self.champion_id]['stats']['statPerk2'])
                },
                champions_inv.get(self.enemy_champion_id): {
                  'username': user2,
                  'teamId': participants[self.enemy_champion_id]['teamId'],
                  'win': participants[self.enemy_champion_id]['stats']['win'],
                  'kills': participants[self.enemy_champion_id]['stats']['kills'],
                  'deaths': participants[self.enemy_champion_id]['stats']['deaths'],
                  'assists': participants[self.enemy_champion_id]['stats']['assists'],
                  'championId': self.enemy_champion_id,
                  'spell1': summoners_dict.get(participants[self.enemy_champion_id]['spell1Id']),
                  'spell2': summoners_dict.get(participants[self.enemy_champion_id]['spell2Id']),
                  'item0': items_dict.get(str(participants[self.enemy_champion_id]['stats']['item0'])),
                  'item1': items_dict.get(str(participants[self.enemy_champion_id]['stats']['item1'])),
                  'item2': items_dict.get(str(participants[self.enemy_champion_id]['stats']['item2'])),
                  'item3': items_dict.get(str(participants[self.enemy_champion_id]['stats']['item3'])),
                  'item4': items_dict.get(str(participants[self.enemy_champion_id]['stats']['item4'])),
                  'item5': items_dict.get(str(participants[self.enemy_champion_id]['stats']['item5'])),
                  'item6': items_dict.get(str(participants[self.enemy_champion_id]['stats']['item6'])),
                  'perk0': runes_dict.get(str(participants[self.enemy_champion_id]['stats']['perk0'])),
                  'perk1': runes_dict.get(str(participants[self.enemy_champion_id]['stats']['perk1'])),
                  'perk2': runes_dict.get(str(participants[self.enemy_champion_id]['stats']['perk2'])),
                  'perk3': runes_dict.get(str(participants[self.enemy_champion_id]['stats']['perk3'])),
                  'perk4': runes_dict.get(str(participants[self.enemy_champion_id]['stats']['perk4'])),
                  'perk5': runes_dict.get(str(participants[self.enemy_champion_id]['stats']['perk5'])),
                  'statPerk0': perks_dict.get(participants[self.enemy_champion_id]['stats']['statPerk0']),
                  'statPerk1': perks_dict.get(participants[self.enemy_champion_id]['stats']['statPerk1']),
                  'statPerk2': perks_dict.get(participants[self.enemy_champion_id]['stats']['statPerk2'])
                }
              }
            }
            match_dict.update(match)
            match_dict.move_to_end(game_id)
          
          else:
            print('Champions in same game not found.')
            continue

    print(f'Finished requests for {self.summoner}...')
    return match_dict
