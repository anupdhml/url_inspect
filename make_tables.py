#!/usr/bin/env python

from __future__ import division
import sys, urllib2, socket
from bs4 import BeautifulSoup , SoupStrainer
from HTMLParser import HTMLParseError
from pprint import pprint
import re
import porter


#link_text_length=15
max_words = 2


class SameStyleLinks:
    def __init__(self):
        self.same_style_links = {}
        self.stemmed_list = []

    def get_common_words(self, table):
        found_words = {}
        for w in self.stemmed_list:
            if w in table:
                found_words[w] = table[w]

        print self.same_style_links
        print 'matched words with  their freq' 
        print found_words
        return found_words

    def get_score(self, found_words):
        if len(found_words):
            print sum(found_words.values()), sum(found_words.values())/len(found_words),\
                  sum(found_words.values())/len(self.stemmed_list)
            #print ''
            #return len(found_words)/len(self.stemmed_list)
            #return sum(found_words.values())/len(found_words)


        print ''
        #return sum(found_words.values())/len(self.stemmed_list)
        return sum(found_words.values())


# source is either a url or a local file
def get_html(source):
    try:
        return urllib2.urlopen(source)
    except:
        try:
            return open(source, 'r')
        except:
            print 'Html not retrieved. Check the file/url'
            #raise


def to_soup(html):
    try:
        soup = BeautifulSoup(html, 'lxml')
        #soup = BeautifulSoup(html, 'lxml', parse_only=SoupStrainer('div'))
        #print soup
        #print ''
        return soup
    except HTMLParseError:
        print 'parse error'
        raise


def stem(word):
    p = porter.PorterStemmer()
    output = ''
    #word_lower = ''.join([c.lower() for c in word if c.isalpha()])
    word_lower = ''.join([c.lower() for c in word if c.isalnum()])
    output += p.stem(word_lower, 0, len(word_lower)-1)
    return output


# For the purposes of this prog, string will be a word.
# But will handle a string too
#def stem(string):
    #p = porter.PorterStemmer()
    #output, word = '', ''
    #line = string + ' '
    #print line
    #for c in line:
        #if c.isalpha():
            #word += c.lower()
        #else:
            #if word:
                #output += p.stem(word, 0, len(word)-1)
                #word = ''
            #output += c.lower()
            #print output
    #return output[:-1] # remove the final space


def check_valid_link(tag):
    return tag.name is 'a' and tag.has_key('href') 


# rec = false, descendants, children, siblings, find_next_sibling, head > title
#soup.select("#link1")byid
#soup.select('a[href*=".com/el"]')
#TODO: Improve this
def check_valid_list(tag): 
    nav_id_present = tag.has_key('id') and re.match('.*(nav).*', tag['id'], re.IGNORECASE)
    #if (nav_id_present):
            #print 'Found a nav bar with id', tag['id']
    return (nav_id_present or tag.name == 'ul')
    #return ( tag.name == 'ul')


def get_same_styles(soup):
    list_links = []

    for listing in soup(check_valid_list):
        link_obj = SameStyleLinks()
        #print listing
        #print ''

        #same_style_links=dict((''.join(link.stripped_strings), link['href']) for link in listing(check_valid_link))
        for link in listing(check_valid_link):
            link_text=''.join(link.stripped_strings)

            if (link_text) and len(link_text.split())<=max_words:
                link_obj.same_style_links[link_text] = link['href']
                for w in link_text.split():
                    stemw = stem(w)
                    if(stemw):              # disregard empty
                        link_obj.stemmed_list.append(stemw)

        if(link_obj) and len(link_obj.same_style_links) > 1:
            list_links.append(link_obj)

    return list_links


# source is either a url or a local file
def lists_for_site(source):
    html = get_html(source)
    if(html):  # not really needed...
        return get_same_styles(to_soup(html))


def print_list(list_of_same_style_links):
    n=0
    for link_obj in list_of_same_style_links:
        #if(link_obj.same_style_links):
        n+=1
        print n
        #print list_of_same_style_links.index(link_obj)
        pprint(link_obj.same_style_links)
        print link_obj.stemmed_list
        print ''


# n will be 1 when we build the table first time.
# might want to change this value when updating table later
def update_table(table, stemmed_list, n):
    for stem in stemmed_list:
        if stem in table:
            table[stem] += n
        else:
            table[stem] = n


def table_for_domain(links_file):
    table = {}
    for link in links_file:
        print ''
        print 'current', link
        try:
            all_link_sets = lists_for_site(link)
            print len(all_link_sets), 'link sets present'
            for link_obj in all_link_sets:
                update_table(table, link_obj.stemmed_list, 1)
        except:
            pass
    return table        


if __name__ == '__main__':
    if ( len(sys.argv) > 3 or len(sys.argv) < 2 ):
       print 'usage: python make_tables.py <url or html file>\n\
       python make_tables.py -f <file with list of urls or html file paths>'
       sys.exit(1)

    if(sys.argv[1] == '-f'):
        filename = sys.argv[2]
        d = table_for_domain(open(filename, 'r'))
        print ''
        print 'Domain table generated for', filename
        #pprint(d)

        dump_filename = 'table_'+filename.replace('/', '-')
        dump_file = open(dump_filename, "wb")
        keys_sorted_by_values = sorted(d, key=d.get, reverse=True)
        for w in keys_sorted_by_values:
            #print w, d[w]
            print>>dump_file, w.encode('utf8', 'replace'), d[w]
        print 'Written to file', dump_filename

    else:
        try:
            print_list(lists_for_site(sys.argv[1]))
        except:
            print 'Error!'
            #raise
