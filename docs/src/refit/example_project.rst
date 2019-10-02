Example Project
===============

Let's bring it all together with an example project.

Hosts
-----

.. literalinclude:: ../../../example_project/deployments/pet_shop/hosts.py

Tasks
-----

Each Task has an ``async run`` method, which performs the actual work.

.. literalinclude:: ../../../example_project/deployments/pet_shop/tasks.py

You can do whatever you like within this method, but a lot of the time you'll
be calling other Task methods, which implement the bulk of Refit's
functionality. Under the hood, these are implemented as :ref:`Mixins`.
