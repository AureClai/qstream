import os

BASE_DIR = os.path.dirname(__file__)
def absolutePath(relativePath):
    return os.path.join(BASE_DIR, relativePath)

old_name = absolutePath('baseQstream/base.gpkg')