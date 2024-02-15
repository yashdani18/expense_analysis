import requests

from splitwise import Splitwise

s = Splitwise('RiCoq0a4P0LElEalLWPmAY8jyNemofZdchMrCg2D', 'voYEUHvKFZabQWa9MotzGII0GcGPlPB3OybvrTyo')

# url, oauth_token_secret = s.getAuthorizeURL()
# #
# print(url, oauth_token_secret)
#
# response = requests.get(url).text

# print(response)

# access_token = s.getAccessToken('IRGe3HuRued53Gekyiwc4hIByY8SJFjQYnCkuLPq', 'ph8pH01Kar8mDuNyxLCzAFOrrhkVNlUpxvTkgHdE', 'pDiH1EclXOtEHu7J2Inf')
#
# print(access_token)
#
# s.setAccessToken(access_token)
# user = s.getCurrentUser()
#
# print(user)

url, state = s.getOAuth2AuthorizeURL("http://localhost:3000/")

print(url, state)

# access_token = s.getOAuth2AccessToken('JllVeD9wdk5C5hrjWYVA', 'https://yashdani27.github.io/')

# access_token = s.getOAuth2AccessToken('6JatUQolu6bqtag7VSO4', 'https://yashdani27.github.io/')

# 6JatUQolu6bqtag7VSO4


