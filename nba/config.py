import os


# Where are we?
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))


# Where is our data director
DATA_DIRECTORY = os.path.join(PROJECT_ROOT, "data")


# The location of our sqlite database relative to the root
DATABASE_LOCATION = os.path.join(DATA_DIRECTORY, "gbling.db")


# The location of model files
MODEL_DIRECTORY = os.path.join(DATA_DIRECTORY, "model")
