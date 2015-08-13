# Python Library for Zoho CRM API

## Install

    pip install zohocrm

or from source:

    git clone git@github.com:Blitzen/zohocrm.git

## Overview

    from zohocrm import API

    api = API(auth_token="Your Auth Token")
    api.get_records()
    # Stuff is returned
