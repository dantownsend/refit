import os

import asyncssh

from . import settings


class FileMixin():

    async def create_file(self, path):
        """
        Create an empty file on the remote server.
        """
        await self.raw(
            f'touch {path}'
        )

    async def create_folder(
        self,
        path: str,
        owner='root',
        group='root',
        permissions='755'
    ):
        """
        Creates folder, and all intermediate directories.

        Only changes the group and owner of the deepest directory. If each
        folder in the chain needs certain permissions, call this function
        repeatedly for each folder.

        """
        await self.raw(
            f'mkdir -p {path} && '
            f'chown {owner}:{group} {path} && '
            f'chmod {permissions} {path}'
        )

    async def path_exists(self, path) -> bool:
        """
        Whether or not the path exists on the remote machine.
        """
        # Not perfect ... but ok for now.
        response = await self.raw(
            f'stat {path}',
            raise_exception=False
        )
        return (response.exit_status == 0)

    async def upload_file(
        self,
        local_path,
        remote_path,
        root=settings.FILES_FOLDER
    ):
        """
        Upload a file using scp to the remote machine.
        """
        full_local_path = os.path.join(
            root,
            local_path
        )

        connection = await self.host.get_connection()

        self._print_command(f'Uploading: {local_path} -> {remote_path}\n')

        return await asyncssh.scp(
            full_local_path,
            (connection, remote_path)
        )
