import requests
import pandas as pd
import time
import os
import random

PRODUCT_HUNT_GRAPHQL_API = 'https://www.producthunt.com/frontend/graphql'

session_token = 'jmWZB9XqR6faezx%2Fi%2FOHb7o0FYfa8urja8tF8fdmbOew1PP%2B2zchQcJSvvqDOHlEBPIjlmjCqT2uSkljhI9IEp11%2FRgux5DJnkUFAloxlh8FUnwKiwOL9NKz69LarjoMoFY%2ByfcKu9urSaYiE0T6zFjk%2Bwp2ZWSCjX3AfvJVh0lKOUVEEJ2b5Dzn9andZJdAIbViUFHs7Jg0jck6eksPK0qBI1lipVGH0mEouG%2FQS%2Fy2COa34LKEBzBMRKfJIobi3ca0awdx6CRlIUlIlQQkzYA9k2BC%2F8fPRvYNBeFGDnFNg50F7oUQECSkf9tyK6Go7QRyrzVEIOYprV01x6oRVOSD54Jx63fk07qBLvmdrAMc6UthEWQwKJWuUjM8f3UNnuXlhPun%2FvGItj3%2FgJDsM%2B%2FZwgvC1cQryz%2BRpBBKN6B6g9u9sU%2FSgFQnnjOXH6RtsWFAGOuEpm%2FKCJtt4EQuRvueW9RqJ9JlNnEkl25BX9ivMJ335iHdLGdN78EUwRZFUowBvXXEZFqMhYqb8Q%3D%3D--gUy1vAqw4jq%2BrkSe--xIRc9QtYwJHMWjRs6wGMlg%3D%3D'

cookies = {
          '_producthunt_session_production': session_token
}

headers = {
          'sec-ch-ua-platform': '"Windows"',
          'x-requested-with': 'XMLHttpRequest',
}


def get_product_info_today():
        
        '''
        This function fetches the product info (name,id,tagline,slug,url,description)
        for the products launched today only . It doesn't take any param.
        :return list of dictionaries: sample:[{'name':'iqoo','id': '407853', tagline: 'future is here', 'slug': 'iq_00', 'url': https://www.producthunt.com/post/iq00,'description': 'This brand is the no.1 brand in the world']
        '''


        product_launched_today_info = []
        
        json_data = {
                    'operationName': 'HomePage',
                    'variables': {
                        'cursor': None,
                        'kind': 'FEATURED',
                        'filters': {},
                    },
                    'query': 'query HomePage($cursor:String$kind:HomefeedKindEnum!$filters:HomefeedFiltersInput!){homefeed(after:$cursor kind:$kind filters:$filters){kind edges{...HomefeedEdgeFragment __typename}pageInfo{hasNextPage endCursor __typename}__typename}mainBanner:banner(position:MAINFEED){id description url desktopImageUuid wideImageUuid tabletImageUuid mobileImageUuid __typename}phHomepageOgImageUrl viewer{id showHomepageOnboarding __typename}}fragment HomefeedEdgeFragment on HomefeedEdgeCustom{node{id title subtitle hideAfter date randomization items{...on Post{id hideVotesCount ...PostItemFragment featuredComment{id body:bodyText user{id ...UserImage __typename}__typename}__typename}...on Ad{id ...AdFragment __typename}__typename}...ComingSoonCardHomepageFragment ...ProductUpdatesCardHomepageFragment __typename}__typename}fragment AdFragment on Ad{id subject post{id slug name updatedAt commentsCount topics(first:3){edges{node{id slug __typename}__typename}__typename}...PostVoteButtonFragment __typename}ctaText name tagline thumbnailUuid url __typename}fragment PostVoteButtonFragment on Post{id featuredAt updatedAt createdAt product{id isSubscribed __typename}disabledWhenScheduled hasVoted ...on Votable{id votesCount __typename}__typename}fragment PostItemFragment on Post{id commentsCount name shortenedUrl slug tagline updatedAt topics(first:4){edges{node{id slug __typename}__typename}__typename}redirectToProduct{id slug __typename}launchTypesInfo{id soloMaker __typename}fundingSurvey{id bootstrapped __typename}...ProductLinkFragment ...PostThumbnail ...PostVoteButtonFragment __typename}fragment PostThumbnail on Post{id name thumbnailImageUuid ...PostStatusIcons __typename}fragment PostStatusIcons on Post{id name productState __typename}fragment ProductLinkFragment on Post{product{id slug name postsCount __typename}__typename}fragment UserImage on User{id name username avatarUrl __typename}fragment ComingSoonCardHomepageFragment on HomefeedPage{comingSoon{id ...UpcomingEventItemFragment __typename}__typename}fragment UpcomingEventItemFragment on UpcomingEvent{id title truncatedDescription isSubscribed post{id createdAt __typename}product{id slug postsCount followersCount followers(first:3 order:popularity excludeViewer:true){edges{node{id ...UserCircleListFragment __typename}__typename}__typename}...ProductItemFragment __typename}...FacebookShareButtonV6Fragment __typename}fragment ProductItemFragment on Product{id slug name tagline followersCount reviewsCount topics(first:2){edges{node{id slug name __typename}__typename}__typename}...ProductFollowButtonFragment ...ProductThumbnailFragment ...ProductMuteButtonFragment ...FacebookShareButtonV6Fragment ...ReviewStarRatingCTAFragment __typename}fragment ProductThumbnailFragment on Product{id name logoUuid isNoLongerOnline __typename}fragment ProductFollowButtonFragment on Product{id followersCount isSubscribed __typename}fragment ProductMuteButtonFragment on Product{id isMuted __typename}fragment FacebookShareButtonV6Fragment on Shareable{id url __typename}fragment ReviewStarRatingCTAFragment on Product{id slug name isMaker reviewsRating __typename}fragment UserCircleListFragment on User{id ...UserImage __typename}fragment ProductUpdatesCardHomepageFragment on HomefeedPage{productUpdates{id body createdAt product{id name tagline path slug ...ProductThumbnailFragment __typename}__typename}__typename}',
                }

        response = requests.post(PRODUCT_HUNT_GRAPHQL_API, json=json_data)

        r = response.json()

        iterable = r["data"]["homefeed"]["edges"][0]["node"]["items"]

        try:

                for item in iterable:
                        maindic = {}
                        dic = {}
                        if "hideVotesCount" in item:
                            dic["name"] = item["name"]
                            dic["id"] = item["id"]
                            dic["tagline"] = item["tagline"]
                            dic["votesCount"] = item["votesCount"]
                            dic["link"] = "https://www.producthunt.com/posts/" + item["slug"]
                            json_data = {
                                        'operationName': 'PostPage',
                                        'variables': {
                                            'slug': item["slug"],
                                        },
                                        'query': 'query PostPage($slug:String!$badgeTypes:[BadgesTypeEnum!]){post(slug:$slug){id slug name trashedAt isArchived product{id slug passedOnePost ...ProductPageReviewSummaryFragment ...ReviewCardFragment __typename}targetedAd(kind:"sidebar"){id ...AdFragment __typename}redirectToProduct{id slug __typename}...PostPageHeaderFragment ...PostPageDescriptionFragment ...PostPageScheduledNoticeFragment ...PostPageLaunchDayNoticeFragment ...PostPageModerationReasonFragment ...PostPageModerationToolsFragment ...PostPageBreadcrumbFragment ...PostPageAboutFragment ...PostPageGalleryFragment ...PostPageBannerFragment ...PostPageCommentPromptFragment ...StructuredDataFromPost ...MetaTags __typename}}fragment MetaTags on SEOInterface{id meta{canonicalUrl creator description image mobileAppUrl oembedUrl robots title type author authorUrl __typename}__typename}fragment StructuredDataFromPost on Post{id structuredData __typename}fragment PostPageHeaderFragment on Post{id name tagline dailyRank createdAt ...PostThumbnail ...PostStatusIcons ...PostVoteButtonFragment ...PostPageGetItButtonFragment ...PostHeaderBadgesFragment ...PostPageActionsFragment __typename}fragment PostStatusIcons on Post{id name productState __typename}fragment PostThumbnail on Post{id name thumbnailImageUuid ...PostStatusIcons __typename}fragment PostVoteButtonFragment on Post{id featuredAt updatedAt createdAt product{id isSubscribed __typename}disabledWhenScheduled hasVoted ...on Votable{id votesCount __typename}__typename}fragment PostPageGetItButtonFragment on Post{id isAvailable productState links{id redirectPath storeName websiteName devices __typename}__typename}fragment PostHeaderBadgesFragment on Post{id badges(first:3 types:$badgeTypes){edges{node{...ProductBadgeFragment __typename}__typename}__typename}__typename}fragment ProductBadgeFragment on Badge{...on TopPostBadge{id ...ProductTopPostBadgeFragment __typename}...on GoldenKittyAwardBadge{id ...ProductGoldenKittyBadgeFragment __typename}...on TopPostTopicBadge{id ...ProductTopPostTopicBadgeFragment __typename}__typename}fragment ProductTopPostBadgeFragment on TopPostBadge{id post{id name __typename}position period date __typename}fragment ProductGoldenKittyBadgeFragment on GoldenKittyAwardBadge{id year position category post{id name __typename}__typename}fragment ProductTopPostTopicBadgeFragment on TopPostTopicBadge{id __typename}fragment PostPageActionsFragment on Post{id slug userId canManage __typename}fragment PostPageDescriptionFragment on Post{id slug tagline description pricingType isArchived createdAt featuredAt ...ShareModalSubjectFragment ...PostThumbnail ...PostPromoCodeFragment product{id slug name tagline logoUuid ...CollectionAddButtonFragment __typename}topics(first:3){edges{node{id slug name __typename}__typename}totalCount __typename}__typename}fragment PostPromoCodeFragment on Post{id promo{text code __typename}__typename}fragment ShareModalSubjectFragment on Shareable{id url ...FacebookShareButtonFragment __typename}fragment FacebookShareButtonFragment on Shareable{id url __typename}fragment CollectionAddButtonFragment on Product{id name description ...ProductItemFragment __typename}fragment ProductItemFragment on Product{id slug name tagline followersCount reviewsCount topics(first:2){edges{node{id slug name __typename}__typename}__typename}...ProductFollowButtonFragment ...ProductThumbnailFragment ...ProductMuteButtonFragment ...FacebookShareButtonV6Fragment ...ReviewStarRatingCTAFragment __typename}fragment ProductThumbnailFragment on Product{id name logoUuid isNoLongerOnline __typename}fragment ProductFollowButtonFragment on Product{id followersCount isSubscribed __typename}fragment ProductMuteButtonFragment on Product{id isMuted __typename}fragment FacebookShareButtonV6Fragment on Shareable{id url __typename}fragment ReviewStarRatingCTAFragment on Product{id slug name isMaker reviewsRating __typename}fragment PostPageScheduledNoticeFragment on Post{id slug name createdAt canCreateUpcomingEvent canViewUpcomingEventCreateBtn upcomingEvent{id canEdit approved __typename}product{id name slug canEdit ...TeamRequestCTAFragment __typename}__typename}fragment TeamRequestCTAFragment on Product{id slug name websiteUrl websiteDomain isClaimed isViewerTeamMember viewerPendingTeamRequest{id __typename}__typename}fragment PostPageLaunchDayNoticeFragment on Post{id slug createdAt isMaker isHunter product{id slug __typename}__typename}fragment PostPageModerationReasonFragment on Post{id moderationReason{reason moderator{id name headline username __typename}__typename}__typename}fragment PostPageModerationToolsFragment on Post{id name slug featuredAt createdAt product{id __typename}...ModerationChangeProductFormPostFragment __typename}fragment ModerationChangeProductFormPostFragment on Post{id name primaryLink{id url __typename}product{id ...ModerationChangeProductFormProductFragment __typename}__typename}fragment ModerationChangeProductFormProductFragment on Product{id name slug tagline cleanUrl websiteUrl ...ProductThumbnailFragment __typename}fragment PostPageBreadcrumbFragment on Post{id slug name product{id slug __typename}__typename}fragment PostPageAboutFragment on Post{id name slug votesCount commentsCount dailyRank weeklyRank createdAt featuredAt canManage product{id name slug tagline reviewersCount reviewsCount followersCount firstPost{id createdAt __typename}...ProductThumbnailFragment ...ProductFollowButtonFragment ...ReviewStarRatingCTAFragment __typename}user{id name username ...UserImage __typename}makers{id name username ...UserImage __typename}topics(first:3){edges{node{id name slug __typename}__typename}__typename}__typename}fragment UserImage on User{id name username avatarUrl __typename}fragment PostPageGalleryFragment on Post{id name media{id originalHeight originalWidth imageUuid mediaType metadata{url videoId interactiveDemoId platform __typename}__typename}links{id redirectPath storeName __typename}__typename}fragment PostPageBannerFragment on Post{id isArchived featuredAt createdAt product{id slug name postsCount __typename}__typename}fragment AdFragment on Ad{id subject post{id slug name updatedAt commentsCount topics(first:3){edges{node{id slug __typename}__typename}__typename}...PostVoteButtonFragment __typename}ctaText name tagline thumbnailUuid url __typename}fragment PostPageCommentPromptFragment on Post{id name isArchived commentPrompt ...PostThumbnail __typename}fragment ProductPageReviewSummaryFragment on Product{id name slug postsCount reviewsCount reviewersCount reviewsRating isMaker reviewers(first:3){edges{node{id username name ...UserImage __typename}__typename}__typename}...ReviewCTAPromptFragment __typename}fragment ReviewCTAPromptFragment on Product{id isMaker viewerReview{id __typename}...ReviewCTASharePromptFragment __typename}fragment ReviewCTASharePromptFragment on Product{id name tagline slug ...ProductThumbnailFragment ...FacebookShareButtonFragment __typename}fragment ReviewCardFragment on Product{id name isMaker ...ReviewCTAPromptFragment __typename}',
                                    }


                            response_2 = requests.post(PRODUCT_HUNT_GRAPHQL_API, cookies=cookies, headers=headers, json=json_data)
                            response_2 = response_2.json()
                            dic["description"] = response_2["data"]["post"]["description"]

                            maindic.update(dic)
                            product_launched_today_info.append(maindic)
        except KeyError:
                    pass

                        

        return (product_launched_today_info)

def get_products_info_before_today(days: int)->list :

         '''
         This function fetches the product info (name,id,tagline,slug,url,description)
         by providing the days i.e product launches of how many days we
         want to fetch.
         :param days: sample: 5
         :return list of dictionaries: sample:[{'name':'iqoo','id': '407853', tagline: 'future is here', 'slug': 'iq_00', 'url': https://www.producthunt.com/post/iq00,'description': 'This brand is the no.1 brand in the world']
         '''
         product_info_before_today = []

         for day in range(int(days)):
                
                json_data = {
                            'operationName': 'HomePage',
                            'variables': {
                                'cursor': None,
                                'kind': 'FEATURED',
                                'filters': {},
                            },
                            'query': 'query HomePage($cursor:String$kind:HomefeedKindEnum!$filters:HomefeedFiltersInput!){homefeed(after:$cursor kind:$kind filters:$filters){kind edges{...HomefeedEdgeFragment __typename}pageInfo{hasNextPage endCursor __typename}__typename}mainBanner:banner(position:MAINFEED){id description url desktopImageUuid wideImageUuid tabletImageUuid mobileImageUuid __typename}phHomepageOgImageUrl viewer{id showHomepageOnboarding __typename}}fragment HomefeedEdgeFragment on HomefeedEdgeCustom{node{id title subtitle hideAfter date randomization items{...on Post{id hideVotesCount ...PostItemFragment featuredComment{id body:bodyText user{id ...UserImage __typename}__typename}__typename}...on Ad{id ...AdFragment __typename}__typename}...ComingSoonCardHomepageFragment ...ProductUpdatesCardHomepageFragment __typename}__typename}fragment AdFragment on Ad{id subject post{id slug name updatedAt commentsCount topics(first:3){edges{node{id slug __typename}__typename}__typename}...PostVoteButtonFragment __typename}ctaText name tagline thumbnailUuid url __typename}fragment PostVoteButtonFragment on Post{id featuredAt updatedAt createdAt product{id isSubscribed __typename}disabledWhenScheduled hasVoted ...on Votable{id votesCount __typename}__typename}fragment PostItemFragment on Post{id commentsCount name shortenedUrl slug tagline updatedAt topics(first:4){edges{node{id slug __typename}__typename}__typename}redirectToProduct{id slug __typename}launchTypesInfo{id soloMaker __typename}fundingSurvey{id bootstrapped __typename}...ProductLinkFragment ...PostThumbnail ...PostVoteButtonFragment __typename}fragment PostThumbnail on Post{id name thumbnailImageUuid ...PostStatusIcons __typename}fragment PostStatusIcons on Post{id name productState __typename}fragment ProductLinkFragment on Post{product{id slug name postsCount __typename}__typename}fragment UserImage on User{id name username avatarUrl __typename}fragment ComingSoonCardHomepageFragment on HomefeedPage{comingSoon{id ...UpcomingEventItemFragment __typename}__typename}fragment UpcomingEventItemFragment on UpcomingEvent{id title truncatedDescription isSubscribed post{id createdAt __typename}product{id slug postsCount followersCount followers(first:3 order:popularity excludeViewer:true){edges{node{id ...UserCircleListFragment __typename}__typename}__typename}...ProductItemFragment __typename}...FacebookShareButtonV6Fragment __typename}fragment ProductItemFragment on Product{id slug name tagline followersCount reviewsCount topics(first:2){edges{node{id slug name __typename}__typename}__typename}...ProductFollowButtonFragment ...ProductThumbnailFragment ...ProductMuteButtonFragment ...FacebookShareButtonV6Fragment ...ReviewStarRatingCTAFragment __typename}fragment ProductThumbnailFragment on Product{id name logoUuid isNoLongerOnline __typename}fragment ProductFollowButtonFragment on Product{id followersCount isSubscribed __typename}fragment ProductMuteButtonFragment on Product{id isMuted __typename}fragment FacebookShareButtonV6Fragment on Shareable{id url __typename}fragment ReviewStarRatingCTAFragment on Product{id slug name isMaker reviewsRating __typename}fragment UserCircleListFragment on User{id ...UserImage __typename}fragment ProductUpdatesCardHomepageFragment on HomefeedPage{productUpdates{id body createdAt product{id name tagline path slug ...ProductThumbnailFragment __typename}__typename}__typename}',
                        }

                
                response = requests.post(PRODUCT_HUNT_GRAPHQL_API, json=json_data)

                r = response.json()

                iterable = r["data"]["homefeed"]["edges"][0]["node"]["items"]

                try:

                    for item in iterable:
                        maindic = {}
                        dic = {}
                        if "hideVotesCount" in item:
                            dic["name"] = item["name"]
                            dic["id"] = item["id"]
                            dic["tagline"] = item["tagline"]
                            dic["votesCount"] = item["votesCount"]
                            dic["link"] = "https://www.producthunt.com/posts/" + item["slug"]
                            json_data = {
                                        'operationName': 'PostPage',
                                        'variables': {
                                            'slug': item["slug"],
                                        },
                                        'query': 'query PostPage($slug:String!$badgeTypes:[BadgesTypeEnum!]){post(slug:$slug){id slug name trashedAt isArchived product{id slug passedOnePost ...ProductPageReviewSummaryFragment ...ReviewCardFragment __typename}targetedAd(kind:"sidebar"){id ...AdFragment __typename}redirectToProduct{id slug __typename}...PostPageHeaderFragment ...PostPageDescriptionFragment ...PostPageScheduledNoticeFragment ...PostPageLaunchDayNoticeFragment ...PostPageModerationReasonFragment ...PostPageModerationToolsFragment ...PostPageBreadcrumbFragment ...PostPageAboutFragment ...PostPageGalleryFragment ...PostPageBannerFragment ...PostPageCommentPromptFragment ...StructuredDataFromPost ...MetaTags __typename}}fragment MetaTags on SEOInterface{id meta{canonicalUrl creator description image mobileAppUrl oembedUrl robots title type author authorUrl __typename}__typename}fragment StructuredDataFromPost on Post{id structuredData __typename}fragment PostPageHeaderFragment on Post{id name tagline dailyRank createdAt ...PostThumbnail ...PostStatusIcons ...PostVoteButtonFragment ...PostPageGetItButtonFragment ...PostHeaderBadgesFragment ...PostPageActionsFragment __typename}fragment PostStatusIcons on Post{id name productState __typename}fragment PostThumbnail on Post{id name thumbnailImageUuid ...PostStatusIcons __typename}fragment PostVoteButtonFragment on Post{id featuredAt updatedAt createdAt product{id isSubscribed __typename}disabledWhenScheduled hasVoted ...on Votable{id votesCount __typename}__typename}fragment PostPageGetItButtonFragment on Post{id isAvailable productState links{id redirectPath storeName websiteName devices __typename}__typename}fragment PostHeaderBadgesFragment on Post{id badges(first:3 types:$badgeTypes){edges{node{...ProductBadgeFragment __typename}__typename}__typename}__typename}fragment ProductBadgeFragment on Badge{...on TopPostBadge{id ...ProductTopPostBadgeFragment __typename}...on GoldenKittyAwardBadge{id ...ProductGoldenKittyBadgeFragment __typename}...on TopPostTopicBadge{id ...ProductTopPostTopicBadgeFragment __typename}__typename}fragment ProductTopPostBadgeFragment on TopPostBadge{id post{id name __typename}position period date __typename}fragment ProductGoldenKittyBadgeFragment on GoldenKittyAwardBadge{id year position category post{id name __typename}__typename}fragment ProductTopPostTopicBadgeFragment on TopPostTopicBadge{id __typename}fragment PostPageActionsFragment on Post{id slug userId canManage __typename}fragment PostPageDescriptionFragment on Post{id slug tagline description pricingType isArchived createdAt featuredAt ...ShareModalSubjectFragment ...PostThumbnail ...PostPromoCodeFragment product{id slug name tagline logoUuid ...CollectionAddButtonFragment __typename}topics(first:3){edges{node{id slug name __typename}__typename}totalCount __typename}__typename}fragment PostPromoCodeFragment on Post{id promo{text code __typename}__typename}fragment ShareModalSubjectFragment on Shareable{id url ...FacebookShareButtonFragment __typename}fragment FacebookShareButtonFragment on Shareable{id url __typename}fragment CollectionAddButtonFragment on Product{id name description ...ProductItemFragment __typename}fragment ProductItemFragment on Product{id slug name tagline followersCount reviewsCount topics(first:2){edges{node{id slug name __typename}__typename}__typename}...ProductFollowButtonFragment ...ProductThumbnailFragment ...ProductMuteButtonFragment ...FacebookShareButtonV6Fragment ...ReviewStarRatingCTAFragment __typename}fragment ProductThumbnailFragment on Product{id name logoUuid isNoLongerOnline __typename}fragment ProductFollowButtonFragment on Product{id followersCount isSubscribed __typename}fragment ProductMuteButtonFragment on Product{id isMuted __typename}fragment FacebookShareButtonV6Fragment on Shareable{id url __typename}fragment ReviewStarRatingCTAFragment on Product{id slug name isMaker reviewsRating __typename}fragment PostPageScheduledNoticeFragment on Post{id slug name createdAt canCreateUpcomingEvent canViewUpcomingEventCreateBtn upcomingEvent{id canEdit approved __typename}product{id name slug canEdit ...TeamRequestCTAFragment __typename}__typename}fragment TeamRequestCTAFragment on Product{id slug name websiteUrl websiteDomain isClaimed isViewerTeamMember viewerPendingTeamRequest{id __typename}__typename}fragment PostPageLaunchDayNoticeFragment on Post{id slug createdAt isMaker isHunter product{id slug __typename}__typename}fragment PostPageModerationReasonFragment on Post{id moderationReason{reason moderator{id name headline username __typename}__typename}__typename}fragment PostPageModerationToolsFragment on Post{id name slug featuredAt createdAt product{id __typename}...ModerationChangeProductFormPostFragment __typename}fragment ModerationChangeProductFormPostFragment on Post{id name primaryLink{id url __typename}product{id ...ModerationChangeProductFormProductFragment __typename}__typename}fragment ModerationChangeProductFormProductFragment on Product{id name slug tagline cleanUrl websiteUrl ...ProductThumbnailFragment __typename}fragment PostPageBreadcrumbFragment on Post{id slug name product{id slug __typename}__typename}fragment PostPageAboutFragment on Post{id name slug votesCount commentsCount dailyRank weeklyRank createdAt featuredAt canManage product{id name slug tagline reviewersCount reviewsCount followersCount firstPost{id createdAt __typename}...ProductThumbnailFragment ...ProductFollowButtonFragment ...ReviewStarRatingCTAFragment __typename}user{id name username ...UserImage __typename}makers{id name username ...UserImage __typename}topics(first:3){edges{node{id name slug __typename}__typename}__typename}__typename}fragment UserImage on User{id name username avatarUrl __typename}fragment PostPageGalleryFragment on Post{id name media{id originalHeight originalWidth imageUuid mediaType metadata{url videoId interactiveDemoId platform __typename}__typename}links{id redirectPath storeName __typename}__typename}fragment PostPageBannerFragment on Post{id isArchived featuredAt createdAt product{id slug name postsCount __typename}__typename}fragment AdFragment on Ad{id subject post{id slug name updatedAt commentsCount topics(first:3){edges{node{id slug __typename}__typename}__typename}...PostVoteButtonFragment __typename}ctaText name tagline thumbnailUuid url __typename}fragment PostPageCommentPromptFragment on Post{id name isArchived commentPrompt ...PostThumbnail __typename}fragment ProductPageReviewSummaryFragment on Product{id name slug postsCount reviewsCount reviewersCount reviewsRating isMaker reviewers(first:3){edges{node{id username name ...UserImage __typename}__typename}__typename}...ReviewCTAPromptFragment __typename}fragment ReviewCTAPromptFragment on Product{id isMaker viewerReview{id __typename}...ReviewCTASharePromptFragment __typename}fragment ReviewCTASharePromptFragment on Product{id name tagline slug ...ProductThumbnailFragment ...FacebookShareButtonFragment __typename}fragment ReviewCardFragment on Product{id name isMaker ...ReviewCTAPromptFragment __typename}',
                                    }


                            response_2 = requests.post(PRODUCT_HUNT_GRAPHQL_API, cookies=cookies, headers=headers, json=json_data)
                            response_2 = response_2.json()
                            dic["description"] = response_2["data"]["post"]["description"]

                            maindic.update(dic)
                            product_info_before_today.append(maindic)
                except KeyError:
                    pass

         return (product_info_before_today)

def get_hunters_and_makers_info(product_ids_list: list)-> list:

        '''
        This function fetch the names of hunters, hunter_and_makers and makers of the products.
        Product ids are passed as a list in param . Return names along with the product id
        :param simple list of ids: sample: ['402396','405815','219786','677335']
        :return list of dictionaries : sample: [{'product_id': '415815', 'hunter': 'Rohan Chaubey', 'list_of_makers': ['Sakshi Gupta', 'Kanishka Thakur', 'Snehil Saluja', 'Gaurav Rawat']}]
        '''
        hunter_and_makers_info_list = []

        try:    
                for ids in product_ids_list:
                        json_data = {
                                    'operationName': 'PostPageSocialProof',
                                    'variables': {
                                        'postId': ids,
                                        'limit': 36,
                                    },
                                    'query': 'query PostPageSocialProof($postId:ID!$limit:Int!){post(id:$postId){id contributors(limit:$limit){role user{id ...UserImage __typename}__typename}__typename}}fragment UserImage on User{id name username avatarUrl __typename}',
                                }

                        response = requests.post(PRODUCT_HUNT_GRAPHQL_API, json=json_data)
                        response = response.json()
                        hunters_and_makers_data = response["data"]["post"]["contributors"]
                        dic = {'product_id':ids}
                        makers_list = []
                        for dictionary in hunters_and_makers_data:
                                if dictionary["role"] == "hunter_and_maker":
                                    dic["hunter_and_maker"] = dictionary["user"]["name"]
                                elif dictionary["role"] == "maker":
                                    makers_list.append(dictionary["user"]["name"])
                                elif dictionary["role"] == "hunter":
                                    dic["hunter"] = dictionary["user"]["name"]
                                elif dictionary["role"] == "commenter" or dictionary["role"] == "upvoter":
                                    break
                        if len(makers_list) != 0:
                                dic["list_of_makers"] = makers_list
                        hunter_and_makers_info_list.append(dic)
        except KeyError:
                        pass

        return (hunter_and_makers_info_list)


def get_upvoters_and_commenters_info(product_ids_list: list)-> list:

        '''
        This function fetch the names of upvoters and commenters of the products.
        Product ids are passed as list in param. Return names along with product id.
        :param simple list of ids: sample: ['402396','405815','219786','677335']
        :return list of dictionaries: sample: [{'id': '419084', 'upvoters_and_commenters': ['Alexander Isora 🦄', 'Samar Ali', 'Business Marketing with Nika']}]
        '''
        upvoters_and_commenters_info_list = []

        try:
                for ids in product_ids_list:
                       

                        json_data = {
                            'operationName': 'PostPageSocialProof',
                            'variables': {
                            'postId': ids,
                            'limit': 1000,
                                        },
                            'query': 'query PostPageSocialProof($postId:ID!$limit:Int!){post(id:$postId){id contributors(limit:$limit){role user{id ...UserImage __typename}__typename}__typename}}fragment UserImage on User{id name username avatarUrl __typename}',
                                }
                        res = requests.post(PRODUCT_HUNT_GRAPHQL_API, json=json_data)
                        res = res.json()
                        upvoters_data = res["data"]["post"]["contributors"]
                        dic = {'id':ids}
                        upvoters_and_commenters_list = []
                        for dictionary in upvoters_data:
                            if dictionary["role"] == "upvoter" or dictionary["role"] == "commenter":             
                                    upvoters_and_commenters_list.append(dictionary["user"]["name"])
                        if len(upvoters_and_commenters_list) != 0:
                            dic["upvoters_and_commenters"] = upvoters_and_commenters_list
                        upvoters_and_commenters_info_list.append(dic)
        except KeyError:
            pass        

        return upvoters_and_commenters_info_list


def get_followers_ids(person_username: str,csvFilePath: str)->str:

    '''
    This function fetch the ids of all the persons that follow the person_username,that person_username
    is taken as param. It also take an empty csv file path which will contain all those ids at the 
    end of the function and will return this file
    :param person_username, csvFilePath :sample "prateek_ghanghas", followings.csv
    :return csv file path :sample followings.csv
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

    df = pd.DataFrame(id_lst, columns = ["person id"])
    df.to_csv(csvFilePath, index = False)
    return csvFilePath

def get_followings_ids(person_username: str,csvFilePath: str)->str:

    '''
    This function fetch the ids of all the persons followed by person_username,that person_username
    is taken as param. It also take an empty csv file path which will contain all those ids at the 
    end of the function and will return this file
    :param person_username, csvFilePath :sample "prateek_ghanghas", followings.csv
    :return csv file path :sample followings.csv
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
            'username': person_username,
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

    df = pd.DataFrame(id_lst, columns = ["person id"])
    df.to_csv(csvFilePath, index = False)
    return csvFilePath

def follow_a_person(person_id: int)->bool:

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
      
def follow_list_of_ids(filePath: str)->bool :

    '''
    This function follow all the persons by providing theirs ids which is done
    by passing a csv file which contain ids of those persons.Returns True when all the persons are followed.
    :param filepath: sample: person_ids.csv
    :return boolean value: sample: True
    '''

    df = pd.read_csv(filePath)

    count = 0

    while(True):

        for index,row in df.iterrows():
            time.sleep(5)
            if(follow_a_person(int(row["person id"]))):
                    count += 1
                    df = df.drop(index)
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

def unfollow_a_person(person_id: int)->bool :
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

def get_non_followbacks_ids(person_username: str, non_followback_filePath:str)->str:

        '''
        This function fetches ids of all the persons who don't followback the 
        person_username , that person_username taken as param . It also takes
        another param which is a csv file path which will contain all those ids
        at the end of this function
        :param person_username, non_followback_filePath :sample "prateek_ghanghas", non-followback.csv
        :return csv file path :sample non-followback.csv
        '''

        follower_file_path = get_followers_ids(person_username,"followers.csv")

        following_file_path = get_followings_ids(person_username,"followings.csv")

        df_followers = pd.read_csv(follower_file_path)
        df_followings = pd.read_csv(following_file_path)
        df_followers['person id'] = df_followers['person id'].astype(str)
        df_followings['person id'] = df_followings['person id'].astype(str)
        follower_list = df_followers["person id"].tolist()
        following_list = df_followings["person id"].tolist()

        non_followback_list = []

        for ids in following_list:
              if ids not in follower_list:
                    non_followback_list.append(ids)

        df = pd.DataFrame(non_followback_list, columns = ["non_followback_ids"])

        df.to_csv(non_followback_filePath, index = False)
        return non_followback_filePath

def unfollow_non_followbacks(person_username: str)->bool:
      
      '''
      This function unfollow all the persons who doesn't follow back the person_username ,
      that person_username is taken as param.Return True if the task is successful.
      :param person_username: sample: "prateek_ghannghas"
      :return boolean value: sample: True
      '''
      
      non_followback_filePath = get_non_followbacks_ids(person_username,"non_followback.csv")

      df = pd.read_csv(non_followback_filePath)
      df["non_followback_ids"] = df["non_followback_ids"].astype(str)

      for index,row in df.iterrows():
                  unfollow_a_person(row['non_followback_ids'])
                  delay = random.randrange(5, 10)
                  time.sleep(delay)
                  df = df.drop(index)
                  if(df.empty):
                     print("All the persons are unfollowed")
                     return True
                  
def comment_on_products_launched_today(days: int)->bool:
      
        '''
        This function creates comments on the product pages . it takes
        days as param which tells the no. of days so that it comments on
        products launched on those days. Returns True if the task is 
        successful.
        :param days: sample: 5
        :return boolean value: sample: True
        '''

        list = get_product_info_today() + get_products_info_before_today(days)

        for dic in list:
                string = f"Congrats team {dic['name']} on your launch!"

                if(create_comment(dic["id"],string)):

                     time.sleep(random.randrange(5,10))
                else:
                      return False
        return True             

def create_comment(product_id: int, comment: str)->bool :
        
        '''
        This function create a comment on the product page by taking product id
        and comment as a string . Returns True if sucessful.
        :param product_id, comment: sample: 4277198, "congrats on launch"
        :return boolean value: sample: True
        '''
        json_data = {
            'operationName': 'CommentCreateWithPoll',
            'variables': {
                'commentsThreadRepliesCursor': '',
                'input': {
                    'subjectId': product_id,
                    'subjectType': 'Post',
                    'body': comment,
                    'inputInfo': 'jQ1NjExOTgJTdCJTIydHMlMjIlM0EzLjM0JTJDJTIydGQlMjIlM0E0NDA2JTJDJTIyZmQlMjIlM0ExMjk4NyUyQyUyMnN2JTIyJTNBMjM3MTMlMkMlMjJzZiUyMiUzQTEwNzI2JTJDJTIycHYlMjIlM0ElMjIlMjIlN0Q=',
                    'pollOptions': None,
                    'reviewRating': 0,
                },
            },
            'query': 'mutation CommentCreateWithPoll($commentsThreadRepliesCursor:String=""$includeThreadForCommentId:ID$input:CommentCreateInput!){response:commentCreate(input:$input){node{id subject{id ...on Commentable{id commentsCount __typename}__typename}...CommentsThreadFragment __typename}errors{field messages __typename}__typename}}fragment CommentsThreadFragment on Comment{id isSticky replies(first:5 after:$commentsThreadRepliesCursor focusCommentId:$includeThreadForCommentId){totalCount edges{node{id ...CommentFragment __typename}__typename}pageInfo{endCursor hasNextPage __typename}__typename}...CommentFragment __typename}fragment CommentFragment on Comment{id award badges body bodyHtml canEdit canViewReplyBtn canDestroy canAward createdAt isHidden path isSticky score inputInfo{id failedChecks{kind title __typename}pastedIndex pastedValue __typename}awardOptions{option __typename}repliesCount subject{id ...on Post{id commentAwardsCount __typename}...on Commentable{id __typename}__typename}user{id headline name firstName username headline ...ComingSoonUserBadgeFragment ...UserImage ...KarmaBadgeFragment ...TopReviewerBadgeFragment __typename}poll{...PollFragment __typename}review{id __typename}...CommentVoteButtonFragment ...FacebookShareButtonFragment __typename}fragment CommentVoteButtonFragment on Comment{id ...on Votable{id hasVoted votesCount __typename}__typename}fragment FacebookShareButtonFragment on Shareable{id url __typename}fragment UserImage on User{id name username avatarUrl __typename}fragment KarmaBadgeFragment on User{id karmaBadge{kind score __typename}__typename}fragment PollFragment on Poll{id answersCount hasAnswered options{id text imageUuid answersCount answersPercent hasAnswered __typename}__typename}fragment ComingSoonUserBadgeFragment on User{id promotableUpcomingEvent{id __typename}__typename}fragment TopReviewerBadgeFragment on User{id isTopReviewer __typename}',
        }

        response = requests.post(PRODUCT_HUNT_GRAPHQL_API, cookies=cookies, headers=headers, json=json_data)

        if response.status_code == 200:
              return True
        else:
              return False
        
def get_streakers_usernames(rounds):

    '''
    This function fetches the usernames of top streakers and return a list with usernames in it.
    It takes one param that is rounds which decides info of how many top streakers we want . In one round
    it fetches 20 top streakers . In next round it will fetch next 20 streakers and so on 
    :params no. of rounds :sample 5
    :return list :sample ['Ankit Sharma', 'Kevin T.']
    '''

    json_data = {
    'operationName': 'VisitStreaksPage',
    'variables': {},
    'query': 'query VisitStreaksPage($cursor:String){visitStreaks(first:20 after:$cursor){edges{node{id ...VisitStreakItemFragment __typename}__typename}pageInfo{endCursor hasNextPage __typename}__typename}}fragment VisitStreakItemFragment on VisitStreak{id duration emoji user{id name ...UserImage ...UserFollowButtonFragment __typename}__typename}fragment UserImage on User{id name username avatarUrl __typename}fragment UserFollowButtonFragment on User{id followersCount isFollowed __typename}',
}

    response = requests.post('https://www.producthunt.com/frontend/graphql', json=json_data)

    response = response.json()

    data = response["data"]["visitStreaks"]["edges"]
    username_list = []

    for edges in data:

        username_list.append(edges["node"]["user"]["username"])

    endCursor = response["data"]["visitStreaks"]["pageInfo"]["endCursor"]

    for round in range(rounds-1):

        json_data = {
        'operationName': 'VisitStreaksPage',
        'variables': {
            'cursor': endCursor,
        },
        'query': 'query VisitStreaksPage($cursor:String){visitStreaks(first:20 after:$cursor){edges{node{id ...VisitStreakItemFragment __typename}__typename}pageInfo{endCursor hasNextPage __typename}__typename}}fragment VisitStreakItemFragment on VisitStreak{id duration emoji user{id name ...UserImage ...UserFollowButtonFragment __typename}__typename}fragment UserImage on User{id name username avatarUrl __typename}fragment UserFollowButtonFragment on User{id followersCount isFollowed __typename}',
        }

        response = requests.post('https://www.producthunt.com/frontend/graphql', json=json_data)

        response = response.json()

        data = response["data"]["visitStreaks"]["edges"]

        endCursor = response["data"]["visitStreaks"]["pageInfo"]["endCursor"]

        for edges in data:

            username_list.append(edges["node"]["user"]["username"])

    return(username_list)


def get_streakers_data(twitter_links_csv: str, rounds: int)->list:

    '''
    This function fetches the info(name,id,VisitStreaks,twitter-links) about top streakers.
    It takes two params . one is csv file path to save the twitter links of streakers if available
    and the other is rounds that decide info of how many top streakers we want . In one round
    it fetches 20 top streakers
    :params csv file, no. of rounds :sample twitter_links.csv, 5
    :return list of dictionary :sample [{'id': '2530835', 'name': 'Ankit Sharma', 'visitStreaks': 711}, {'id': '2262689', 'name': 'Kevin T.', 'visitStreaks': 711}]
    '''

    username_list = get_streakers_usernames(rounds)

    streaker_info = []

    twitter_links = []


    for username in username_list:
           try:
                json_data = {
                'operationName': 'ProfileLayoutQuery',
                'variables': {
                    'username': username,
                },
                'query': 'query ProfileLayoutQuery($username:String!){profile:user(username:$username){id isTrashed productsCount submittedPostsCount collectionsCount followersCount followingsCount collectionsCount username ...ProfileLayoutHeaderFragment __typename}}fragment ProfileLayoutHeaderFragment on User{id headline headerUuid isFollowingViewer isMaker isViewer name twitterUsername username visitStreak{emoji duration __typename}...KarmaBadgeFragment ...UserImage ...UserFollowButtonFragment ...UserStackPreviewFragment __typename}fragment UserImage on User{id name username avatarUrl __typename}fragment UserFollowButtonFragment on User{id followersCount isFollowed __typename}fragment KarmaBadgeFragment on User{id karmaBadge{kind score __typename}__typename}fragment UserStackPreviewFragment on User{id username stacksCount stacks(first:3){edges{node{id product{id slug ...ProductThumbnailFragment __typename}__typename}__typename}__typename}__typename}fragment ProductThumbnailFragment on Product{id name logoUuid isNoLongerOnline __typename}',
            }

                response = requests.post('https://www.producthunt.com/frontend/graphql', json=json_data)
                response = response.json()
                dic = {}
                dic["id"] = response["data"]["profile"]["id"]
                dic["name"] = response["data"]["profile"]["name"]
                if response["data"]["profile"]["twitterUsername"] != "" and response["data"]["profile"]["twitterUsername"] != None:
                       dic["twitter"] = f'https://X.com/{response["data"]["profile"]["twitterUsername"]}'
                       twitter_links.append(dic["twitter"])
                dic["visitStreaks"] = response["data"]["profile"]["visitStreak"]["duration"]
                streaker_info.append(dic)

           except KeyError:
                      pass

    df = pd.DataFrame(twitter_links, columns = ["twitterUrl"])
    df.to_csv(twitter_links_csv, index = False)
    return streaker_info

if __name__ == "__main__":
      print("Hello, world")
