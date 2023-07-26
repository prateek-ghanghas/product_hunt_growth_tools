import requests
from bs4 import BeautifulSoup as bs
import json

def get_commentor_info_for_product_id(product_id):

        '''
        This function fetches commenters and upvoters names by providing the id of that paricular product
        :param product_id: sample: 402396
        :return list: sample: [....]
        '''
        upvote_and_commenters_list = []
        
        json_data = {
              'operationName': 'PostPageSocialProof',
              'variables': {
              'postId': product_id,
              'limit': 1000,
                         },
              'query': 'query PostPageSocialProof($postId:ID!$limit:Int!){post(id:$postId){id contributors(limit:$limit){role user{id ...UserImage __typename}__typename}__typename}}fragment UserImage on User{id name username avatarUrl __typename}',
                 }
        res = requests.post('https://www.producthunt.com/frontend/graphql', json=json_data)
        res = res.json()
        upvoters_data = res["data"]["post"]["contributors"]
        for dict in upvoters_data:
              if dict["role"] == "upvoter" or dict["role] == "commenter":
                      upvote_and_commenters_list.append(dict["user"]["name"])
        print(upvote_and_commenters_list)
if __name__ == "__main__":
        product_id = int(input("Enter the product id: "))
        get_commentor_info_for_product_id(product_id)
        
