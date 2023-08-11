import requests
import pandas as pd
import time

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
    '_hjHasCachedUserAttributes': 'true',
    'intercom-session-fe4ce68d4a8352909f553b276994db414d33a55c': '',
    'analytics_session_id': '1691513461352',
    '_hjAbsoluteSessionInProgress': '1',
    '_hjIncludedInSessionSample_3508551': '0',
    '_hjSession_3508551': 'eyJpZCI6ImYzYzRlZWY1LTk2ZjUtNGY0Mi1iMGI1LWRjM2M3OTNkNjE3MyIsImNyZWF0ZWQiOjE2OTE1MTM0NjY1NTUsImluU2FtcGxlIjpmYWxzZX0=',
    'csrf_token': 'W4IQ0p2YGhOSVtgMvGBRh0hLmnqHjLR4__Zd80swYot9dbxQT5s2VPS8h0svazUhapvRws3h_6-FBqE8IVmYlw',
    '_producthunt_session_production': 'OSf3xKPYByDwwW3YgyA0lXpmXswQe7M%2FwsyrNOLSNPgj1kgRzt2p9urAI8NjiqPKcC45uzm98eZ5K8v43wxVBsdtjMoJ8HOkh5WaAo%2Fv8z00LQ2fax0lIzyrQLVE7hbl%2BmE7MJ4z7qVq9pEFF7uS4uYTdYQD9y8Ehzvc0W%2B8big%2B%2BxNih%2FSMf%2FdtO5mvWUcNVHH9JGGeo1p0EkNorUp7ArowwwPpqjeuxqEUy1dp0jr7g1Wr8sHBZdLM55gkC1nNAmYjf4kNB6g2d0uKMZhfdordK2e2IFaUbpuZrEf%2F6BBMYiwCPz9lopb1WjjovkuqgldCYuhJhGu5O6rj%2FKtRiOFuzcqQAO6085CFgtvMFlvdxTdtj5DwDVOpJV78V7dWn0jpu%2BcdZ5FSdlEDrs0Zx716QxOaKbtNnHWr1OaNPKIp6Ft4JJ8i5rZ5UgWsStlw4nPPoTXWQNqBrbC1wCu%2BwNOyk1wlaYg8EZ%2B5wVfEg2CAmLRN2n%2FTi7qlR5gpkYwnv7igrWBtmacJY8GziQ%3D%3D--SfIMKCTzQmgIiVkM--hbRy8HbB9c8bEVneYjHwpQ%3D%3D',
    'analytics_session_id.last_access': '1691513931850',
    '_ga_WZ46833KH9': 'GS1.1.1691513462.24.1.1691513932.60.0.0',
}

headers = {
    'authority': 'www.producthunt.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.producthunt.com',
    'referer': 'https://www.producthunt.com/@emmanuelonuoha',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

def follow_persons_followers(person_username):

    id_lst = []


    json_data = {
        'operationName': 'ProfileFollowersQuery',
        'variables': {
            'username': person_username,
            'cursor': None,
            'query': '',
        },
        'query': 'query ProfileFollowersQuery($username:String!$cursor:String){profile:user(username:$username){id followersCount followers(first:20 after:$cursor){edges{node{id ...UserItemFragment __typename}__typename}pageInfo{endCursor hasNextPage __typename}__typename}...MetaTags __typename}}fragment MetaTags on SEOInterface{id meta{canonicalUrl creator description image mobileAppUrl oembedUrl robots title type author authorUrl __typename}__typename}fragment UserItemFragment on User{id name headline username followersCount ...UserImage ...UserFollowButtonFragment __typename}fragment UserFollowButtonFragment on User{id followersCount isFollowed __typename}fragment UserImage on User{id name username avatarUrl __typename}',
    }

    first_response = requests.post('https://www.producthunt.com/frontend/graphql', cookies=cookies, headers=headers, json=json_data)

    first_response = first_response.json()

    first_followers = first_response["data"]["profile"]["followers"]["edges"]
    end_cursor = first_response["data"]["profile"]["followers"]["pageInfo"]["endCursor"]
    next_page = first_response["data"]["profile"]["followers"]["pageInfo"]["hasNextPage"]

    for nodes in first_followers:
          id_lst.append(nodes["node"]["id"])

    while(next_page == True):
              json_data = {
                'operationName': 'ProfileFollowersQuery',
                'variables': {
                    'username': person_username,
                    'cursor': end_cursor,
                    'query': '',
                },
                'query': 'query ProfileFollowersQuery($username:String!$cursor:String){profile:user(username:$username){id followersCount followers(first:20 after:$cursor){edges{node{id ...UserItemFragment __typename}__typename}pageInfo{endCursor hasNextPage __typename}__typename}...MetaTags __typename}}fragment MetaTags on SEOInterface{id meta{canonicalUrl creator description image mobileAppUrl oembedUrl robots title type author authorUrl __typename}__typename}fragment UserItemFragment on User{id name headline username followersCount ...UserImage ...UserFollowButtonFragment __typename}fragment UserFollowButtonFragment on User{id followersCount isFollowed __typename}fragment UserImage on User{id name username avatarUrl __typename}',
            }

              response = requests.post('https://www.producthunt.com/frontend/graphql', cookies=cookies, headers=headers, json=json_data)

              response = response.json()

              followers = response["data"]["profile"]["followers"]["edges"]

              end_cursor = response["data"]["profile"]["followers"]["pageInfo"]["endCursor"]

              next_page = response["data"]["profile"]["followers"]["pageInfo"]["hasNextPage"]

              for nodes in followers:
                    id_lst.append(nodes["node"]["id"])
    print(len(id_lst))
    print(id_lst)

    df = pd.DataFrame(id_lst, columns = ["person id"])


    df.to_csv('person_ids.csv', index = False)

    df = pd.read_csv('person_ids.csv')
    count = 0

    while(True):

        for i,r in df.iterrows():
            time.sleep(5)
            if(follow_a_person(int(r["person id"]))):
                    count += 1
                    df = df.drop(i)
            else:
                    break
        if (df.empty):
              print("All followers are followed")
              break
        df.to_csv("person_ids",index = False)
        print("followed count: ",count)
        time.sleep(3600)
        df = pd.read_csv("person_ids.csv")
        


def follow_a_person(person_id):

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

      res = requests.post('https://www.producthunt.com/frontend/graphql', cookies=cookies, headers=headers, json=json_data)
      res = res.json()

      res = res["data"]["response"]["node"]

      if res == None:
          return False
      else:
          return True


if __name__ == "__main__":
       username = input("enter username: ")
       follow_persons_followers(username)

