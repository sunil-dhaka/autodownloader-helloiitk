# `Hello IITK video downloader`

It is a simple script that automates resources(like videos, pdfs etc) downloading from Hello IITK website.
---
`Working:`
- login using request session
- collect lectures data from api
- simple loop to get necessary info
- create dirs and download files that are not there in dirs

## todos
- [ ] add progressbar for request downloads
- [ ] add resume functionality for request downloads
- [ ] add visual confirmation with progressbar

---
`Project files tree`
```
.
├── downloader.py
├── forumsScrapper.py
├── LICENSE
└── README.md
```
---
`How to use from cdl`    
- make script executable(here name of script is: `downloader.py`)
    ```sh
    chmod +x `name-of-script`
    ```
    - add a shebang line(`#!bin/sh`) that points to system `Python` interpreter
    ```python
    #-----add this line at the top of your script-----#
    #!/usr/bin/env python 
    #----- above is specific for python-------#
    ```
    - create `~/bin` directory in user home directory
    ```sh
    mkdir --parents ~/bin
    # to avoid exisiting parent error flag it with `--parents`
    ```
    - rename script and copy it into `~/bin` directory
    ```sh
    mv script.py script
    cp script ~/bin
    ```
    - add `PATH` to the `.bash_profile` or `.profile` file
    ```sh
    gedit .bash_profile
    ## add this line into `.bash_profile`
    export PATH=$PATH":$HOME/bin" # this needs to be excat
    ```
- change to the dir where you want to create course dirs and download resources
- execute the command ... and give appropriate inputs