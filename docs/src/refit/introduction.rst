Introduction
============

Welcome to Refit - simple remote server configuration, using asyncio.

Installation
------------

Make sure Python 3.7 or above is installed, then install the following
(preferably in a virtualenv):

.. code-block:: bash

    pip install refit

Creating a project
------------------

For the purposes of the documentation, we'll assume we're creating a pet shop
web app.

.. code-block:: bash

    refit scaffold pet_shop

This will create a ``deployments`` folder in the current directory, with a
``pet_shop`` folder inside, containing a ``hosts.py`` and ``tasks.py`` file.

You can create as many different deployments as you like - each one represents
a collection of tasks which achieve some objective. For example deploying a
web app, or configuring a database server.

Hosts
-----

In the hosts file, we define the remote machines we want to connect to.

It's important that each ``Host`` gets registered with the ``HostRegistry``.
The recommended way of doing this is using the decorator syntax.

.. literalinclude:: ../../../example_project/deployments/pet_shop/hosts.py

.. hint:: Refit uses SSH to communicate with remote servers. In order to access
   your remote servers, make sure your SSH public key is present in the
   ``known_hosts`` file on each remote server. For example,
   ``/home/my_user/.ssh/known_hosts``.

Tasks
-----

Tasks are what get run on hosts. Examples are uploading files, or running a
bash command.

Similarly to ``Host``, it's important that each ``Task`` gets registered with
the ``TaskRegistry``, otherwise it won't get run.

.. literalinclude:: ../../../example_project/deployments/pet_shop/tasks.py

The order in which a ``Task`` is added to the registry determines the order
in which it runs.

run
~~~

Each Task has an ``async run`` method, which performs the actual work.

You can do whatever you like within this method, but a lot of the time you'll
be calling other Task methods, which implement the bulk of Refit's
functionality. Under the hood, these are implemented as :ref:`Mixins`.

Running tasks
-------------

Once you have defined your hosts and tasks, you run them with the following
command:

.. code-block:: bash

    refit deploy --environment=test pet_shop

You'll notice in your hosts file that there's multiple ``Host`` subclasses,
one for each environment. You need to specify which environment you want to
deploy to when running your tasks.
