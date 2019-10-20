Tags
====

Tags are how you associate Tasks with certain Hosts.

If you don't specify any tags when you register your Tasks, the Task will be
run for each Host in the current environment.

If you specify any tags, then the Task will only get run on Hosts with a
matching tag. An example tag is ``'database'``, for a database server.

.. code-block:: python

    task_registry = TaskRegistry()
    task_registry.register(TaskOne, tags=['database'])

    @task_registry.register(tags=['load_balancer'])
    class TaskTwo(Task):
        async def run(self):
            print("Running on load_balancer servers")
