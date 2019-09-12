<p align="center">
    <img src="./logo.png" width="180">
</p>

<p align="center">
  <a href="https://github.com/X1Zeth2X/zimmermanv2/commits/master">
    <img src="https://img.shields.io/github/last-commit/X1Zeth2X/zimmermanv2" alt="last-commit">
  </a>
  <a>
    <img src="https://img.shields.io/github/v/release/X1Zeth2X/zimmermanv2?include_prereleases" alt="release">
  </a>
  <a>
    <img src="https://img.shields.io/badge/python-3.6%2B-blue" alt="python">
  </a>
  <a>
    <img src="https://img.shields.io/badge/contributions-welcome-brightgreen" alt="contributions">
  </a>
  <a href="./LICENSE.md">
    <img src="https://img.shields.io/github/license/x1zeth2x/zimmermanv2" alt="license">
  </a>
</p>

Zimmerman's repository, which is Konishi's backend written in Python 3+. Zimmerman is a free and open source REST API that aims to have the core features of Facebook groups with the added bonus of transparency, flexibility, and other FOSS goodness.

Official frontend repo can be found [here](https://github.com/x1zeth2x/kagawasan). (Please note that the frontend is currently broken due to library updates, and upgrades to other components, fixes and updates coming soon.)


## Requirements

This version uses PostgreSQL although you can use SQLite if you wish to.

When creating a Postgres Database, make sure to name it 'konishidb' or whatever you like and change the config name for the database in `zimmerman/main/config.py`

**PostgreSQL Installation**

This can vary for many different distributions/operating systems.
You can find many guides for that through your distribution's guide/community. (https://www.postgresql.org)


This may also work for their derivatives but make sure to double check as well, it isn't going to harm anybody.. except maybe your distro...

Resourceful Links for the commonly used distros ;)

* Debian - (https://wiki.debian.org/PostgreSql)

* Ubuntu - 
(https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04)

* Arch Linux - (https://wiki.archlinux.org/index.php/PostgreSQL)

* Gentoo - (https://wiki.gentoo.org/wiki/PostgreSQL/QuickStart)

## Contributing

The Konishi project is a community project which includes Zimmerman. We are welcoming contributors who would like to make an impact in the project and eventually the social networking industry.

Current guidelines for contributing is currently work in progress but here are currently the ways you can help.

Feel free to contact the lead developer [X1Zeth2X](https://github.com/X1Zeth2X) for further or other inquiries.

* Contributing to the source code.
* Contributing to the documentation of the APIs.
* Financial support/contribution.
* Suggesting improvements, features.

## Install and Setting up

**Clone the repo**
```bash
$ git clone https://github.com/X1Zeth2X/zimmermanv2.git
$ cd zimmermanv2
```

**Create the virtualenv and activate**
```bash
$ virtualenv konishienv
$ source konishienv/bin/activate
```

**Install dependencies**
```bash
$ pip install -r requirements.txt
```

**Setting up the database** 

After metting the requirements and installing PostGreSQL, make sure you've set the configurations to match your local PSQL credentials. Afterwards initialize the database to work with the app using:

```bash
$ python manage.py db init
$ make migrate
```

**Running the application**
```bash
$ python manage.py run
```