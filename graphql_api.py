import requests

json_data = {
    'operationName': 'HomePage',
    'variables': {
        'cursor': '0-50',
        'kind': 'FEATURED',
        'filters': {},
    },
    'query': 'query HomePage($cursor:String$kind:HomefeedKindEnum!$filters:HomefeedFiltersInput!){homefeed(after:$cursor kind:$kind filters:$filters){kind edges{node{id title subtitle hideAfter date randomization items{...on Post{id hideVotesCount ...PostItemFragment featuredComment{id body:bodyText user{id ...UserImage __typename}__typename}__typename}...on DiscussionThread{id ...DiscussionHomepageItemFragment __typename}...on AnthologiesStory{id ...StoryHomepageItemFragment __typename}...on Ad{id ...AdFragment __typename}...on Collection{id ...CollectionHomepageItemFragment __typename}__typename}...ComingSoonCardHomepageFragment __typename}__typename}pageInfo{hasNextPage endCursor __typename}__typename}mainBanner:banner(position:MAINFEED){id description url desktopImageUuid wideImageUuid tabletImageUuid mobileImageUuid __typename}phHomepageOgImageUrl viewer{id showHomepageOnboarding __typename}}fragment AdFragment on Ad{id subject post{id slug name updatedAt commentsCount topics(first:1){edges{node{id name __typename}__typename}__typename}...PostVoteButtonFragment __typename}ctaText name tagline thumbnailUuid url __typename}fragment PostVoteButtonFragment on Post{id featuredAt updatedAt createdAt product{id isSubscribed __typename}disabledWhenScheduled hasVoted ...on Votable{id votesCount __typename}__typename}fragment PostItemFragment on Post{id commentsCount name shortenedUrl slug tagline updatedAt pricingType topics(first:1){edges{node{id name slug __typename}__typename}__typename}redirectToProduct{id slug __typename}...PostThumbnail ...PostVoteButtonFragment __typename}fragment PostThumbnail on Post{id name thumbnailImageUuid ...PostStatusIcons __typename}fragment PostStatusIcons on Post{id name productState __typename}fragment UserImage on User{id name username avatarUrl __typename}fragment DiscussionHomepageItemFragment on DiscussionThread{id title descriptionText slug commentsCount user{id firstName username avatarUrl name headline isMaker isViewer badgesCount badgesUniqueCount karmaBadge{kind score __typename}__typename}discussionCategory:category{id name slug __typename}...DiscussionThreadItemVote __typename}fragment DiscussionThreadItemVote on DiscussionThread{id hasVoted votesCount __typename}fragment StoryHomepageItemFragment on AnthologiesStory{id slug title description minsToRead commentsCount ...StoryVoteButtonFragment storyCategory:category{name slug __typename}author{id username firstName avatarUrl name headline isMaker isViewer badgesCount badgesUniqueCount karmaBadge{kind score __typename}__typename}__typename}fragment StoryVoteButtonFragment on AnthologiesStory{id hasVoted votesCount __typename}fragment CollectionHomepageItemFragment on Collection{id slug name collectionTitle:title description user{id name username __typename}...CollectionsThumbnailsFragment __typename}fragment ProductThumbnailFragment on Product{id name logoUuid isNoLongerOnline __typename}fragment CollectionsThumbnailsFragment on Collection{products(first:1){edges{node{id ...ProductThumbnailFragment __typename}__typename}__typename}__typename}fragment ComingSoonCardHomepageFragment on HomefeedPage{comingSoon{id ...UpcomingEventItemFragment __typename}__typename}fragment UpcomingEventItemFragment on UpcomingEvent{id title truncatedDescription isSubscribed post{id createdAt __typename}product{id slug postsCount followersCount followers(first:3 order:popularity excludeViewer:true){edges{node{id ...UserCircleListFragment __typename}__typename}__typename}...ProductItemFragment __typename}...FacebookShareButtonV6Fragment __typename}fragment ProductItemFragment on Product{id slug name tagline followersCount reviewsCount topics(first:2){edges{node{id slug name __typename}__typename}__typename}...ProductFollowButtonFragment ...ProductThumbnailFragment ...ProductMuteButtonFragment ...FacebookShareButtonV6Fragment ...ReviewStarRatingCTAFragment __typename}fragment ProductFollowButtonFragment on Product{id followersCount isSubscribed __typename}fragment ProductMuteButtonFragment on Product{id isMuted __typename}fragment FacebookShareButtonV6Fragment on Shareable{id url __typename}fragment ReviewStarRatingCTAFragment on Product{id slug name isMaker reviewsRating __typename}fragment UserCircleListFragment on User{id ...UserImage __typename}',
}

response = requests.post('https://www.producthunt.com/frontend/graphql', json=json_data)

r = response.json()

iterable = r["data"]["homefeed"]["edges"][0]["node"]["items"]
info = []

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

print(info)

