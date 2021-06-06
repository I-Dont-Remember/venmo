# Recurring & Scheduled Venmo

Inspired by [Joe Previte's recurring Venmo script](https://joeprevite.com/send-automatic-recurring-payments-on-venmo), I wanted my own.
Venmo deprecated new sign ups with access tokens through the `Settings->Developer` page of the account [described in their docs](https://venmo.com/gettingstarted/createapp), but the handy dandy library from [mmohades](https://github.com/mmohades/Venmo) still has the ability to login and get credentials to access as of 06/2021.

Trying to keep things simple to start, but would like to expand it and make it much easier to use. Spreading this widely might be against the wishes of Venmo, will have to be not dumb with it.

## User IDs

You can't just request payment based on a given username, you have to search for it and then get the Venmo user id for it. If you don't care about extra calls to the API you can let it search each time, otherwise you can run it once locally and store them somewhere.

```python
user = venmo_client.user.get_user_by_username(username)
print(user)
venmo_client.payment.request_money(amount, note, target_user_id=user.id, privacy_setting=PaymentPrivacy.PRIVATE)
```

## Alternative Option for Recurring Venmo

Venmo does have the option for payment links if you don't want to deal with the fuss of OAuth and having to safeguard credentials, more information can be found [here](https://venmo.com/paymentlinks). Only thing needed to be automated with these is sending out the links to the list of recipients, and there are a million options for that from GitHub Actions, Autocode, Zapier, Integromat, etc.

```text
# Example from Venmo docs
Suggested payment with no recipient:
https://venmo.com/?txn=pay&amount=3.25&note=for+a+latte

Charge multiple recipients for dinner:
https://venmo.com/?txn=charge&amount=23.25&note=for+dinner&recipients=hamilton@venmo.com,646.863.9557,john
```

### Pros

* Recipients can be username, phone, or email.
* Creates a link which deeplinks into the Venmo app with the charge pulled up; so it's almost as good as automated charge.

### Cons

* Considering the Venmo API has the same endpoint for sending & requesting money, it's not easy to reduce the risk involved with working with their API even if you use OAuth scopes instead of your personal access token. For anything meant to be used beyond the builder themselves, this seems like the better path. Too much risk involved with safeguarding tokens which can send money to anyone vs saving the convenience of requesting manually. Asymmetric risk in the wrong direction.

## Sandbox

Haven't used it yet, but they have a Sandbox account you can interact with, though the endpoint is different. No idea if this is functional,  [Official docs link](https://venmo.com/resources/sandbox).

## Notifications

the [notifiers](https://notifiers.readthedocs.io/en/latest/index.html) library has a lot of good options and is well made, have used in other projects, but in this case none of it's options work for me off the bat. If I was going to expand this, I would use [Popcorn notify](https://popcornnotify.com/) since $0.01 per message isn't a bad deal if it's so easy to add to your project and it supports a solo developer.

I can't use Zapier for now because they made webhooks a Premium feature you have to pay to use :(.

Instead I have set up with [IFTTT](https://ifttt.com/home) a webhook that sends myself a text with a message defined in the body of the webhook, [like so](https://help.ifttt.com/hc/en-us/articles/115010230347-Webhooks-service-FAQ). This is super simple to add to any project and will probably be my go to in the future for simple scripts.
