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
           :width: 50 %
           :scale: 50 %


Code is functionally divided as packages

|l2tree|

  .. |l2tree| image:: images/c0mbat-l2.png
           :width: 50 %
           :scale: 50 %


Code re-usability
-----------------

Source code allows for easy reuse of various components

  #. All variables and objects are initailized as run-time from "packages/conf/configinit.py"
  #. Initialized objects are available at run-time in "packages/globalvars.py"
  #. Re-use is as simple as calling the desired object with globalvars.<object>
     
     #. Example: to log a debug message use - globalvars._stats_logger.debug("YOUR MESSAGE!")
  

5. Usage
========

  #. Installation instructions `README.txt <https://github.com/weqaar/c0mbat/blob/master/README.txt>`_ 
  #. c0mbat provides a CLI Interface, run with: python c0mbat.py -h

