# Gallery

## DONE First milestone
[x] Create a nice looking html gallery from a bunch of jpegs in a folder.
[x] Downsize all jpegs for web consumption.

## DONE Second milestone
[x] Create individual pages for each picture
[x] Add links to next and previous pages to each single picture
    [x] add next_pic, previous_pic to template vars (in python file)
    [x] with the help of enumerate  function in for loop on line 81 (for i, item in enumerate(list): if i > 0...) of met range.
    [x] add next and previous to template and to single page function
    [x] if next_pic or previous_pic is NONE, don't show link (in template)

## DONE Third milestone
[x] adjust addresses to fit for web server in html dir.
[x] add index html with featured pic (best pic of every gallery, random pick every time site is updated?)
[x] Create header and footer for standard start page freelance portfolio
[x] header central: author (other color, clickable), below navbar centralized vs header left author and right navbar
[x] get text for footer from yaml (?) file in txt directory.
[x] make vertical pics right height: set max-height in css (or other solution, like object-fit scale-down)
[x] make a home page (index.html) with a list of the galleries or with one FEATURED pic.
[x] change gallery.htmls to index.htmls in each corresponding folder
[x] too much dirs: img dir in each gallery folder and not separate with apart folders...

## DONE Fourth milestone
[x] make projects autopopulate dropdown with gallery folders and links to them (except for active gallery)
[x] Rename pictures (number and name of folder). Make helper function for renaming.
[x] Add text to those individual pages, based on individual md files in other folder (txt. Link to photo by id/conf var in file itself)
[x] If img folder contains "about.md" add this text as html to the gallery overview page. (or YAML: is easier, can even be numbered)
[x] Add alt name to img (from md or YAML file)

## DONE Fifth milestone
[x] function md change into dir html?
[x] make system for converting about page and cv page. Markdown to html converter (txt dir)
[x] make markdown be parsed by jinja and NEW template (page.html)?
[x] fix menu links when browsing in gallery
[x] All files in txt dir will become links in the nav bar!

##  DONE Sixth milestone
[x] if no description or content beneath picture, leave empty (change template YAML function)
[x] Create a beutiful header
[x] add sitename apart from author name
[x] name above picture, content beneath picture (or beside)
[x] Delete link to startpage on startpage
[x] Change INDEX as squarespace (no dropdown menu, but picture links)

## Seventh Milestone
[x] Numbering error: mismatch jpeg nr.s and yaml (1, 10, 11 in stead of 1,2,3): in CREATE_GALLERIES function
[x] Add BULMA
[x] Create NAVBAR in Bulma
[x] Create Footer in Bulma
[x] Add BULMA to SINGLE page
    [x] Single photo without text
    [x] Single photo with text
    [x] Center Portrait pics (nest inside COLUMNS)
    [x] Center first and last pics
    [x] What to do with title and text? On the photo (overlay)? Under the photo...
    [x] fix mismatch error
    [x] get footer stick below
    [x] get picture to fill viewport, but not stick out (edit general img tag in css (.grid img))
[x] Add BULMA to GALLERY page
    [x] create function to differentiate between portrait and landscape photo's (and square!)
    [x] description + title on pic (black text on white background)
    [x] tile rest of pictures. If LS, then 2 vertical tiles. If SQ or LS, 1 tile. (tile groups)
    [x] end of page: link to next or previous gallery
    [x] Add BULMA to START page
    [x] make grid with featured photos
[x] Add BULMA to ABOUT page
    [x] change the css

## Eighth Milestone
[x] titels van de tabs
[x] Add FTP upload functionality
[x] Write About page
[x] Write Readme.md
[x] Pick best photos
[x] Write Gallery descriptions
[x] Revise about page
[x] Upload site
[x] Change css (title on pics, black and white, no accent color, only black frame around text in monotype)
[x] Make movie
[x] Revise Readme.md
[x] Upload files to CS50
[x] Submit
[x] CS50 enter as final work

## Ninth Milestone
[ ] Make script to delete everything from site
[ ] In index folder name wijzigen!!
[ ] Add Title tag to gallery config (in case of capitalization problems or other wishes)
[ ] gallery: no more first picture in grid. Start with featured picture.
[ ] Pic navigation with keyboard arrows (html attribute?)
[ ] Exif files met copyrightgegevens enz.
[ ] Featured pic in YAML en functie die het in de map plaatst en converteert In de YAML per foto een FEATURED link toevoegen. (FEATURED:YES)
[ ] rewrite reload script: delete html files and all other files (config) before recreating
[ ] Background color, font and font color config in YAML (per gallery)
[ ] No nonsense design zoals https://note.nkmk.me/en/python-opencv-pillow-image-size/. Nog inspiratie: https://www.thierryvanleephotography.com/singles, https://www.squarespace.com/templates/balboa-demo, https://www.squarespace.com/templates/pazari-demo



## Last milestone
[ ] Add header with facebook, twitter and so on SEO and copyright data
[ ] Refactor
[ ] Sell it! - As as skeleton with custom css / as a SASS / stand-alone app?
[ ] Brand name: fotki
[ ] Config through web page (form)
[ ] Add blogging functionality (extra)
[ ] Sell as skeleton with possibility to adapt css
[ ] 3 themes: elegant, brutal, fun
[ ] Use it myself
[ ] Make colleagues try it
[ ] Sell online as SAAS or stand-alone solution
[ ] Add accent color per gallery
[ ] Make top level img dir accept files (change compress and save pictures function, os.listdir)