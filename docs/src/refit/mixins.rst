.. _Mixins:

Mixins
======

The ``Task`` class inherits from many mixins, which provide a lot of useful
utilities for performing common server admin tasks.

AptMixin
--------

.. autoclass:: refit.mixins.apt.AptMixin
    :members:
    :undoc-members:

DockerMixin
-----------

.. autoclass:: refit.mixins.docker.DockerMixin
    :members:
    :undoc-members:

FileMixin
---------

.. autoclass:: refit.mixins.file.FileMixin
    :members:
    :undoc-members:

PathMixin
---------

.. autoclass:: refit.mixins.path.PathMixin
    :members:
    :undoc-members:

PythonMixin
-----------

.. autoclass:: refit.mixins.python.PythonMixin
    :members:
    :undoc-members:

SystemdMixin
------------

.. autoclass:: refit.mixins.systemd.SystemdMixin
    :members:
    :undoc-members:


TemplateMixin
-------------

.. autoclass:: refit.mixins.template.TemplateMixin
    :members:
    :undoc-members:

Custom Mixins
-------------

There's nothing magical about the builtin mixins - you can develop your own,
and inherit from them.

.. code-block:: python

    from refit.task import Task


    class MyMixin():
        def hello_world(self):
            print('hello world')


    class MyTask(Task, MyMixin):
        async def run(self):
            self.hello_world()
