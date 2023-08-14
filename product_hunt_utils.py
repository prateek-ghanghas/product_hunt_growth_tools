import requests
import pandas as pd
import time
import os

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

def get_products_info(days: int)->list :

         '''
         This function fetches the product info (name,tagline,slug,url)
         by providing the days i.e product launches of how many days we
         want to fetch and returns the info.
         :param days: sample: 1
         :return list of dictionaries: sample:[{'name':'iqoo',tagline: 'future is here', 'slug': 'iq_00', 'url': https://www.producthunt.com/post/iq00]
         '''
         info = []

         for i in range(int(days)):

                json_data = {
                    'operationName': 'HomePage',
                    'variables': {
                        'cursor': str(i),
                        'kind': 'FEATURED',
                        'filters': {},
                    },
                    'query': 'query HomePage($cursor:String$kind:HomefeedKindEnum!$filters:HomefeedFiltersInput!){homefeed(after:$cursor kind:$kind filters:$filters){kind edges{node{id title subtitle hideAfter date randomization items{...on Post{id hideVotesCount ...PostItemFragment featuredComment{id body:bodyText user{id ...UserImage __typename}__typename}__typename}...on DiscussionThread{id ...DiscussionHomepageItemFragment __typename}...on AnthologiesStory{id ...StoryHomepageItemFragment __typename}...on Ad{id ...AdFragment __typename}...on Collection{id ...CollectionHomepageItemFragment __typename}__typename}...ComingSoonCardHomepageFragment __typename}__typename}pageInfo{hasNextPage endCursor __typename}__typename}mainBanner:banner(position:MAINFEED){id description url desktopImageUuid wideImageUuid tabletImageUuid mobileImageUuid __typename}phHomepageOgImageUrl viewer{id showHomepageOnboarding __typename}}fragment AdFragment on Ad{id subject post{id slug name updatedAt commentsCount topics(first:1){edges{node{id name __typename}__typename}__typename}...PostVoteButtonFragment __typename}ctaText name tagline thumbnailUuid url __typename}fragment PostVoteButtonFragment on Post{id featuredAt updatedAt createdAt product{id isSubscribed __typename}disabledWhenScheduled hasVoted ...on Votable{id votesCount __typename}__typename}fragment PostItemFragment on Post{id commentsCount name shortenedUrl slug tagline updatedAt pricingType topics(first:1){edges{node{id name slug __typename}__typename}__typename}redirectToProduct{id slug __typename}...PostThumbnail ...PostVoteButtonFragment __typename}fragment PostThumbnail on Post{id name thumbnailImageUuid ...PostStatusIcons __typename}fragment PostStatusIcons on Post{id name productState __typename}fragment UserImage on User{id name username avatarUrl __typename}fragment DiscussionHomepageItemFragment on DiscussionThread{id title descriptionText slug commentsCount user{id firstName username avatarUrl name headline isMaker isViewer badgesCount badgesUniqueCount karmaBadge{kind score __typename}__typename}discussionCategory:category{id name slug __typename}...DiscussionThreadItemVote __typename}fragment DiscussionThreadItemVote on DiscussionThread{id hasVoted votesCount __typename}fragment StoryHomepageItemFragment on AnthologiesStory{id slug title description minsToRead commentsCount ...StoryVoteButtonFragment storyCategory:category{name slug __typename}author{id username firstName avatarUrl name headline isMaker isViewer badgesCount badgesUniqueCount karmaBadge{kind score __typename}__typename}__typename}fragment StoryVoteButtonFragment on AnthologiesStory{id hasVoted votesCount __typename}fragment CollectionHomepageItemFragment on Collection{id slug name collectionTitle:title description user{id name username __typename}...CollectionsThumbnailsFragment __typename}fragment ProductThumbnailFragment on Product{id name logoUuid isNoLongerOnline __typename}fragment CollectionsThumbnailsFragment on Collection{products(first:1){edges{node{id ...ProductThumbnailFragment __typename}__typename}__typename}__typename}fragment ComingSoonCardHomepageFragment on HomefeedPage{comingSoon{id ...UpcomingEventItemFragment __typename}__typename}fragment UpcomingEventItemFragment on UpcomingEvent{id title truncatedDescription isSubscribed post{id createdAt __typename}product{id slug postsCount followersCount followers(first:3 order:popularity excludeViewer:true){edges{node{id ...UserCircleListFragment __typename}__typename}__typename}...ProductItemFragment __typename}...FacebookShareButtonV6Fragment __typename}fragment ProductItemFragment on Product{id slug name tagline followersCount reviewsCount topics(first:2){edges{node{id slug name __typename}__typename}__typename}...ProductFollowButtonFragment ...ProductThumbnailFragment ...ProductMuteButtonFragment ...FacebookShareButtonV6Fragment ...ReviewStarRatingCTAFragment __typename}fragment ProductFollowButtonFragment on Product{id followersCount isSubscribed __typename}fragment ProductMuteButtonFragment on Product{id isMuted __typename}fragment FacebookShareButtonV6Fragment on Shareable{id url __typename}fragment ReviewStarRatingCTAFragment on Product{id slug name isMaker reviewsRating __typename}fragment UserCircleListFragment on User{id ...UserImage __typename}',
                }

                response = requests.post(PRODUCT_HUNT_GRAPHQL_API, json=json_data)

                r = response.json()

                iterable = r["data"]["homefeed"]["edges"][0]["node"]["items"]

                try:

                    for i in iterable:
                        maindic = {}
                        dic = {}
                        if "hideVotesCount" in i:
                            dic["name"] = i["name"]
                            dic["tagline"] = i["tagline"]
                            dic["votesCount"] = i["votesCount"]
                            dic["link"] = "https://www.producthunt.com/posts/" + i["slug"]
                            maindic.update(dic)
                            info.append(maindic)
                except KeyError:
                    pass

         return (info)

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

        return upvote_and_commenters_list

def follow_persons_followers(person_username: str,followersFilePath: str)->bool :

    '''
    This function follows all the followings of a person by taking
    his username and filepath as a param.
    :param person_username, filepath: sample: alicea_hughes, person_ids.csv
    :return Boolean value: sample: True
    '''

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

    first_response = requests.post(PRODUCT_HUNT_GRAPHQL_API, cookies=cookies, headers=headers, json=json_data)

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

              response = requests.post(PRODUCT_HUNT_GRAPHQL_API, cookies=cookies, headers=headers, json=json_data)

              response = response.json()

              followers = response["data"]["profile"]["followers"]["edges"]

              end_cursor = response["data"]["profile"]["followers"]["pageInfo"]["endCursor"]

              next_page = response["data"]["profile"]["followers"]["pageInfo"]["hasNextPage"]

              for nodes in followers:
                    id_lst.append(nodes["node"]["id"])


    return follow_list_of_ids(id_lst, followersFilePath)


def follow_persons_followings(person_username: str, followingsFilePath: str)->bool :

    '''
    This function follows all the followings of a person by taking
    his username and filepath as a param.
    :param person_username, filepath: sample: alicea_hughes, person_ids.csv
    :return Boolean value: sample: True
    '''

    json_data = {
    'operationName': 'ProfileFollowingQuery',
    'variables': {
        'username': person_username,
        'cursor': None,
        'query': '',
    },
    'query': 'query ProfileFollowingQuery($username:String!$cursor:String){profile:user(username:$username){id isTrashed followingsCount following(first:20 after:$cursor){edges{node{id ...UserItemFragment __typename}__typename}pageInfo{endCursor hasNextPage __typename}__typename}...MetaTags __typename}}fragment MetaTags on SEOInterface{id meta{canonicalUrl creator description image mobileAppUrl oembedUrl robots title type author authorUrl __typename}__typename}fragment UserItemFragment on User{id name headline username followersCount ...UserImage ...UserFollowButtonFragment __typename}fragment UserFollowButtonFragment on User{id followersCount isFollowed __typename}fragment UserImage on User{id name username avatarUrl __typename}',
}

    first_response = requests.post(PRODUCT_HUNT_GRAPHQL_API, cookies=cookies, headers=headers, json=json_data)

    first_response = first_response.json()

    id_lst = []

    first_followings = first_response["data"]["profile"]["following"]["edges"]
    end_cursor = first_response["data"]["profile"]["following"]["pageInfo"]["endCursor"]
    next_page = first_response["data"]["profile"]["following"]["pageInfo"]["hasNextPage"]

    for nodes in first_followings:
            id_lst.append(nodes["node"]["id"])

    while(next_page == True):
        json_data = {
        'operationName': 'ProfileFollowingQuery',
        'variables': {
            'username': 'alicea_hughes',
            'cursor': end_cursor,
            'query': '',
        },
        'query': 'query ProfileFollowingQuery($username:String!$cursor:String){profile:user(username:$username){id isTrashed followingsCount following(first:20 after:$cursor){edges{node{id ...UserItemFragment __typename}__typename}pageInfo{endCursor hasNextPage __typename}__typename}...MetaTags __typename}}fragment MetaTags on SEOInterface{id meta{canonicalUrl creator description image mobileAppUrl oembedUrl robots title type author authorUrl __typename}__typename}fragment UserItemFragment on User{id name headline username followersCount ...UserImage ...UserFollowButtonFragment __typename}fragment UserFollowButtonFragment on User{id followersCount isFollowed __typename}fragment UserImage on User{id name username avatarUrl __typename}',
    }


        response = requests.post(PRODUCT_HUNT_GRAPHQL_API, cookies=cookies, headers=headers, json=json_data)

        response = response.json()

        followings = response["data"]["profile"]["following"]["edges"]

        end_cursor = response["data"]["profile"]["following"]["pageInfo"]["endCursor"]

        next_page = response["data"]["profile"]["following"]["pageInfo"]["hasNextPage"]

        for nodes in followings:
            id_lst.append(nodes["node"]["id"])


    return follow_list_of_ids(id_lst, followingsFilePath)

def follow_a_person(person_id):

      """
        This function try follows a person by providing id of that person
        and return True if succeed otherwise False
        :param person_id: sample: 922865
        :return boolean values: sample: True or False
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

      res = requests.post(PRODUCT_HUNT_GRAPHQL_API, cookies=cookies, headers=headers, json=json_data)
      res = res.json()

      res = res["data"]["response"]["node"]

      if res == None:
          return False
      else:
          return True

def follow_list_of_ids(id_lst: list, filePath: str)->bool :

    '''
    This function follow all the persons by providing theirs ids which is done
    by passing a DataFrame which contain ids of those persons, it also take
    csv filepath as a param so that reading and writing in file can be done
    accordingly.
    :param id_lst filepath: sample: [408087,593738,......], person_ids.csv
    :return boolean value: sample: True
    '''
    df = pd.DataFrame(id_lst, columns = ["person id"])

    df.to_csv(followersFilePath, index = False)

    df = pd.read_csv(followersFilePath)

    count = 0

    while(True):

        for i,r in df.iterrows():
            time.sleep(5)
            if(follow_a_person(int(r["person id"]))):
                    count += 1
                    df = df.drop(i)
            else:
                    break
        if(df.empty):
              print("All the persons are followed")
              return True

        df.to_csv(filePath,index = False)
        print("followed count: ",count,)
        print("wait before start following again: 1 Hr")
        time.sleep(3600)
        df = pd.read_csv(filePath)

def unfollow_non_followbacks(non_followback_filePath):

        # FOR FOLLOWINGS
        json_data = {
            'operationName': 'ProfileFollowingQuery',
            'variables': {
                'username': 'prateek_ghanghas',
                'cursor': None,
                'query': '',
            },
            'query': 'query ProfileFollowingQuery($username:String!$cursor:String){profile:user(username:$username){id isTrashed followingsCount following(first:20 after:$cursor){edges{node{id ...UserItemFragment __typename}__typename}pageInfo{endCursor hasNextPage __typename}__typename}...MetaTags __typename}}fragment MetaTags on SEOInterface{id meta{canonicalUrl creator description image mobileAppUrl oembedUrl robots title type author authorUrl __typename}__typename}fragment UserItemFragment on User{id name headline username followersCount ...UserImage ...UserFollowButtonFragment __typename}fragment UserFollowButtonFragment on User{id followersCount isFollowed __typename}fragment UserImage on User{id name username avatarUrl __typename}',
        }

        first_response = requests.post(PRODUCT_HUNT_GRAPHQL_API, cookies=cookies, headers=headers, json=json_data)

        first_response = first_response.json()

        following_list = []

        first_followings = first_response["data"]["profile"]["following"]["edges"]
        end_cursor = first_response["data"]["profile"]["following"]["pageInfo"]["endCursor"]
        next_page = first_response["data"]["profile"]["following"]["pageInfo"]["hasNextPage"]

        for nodes in first_followings:
                following_list.append(nodes["node"]["id"])

        while(next_page == True):
            json_data = {
            'operationName': 'ProfileFollowingQuery',
            'variables': {
                'username': 'prateek_ghanghas',
                'cursor': end_cursor,
                'query': '',
            },
            'query': 'query ProfileFollowingQuery($username:String!$cursor:String){profile:user(username:$username){id isTrashed followingsCount following(first:20 after:$cursor){edges{node{id ...UserItemFragment __typename}__typename}pageInfo{endCursor hasNextPage __typename}__typename}...MetaTags __typename}}fragment MetaTags on SEOInterface{id meta{canonicalUrl creator description image mobileAppUrl oembedUrl robots title type author authorUrl __typename}__typename}fragment UserItemFragment on User{id name headline username followersCount ...UserImage ...UserFollowButtonFragment __typename}fragment UserFollowButtonFragment on User{id followersCount isFollowed __typename}fragment UserImage on User{id name username avatarUrl __typename}',
        }


            response = requests.post(PRODUCT_HUNT_GRAPHQL_API, cookies=cookies, headers=headers, json=json_data)

            response = response.json()

            followings = response["data"]["profile"]["following"]["edges"]

            end_cursor = response["data"]["profile"]["following"]["pageInfo"]["endCursor"]

            next_page = response["data"]["profile"]["following"]["pageInfo"]["hasNextPage"]

            for nodes in followings:
                following_list.append(nodes["node"]["id"])

        #FOR FOLLOWERS
        follower_list = []
        json_data = {
            'operationName': 'ProfileFollowersQuery',
            'variables': {
            'username': 'prateek_ghanghas' ,
            'cursor': None,
            'query': '',
        },
        'query': 'query ProfileFollowersQuery($username:String!$cursor:String){profile:user(username:$username){id followersCount followers(first:20 after:$cursor){edges{node{id ...UserItemFragment __typename}__typename}pageInfo{endCursor hasNextPage __typename}__typename}...MetaTags __typename}}fragment MetaTags on SEOInterface{id meta{canonicalUrl creator description image mobileAppUrl oembedUrl robots title type author authorUrl __typename}__typename}fragment UserItemFragment on User{id name headline username followersCount ...UserImage ...UserFollowButtonFragment __typename}fragment UserFollowButtonFragment on User{id followersCount isFollowed __typename}fragment UserImage on User{id name username avatarUrl __typename}',
    }

        first_response = requests.post(PRODUCT_HUNT_GRAPHQL_API, cookies=cookies, headers=headers, json=json_data)

        first_response = first_response.json()

        first_followers = first_response["data"]["profile"]["followers"]["edges"]
        end_cursor = first_response["data"]["profile"]["followers"]["pageInfo"]["endCursor"]
        next_page = first_response["data"]["profile"]["followers"]["pageInfo"]["hasNextPage"]

        for nodes in first_followers:
           follower_list.append(nodes["node"]["id"])

        while(next_page == True):
              json_data = {
                'operationName': 'ProfileFollowersQuery',
                'variables': {
                    'username': 'prateek_ghanghas',
                    'cursor': end_cursor,
                    'query': '',
                },
                'query': 'query ProfileFollowersQuery($username:String!$cursor:String){profile:user(username:$username){id followersCount followers(first:20 after:$cursor){edges{node{id ...UserItemFragment __typename}__typename}pageInfo{endCursor hasNextPage __typename}__typename}...MetaTags __typename}}fragment MetaTags on SEOInterface{id meta{canonicalUrl creator description image mobileAppUrl oembedUrl robots title type author authorUrl __typename}__typename}fragment UserItemFragment on User{id name headline username followersCount ...UserImage ...UserFollowButtonFragment __typename}fragment UserFollowButtonFragment on User{id followersCount isFollowed __typename}fragment UserImage on User{id name username avatarUrl __typename}',
            }

              response = requests.post(PRODUCT_HUNT_GRAPHQL_API, cookies=cookies, headers=headers, json=json_data)

              response = response.json()

              followers = response["data"]["profile"]["followers"]["edges"]

              end_cursor = response["data"]["profile"]["followers"]["pageInfo"]["endCursor"]

              next_page = response["data"]["profile"]["followers"]["pageInfo"]["hasNextPage"]

              for nodes in followers:
                    follower_list.append(nodes["node"]["id"])

        unfollowed_list = []

        for ids in following_list:
              if ids not in follower_list:
                    unfollowed_list.append(ids)

        print(len(unfollowed_list))
        df = pd.DataFrame(unfollowed_list, columns = ["non_followback_ids"])

        for i,r in df.iterrows():
             unfollow_id(r['non_followback_ids'])

        df.to_csv(non_followback_filePath, index = False)


def unfollow_id(person_id):
      json_data = {
    'operationName': 'UserFollowDestroy',
    'variables': {
        'input': {
            'userId': person_id,
        },
    },
    'query': 'mutation UserFollowDestroy($input:UserFollowDestroyInput!){response:userFollowDestroy(input:$input){node{id ...UserFollowButtonFragment __typename}__typename}}fragment UserFollowButtonFragment on User{id followersCount isFollowed __typename}',
}

      response = requests.post('https://www.producthunt.com/frontend/graphql', cookies=cookies, headers=headers, json=json_data)
      response = response.json()

      data = response["data"]["response"]["node"]["isFollowed"]

      if data == False:
         return True
      else:
         return False



if __name__ == "__main__":

       days = int(input("product info for how many days? : "))
       get_products_info(days)
       product_id = int(input("Enter product id: "))
       get_commentor_info_for_product_id(product_id)
       person_username = input("Enter username: ")
       followersFilePath = input("Enter file path for followers here: ")
       followingsFilePath = input("Enter file path for followings here: ")
       follow_persons_followers(person_username,followersFilePath)
       follow_persons_followings(person_username,followingsFilePath)
       non_followback_filePath = input("Enter file path for non followbacks: ")
       unfollow_non_followbacks(non_followback_filePath)




