import requests
from bs4 import BeautifulSoup

# URL = "https://www.prothomalo.com/topic/%E0%A6%97%E0%A6%B2%E0%A7%8D%E0%A6%AA"
URL = "https://www.bondhushava.com/writings/%E0%A6%A6%E0%A7%87%E0%A6%AC%E0%A7%80"
web_data = requests.get(URL)
soup = BeautifulSoup(web_data.content, 'lxml')

story = {}
story['name'] = ""
story['author'] = ""
story['text'] = []

#########################################
def get_story_name():
    global soup
    _story_name_section = soup.find('div',class_="story-title-info storytitleInfo-m__wrapper__1edlu")
    _name = _story_name_section.find_all('div')[2].text
    #story_name_section.find('h1',class_="headline headline-type-9  story-headline bn-story-headline headline-m__headline__3vaq9 headline-m__headline-type-9__3gT8S")
    story_name = ""
    if len(_name)!=0:
        story_name = _name
        return story_name
    else:
        raise Exception("Sorry, no story name found") 

# get_story_name()
############################################


def get_story_author():
    global soup
    _story_author_section = soup.find('div',class_="author-name-location-wrapper")
    _story_author = _story_author_section.find_all('span')[1].text
    author = ""
    if len(_story_author)!= 0 :
        author = _story_author
        return author
    else:
        raise Exception("author name not found")


# get_story_author()

def get_main_image():
    global soup
    _image_section = soup.find('div',class_="story-content no-key-elements")
    print(_image_section)
    # get the main banner
    main_image_url = ""


# get_main_image()


def get_story_text():
    global soup
    _story_text_section = soup.find('div',class_="story-content no-key-elements")
    _text_divs = _story_text_section.find_all('div',class_="story-element story-element-text")
    lines = []
    for _div in _text_divs:
        p = _div.find_all('p')
        for _p in p:
            lines.append(_p.text)

    if len(lines)!= 0:
        return lines
    else:
        raise Exception("no text found")



def get_other_images():
    # other small image's url
    other_image_url = ""

def make_story():
    global story
    file_name = story['name'].replace(" ","-")
    f = open(f'./stories/bondhushava/{file_name}.md','w')
    f.write(f"<div align=center><h2 align=center>{story['name']}</h4>")
    f.write(f"<h3 align=center>{story['author']}</h3></div>\n\n")
    for line in story['text']:
        f.write(f'{line}\n\n')
    f.close()
    print("completed :)")



def get_story():
    global story
    
    story['name'] = get_story_name()
    story['author'] = get_story_author()
    story['text'] = get_story_text()

    make_story()

get_story()