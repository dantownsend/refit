import json


class DockerMixin():

    async def pull_docker_image(self, image_name):
        await self.raw(
            f'docker pull {image_name}'
        )

    async def docker_compose_up(self, compose_file_path):
        await self.raw(
            f'docker-compose -f {compose_file_path} up -d'
        )

    async def get_docker_network_names(self):
        response = await self.raw(
            f'curl --unix-socket /var/run/docker.sock http:/networks'
        )
        network_data = json.loads(response.stdout)
        return [i['Name'] for i in network_data]

    async def create_docker_network(self, network_name):
        if not network_name in await self.get_docker_network_names():
            await self.raw(
                f'docker network create {network_name}'
            )

    async def docker_prune(self):
        await self.raw(
            f'yes | docker system prune'
        )
