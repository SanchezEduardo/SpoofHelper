#!/usr/bin/env python3

import json

# parsing through item data json file to create dictionary of n -> itemName
item_ids = []
item_names = []

with open('items.json') as f:
  data = json.load(f)

for n in data['data']:
  item_ids.append(n)

for n in item_ids:
  item_names.append(data['data'][n]['name'])

item_ids = [int(i) for i in item_ids]
item_dict =  {item_ids[i]: item_names[i] for i in range(len(item_ids))}

with open('items_dict.json', 'w') as f:
  json.dump(item_dict, f)

# parsing through rune data json file to create dictionary of n -> runeName
rune_ids = []
rune_names = []

rune_tree_id = []
rune_tree_names = []

with open('runes.json') as f:
  data = json.load(f)

for n in data:
  rune_tree_id.append(n['id'])
  rune_tree_names.append(n['key'])

runeTreeDict =  {rune_tree_id[i]: rune_tree_names[i] for i in range(len(rune_tree_id))}


for i in range(len(rune_tree_id)):
  for x in data[i]['slots']:
    for n in x['runes']:
      rune_ids.append(n['id'])
      rune_names.append(n['key'])

print(rune_tree_names)
print(rune_tree_id)

rune_dict = {rune_ids[i]: rune_names[i] for i in range(len(rune_names))}

with open('rune_dict.json', 'w') as f:
  json.dump(rune_dict, f)

# parsing through champion data json to create dictionary of champion_name -> champion_id
champion_names = []
champion_ids = []

with open('champions.json') as f:
  data = json.load(f)

for n in data:
  champion_names.append(n)

for x in champion_names:
  champion_ids.append(data[x]['id'])

champion_dict = {champion_names[i]: champion_ids[i] for i in range(len(champion_names))}

with open('champion_dict.json', 'w') as f:
  json.dump(champion_dict, f)
