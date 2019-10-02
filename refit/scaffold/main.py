import os

from jinja2 import Environment, FileSystemLoader

from .. import __VERSION__


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


ENV = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def make_titlecase(text: str) -> str:
    return text.title().replace(" ", "")


def scaffold(deployment_name: str):
    """
    Scaffold a project.
    """
    current_directory = os.getcwd()
    deployments_folder = os.path.join(current_directory, "deployments")
    if not os.path.exists(deployments_folder):
        print(f"Creating deployment folder at {deployments_folder}")
        os.mkdir(deployments_folder)

    folder_name = deployment_name.lower().replace(" ", "_")

    sub_folder = os.path.join(deployments_folder, folder_name)
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)

    render_kwargs = {
        "titlecase_name": make_titlecase(deployment_name),
        "refit_version": __VERSION__,
    }

    for filename in ("hosts.py.jinja", "tasks.py.jinja"):

        template = ENV.get_template("hosts.py.jinja")
        output_filename = filename.rsplit(".", maxsplit=1)[0]

        with open(os.path.join(sub_folder, output_filename), "w") as f:
            f.write(template.render(**render_kwargs))
