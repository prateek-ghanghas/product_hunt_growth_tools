import requests
from bs4 import BeautifulSoup as bs
import json

URL = "https://www.producthunt.com/"

response = requests.get(URL)

html = bs(response.content, 'lxml')


tags = html.find('script', attrs = {'id':"__NEXT_DATA__"}).string.strip()


data = json.loads(tags)


data = data["props"]["apolloState"]

ref = []  #ref will have product ids (not as it is)

for i in data:
        if "HomefeedPageFEATURED" in i:
            for j in range(len(data[i]["items"])):
                ref.append(data[i]["items"][j]["__ref"])

upvote_list = []

for k in ref:
      if "Ad" in k or "Discussion" in k or "Antholo" in k or "Collection" in k:
            continue
      json_data = {
            'operationName': 'PostPageSocialProof',
            'variables': {
            'postId': k[4:],
            'limit': 500,
                         },
            'query': 'query PostPageSocialProof($postId:ID!$limit:Int!){post(id:$postId){id contributors(limit:$limit){role user{id ...UserImage __typename}__typename}__typename}}fragment UserImage on User{id name username avatarUrl __typename}',
                 }
      r = requests.post('https://www.producthunt.com/frontend/graphql', json=json_data)
      r= r.json()
      data2 = r["data"]["post"]["contributors"]
      l = []
      upvote_dic = {}
      upvote_maindic = {}
      for h in data2:
            if h["role"] == "upvoter":
                  l.append(h["user"]["name"])
      upvote_dic["product_id"] = int(k[4:])
      upvote_dic["upvoter_names"] = l
      upvote_maindic.update(upvote_dic)
      upvote_list.append(upvote_maindic)



p_id = int(input("enter product id: "))

for p in upvote_list:
      if p["product_id"] == p_id:
          print(p["upvoter_names"])