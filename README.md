# linkedin-connect-bot

## Prerequisite

1. Make sure you already install python [here](https://www.python.org/downloads/)
2. Install chrome webdriver [here](https://developer.chrome.com/docs/chromedriver/downloads)
3. Install required library ([requirements.txt](./requirements.txt))

## How to use

### Add connection from people that like a post

1. Copy and paste `.env.example` into `.env`
2. Fill the variable in `.env`
   - For `LI_AT`, you can look at the cookie in your browser that already logged-in your LinkedIn account
   - `TARGET_URL` is the url of a LinkedIn post which you want to connect the reactors/people who engage to that post
3. Run `python from_like.py`
