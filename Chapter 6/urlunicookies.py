#Program to fetch URL five times and grab/display each unique cookie
#Uses the user created anon_browser class
#Chapter 6 converted Python2 to Python3

from anon_browser import AnonBrowser

ab = AnonBrowser(user_agents=['User-agent', 'superSecretBrowser'])

for attempt in range(1, 6):
    ab.anonymize()
    print('[*] Fetching page')
    response = ab.open('http://www.yahoo.com')
    for cookie in ab.cookie_jar:
        print(cookie)
