#!/usr/bin/env python

import sys, os
import make_tables
from pprint import pprint

# a way to filter while reading table from file
#ban_list = ['the', 'of']

def read_table(table_filename):
    # fixes paths
    __dir__ = os.path.dirname(os.path.abspath(__file__))
    table_path = os.path.join(__dir__, table_filename)

    domain_table = {}

    try:
        for line in open(table_path, 'r'):
            k,v = line.split()
            #if k not in ban_list and int(v) > 1:
                #domain_table[k.decode('utf-8')] = int(v)
            domain_table[k.decode('utf-8')] = int(v)
        return domain_table
    except:
        print 'Error while reading the table file %s' %table_filename
        #print 'A line on the file should be of format <stem> <frequency>' 
        raise


def fix_urls(links_dict, url):
    if url[-1] != '/':
        url += '/'
    for k in links_dict:
        if "http://" not in links_dict[k]:
            corrected_link = url + links_dict[k]
            links_dict[k] = corrected_link
    return {"url":url, "links_dict":links_dict}
    #return links_dict


def hij_inspect(table_filename, sitesource):
    t = read_table(table_filename)
    #pprint(t)
    #print ''

    list_of_same_style_links = make_tables.lists_for_site(sitesource)
    #make_tables.print_list(list_of_same_style_links)

    score_list = [ lo.get_score(lo.get_common_words(t)) for lo in list_of_same_style_links]
    
    if score_list:
        print 'Finding the best ones...\n'
        print 'Score list'
        pprint(score_list)
        print ''

        m = max(score_list)
        max_items_indices = [i for i, j in enumerate(score_list) if j == m]

        if len(max_items_indices) == 1:
            best_links_obj = list_of_same_style_links[score_list.index(m)] 
        else:
            print 'More that one set of links have the same score. Choosing the first one for now...'
            best_links_obj = list_of_same_style_links[max_items_indices[0]]

        best_links = fix_urls(best_links_obj.same_style_links, sitesource)
        #pprint(best_links_obj.same_style_links)
        pprint(best_links)
        print 'score: ', m

        return best_links

    else:
        print 'No url link sets found in the given page'


if __name__ == '__main__':
    if (len(sys.argv) != 3):
       print 'usage: python hij_inspect.py <table filename> <url or html file>'
       sys.exit(1)

    table_filename = sys.argv[1]
    sitesource = sys.argv[2]    # url or html file 
    best_link_coll = hij_inspect(table_filename, sitesource)
