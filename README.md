# Quiz Service

[![Build Status](https://travis-ci.org/holderdeord/hdo-quiz-service.svg?branch=master)](https://travis-ci.org/holderdeord/hdo-quiz-service)
[![codecov](https://codecov.io/gh/holderdeord/hdo-quiz-service/branch/master/graph/badge.svg)](https://codecov.io/gh/holderdeord/hdo-quiz-service)

## Requirements

* Facebook app

## Install
    python3 -m venv venv
    . venv/bin/activate
    pip install -U pip wheel
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver

    
## Import
    # From CSV-file
    python manage.py sync_promises --check-file FILE
    # From Google Spreadsheet (needs configuration)
    python manage.py sync_promises --google
    
## Configure
