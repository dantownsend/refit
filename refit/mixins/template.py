import os
import typing as t
import uuid

import asyncssh
import jinja2

from .base import MixinBase


ENVIRONMENT = jinja2.Environment(enable_async=True)


class TemplateMixin(MixinBase):
    async def upload_template(
        self,
        local_path: str,
        remote_path: str,
        context: t.Dict[str, t.Any],
        root="",
    ):
        """
        Render a jinja template using the provided context, and upload it
        to the remote server using scp.
        """
        full_local_path = os.path.join(root, local_path)

        with open(full_local_path) as f:
            template = f.read()

        template = ENVIRONMENT.from_string(template)

        contents = await template.render_async(**context)

        tmp_name = str(uuid.uuid4())
        tmp_file_path = f"/tmp/{ tmp_name }"

        with open(tmp_file_path, "w") as f:
            f.write(contents)

        connection = await self.host_class.get_connection()

        self._print_command(f"Uploading: {local_path} -> {remote_path}\n")

        return await asyncssh.scp(tmp_file_path, (connection, remote_path))
