class TaskRunner():

    def __init__(self, tasks):
        self.tasks = tasks

    async def entrypoint(self):
        await self.run(self.tasks)

    async def run(self, tasks):
        """
        Recursively executes all of the tasks.
        """
        for task in tasks:
            for sub_task in task.sub_tasks:
                await self.run(sub_task)
            await task.entrypoint()

    async def inspect(self, tasks):
        """
        Not sure about this yet, but need something that inspects the task
        tree, and outputs a visualisation.
        """
        pass
