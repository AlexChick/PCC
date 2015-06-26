
# The code below main() allows this to be run with either of these commands:

# As-MacBook-Air:my_answers achick$ python update_in_Parse.py
# As-MacBook-Air:Questions_and_Answers achick$ python -m my_answers.update_in_Parse


# Import stuff.


from __future__ import print_function # allows Python-3 style printing. Must be first import.

#import backoff # Not sure if needed or working.

# import Python modules
import itertools
import logging
import math
import random
import re
import sys
import time


from enum import Enum # Do I need to use Enums?
import flufl # a better(?) type of enum. To use, make a class be a subclass of flufl.enum.Enum

# Allows sorting by value of attribute of key string name.
# (ex) sorted([o for o in li], key = attrgetter("num")) --> list
# For getting a value of a single object's attribute, use getattr() like so:
# (ex) getattr(o, "num") --> value of "num" (o.num)
# attrsetter also exists. Currently unused.
from operator import attrgetter, attrsetter

# For flat list and dictionary printing.
from pprint import pprint

# For interacting with Parse through its API (not ParsePy); 
# I'm using the API directly for cloud code and background jobs. 
# See https://www.parse.com/docs/rest/guide#cloud-code.
import json, httplib

# Not sure if needed.
import requests

# Import custom modules, mostly from GitHub
from firebase import Firebase # https://github.com/mikexstudios/python-firebase
import names # https://github.com/treyhunner/names

# Import ParsePy stuff. ParsePy makes using Parse in Python much easier.
from parse_rest.connection import ParseBatcher, register, SessionToken
from parse_rest.datatypes import Function, Object, ACL
from parse_rest.role import Role
from parse_rest.user import User

# Import my own modules.
from upload_my_answers_to_Parse import make_answers

# Calling "register" allows parse_rest / ParsePy to work.
# - register(APPLICATION_ID, REST_API_KEY, optional MASTER_KEY)
register("AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", 
         "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS", 
         master_key = "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv"
         )

################################################################################

class Answer(Object):

	def make_object(self):



	pass





















