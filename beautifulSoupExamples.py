# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:41:51 2017

@author: jessicasutd
"""

from bs4 import BeautifulSoup
html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
soup = BeautifulSoup(html)

#print soup.prettify()



#tags: 
#print soup.title
#<title>The Dormouse's story</title>

#print soup.head
#<head><title>The Dormouse's story</title></head>

#print soup.a
#<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>

#print soup.a.attrs
#{'href': 'http://example.com/elsie', 'class': ['sister'], 'id': 'link1'}

#print soup.a['href'] =>treat it as dic, can modify or delete or...
#or print soup.a.get('herf')
#'http://example.com/elsie'

#get the info easily! Much easier than re!!
#but can only find the first tag that meets the requirement



#.content:
#print soup.head.content return a list

#.child/ .descendants: 
#similar use, but need traverse
#for child in soup.descendants:
    #print child

#.string:
#print soup.head.string 
#or print soup.title.string
#The Dormouse's story
#if a tag doesn't contain a child tag, return the comment inside
#if a tag contains an only child tag, still return the comment
#if a tag contains many child tags, return None

#.strings   .stripped_strings
#for string in soup.stripped_strings:
    #print string

#.parent 
#h=soup.title
#print h.parent.name #head #remeber .name!

#.parents (all parent nodes)
#cont=soup.title
#for par in cont.parents:
    #print par.name  #remeber .name!
#head
#html
#[document]

#.next_sibling  .previous_sibling (sibling node)
#space and  are also nodes. so the result sometimes looks blank
#as a result, we can try .next_sibling.next_sibling

#.next_siblings  .previous_siblings
#need traverse

#node
#.next_element  .previous_element
#print soup.head.next_element
#<title>The Dormouse's story</title>
#.next_elements  .previous_elements



#find_all( name , attrs , recursive , text , **kwargs )
    #1. find all tags called 'a'
    #print soup.find_all('a')
    #[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, 
      #<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, 
      #<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
    
    #2. with re
    #for tag in soup.find_all(re.compile("^b")):
        #print(tag.name)
        
    #3. find all tags 'a' and 'b'
    #print soup.find_all(['a','b'])
    
    #4. find all tags
    #for tag in soup.find_all(True):
        #print(tag.name)
    # html
    # head
    # title
    # body
    # p
    # b
    # p
    # a
    # a
    
    #5. find with method
    #def has_class_but_no_id(tag):
        #return tag.has_attr('class') and not tag.has_attr('id')
    #soup.find_all(has_class_but_no_id)

    #6. keyword
    #soup.find_all(id='link2')
    #soup.find_all(href=re.compile("elsie"))
    #soup.find_all(href=re.compile("elsie"), id='link1')
    #soup.find_all("a", class_="sister") #class is reserve word, so add underscore
    #soup.find_all(text='Elsie')  [u'Elsie']
    #soup.find_all(text=re.compile("Dormouse"))  [u"The Dormouse's story", u"The Dormouse's story"]
    
    #Sometimes the search doesn't work:
    #data_soup = BeautifulSoup('<div data-foo="value">foo!</div>')
    #data_soup.find_all(data-foo="value")
    # SyntaxError: keyword can't be an expression
    #Then try the following:
    #data_soup.find_all(attrs={"data-foo": "value"})
    #[<div data-foo="value">foo!</div>]
    
    #7. limit param
    #only return the first 2
    #soup.find_all("a", limit=2)
    
    #8. recursive
    #When using find_all(), we search for all nodes under a tag
    #If we only want to search for the direct child node: use recursive=False
    
    #soup.html.find_all("title")
    # [<title>The Dormouse's story</title>]
    #soup.html.find_all("title", recursive=False)
    # []
 
    
#find( name , attrs , recursive , text , **kwargs )
    #find_all() return a list of all results
    #find() return the result directly
    
#similarly, there are:
    #find_parents()  find_parent() search for parent node(s) of the current node
    #find_next_siblings()  find_next_sibling() find_previous_siblings()  find_previous_sibling()
    #find_all_next()  find_next()
    #find_all_previous() 和 find_previous()
    


#CSS
#soup.select() return a list
    #1. Search with tag:
    #print soup.select('title') 
    #[<title>The Dormouse's story</title>]
    
    #2. Search with class name:  add '.'
    #print soup.select('.sister')
    #[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, 
      #<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, 
      #<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
    
    #3. Search with id:  add '#'
    #print soup.select('#link1')
    #[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
    
    #4. Search with hierachy
    #print soup.select('p #link1') return in p tag, id='link1'
    #[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
    
    #print soup.select("head > title") return tag title in tag head
    #[<title>The Dormouse's story</title>]

    #5. Search with attributes
    #'tagName[...='...']' no space in between if same node
    #print soup.select('a[class="sister"]')
    #[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, 
      #<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, 
      #<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
    
    #'tag1Name tag2Name[...='...']' a space if not in same node
    
    #6. How to get result? =>get_text()
    #for title in soup.select('title'):
        #print title.get_text()
    
    
    
    
    
    
    
    
    
    
    
  