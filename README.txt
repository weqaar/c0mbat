c0mbat - Zero-Configuration Management and Build Automorphic Tool

Author: Weqaar Janjua <weqaar.janjua@gmail.com>
Version: 3.7a


Requirements
------------
* Linux
* Python 2.x
* Computer sense!

Install Dependencies
--------------------
* run "bootstrap.sh" for options
* ./bootstrap.sh -d <INSTALL_DIR>

Running application
-------------------
* cd <INSTALL_DIR>
* python c0mbat.py -h

Detailed Documentation
----------------------
* see README.txt - https://github.com/weqaar/c0mbat/tree/master/src
* See PDF document - https://github.com/weqaar/c0mbat/blob/master/docs/build/latex/c0mbat-ProductDocumentation.pdf

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

** If you run into any error(s) building any of these doc formats, most probably appropriate packages/libraraies aren't available on your system, install them first!
