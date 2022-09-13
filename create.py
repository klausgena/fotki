import os
import re
import yaml
import markdown
import PIL
from PIL import Image
from jinja2 import Environment, FileSystemLoader, select_autoescape, Template

### Create html  galleries from a bunch of jpegs in a folder ###

# Create the Jinja environment

env = Environment(
    loader=FileSystemLoader('templates/'),
    autoescape=select_autoescape()
)
# Add jinja filters
# strip jpeg or jpg from picture name (for naming the single page)
def strip_jpg(string):
    stripped_string = re.sub("\.jpe?g$", "", string)
    return stripped_string

def strip_md(string):
    stripped_string = re.sub("\.md$", "", string)
    return stripped_string

def clean_folder_name(string):
    '''folders with spaces and capitals: make
    them lowercase and replace space with _'''
    clean_string = string.replace(" ", "_").lower()
    return clean_string

def folder_name_to_title(string):
    '''Turn folder name into readable title'''
    clean_string = string.replace("_", " ").capitalize()
    return clean_string


def get_previous_and_next(el, list):
    '''return the previous and next element in a
    list. (for navigation)'''
    prevnext = [None, None]
    for counter, element in enumerate(list):
        if element == el and counter != 0:
            prevnext[0] = list[counter - 1]
        if element == el and len(list) > counter + 1:
            prevnext[1] = list[counter + 1]
    return prevnext

# TODO refactor to strip_extension and change in base template
env.filters["strip_jpg"] = strip_jpg
env.filters["clean_folder_name"] = clean_folder_name
env.filters["strip_md"] = strip_md
env.filters['folder_name_to_title'] = folder_name_to_title
# DEBUG env.filters['get_previous_and_next'] = get_previous_and_next

# Add custom functions to templates

env.globals.update(get_previous_and_next = get_previous_and_next)

# get config constants from config.YAML

with open(r'config.yaml') as file:
    config = yaml.full_load(file)

FOOTER = config['footer']
SITENAME = config['sitename']
AUTHOR = config['author']
CONTENT = config['content']


# helper functions


def compress_pictures(picture_list, picture_folder):
    '''
    Resize and compress every picture from img folder for web consumption
    '''
    for count, picture in enumerate(picture_list):
        pic_path = "img/" + picture_folder + "/" + picture # TODO make  a folder choice in console app / config
        # new path for web usage
        new_path = "html/" + clean_folder_name(picture_folder) + "/img/"
        # TODO create nice picture name
        nice_name = nice_name_picture(clean_folder_name(picture_folder), count)
        new_pic_path = new_path + nice_name
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        with Image.open(pic_path) as pic:
            # resize to 1920 width
            pic.thumbnail(size=(1920, 1920))
            # compress
            pic.save(new_pic_path, 'jpeg', quality=30)
    print("Pictures in folder '{}' resized and compressed.".format(picture_folder))


def get_image_folders():
    '''
    Get the folders where the compressed images reside
    '''
    path = os.getcwd() + "/html"
    folders = [x.name for x in os.scandir(path) if x.is_dir() and x.name != "_feature"]
    return folders


def nice_name_picture(folder, counter):
    '''Create picture name (folder name + counter) that is sortable.'''
    if counter < 10:
        counter_string = "00" + str(counter)
    elif counter < 100 and counter > 9:
        counter_string = "0" + str(counter)
    else:
        counter_string = str(counter)
    pic_name = folder + "_" + counter_string + ".jpg"
    return pic_name


def get_pic_orientation(folder, pic):
    '''take a picture (filename) in a folder and return
    portrait, landscape or square'''
    image = Image.open(folder + "/" + pic)
    w, h = image.size
    # if width > height = landscape
    if w > h:
        return "landscape"
    # if width = height = square
    elif w == h:
        return "square"
    # else = portrait
    else:
        return "portrait"


def create_gallery_configs():
    '''
    Create a _folder_.yaml file in 'txt' for every _folder_, with dummy config data, 
    unless it already exists.
    '''
    path = "txt/"
    folders = get_image_folders()
    for folder in folders:
        file = path + folder + ".yaml"
        if not os.path.exists(file):
            content = create_config_template(folder)
            with open(file, "w+") as config_file:
                config_file.write(content)


def create_config_template(folder):
    '''
    Create the dummy config templates for a folder
    '''
    path = "html/" + folder + "/img"
    pic_list = os.listdir(path)
    # get pic orientations
    orientations = []
    for pic in pic_list:
        orientation = get_pic_orientation(path, pic)
        orientations.append({"name": pic, "orientation": orientation})
    index_text =  '''

## Configure your gallery index:
# add a description of your gallery after "content:" (optional)

content:


# Set a featured picture (a number, based on the picture number in the final gallery), ex. 'featured: "001"' (mind leading zeroes and parentheses):

featured: "001" # You can change this number to the picture you prefer.


# Configure your picture descriptions: 
# give your picture a name (optional, insert after "title:")
# or say something about the picture (optional, insert after "description:")


pictures:
    '''
    main_content = ""
    for i, pic in enumerate(orientations):
        pic_name = "\n    name: " + pic["name"] + "\n"
        pic_orientation = "    orientation: " + pic["orientation"] + "\n"
        pic_title = "    title: " + "\n"
        pic_description = "    description: " + "\n"
        pic_text = pic_name + pic_orientation + pic_title + pic_description
        ind_pic_text = "- " + str(i) + ":" + pic_text
        main_content = main_content + ind_pic_text + "\n"
    main_content = index_text + "\n" + main_content
    return main_content


def parse_gallery_config(folder):
    '''
    Parse the yaml config file for each gallery page (and individual pages)
    and return a dict with the data
    '''
    path = "txt/" + folder + ".yaml"
    with open(path, "r") as file:
        config = yaml.full_load(file)
    return config


def list_md_files(folder):
    '''
    Get list of md files
    '''
    path = os.getcwd() + "/" + folder
    return [x for x in os.listdir(path) if x.endswith('.md')]


def convert_md_into_html(source_folder, file_list):
    '''
    Convert md files into html, for further use in template. Returns list with 
    dicts with file name and all the content of the md files as html to be embedded.
    '''
    html_content = []
    for file in file_list:
        file_path = source_folder + "/" + file
        with open(file_path) as f:
            lines = f.read()
            html = markdown.markdown(lines)
            name_content_dict = {'name': file, 'content': html}
            html_content.append(name_content_dict)
    return html_content


def get_gallery_configs(folders):
    '''Create a list of gallery config dicts to transfer as 
    a template var while creating the index'''
    config_list = []
    for folder in folders:
        dict = parse_gallery_config(folder)
        config_list.append({'folder': folder, 'config': dict})
    return config_list


# page functions

# CONSTANTS

FOLDERS = get_image_folders()
MD_FILES = list_md_files("txt")

def create_page_from_md(content_dic):
    '''
    Fill a page.html template with data from content 
    dict and create the subsequent page.
    '''
    # TODO make function to create BASE html part (make_header_and_footer)
    # get vars 
    title = content_dic['name']
    description = content_dic['name'] # TODO change
    content = content_dic['content']
    page_name = strip_md(content_dic['name'])
    # fill template
    template = env.get_template("page.html")
    html = template.render(title=title, sitename= SITENAME, description=description, 
    content=content, author=AUTHOR, folders=FOLDERS, footer=FOOTER, pages=MD_FILES)
    # create page inside html folder
    file = "html/" + page_name + ".html"
    with open(file, "w+") as html_page:
        html_page.write(html)
    print("Page for '{}' succesfully created".format(content_dic['name']))


def create_html_for_all_md(source_folder, file_list):
    '''
    Create html pages for all md pages in txt dir.
    '''
    # get data
    all_content = convert_md_into_html(source_folder, file_list)
    # convert data to html
    for content in all_content:
        create_page_from_md(content)


def create_gallery(picture_list, folder_name, folders):
    '''
    Create an HTML gallery index page from a list of pictures
    '''
    # get vars
    title = folder_name
    description = folder_name # cleanup?
    # Get the gallery config data
    gallery_config = parse_gallery_config(folder_name)
    # get template
    template = env.get_template("gallery.html")
    # fill template with vars and create it
    html = template.render(title=title, sitename=SITENAME, description=description,
    author=AUTHOR, pictures=picture_list, footer=FOOTER, 
    folder_name=folder_name, folders=folders, 
    content = gallery_config["content"], pages=MD_FILES,
    picture_data = gallery_config)
    # DEBUG
    print(folders, title)
    # create index.html from template in gallery folder inside html folder
    file = "html/" + folder_name + "/index.html"
    with open(file, "w+") as html_gallery:
        html_gallery.write(html)
    # print success message
    print("Gallery '{}' created.".format(folder_name))


def compress_and_save_pictures(folder_name):
    '''
    Take the pictures and save them to the new folder
    '''
    # Load picture names into list
    folders = os.listdir(folder_name)
    for folder in folders:
        path = folder_name + "/" + folder
        folder_pics = os.listdir(path)
        # compress pics for web and save them in new folder
        compress_pictures(folder_pics, folder)


def create_galleries():
    '''
    Create html gallery as index.html in each gallery folder with pics from an 
    img directory in that folder.
    '''
    folders = get_image_folders() # web folders
    # get pic names
    for folder in folders:
        pic_path = "html/" + folder + "/img"
        folder_pics = [x.name for x in os.scandir(pic_path) if x.is_file and x.name != "index.html"]
        gallery_config = parse_gallery_config(folder)
        for count, picture in enumerate(folder_pics):
            # get previous and next pics for navigation
            previous = None
            next = None
            if count > 0:
                previous = folder_pics[count - 1]
            if count + 1 < len(folder_pics):
                next = folder_pics[count + 1]
            # get pic name and content
            pic_name =  gallery_config["pictures"][count][count]["name"]
            pic_content = gallery_config["pictures"][count][count]["description"]
            pic_config = gallery_config['pictures'][count][count]
            # create single picture pages
            create_single_picture(picture, folder, previous, next, pic_name, pic_content, pic_config)
        # create gallery page with pics
        create_gallery(folder_pics, folder, folders)
    print("Galleries created")

# TODO pass template vars all in GALLERY CONFIG (refactor)

def create_single_picture(picture, folder_name, previous, next, pic_name, pic_content, pic_config):
    '''
    Create html page from a single picture.
    '''
    # get vars
    pic_title = pic_config['title'] if pic_config['title'] else pic_name
    title = pic_title + " in " + folder_name.capitalize()
    description = folder_name # TODO change
    folder_name = folder_name
    # strip jpeg or jpg from picture name (for naming the single page)
    stripped_picture = re.sub("\.jpe?g$", "", picture)
    # create web safe folder name
    u_folder_name = folder_name.replace(" ", "_").lower()
    # get template
    template = env.get_template("picture.html")
    # fill template with vars and create it
    # TODO FOLDERS outdated??? add folders to function call?
    html = template.render(title=title, sitename=SITENAME, description=description,
    author=AUTHOR, picture=picture, previous=previous, next=next,
    footer=FOOTER, folder_name=folder_name, folders=FOLDERS, pic_name=pic_name, 
    pic_content=pic_content, pages=MD_FILES, config=pic_config)
    # create html from template and put it in 'html' folder
    file = "html/" + u_folder_name + "/" + stripped_picture + ".html"
    with open(file, "w+") as html_single:
        html_single.write(html)
    # print success message
    print("Individual page for picture '{}' with name '{}' created.".format(picture, pic_name))


def create_index():
    '''
    Create index page with feature pic
    and content from config
    '''
    # get vars
    title = AUTHOR + " | Portfolio" # TODO maybe also change in config
    description = title # TODO change
    gallery_configs = get_gallery_configs(FOLDERS)
    # get template
    template = env.get_template("index.html")
    # fill template with vars and create it
    html = template.render(title=title, sitename=SITENAME, description=description,
    author=AUTHOR, content=CONTENT, footer=FOOTER, folders=FOLDERS, 
    pages=MD_FILES, configs=gallery_configs)
    # TODO delete folders from template?
    # create html from template and put it in 'html' folder
    file = "html/index.html"
    with open(file, "w+") as html_index:
        html_index.write(html)
    # print success message
    print("Index created.")


def create_portfolio():
    '''
    The right order in which to execute all functions to create a full-fledged
    static portfolio site
    '''
    print("Compressing pictures...")
    compress_and_save_pictures("img")
    print("Creating html from md files...")
    create_html_for_all_md("txt", MD_FILES)
    print("Creating config files...")
    create_gallery_configs()
    print("Creating index...")
    create_index()
    print("Creating gallery indices...")
    create_galleries()
    

if __name__ == "__main__":
    print("Creating your portfolio site...")
    create_portfolio()
