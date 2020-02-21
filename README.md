Task
=====

NDA

Intro
======
For this task I've chosen Django Python Web framework that encourages rapid development and clean, pragmatic design.

And "tox" to automate and standardize testing in Python. It is part of a larger vision of easing the packaging, testing and release process of Python software.


Requirements
------

* Python 3.7.1
* pip
* tox (https://tox.readthedocs.io/en/latest/)

Setup
------

1. First, install tox with

        pip install tox

2. Launch the development server:

        tox -e runserver

    Tox will install all requirements into private python virtualenv

3. By default Web server listen on http://127.0.0.1:9000


Tests
------

The unit and functioning tests are located under the *tests/* directory. To execute it, just type: _tox_


Data model
==========
URL data model consists with following fields:

* target - saves the target address;
* tiny - saves the "shortener" address;
* created - datatime when record's created. Default current;
* usage_count - how many time this record was called


Settings
=========

* SHORT_URL_MIN_LENGTH - settings control the lengths (and bruteforce attack complexity at whole) of the tiny URL
* SHORT_URL_MAX_LENGTH_SCALING - settings control the hash windows scaling

Assumptions
===========

1. Ipv6 URLs is not full supported

2. target and tiny URLs max_lengths has strict limit up to 2048 symbols because some  browsers have a "Address bar" length limit:

        Browser     Address bar   document.location
                                    or anchor tag
        ------------------------------------------
        Chrome          32779           >64k
        Android          8192           >64k
        Firefox          >64k           >64k
        Safari           >64k           >64k
        IE11             2047           5120
        Edge 16          2047          10240

3. Cleanup/Records expiration functionality haven't implemented
