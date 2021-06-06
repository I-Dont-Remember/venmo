from venmo_api import Client
# https://github.com/mmohades/Venmo

print("Login using account to get an access token for the API.")
email = input('Venmo Email:')
if '@' not in email:
    print('! yo what the heck you sure thats an email')
    raise SystemExit

password = input('Venmo Password:')

# Don't necessarily need to complete 2FA
Client.get_access_token(username=email, password=password)
###### Output #######
# IMPORTANT: Take a note of your device-id to avoid 2-factor-authentication for your next login.
# device-id: <id>
# IMPORTANT: Your Access Token will NEVER expire, unless you logout manually (client.log_out(token)).
# Take a note of your token, so you don't have to login every time.

# Successfully logged in. Note your token and device-id
# access_token: <token>
# device-id: <id>
