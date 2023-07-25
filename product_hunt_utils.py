import requests
from bs4 import BeautifulSoup as bs
import json

URL = "https://www.producthunt.com/"

response = requests.get(URL)

html = bs(response.content, 'lxml')


tags = html.find('script', attrs = {'id':"__NEXT_DATA__"}).string.strip()


data = json.loads(tags)


data = data["props"]["apolloState"]

refrences = []  #refrences will have product ids (not as it is)

for dict_ in data:
        if "HomefeedPageFEATURED" in dict_:
            for count in range(len(data[dict_]["items"])):
                ref.append(data[dict_]["items"][count]["__ref"])

upvote_list = []

for ref in refrences:
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
      res = requests.post('https://www.producthunt.com/frontend/graphql', json=json_data)
      res = res.json()
      upvoters_data = res["data"]["post"]["contributors"]
      names_list = []
      upvote_dic = {}
      upvote_maindic = {}
      for dict in upvoters_data:
            if dict["role"] == "upvoter":
                  names_list.append(dict["user"]["name"])
      upvote_dic["product_id"] = int(k[4:])
      upvote_dic["upvoter_names"] = l
      upvote_maindic.update(upvote_dic)
      upvote_list.append(upvote_maindic)



product_id = int(input("enter product id: "))

for dictionary in upvote_list:
      if dictionary["product_id"] == product_id:
          print(dictionary["upvoter_names"])
