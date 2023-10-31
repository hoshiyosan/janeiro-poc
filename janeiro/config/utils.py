import inspect
import os


def package_relative_path(path: str):
    parent_folder = os.path.dirname(inspect.stack()[1].filename)
    absolute_path = os.path.join(parent_folder, path)
    return absolute_path
