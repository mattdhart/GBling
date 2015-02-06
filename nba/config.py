import os


# Where are we?
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))


# The location of our sqlite database relative to the root
DATABASE_LOCATION = os.path.join(PROJECT_ROOT, "data/gbling.db")
