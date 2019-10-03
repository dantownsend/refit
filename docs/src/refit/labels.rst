Labels
======

Labels are how you associate Tasks with certain Hosts.

If you don't specify any labels when you register your Tasks, the Task will be
run for each Host in the current environment.

If you specify any labels, then the Task will only get run on Hosts with a
matching label. An example label is ``'database'``, for a database server.

.. code-block:: python

    task_registry = TaskRegistry()
    task_registry.register(TaskOne, labels=['database'])

    @task_registry.register(['load_balancer'])
    class TaskTwo(Task):
        async def run(self):
            print("Running on load_balancer servers")
