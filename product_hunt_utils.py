import requests
from bs4 import BeautifulSoup as bs
import json

PRODUCT_HUNT_GRAPHQL_API = 'https://www.producthunt.com/frontend/graphql'
cookies = {
            '_delighted_web': '{%2271AaKmxD4TpPsjYW%22:{%22_delighted_fst%22:{%22t%22:%221689247698039%22}}}',
            '_ga': 'GA1.1.845259885.1689247698',
            'ajs_anonymous_id': '98a3c2ff-2922-4519-9794-e4f731553551',
            'visitor_id': 'ddc2a4ea-9274-469e-aaba-87f9e81c7597',
            'track_code': 'a7ccfbaf01',
            'intercom-id-fe4ce68d4a8352909f553b276994db414d33a55c': '06cb8ae7-ecdd-49c6-84a8-d9c926edc77d',
            'intercom-device-id-fe4ce68d4a8352909f553b276994db414d33a55c': '63d09907-e9c8-4aa3-bd10-eb96e1b656df',
            '_hjSessionUser_3508551': 'eyJpZCI6ImVhYzIzNzQxLWQ1MWItNWE0NS1iYzc5LTcxYWExNDlhMmU5YyIsImNyZWF0ZWQiOjE2ODkyNDc2OTgyODksImV4aXN0aW5nIjp0cnVlfQ==',
            'ajs_user_id': '5826028',
            'g_state': '{"i_l":2,"i_p":1690215702448}',
            'first_visit': '1691049905',
            'first_referer': 'https://www.google.com/',
            '_hjIncludedInSessionSample_3508551': '0',
            '_hjSession_3508551': 'eyJpZCI6IjViYzRiZGE2LTNmYjQtNDMyZS1hYjllLWJhZjc4N2EwNGE3OCIsImNyZWF0ZWQiOjE2OTEwNDk5MDU3OTUsImluU2FtcGxlIjpmYWxzZX0=',
            '_hjAbsoluteSessionInProgress': '0',
            '_hjHasCachedUserAttributes': 'true',
            'analytics_session_id': '1691049906136',
            'intercom-session-fe4ce68d4a8352909f553b276994db414d33a55c': '',
            'csrf_token': 'Iag41cQRyT8JKGnIIybnzk1jL1aJyzeo3gUs1yM3kBgHX5RXFhLleG_CNo-wLYNob7Nk7sOmfH-k9dAYSV5qBA',
            '_producthunt_session_production': '1Vb7%2FpKi9%2FiprTr4nBWcH009BuUA3zMrDjxKIW4QeFADdUeZdAEqdpn5BK12nAsqFoIbye8E0r1v7SBtPKfqTm%2BtagcxzQ%2BpX6vV7otwteoWBNsvVs%2FxEbxuo5ngYtwBf40FzN7jpDR2WoztTufY3xqXG0rPZLR17xfxC1mzeXo6YYaJ%2F5hz9oPrtBIShcEbajOHpsrkfDpHn%2FkBTIIDJzxjRu4nG%2FaAcN5W48x7CoBg6ywugpYuMAN%2F%2FQ4T4JNZMCeYO0O6a87XIMwSxgBDoIRTMcVCmB5wMhDZgRBJAJ8dHzd96Rt%2Fdd50ADihxkGfxgOPtx2UYanDo0tDKF8%2BK1mZgz1LNYxDLjUFUtJhbwEpFYL%2FNPLQ3s11AjeFlXTl05Vj%2FA2DdrC4gUvr0J5Ix7sDxrhio9RgpC%2BXpeCSyIjjbngOD518vdQ8DlbDMHCeRiRCdjoWtmUdO83wSUyY9vGRaszBqBimUnIwenzLG2WH5bCoj%2BmUZpYCfdIOwJXdoPyDFT%2BqF%2F9hKI7VAA%3D%3D--kiyd7zeABja6J%2Fpa--KBNRT6d%2FeHZfge1nwz615Q%3D%3D',
            'analytics_session_id.last_access': '1691052362270',
            '_ga_WZ46833KH9': 'GS1.1.1691049905.19.1.1691052363.60.0.0',
        }
headers = {
            'authority': 'www.producthunt.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://www.producthunt.com',
            'referer': 'https://www.producthunt.com/@cyriljeet',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

def get_commentor_info_for_product_id(product_id: int)-> list:

        '''
        This function fetches commenters and upvoters names by providing the id of that paricular product
        :param product_id: sample: 402396
        :return upvote_and_commenters_list: sample: ['Nick Anisimov', 'Cyril Gupta', 'Victor Antonov', 'Shoaib Iqbal',........]
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
        res = requests.post(PRODUCT_HUNT_GRAPHQL_API, json=json_data)
        res = res.json()
        upvoters_data = res["data"]["post"]["contributors"]
        for dict in upvoters_data:
              if dict["role"] == "upvoter" or dict["role"] == "commenter":
                      upvote_and_commenters_list.append(dict["user"]["name"])
        print(upvote_and_commenters_list)

def follow_person_using_person_id(person_id: int)-> bool:
        
        """
        This function try follows a person by providing id of that person
        and return True if succeed otherwise False
        :param person_id: sample: 922865
        :return True or False
        """

        json_data = {
            'operationName': 'UserFollowCreate',
            'variables': {
                'input': {
                    'userId': person_id,
                    'sourceComponent': 'user_profile',
                },
            },
            'query': 'mutation UserFollowCreate($input:UserFollowCreateInput!){response:userFollowCreate(input:$input){node{id ...UserFollowButtonFragment __typename}__typename}}fragment UserFollowButtonFragment on User{id followersCount isFollowed __typename}',
        }

        res = requests.post(PRODUCT_HUNT_GRAPHQL_API = 'https://www.producthunt.com/frontend/graphql', cookies=cookies, headers=headers, json=json_data)

        res = res.json()

        res = res["data"]["response"]["node"]

        if res == None:
            return False
        else:
            return True
        
        

        
if __name__ == "__main__":
        product_id = int(input("Enter the product id: "))
        get_commentor_info_for_product_id(product_id)
        person_id = int(input("Enter person id: "))
        follow_person_with_person_id(person_id)
        
