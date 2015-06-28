# import stuff
from __future__ import print_function
import math
import random
import re
import sys
import time
#import json, httplib
from enum import Enum
from operator import attrgetter
from pprint import pprint

# Import custom modules, mostly from GitHub
#from firebase import Firebase # https://github.com/mikexstudios/python-firebase
import names # https://github.com/treyhunner/names
from bs4 import BeautifulSoup

# Import ParsePy stuff. ParsePy makes using Parse in Python much easier.
from parse_rest.connection import ParseBatcher, register, SessionToken
from parse_rest.datatypes import Function, Object, ACL
from parse_rest.role import Role
from parse_rest.user import User

# Calling "register" allows parse_rest / ParsePy to work.
# - register(APPLICATION_ID, REST_API_KEY, optional MASTER_KEY)
register("AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", 
     "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS", 
     master_key = "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv"
  )

"""


Instance members of a Question():

    objectId = String = "F*3ng3.rh" (from Parse)
    num = Int = 1234
    serial = String = "01234"
    ID = String = "Question_01234"
    text = String
    image = String = the URL where it lives
    category = any of 1 2 3 4
    real_answer = String or None
    num_blanks = 0, 1, 2
    num_answers = 2-10
    li_a_cats = [one of 1-9] * num_answers  
    li_a_tenses = [one of 1-]
    li_a_serials
    str_a_cats
    str_a_tenses
    str_a_serials


Question Categories:

    1 = question
    2 = statement
    3 = quote
    4 = lyrics

Question Tags:




# Answer Categories:
# (Tenses should take care of these)

#     1 = person
#     2 = place
#     3 = thing
#     4 = animal
#     5 = verb
#     6 = adjective
#     7 = interjection
#     8 = other
#     9 = any

Answer Tenses:

    1.1 = person - singular
    1.2 = person - plural

    2.1 = place - singular
    2.2 = place - plural

    3.1 = thing - singular
    3.2 = thing - plural

    4.1 = animal - singular
    4.2 = animal - plural

    5.1 = verb - simple (run)
    5.2 = verb - past (ran)
    5.3 = verb - continuous (running)

    6.1 = adjective - adjective
    6.2 = adjective - adverb

    7.1 = interjection - none

    8.1 = other - none

    9.1 = any - none

"""



class Category(Enum):
    
    Question = 1
    Quote = 2
    Statement = 3
    
    pass


# for Parse
class Question(Object):
    pass



# for here
class _Question(Object):

    LIQ = [] # holds Questions
    LI_Q = [] # holds _Questions
    NUM = 1
    LI_ATTR = [
        "objectId", "num", "serial", "ID", "text", "image", "category", 
        "real_answer", "num_blanks", "num_answers", "li_a_cats", "li_a_tenses", 
        "li_a_serials", "str_a_cats", "str_a_tenses", "str_a_serials", "li_attr"
        ]

    def __init__(self,
        objectId = "",
        num = 0,
        serial = "",
        ID = "",
        text = "",
        image = "",
        category = "",
        real_answer = "",
        num_blanks = 0,
        num_answers = 0,
        li_a_cats = [10,24,1988],
        li_a_tenses = [],
        li_a_serials = [],
        str_a_cats = "",
        str_a_tenses = "",
        str_a_serials = ""
        ):

        self.objectId = objectId       
        self.num = _Question.NUM
        self.serial = get_serial(n = self.num, length_desired = 5)
        self.ID = get_id(prefix=self.__class__.__name__[1:], serial=self.serial) 
        self.text = text
        self.image = image
        self.category = category
        self.real_answer = real_answer
        self.num_blanks = num_blanks
        self.num_answers = num_answers
        self.li_a_cats = li_a_cats
        self.li_a_tenses = li_a_tenses
        self.li_a_serials = li_a_serials
        self.str_a_cats = str_a_cats
        self.str_a_tenses = str_a_tenses
        self.str_a_serials = str_a_serials
        self.li_attr = _Question.LI_ATTR

        _Question.NUM += 1

        pass

    def make_Parse_Object(self):
        return Question(
            num = self.num,
            serial = self.serial,
            ID = self.ID,
            text = self.text,
            image = self.image,
            category = self.category,
            num_blanks = self.num_blanks,
            num_answers = self.num_answers,
            li_a_cats = self.li_a_cats,
            li_a_tenses = self.li_a_tenses,
            li_a_serials = self.li_a_serials,
            str_a_cats = self.str_a_serials,
            str_a_tenses = self.str_a_tenses,
            str_a_serials = self.str_a_serials,
            li_attr = self.li_attr
            )

    def __iter__(self):
        # first start by grabbing the Class items
        iters = dict((x,y) for x,y in self.__class__.__dict__.items() 
            if x[:2] != '__' 
                and x not in set(["LIA", "LI_A", "NUM", "LI_FILENAMES", "LI_ATTR"])
                and x not in set(["make_Parse_Object", "get_li_attributes"])
                and x not in set(["ENDPOINT_ROOT", "Query"])
            )
        # then update the class items with the instance items
        iters.update(self.__dict__)
        # now 'yield' through the items
        for x,y in iters.items():
            yield x,y

    pass



def get_serial(n, length_desired): # no prefix
    return "{}{}".format("0"*(length_desired - len(str(n))), n)

def get_id(prefix, serial):
    return "{}_{}".format(prefix, serial)



# Make Question objects by reading <my_questions.txt>.
def make_questions(filename = "/Users/achick/Google_Drive_Alex/Daeious/ParseCloudCode/cloud/my_questions/my_questions.txt"):
    # Get rid of newline chars ("\n").
    lines = [line.strip('\n') for line in open(filename) if line[0] != "#" and line != "\n"]
    # For now, get rid of anything in parentheses.
    lines = [line.split(" (")[0] for line in lines]
    # Each line in lines is now a question's text and nothing extra.
    ### pprint(lines)
    # Create _Question and Question objects and put them in the class lists
    _Question.LI_Q = [_Question(
        text = line,
        num_blanks = line.count("___")
        ) for line in lines]

    # _Question.LIQ = [q.make_Parse_Object() for q in _Question.LI_Q]
    # _Question.LIQ.sort(key = attrgetter("num"))
    print(len(_Question.LI_Q), "_Questions exist here.")

    return sorted([q.make_Parse_Object() for q in _Question.LI_Q],
                  key = attrgetter("num"))



def put_questions_in_Parse():

    # Query for Questions
    queryset = list(Question.Query.all().limit(1000))
    while True:
        if not queryset:
            print("No Questions to delete from Parse -- none exist.")
            break
        elif len(queryset) == len(_Question.LI_Q):
            print("{} Questions already exist in Parse.".format(len(queryset)))
            srsly_delete_stuff = raw_input("Continue with delete anyway? (Y/n): ")
            if srsly_delete_stuff != "Y":
                print("Delete skipped. Upload skipped.")
                return
        else:
            print("There are {} Questions to delete from Parse.".format(len(queryset)))
            srsly_delete_stuff = raw_input("Delete Questions from Parse? (Y/n): ")
            if srsly_delete_stuff != "Y":
                print("Delete skipped. Upload skipped.")
                return

        # batch_delete in chunks of no more than 50
        batcher = ParseBatcher()
        lili_chunks = [queryset[i:i+50] for i in range(0, len(queryset), 50)]
        for index, chunk in enumerate(lili_chunks):
            batcher.batch_delete(chunk)
            print("\r{} of {} Questions deleted from Parse".format(50*(index+1), len(queryset)), end = "\r")
            sys.stdout.flush()
        print
        break

    # batch_save in chunks of no more than 50
    len_li_q = len(_Question.LIQ)
    batcher = ParseBatcher()
    lili_chunks = [_Question.LIQ[i:i+50] for i in range(0, len_li_q, 50)]
    for index, chunk in enumerate(lili_chunks):
        batcher.batch_save(chunk)
        print("\r{} of {} Questions uploaded to Parse".format(50*(index+1), len_li_q), end = "\r")
        sys.stdout.flush()
    print
    pass


def main():
    make_questions()
    put_questions_in_Parse()

    [print(enum, enum.name, enum.value) for enum in Category]
    
    print([enum.name for enum in Category if enum.value == 1][0])

    pass

if __name__ == '__main__':
    status = main()
    sys.exit(status)





























