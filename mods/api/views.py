""" Main views.py for api module """
# -*- coding: utf-8 -*-
from mods.api import config
from connexion import Api as cnxn_api

# Define APIs (as Flask Blueprints)
api_v2 = cnxn_api(config.API_V2,
                  arguments={'title': 'MalwareScan API'},
                  options={"swagger_ui": False},
                  strict_validation=True,
                  validate_responses=True).blueprint
api_v3 = cnxn_api(config.API_V3,
                  arguments={'title': 'MalwareScan API'},
                  options={"swagger_ui": False},
                  strict_validation=True,
                  validate_responses=True).blueprint
blueprints = [api_v3, api_v2]
