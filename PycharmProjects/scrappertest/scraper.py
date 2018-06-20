#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import simplejson


BASE_URL = "https://www.googleapis.com/customsearch/v1?key=AIzaSyBzDTo8YT68ogAHBxDqR9r_0JTCRbqFSNA&cx=006290677657403172633:fxojpuow9g4"


def __get_all_hcards_from_query(query, index=0, hcards={}):

    url = query

    if index != 0:

        url = url + '&start=%d' % (index)

    json = simplejson.loads(urllib.urlopen(url).read())

    if json.has_key('error'):

        print "Stopping at %s due to Error!" % (url)

        print json

    else:

        for item in json['items']:

            try:

                hcards[item['pagemap']['hcard'][0]['fn']] = item['pagemap']['hcard'][0]['title']

            except KeyError as e:

                pass

        if json['queries'].has_key('nextPage'):

            return __get_all_hcards_from_query(query, json['queries']['nextPage'][0]['startIndex'], hcards)

    return hcards


def get_all_employees_by_company_via_linkedin(company):

    queries = ['"at %s" inurl:"in"', '"at %s" inurl:"pub"']


    result = {}

    for query in queries:

        _query = query % company
        print(_query)

        result.update(__get_all_hcards_from_query(BASE_URL + '&q=' + _query))

    return list(result)

get_all_employees_by_company_via_linkedin('sinay')