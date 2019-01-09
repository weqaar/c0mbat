.. _Introduction:

============
Introduction
============


General Introduction
====================

c0mbat is a Configuration Management tool developed with `Slack <http://www.slack.com>`_. 

c0mbat is short for Zero-Configuration Management and Build `Automorphic <https://en.wikipedia.org/wiki/Automorphic_number>`_ Tool.


Product
=======

c0mbat is intended for configuration management in Cloud Infrastructures.

* Features
  
  #. Multi-threaded (uses multiple cores as scheduled by the OS or by user i.e. numa utils)
  #. Parallel deployment currently over SSH channel
  #. Application wide configuration file: c0mbat.conf
  #. APT package manager handling: install, uninstall (remove), update
  #. Services handling: start, stop, restart, reload
  #. Inventory and Artifacts handled seprately under dir "deploy"

       #. deploy/artifacts
       #. deploy/inventory

  #. Idempotency with deployments: keeps MD5 Hashes as deployment cache for each host and it's artifact relationships

      #. Filesystem hash of individual artifacts under deploy/artifacts
      #. Configuration hash of individual artifacts, defined in deploy/artifacts/artifacts.json
      #. Hashes are maintained as cache under "cache/cache.json" that is built after initial run
      #. In ideal situation this should be a distributed cache accessible over IP i.e. NoSQL DB, to allow multiple client's to sync

  #. Two types of deployments currently supported

     #. APT package manager based
     #. Manual

  #. Manual type deployments support Permssions, this is specified optionally as artifact's metadata (see deploy/artifacts/artifacts.json)

  #. Logging under dir "logs/"

  #. Cleanup runtime/transient data with the script "clean.sh". Note this cleans up the logs and cache as well.


Availability of code
====================

Available on Github at `c0mbat repo <https://github.com/weqaar/c0mbat>`_


Architectrure / Code Walk-through
=================================

Structure
---------

Code is organized in this hierarchy 

|l1tree|

  .. |l1tree| image:: images/c0mbat-l1.png
           :width: 60 %
           :scale: 50 %


Code is functionally divided as packages

|l2tree|

  .. |l2tree| image:: images/c0mbat-l2.png
           :width: 60 %
           :scale: 50 %


Code re-usability
-----------------

Source code allows for easy reuse of various components

  #. All variables and objects are initailized as run-time from "packages/conf/configinit.py"
  #. Initialized objects are available at run-time in "packages/globalvars.py"
  #. Re-use is as simple as calling the desired object with globalvars.<object>
     
     #. Example: to log a debug message use - globalvars._stats_logger.debug("YOUR MESSAGE!")
  

Usage
========

  #. Installation instructions `README.txt <https://github.com/weqaar/c0mbat/blob/master/README.txt>`_ 
  #. c0mbat provides a CLI Interface, run with: python c0mbat.py -h


Inventory
---------

Hosts or Nodes are defined in the inventory file "inventory.json" available under "deploy/inventory/" directory.

Format is:::

    "Host" : {
        "Address" : "0.0.0.0",
        "Auth" : { "username": "root", "password" : "r00t" },
        "disabled" : false,
        "Artifacts" : ["artifact-1", "artifact-2"]
    },


Artifacts
---------

Artifacts are the source files and/or directories that need deployment on a remote node. 
These are defined in the artifacts file "artifacts.json" available under "deploy/artifacts/" directory.

Format is:::

   "Apache" : {
        "pkg-type": "apt",
        "pkg-name" : "apache2",
        "pkg-action" : "install",
        "pre-deploy-trigger" : "update",
        "post-deploy-trigger" : "restart",
        "service-name" : "apache2"
    },
    "php-app" : {
        "pkg-type": "manual",
        "pkg-action" : "install",
        "pkg-path" : "/var/www/html",
        "dependency" : {
            "service-name" : "apache2",
            "pre-deploy-trigger" : null,
            "post-deploy-trigger" : "restart"
        },
        "metadata" : {
        "owner" : "www-data",
        "group" : "www-data",
        "mode" : "644"
        }
    }


Artifacts of type "manual" must then be placed under filesystem path as under:::

   deploy/artifacts/php-app/


Relationship between 'Inventory' and 'Artifacts'
------------------------------------------------

There is one-to-many relationship between Inventory and Artifact elements.

|one-to-many|

  .. |one-to-many| image:: images/one-to-many.png
                   :width: 80 %
                   :scale: 50 %


To clarify this relationship, a single node may relate to many Artifacts. As an example:

* Inventory::

    "Zebra" : {
        "Address" : "10.10.10.10",
        "Auth" : { "username": "root", "password" : "r00t" },
        "disabled" : false,
        "Artifacts" : ["Apache", "php-app"]
    },  


* Artifacts::

   "Apache" : {
        "pkg-type": "apt",
        "pkg-name" : "apache2",
        "pkg-action" : "install",
        "pre-deploy-trigger" : "update",
        "post-deploy-trigger" : "restart",
        "service-name" : "apache2"
    },
    "php-app" : {
        "pkg-type": "manual",
        "pkg-action" : "install",
        "pkg-path" : "/var/www/html",
        "dependency" : {
            "service-name" : "apache2",
            "pre-deploy-trigger" : null,
            "post-deploy-trigger" : "restart"
        },
        "metadata" : {
        "owner" : "www-data",
        "group" : "www-data",
        "mode" : "644"
        }
    }


Host "Zebra" needs to be deployed Artifacts "Apache" and "php-app", thus it relates to both of them.

