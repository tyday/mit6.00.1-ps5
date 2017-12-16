# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Ty Day
# Collaborators: NONE
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import re


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_link(self):
        return self.link
    def get_pubdate(self):
        return self.pubdate



#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def  __init__(self,phrase):
        self.phrase = phrase.lower()
    def is_phrase_in(self, test_string):
        text = '\\b' + self.phrase + '\\b'
        re_text = re.compile(text)
        test_string = test_string
        for p in string.punctuation:
            test_string = test_string.replace(p, " ")
        test_string = test_string.lower()
        test_string = " ".join(test_string.split())
        if re_text.search(test_string):
            return True
        else:
            return False

        
# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def evaluate(self,phrase):
        return self.is_phrase_in(phrase.get_title())
        


# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, phrase):
        return self.is_phrase_in(phrase.get_description())

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, time_string):
        temp_date = datetime.strptime(time_string, '%d %b %Y %H:%M:%S')
        temp_date = temp_date.replace(tzinfo=pytz.timezone("EST"))
        self.tt_Date = temp_date



# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        comp_date = story.get_pubdate()
        if comp_date.tzinfo is None:
            comp_date = comp_date.replace(tzinfo=pytz.timezone("EST"))
        if self.tt_Date > comp_date:
            return True

class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        comp_date = story.get_pubdate()
        if comp_date.tzinfo is None:
            comp_date = comp_date.replace(tzinfo=pytz.timezone("EST"))
        if self.tt_Date < comp_date:
            return True

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, other_trigger):
        self.other_trigger = other_trigger
    def evaluate(self, story):
        return not self.other_trigger.evaluate(story)

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger_one, trigger_two):
        self.trigger_one = trigger_one
        self.trigger_two = trigger_two
    def evaluate(self, story):
        return self.trigger_one.evaluate(story) and self.trigger_two.evaluate(story)

# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger_one, trigger_two):
        self.trigger_one = trigger_one
        self.trigger_two = trigger_two
    def evaluate(self, story):
        return self.trigger_one.evaluate(story) or self.trigger_two.evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    story_list = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                story_list.append(story)
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    return story_list #stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    return_dict = {}
    return_list = []
    tempstring = ''
    for line in lines:
        templine = line.split(',')
        dic_key = templine[0]#:line[0:2]
        trig_desc = templine[1]
        if trig_desc == 'TITLE':
            #tempstring = line[0:1] + ' = ' + 'TitleTrigger(' + templine[2] + ')'
            return_dict[dic_key] = TitleTrigger(templine[2])
            #return_list.append(return_dict[dic_key])
        elif trig_desc == 'DESCRIPTION':
            #tempstring = line[0] + ' = ' + 'DescriptionTrigger(' + templine[2] + ')'
            return_dict[dic_key] = DescriptionTrigger(templine[2])
        elif trig_desc == 'BEFORE':
            #tempstring = line[0] + ' = ' + 'BeforeTrigger(' + templine[2] + ')'
            return_dict[dic_key] = BeforeTrigger(templine[2])
        elif trig_desc == 'AFTER':
            #tempstring = line[0] + ' = ' + 'AfterTrigger(' + templine[2] + ')'
            return_dict[dic_key] = AfterTrigger(templine[2])
        elif trig_desc == 'NOT':
            #tempstring = line[0] + ' = ' + 'NotTrigger(' + templine[2] + ')'
            return_dict[dic_key] = NotTrigger(templine[2])
        elif trig_desc == 'AND':
            #tempstring = line[0] + ' = ' + 'AndTrigger(' + templine[2] + ', ' + templine[3] + ')'
            return_dict[dic_key] = AndTrigger(return_dict[templine[2]], return_dict[templine[3]])
        elif trig_desc == 'OR':
            #tempstring = line[0] + ' = ' + 'OrTrigger(' + templine[2] + ', ' + templine[3]+ ')'
            return_dict[dic_key] = OrTrigger(return_dict[templine[2]], return_dict[templine[3]])
        elif templine[0] =='ADD':
            for elem in line.split(','):
                if elem in return_dict:
                    return_list.append(return_dict[elem])

    print(return_list) # for now, print it so you see what it contains!
    return return_list



SLEEPTIME = 20 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("trump")
        t3 = DescriptionTrigger("clinton")
        t4 = AndTrigger(t2, t3)
        #triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("https://news.google.coms/rss/headlines?gl=US&ned=us&hl=en")#("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

