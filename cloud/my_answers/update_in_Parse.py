
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
from operator import attrgetter

# For flat list and dictionary printing.
from pprint import pprint

# For interacting with Parse through its API (not ParsePy); 
# I'm using the API directly for cloud code and background jobs. 
# See https://www.parse.com/docs/rest/guide#cloud-code.
import json, httplib

# Not sure if needed.
import requests

# Import custom modules, mostly from GitHub
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

def set_P_classes(li_classnames):
    """ Return a list of Parse Classes so we can use them. """
    return [type(cn, (Object,), {}) for cn in li_classnames]


# def p_query(classname, limit = None):

#   # if how_many == "all" or how_many > 1000:

#   pb = P_Batcher()
#   P_Batcher.batch_query(classname, limit = limit)

#       #return list(type(classname,(Object,),{}).Query.all())
#   # if option == 1:
#   #   ct = cls.Query.all().count()
#   #   print(ct)
#   #   pass
#   # elif option == 2:
#   #   cls = type(cls, (Object,), {})
#   #   ct = cls.Query.all().count()
#   #   print(ct)
#   #   pass

class P_Batcher(ParseBatcher):
    """ Already has batch, batch_save, batch_delete methods. """

    def __init__(self, cn_Parse, cn_Python):
        self.cn_Parse = cn_Parse
        self.cn_Python = cn_Python

    def batch_with_wait(self, func_name, li_objects_to_modify, wait = 5):
        li = li_objects_to_modify
        lili_chunks = [li[i:i+50] for i in range(0, len(li), 50)]
        print(len(lili_chunks), "chunks")
        print(lili_chunks[0][0].__class__.__name__)
        for index, chunk in enumerate(lili_chunks):

            # if func_name == "create":
            #     ParseBatcher().batch_save(chunk)
            # elif func_name == "remove":
            #     ParseBatcher().batch_delete(chunk)
            # print("\r{0} of {1} Objects {2}d in Parse".format(
            #     50*(index+1), len(li), func_name
            #     ), end = "\r")
            # sys.stdout.flush()
            # #break

            while True:
                try:
                    if func_name == "create":
                        ParseBatcher().batch_save(chunk)
                    elif func_name == "remove":
                        ParseBatcher().batch_delete(chunk)
                    print("\r{0} of {1} Objects {2}d in Parse".format(
                        50*(index+1), len(li), func_name
                        ), end = "\r")
                    sys.stdout.flush()
                    break
                except:
                    print("\nSleeping for {} seconds.\r".format(wait))
                    time.sleep(wait)
        print("\n\n")

    def batch_query(self, limit = 100000):
        """ Returns a sorted list (of any size) of queried objects. 
            Gets past the 1000 query limit in Parse.
            List is always sorted by "num" attribute.
        """
        print("Querying a max of {} {}'s from Parse".format(limit, self.cn_Parse))
        queryset = []
        if limit > 0:
            for t in range(0, limit, min(1000,limit)):
                # Stop if t >> limit; we won't get anything.
                if t <= 1000 + len(queryset): 
                    queryset += sorted(
                        list(type(self.cn_Parse,(Object,),{})
                        .Query.all().skip(t).limit(min(1000,limit))),
                        key = attrgetter("num"))
            #print(getattr(queryset[0],"num"), getattr(queryset[-1],"num"))
        print("{} {}s found".format(len(queryset), self.cn_Parse))
        return queryset

    def batch_create(self, li_objects_to_create):
        return self.batch_with_wait("create", li_objects_to_create)

    def batch_remove(self, li_objects_to_remove):
        return self.batch_with_wait("remove", li_objects_to_remove)

    def batch_update(self, li_old_objects, li_new_objects):
        # OLD objects came from a Parse Query. They currently exist in Parse.
        # NEW objects were created in code.

        # If li_old_objects is empty (none exist in Parse), 
        # call batch_create on li_new_objects and return.
        print(len(li_new_objects))
        if not li_old_objects:
            print("No old objects, uploading all new objects")
            return self.batch_create(li_new_objects)

        li_old = li_old_objects # alias
        li_new = li_new_objects # alias
        li_objects_to_save = []
        li_objects_to_delete = []
        set_matching_object_nums = set([no.num for no in li_new if no.num in [oo.num for oo in li_old]])
        print("set_matching_object_nums has {} members\n".format(len(set_matching_object_nums)))

        # Add the New objects that don't have a corollary in the Old list to the list to save,
        # then remove them from li_new.
        li_objects_to_save += [no for no in li_new if no.num not in set_matching_object_nums]
        for o in li_objects_to_save:
            li_new.remove(o)

        # Add the Old objects that don't have a corollary in the New list to the list to delete,
        # then remove them from li_old.
        li_objects_to_delete += [oo for oo in li_old if oo.num not in set_matching_object_nums]
        for o in li_objects_to_delete:
            li_old.remove(o)

        # Compare the pair of old and new objects with the same "num".
        attributes = [key for key, value in list()]
        print("{} old objects, and {} new objects.".format(len(li_old), len(li_new)))
        ##print([o.num for o in li_objects_to_save])
        ##print([o.num for o in li_objects_to_delete])
        print()
        for old, new in zip(li_old, li_new):
            ##print(old.__class__.__name__)
            # compare all attributes of the New object's class.
            # if an attribute is different, set the old object's attribute to the new object's attribute,
            # and add it to the list to save.
            # if all attributes are the same, keep in Parse (don't do anything).
            equivalent = True
            for att in attributes:
                if getattr(old, att) != getattr(new, att):
                    #print(getattr(old, att), "is old's old attr value")
                    setattr(old, att, getattr(new, att))
                    #print(getattr(old, att), "is old's new attr value")
                    equivalent = False
            if equivalent == False:
                li_objects_to_save.append(old)
        print(len(li_objects_to_save), "objects to save")
        print(len(li_objects_to_delete), "objects to delete\n")

        # Save the list to save and delete the list to delete.
        if li_objects_to_save:
            self.batch_create(li_objects_to_save)
        if li_objects_to_delete:
            self.batch_remove(li_objects_to_delete)

        return




def main():

    # Make a list of classnames in Parse you want to update.
    li_classnames = ["Question", "Answer"]

    # Create local references to those classes.
    set_P_classes(li_classnames)

    # For each class to update...
    for cn in li_classnames:
        # Initialize a custom P_Batcher for the classname.
        # Get a list of objects currently in Parse.
        li_queried = P_Batcher(cn, "_"+cn).batch_query()
        # Update that list with whatever is in local files.
        if cn == "Question":
            P_Batcher(cn, "_"+cn).batch_update(li_queried, make_questions())
        elif cn == "Answer":
            P_Batcher(cn, "_"+cn).batch_update(li_queried, make_answers())
    # li_q_queried = pb.batch_query("Question", limit = 100000)
    # li_a_queried = pb.batch_query("Answer", limit = 100000)
    # pb.batch_update(li_q_queried, make_questions())
    # pb.batch_update(li_a_queried, make_answers())
    return



if __name__ == '__main__':

    if __package__ is None:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        from my_questions.upload_my_questions_to_Parse import make_questions
    else:
        from my_questions.upload_my_questions_to_Parse import make_questions

    status = main()
    sys.exit(status)



















