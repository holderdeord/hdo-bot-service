# Bot Service

[![Build Status](https://travis-ci.org/holderdeord/hdo-bot-service.svg?branch=master)](https://travis-ci.org/holderdeord/hdo-bot-service)
[![codecov](https://codecov.io/gh/holderdeord/hdo-bot-service/branch/master/graph/badge.svg)](https://codecov.io/gh/holderdeord/hdo-bot-service)

## Requirements

For Facebook you need to setup a page and an app. You can follow the guide [here](https://developers.facebook.com/docs/messenger-platform/guides/quick-start/).

## Install
    python3 -m venv venv
    . venv/bin/activate
    pip install -U pip wheel
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver

## Configure
Relevant settings:

    FACEBOOK_PAGE_ID
    FACEBOOK_APP_ID
    FACEBOOK_APP_ACCESS_TOKEN
    FACEBOOK_APP_VERIFICATION_TOKEN
    GOOGLE_OAUTH2_CLIENT_ID
    GOOGLE_OAUTH2_CLIENT_SECRET
    GOOGLE_SPREADSHEET_ID
    BASE_URL
    ALLOWED_HOSTS
    MANUSCRIPT_API_ALLOW_ANY

## Development
    # Quiz styles
    cd quiz/static/quiz
    yarn
    npm run styles
    npm run watch
    
## Import promises
    # From CSV-file
    python manage.py sync_promises --check-file FILE
    # From Google Spreadsheet (needs configuration)
    python manage.py sync_promises --google

## Deployment
    fab deploy  # You need your SSH-key on the server first

Also see [puppet/README.md](./puppet/README.md)
