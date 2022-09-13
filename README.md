# Static Portfolio Website Generator

#### Video Demo: https://youtu.be/AxG8uRAjkvA

## Description
Convert an `img` folder filled with jpeg files to a static portfolio website for photographers or other visual artists. Markdown texts in a `txt` folder are converted to separate HTML pages on the website. The resulting files and folders are automatically uploaded to a web server over FTP.

## Reasoning
 After some false starts, I was looking for a feasible project. Being an amateur photographer, I need a portfolio site. Existing solutions like Squarespace don't offer self-hosted setups and have a subscription model I find too expensive. I always liked the idea of static websites, where folders of markdown files automatically get converted into HTML pages and reside on your pc, giving you full control over the process. However, I couldn't find any static site builders specifically targeted to visual artists' portfolios. So I decided to create one for myself, inspired by Squarespace templates.

## How it works
1) **Add pictures**: users fill the `img` folder with jpegs they want to showcase on their website. Each subfolder will represent an image gallery on the portfolio website. The picture size in MB doesn't matter.
2) **Enter personal data**: users enter their data into the `config.yaml` file.
3) **Generate the HTML**: users run the `reload.sh` bash script. This script launches the file `create.py`, which contains the main functionality and creates the HTML pages for the website: home page, gallery pages, individual picture pages and text pages, such as an about page. `create.py` also creates `yaml` config pages, in which users can enter personal information and add text and titles to the individual photo and gallery pages. Finally, `reload.sh` starts a local web server so that users can check and edit the resulting website before uploading.
4) **Add gallery and image descriptions**: after a first run of `reload.sh`, the HTML structure is ready, but users still have to configure the website to reflect their personal preferences. Therefore, users should open the `txt` folder and edit the individual `yaml` pages as they see fit. If users want to add text to photographs, the final layout will automatically change to accommodate the added text. After entering the additional information, users should rerun the `reload.sh` script. Now the website is ready to be uploaded to the server.
5) **Upload the website**: before uploading your website, make sure you've entered your sftp credentials in the `config.yaml` script. Run the script. Your site is now online and will render very fast: the jpegs are optimised for online viewing and the server serves static web pages.
6) **Keep the site updated**: if you want to make any changes or edits, just make changes in the existing `yaml` files or add a new folder with images to the `img` folder. The `create.py` script checks for changes in existing `yaml` files and creates new ones where necessary. After rerunning `reload.sh` and `upload.py`, your site will be fully updated.

## The `create.py` file in detail

### Imported libraries

To implement the main functionality, I used the following libraries: `os`, `re`, `yaml`, `markdown`, `PIL` and `jinja2`.

The `os` library is used for file, path and directory manipulation, as I am working with static files, residing on my hard drive.

The `re` regex library is used to implement additional filtering functions to use in my `jinja` templates.

The `yaml` library is used to store and read user data, residing in `yaml` config files. I considered `yaml` to be the most readable and editable format for this purpose.

The `markdown` library is used to convert the pages, written in markdown, into HTML.

The `PIL` library is used to compress the jpeg files (that can be large) to smaller jpegs (both in pixel and in byte size), to make the site load faster and the resulting images less prone to unauthorised usage. As of now, the sizes are hard-coded into the script, but it might be useful to have an option to change them in the main config file. Another extra feature might be to use the jpegs' EXIF data for navigation purposes (tags, filtering, sorting: a javascript solution, to avoid generating hundreds of pages for all possible combinations). The `PIL` library is also used to check if a picture is taken in landscape or portrait mode so that the galleries have a more esthetically pleasing look.

And finally, I use the `jinja2` template library that does the heavy lifting of converting all the data into HTML pages. I chose *not* to create an entire `Flask` app, as the templating library was all I needed for this static website. Flask's routing, authentication or web form parsing functionality was not needed.

### Functions

#### Helper functions

The first five functions, `strip_jpg`, `strip_md`, `clean_folder_name`, `folder_name_to_title` and `get_previous_and_next`, are filter functions that I added to templates for the purposes of cleaning up file and folder names, in order to use them as titles on my web pages. The last function gets the previous and last picture in every gallery, to make the arrow navigation work.

The following function, `compress_pictures`, prepares the pictures to be used on the website, changing their size and their names.

The following three functions, `compress_pictures`, `get_image_folders`, `nice_name_picture`, `get_pic_orientation` are helper functions that I created to simplify the functions that contain the main functionality (creating the pages from the templates).

`create_gallery_configs` checks, for every picture folder in `img`, if the root directory contains a corresponding `yaml` config file. If not, it creates these files, based on the template in `create_config_template`, the following function.

`parse_gallery_config` parses the data of each gallery's config file and passes this data to the templating functions.

`list_md_files` gets a list of markdown files, to be used by the following function, `convert_md_into_html`, that converts all the markdown content to HTML pages.

`get_gallery_configs` is a function that sends the data of all config files to the function that creates the main home page.

#### Main functionality

The functions `create_page_from_md` and `create_html_for_all_md` create the final markdown pages based on the `jinja` templates, residing in the `templates` folder.

`create_gallery` creates an individual gallery from a folder and is used by `create_galleries`, which creates HTML pages of all galleries from all folders.

`compress_and_save_pictures` uses the previously mentioned helper function `compress_pictures` to take all pictures in the `img` folder, prepare them and save them in the `html` folder, which contains all the files that have to be uploaded to the server.

The functions `create_single_picture` and `create_index` respectively create all the individual picture pages and the main home page, using the corresponding `jinja` templates in the `templates` folder.

And finally, to generate the entire website, there is the wrapper function `create_portfolio`, which contains all the previously mentioned functions and outputs status or error messages to the user while the website is being created.

## The `upload.py` file in detail

The `upload.py` script uses the pysftp library to upload the HTML files that the `create.py` script generated onto a web server. This script uses the same structure as `create.py`: helper functions followed by the main functionality. The main function has been written as a recursive function because I have to walk through a nested folder structure. I had to resort to this solution because the internal batch processing functions of the `pysftp` library did not appear to work under Windows, the operating system I am using.

## File structure

### The `config.yaml` file

In this file, users can alter the website title, the author's name and the footer text. SFTP connection data are also stored in this file. For users using Git, it is important to add this file to `.gitignore`, because it contains confidential login information.

### The `templates` directory

The `templates` folder contains all the templates needed for the creation of a portfolio website. The website contains four types of pages: an individual picture page (`picture.html`), ordinary HTML pages, converted from markdown (`page.html`), the home page (`index.html`) and the gallery indices (`gallery.html`) containing an overview of all pictures in a gallery. All the templates are based on the `base.html` template, which contains repeated content (ex. headers and footers).

### The `html` directory

After the `create.py` script has been run, this folder is filled with the final HTML pages, CSS files and images. Images used in the markdown files are saved in the root directory, next to `index.html` and the two `css` files, `main.css` and `custom.css`. For every gallery, a separate folder is created. This folder contains an `img` folder with the converted jpegs, an `index.html` for the gallery in question and the individual HTML files for every picture.

### The `txt` directory

The `txt` directory contains all the extra HTML pages the user wants to add to the site, like for example an about page or a cv. These pages have to be written in markdown to be seen by the script. They are converted to HTML and a link to these pages is added to the top menu of the website.

This directory also contains all the config files for the galleries in `yaml` format, so that the user can easily alter their content and regenerate the website.

#### A gallery config file in detail

Each gallery config file contains clear instructions for how to fill it in and offers several customisation possibilities:

Users can choose to:

- Enter an introduction text for each gallery (where and why the pictures were taken, for example)
- Pick a *featured picture* to be used on the main index pages (home page and main gallery page)
- Pick a title and a description for each picture, that appears on the individual page for the corresponding picture.

## CSS framework

I picked [Bulma](https://bulma.io) as a CSS framework because I prefer it above Bootstrap. I have kept CSS to a minimum. The `main.css` file contains the CSS needed to compose the picture galleries and the layout, while `custom.css` can be used to make the website more esthetically pleasing (adding colours, changing fonts, etc.) or to personalise it.

## Ideas for the future

- `reload.sh`: rewrite this script or offer a more user-friendly solution, to convince colleagues to use the system.

## Conclusion
I had a lot of fun creating this small program. It was challenging but feasible. I underestimated the time it would take. To keep things manageable, I divided the project into milestones (see `TODO.md` for details) that got adapted while I created the program and encountered new problems to solve. I learned to use the basics of Git and even created and merged a branch when trying out new functionality.

Seasoned programmers will probably have a good laugh at how I solved several problems and how much time it took me to tackle them, but hey, I made it to the finish line.

I will use this program for my website and hope to further optimize it, first of all, to make it useable by colleague photographers.

My ultimate goal is to make a living as a programmer. I am trying to find out which steps I should take next.