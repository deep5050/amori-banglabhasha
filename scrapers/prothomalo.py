import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import shutil

# getting the url to scrape
url_file = open("./url.txt", "r")
url = url_file.readline()
url_file.close()

base_url = "https://www.prothomalo.com"

# if chromedriver is not added to the PATH, uncomment the below line
# webdriver.Chrome(executable_path="./driver/chromedriver")
options = webdriver.ChromeOptions()
options.add_argument("headless")  # headless mode, suitable for CI/CD

# start chrome browser
browser = webdriver.Chrome(chrome_options=options)
browser.get(url)


# scrolling to get the lazy-loading image src
lastHeight = browser.execute_script("return document.body.scrollHeight")
html = browser.page_source
browser.quit()

soup = BeautifulSoup(html, "lxml")

story = {}
story["name"] = ""
story["author"] = ""
story["text"] = []
story["img_src"] = ""


def get_story_name():
    global soup
    _story_name_section = soup.find(
        "div", class_="story-title-info storytitleInfo-m__wrapper__1edlu"
    )
    _name = _story_name_section.find_all("div")[2].text
    story_name = ""
    if len(_name) != 0:
        story_name = _name
        return story_name  # got the right story name
    else:
        raise Exception("Error: no story name found")


def get_story_author():
    global soup
    _story_author_section = soup.find("div", class_="author-name-location-wrapper")
    _story_author = _story_author_section.find_all("span")[0].text

    if _story_author == "" or _story_author == "লেখা":
        # apply second method, may be left-aligned story
        try:
            _story_author = _story_author_section.find_all("span")[1].text
        except:
            # author having clickble link
            _story_author = _story_author_section.find_all("a")[0].text

    author = ""

    if len(_story_author) != 0:
        author = _story_author
        return author  # got the right author name
    else:
        raise Exception("Error: author name not found")


def get_main_image():
    global soup

    _img_src = ""
    _img_section = ""

    try:
        _img_section = soup.find(
            "div", class_="story-card-m__wrapper__ounrk story-card-m__bn-wrapper__OgEBK"
        )
        _img_src = _img_section.find_all("img")[0]["src"]
        _img_src = _img_src.split("?")[0]
    except:
        try:
            # left aligned stories
            _img_section = soup.find_all(
                "div",
                class_="story-card-m__wrapper__ounrk story-card-m__left-align__2JTUo story-card-m__bn-wrapper__OgEBK",
            )[0]
            _img_src = _img_section.find_all("img")[0]["src"]
            _img_src = _img_src.split("?")[0]
        except:
            # new card type images > oct, 2020
            try:
                _img_section = soup.find_all(
                    "div",
                    class_="card-image-wrapper cardImage-m__card-image-wrapper__2Ozvn",
                )[0]
                _img_src = _img_section.find_all("img")[0]["src"]
                _img_src = _img_src.split("?")[0]
            except:
                try:
                    # even older version
                    _img_section = soup.find_all(
                        "div",
                        class_="story-card-m__wrapper__ounrk story-card-m__bn-wrapper__OgEBK story-card-m__left-align__2JTUo",
                    )[0]
                    _img_src = _img_section.find_all("img")[0]["src"]
                    _img_src = _img_src.split("?")[0]

                except:
                    print("Warning: no method worked for finding the image src")
                    return ""

    main_image_url = ""

    if len(_img_src) != 0:
        main_image_url = _img_src
        return main_image_url
    else:
        raise Exception("Error: in finding image src")


def get_story_text():
    global soup
    _story_text_section = soup.find("div", class_="story-content no-key-elements")
    _text_divs = _story_text_section.find_all(
        "div", class_="story-element story-element-text"
    )

    lines = []
    for _div in _text_divs:
        p = _div.find_all("p")

        # writing all the story lines
        for _p in p:
            lines.append(_p.text)

    if len(lines) != 0:
        return lines
    else:
        raise Exception("Error: no story text found")


def get_other_images():
    # other small image's url
    pass


def write_image(file_name):
    global story

    url = story["img_src"]
    response = requests.get(url, stream=True)
    with open(f"./stories/images/prothomalo/{file_name}.jpg", "wb") as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


def make_story():
    global story
    story_name = story["name"]
    story_name = story_name.strip().replace(" ", "-")
    author_name = story["author"]
    author_name = author_name.strip().replace(" ", "-")

    file_name = f"{story_name}@{author_name}"

    print(f"making story: {file_name}")

    f = open(f"./stories/prothomalo/{file_name}.md", "w")
    f.write("<div align=center>")

    # if the story has a valid image src write it
    if story["img_src"] != "":
        write_image(file_name)
        f.write(
            f" <img align=center src='../images/prothomalo/{file_name}.jpg' width=500px >\n\n"
        )

    f.write(f"<h2 align=center>{story['name']}</h4>")
    f.write(f"<h3 align=center>{story['author']}</h3>\n</div>\n\n")

    for line in story["text"]:
        f.write(f"{line}\n\n")

    f.close()
    print("completed :)")


def get_story():
    global story

    story["name"] = get_story_name()
    story["author"] = get_story_author()
    story["text"] = get_story_text()
    story["img_src"] = get_main_image()

    make_story()


get_story()


# print(get_main_image())
# print(get_story_text())
# print(get_story_author())
