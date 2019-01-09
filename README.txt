c0mbat - Zero-Configuration Management and Build Automorphic Tool

Author: Weqaar Janjua <weqaar.janjua@gmail.com>
Version: 3.6 alpha


Requirements
------------
* Linux
* Python 2.x
* Computer sense!

Install Dependencies
--------------------
run "bootstrap.sh" in root application folder

Running application
-------------------
cd src/
python c0mbat.py -h (CLI provides you with options)

Docs
----
* cd docs/build
** Document formats available: pdf, html, singlehtml, text, man

* Build/update documentation
** cd docs/
** pdf -> make latexpdf
** html -> make html
** singlehtml -> make singlehtml
** text -> make text
** man -> make man

** If you run intp errors building any of these doc formats, most probably appropriate packages/libraraies aren't available on your system, install them first!
