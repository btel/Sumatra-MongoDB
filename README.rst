This is an implementation of data server working with sumatra -
web-based electronic labbook: http://neuralensemble.org/trac/sumatra.

The data is sent to the server via http_store (sumatra plugin) and
stored in a MongoDB database: http://www.mongodb.org/

Files
-----



Instructions
------------


1. Run an instance of mongodb. For more information see MongoDB
   quickstart: http://www.mongodb.org/display/DOCS/Quickstart

#. Install pymongo and httplib2:

      easy_install pymongo
      easy_install httplib2

#. Run the server from the command-line:

      python json_server.py

#. Create a sumatra project:

      smt init --plugins=sumatra.recordstore.http_store TestProject
      smt configure -e python -m test.py

   Please use the http_store from this repository as it takes care to set
   the correct url and port number (either copy it to sumatra tree or set
   the python path to the directory containing the supplied http_store in
   which case you can remove sumatra.recordstore prefix from the command above).

#. Now you can run the simulations:

      smt run 

#. The server does not implement GET method (yet!). In order to access
   the data you will need to use mongo client:

      $ mongo
      > use smtdb
      > db.simulations.find()

   The data sent by http_store client should be in the database

TODO
----

* implement GET and DELETE methods (see http_store)
* add web interface (could smtweb be used here?)
* define parameters as a seprerate mongodb collections

Authors
-------

Client (http_store.py): Andrew Davison

Server (json_server.py): Bartosz Telenczuk
