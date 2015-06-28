# import stuff
import itertools
import logging
import math
import random
import re
import sys
import time
#import json, httplib
import requests
from enum import Enum
import flufl # a better(?) type of enum. To use, make a class be a subclass of flufl.enum.Enum
from operator import attrgetter
from pprint import pprint

# Import custom modules, mostly from GitHub
#from firebase import Firebase # https://github.com/mikexstudios/python-firebase
import names # https://github.com/treyhunner/names
import backoff

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

Instance members of an _Answer():

    objectId
    num
    serial
    ID
    text
    image
    category
    li_tags
    tense
    syllables
    num_words
    num_chars
    li_q_serials
    str_q_serials


# Answer Categories:

#     1 = person
#     2 = place
#     3 = thing
#     4 = animal
#     5 = verb
#     6 = adjective
#     7 = interjection
#     8 = other
#     9 = any


Answer Tags:

    0 --> Can apply to any Category.

    0.1 = has_bold
    0.2 = has_italics
    0.3 = has_underline
    0.4 = has_copyright
    0.5 = has_trademark
    0.6 = is_real
    0.7 = is_fake
    0.8 = is_singular
    0.9 = is_plural

    N --> Can only apply to Category N.

    1.1 = is_male
    1.2 = is_female
    1.3 = is_actor
    1.4 = is_athlete
    1.5 = is_musician
    1.6 = is_doing_something

    4.1 = is_doing_something



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

class Tag(Enum):

    is_real = 1.1
    is_fake = 1.2

    has_bold = 2.1
    has_italics = 2.2
    has_underline = 2.3

    is_actor = 3.1
    is_athlete = 3.2
    is_musician = 3.3

    pass

class Tense(Enum):

    person_singular = 1.1
    person_plural = 1.2

    place_singular = 2.1
    place_plural = 2.2

    thing_singular = 3.1
    thing_plural = 3.2

    animal_singular = 4.1
    animal_plural = 4.2

    verb_simple = 5.1
    verb_past = 5.2
    verb_continuous = 5.3

    adjective_adjective = 6.1
    adjective_adverb = 6.2

    interjection_none = 7.0

    other_none = 8.0

    any_none = 9.0

    pass



# for Parse
class Answer(Object):

    # LIA = [] # holds Answers (Parse)
    pass



# for here
class _Answer(Object):

    LIA = [] # holds Answers (Parse)
    LI_A = [] # holds _Answers (here)
    NUM = 1
    LI_FILENAMES = [
        "adjectives.txt", "animals.txt", "interjections.txt", "other.txt",
        "people.txt", "places.txt", "things.txt", "verbs.txt"
        ] 
    LI_ATTR = [
        "ID", "num", "serial", "text", "image", "category", "li_tags", "tense", 
        "syllables", "num_words", "num_chars", "li_q_serials", "str_q_serials",
        "li_attr"
        ]

    def __init__(self,
        objectId = "",
        num = 0,
        serial = "",
        ID = "",
        text = "",
        image = "",
        category = "",
        li_tags = [],
        tense = "",
        syllables = 0,
        num_words = 0,
        num_chars = 0,
        li_q_serials = [],
        str_q_serials = []
        ):

        self.objectId = objectId
        self.num = _Answer.NUM
        self.serial = get_serial(n = self.num, length_desired = 5)
        self.ID = get_id(prefix=self.__class__.__name__[1:], serial=self.serial)
        self.text = text
        self.image = image
        self.category = category
        self.li_tags = li_tags
        self.tense = tense
        self.syllables = syllables
        self.num_words = num_words
        self.num_chars = num_chars
        self.li_q_serials = li_q_serials
        self.str_q_serials = str_q_serials

        self.li_attr = _Answer.LI_ATTR

        _Answer.NUM += 1

        pass

    def make_Parse_Object(self):
        return Answer(
            objectId = self.objectId,
            ID = self.ID,
            num = self.num,
            serial = self.serial,
            text = self.text,
            image = self.image,
            category = self.category,
            li_tags = self.li_tags,
            tense = self.tense,
            syllables = self.syllables,
            num_words = self.num_words,
            num_chars = self.num_chars,
            li_q_serials = self.li_q_serials,
            str_q_serials = self.str_q_serials,
            li_attr = self.li_attr
            )

    def get_li_attributes(self):
        return _Answer.LI_ATTR

    def __iter__(self):
        # first start by grabbing the Class items
        iters = dict((x,y) for x,y in _Answer.__dict__.items() 
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


# Make _Answer objects by reading <>.
def make_answers():

    for filename in _Answer.LI_FILENAMES:
        # Get rid of comments ("#") and newline chars ("\n").
        lines = [line.strip('\n') for line in open(filename) if line[0] != "#" and line != "\n"]
        # For now, get rid of anything past the first "(".
        lines = [line.split(" (")[0] for line in lines]
        # Each line in lines is now an answers's text and nothing extra.
        #print(lines)
        # Create _Answer and Answer objects and put them in the class lists
        # for line in lines:
        #     _Answer.LI_A.append(
        #         _Answer(
        #             text = line,
        #             num_words = len(line.split()),
        #             num_chars = len(line)
        #             ))
        _Answer.LI_A += [_Answer(
            text = line,
            num_words = len(line.split()),
            num_chars = len(line)
            ) for line in lines]

    # _Answer.LIA = [a.make_Parse_Object() for a in _Answer.LI_A]
    # #print(_Answer.LIA[0].num, _Answer.LIA[-1].num)
    # _Answer.LIA.sort(key = attrgetter("num"))
    # #print(_Answer.LIA[0].num, _Answer.LIA[-1].num)
    # return _Answer.LIA

    return sorted([a.make_Parse_Object() for a in _Answer.LI_A],
                  key = attrgetter("num"))
    


def put_answers_in_Parse():

    # Query for first 1000 Answers
    queryset = list(Answer.Query.all().limit(1000))
    while True:
        if not queryset:
            print("No Answers to delete from Parse -- none exist.")
            break # skip to batch_save without deleting
        elif len(queryset) == len(_Answer.LI_A):
            print("{} Answers already exist in Parse.".format(len(queryset)))
            srsly_delete_stuff = raw_input("Continue with delete anyway? (Y/n): ")
            if srsly_delete_stuff != "Y":
                print "Delete skipped. Upload skipped."
                return
        else:
            print("There are {} Answers to delete from Parse.".format(len(queryset)))
            srsly_delete_stuff = raw_input("Delete Answers from Parse? (Y/n): ")
            if srsly_delete_stuff != "Y":
                print "Delete skipped. Upload skipped."
                return

        # batch_delete in chunks of no more than 50
        batcher = ParseBatcher()
        lili_chunks = [queryset[i:i+50] for i in range(0, len(queryset), 50)]
        for index, chunk in enumerate(lili_chunks):
            batcher.batch_delete(chunk)
            print "\r{} of {} Answers deleted from Parse".format(50*(index+1), len(queryset)),
            sys.stdout.flush()
        print
        break # go to batch_save

    # batch_save in chunks of no more than 50
    len_lia = len(_Answer.LIA)
    batcher = ParseBatcher()
    lili_chunks = [_Answer.LIA[i:i+50] for i in range(0, len_lia, 50)]
    for index, chunk in enumerate(lili_chunks):
        while True:
            try:
                batcher.batch_save(chunk)
                print "\r{} of {} Answers uploaded to Parse".format(50*(index+1), len_lia),
                sys.stdout.flush()
                break
            except:
                print("Locked. Sleeping for 5 seconds.")
                time.sleep(5)
    print
    pass

def update_answers_in_Parse():

    # Get a list of all Answers in Parse.
    ct_a = Answer.Query.all().count()
    queryset = []
    batcher = ParseBatcher()
    print("{} Answers exist in Parse.".format(ct_a))
    if ct_a == 0: # None exist; upload whole list
        pass
    elif ct_a > 0: # There's at least 1 to get
        for i in range(0, ct_a, min(ct_a,1000)): # for each chunk of <= 1000 answers
            queryset += list(Answer.Query.all().skip(i).limit(1000)) # get the chunk, add to queryset
        queryset.sort(key = attrgetter("num"))
        for A, a in zip(queryset, [a for a in _Answer.LIA if queryset[a.num-1].num == a.num]): # for each answer with the same num
            # compare all attributes of the _Answer class.
            # if different, set Parse object's attribute to _Answer object's attribute;
            # if all are same, keep in Parse and delete from LIA
            for key in _Answer.LI_ATTR: # for all attributes of the _Answer class
                if getattr(A, key) != getattr(a, key): # if different
                    print(key, getattr(A,key), getattr(a,key))
                    batcher.batch_delete([A])
                    batcher.batch_save([a])
                    # print("{} updated in Parse".format(a.ID))
                    break
                elif _Answer.LI_ATTR[-1] == key:
                    _Answer.LIA.remove(a)
        print("{} Answers updated in Parse.".format(len(queryset)-len(_Answer.LIA)))
        print("{} Answers must be created in Parse.".format(len(_Answer.LIA)))

    # Now, upload those remaining in _Answer.LIA to Parse
    # (should put batch_upload_with_sleep in a separate function)
    # batch_save in chunks of no more than 50
    len_lia = len(_Answer.LIA)
    batcher = ParseBatcher()
    lili_chunks = [_Answer.LIA[i:i+50] for i in range(0, len_lia, 50)]
    for index, chunk in enumerate(lili_chunks):
        while True:
            try:
                batcher.batch_save(chunk)
                print "\r{} of {} Answers uploaded to Parse".format(50*(index+1), len_lia),
                sys.stdout.flush()
                break
            except:
                print("Locked. Sleeping for 5 seconds.")
                time.sleep(5)
    print






def main():

    # li = make_answers()
    # update_answers_in_Parse()

    print(_Answer.__dict__)
    print("\n\n")
    a = _Answer()
    pprint(list(a))
    print("\n\n")
    print([key for key, value in list(a)])
    print("\n\n")
    pass

if __name__ == '__main__':
    logging.getLogger('backoff').addHandler(logging.StreamHandler())
    status = main()
    sys.exit(status)

# Logging

# # define a Handler which writes ERROR messages or higher to the sys.stderr
# console = logging.StreamHandler()
# # set up logging to file - see previous section for more details
# logging.basicConfig(level=logging.ERROR,
#                     #format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
#                     datefmt='%m-%d %H:%M',
#                     filename='',
#                     filemode='w')
# # set a format which is simpler for console use
# formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# # tell the handler to use this format
# console.setFormatter(formatter)
# # add the handler to the root logger
# #logging.getLogger('').addHandler(console)
# logging.getLogger('').addHandler(logging.StreamHandler())

#logging.error("\n\n\n\n\n      (Oops! Too many requests to Parse again!)\n\n\n\n\n")



























