import sys
import os
path_to_append = os.path.join(os.path.dirname(__file__), os.pardir, "mockportfolio")
print(path_to_append)
sys.path.append(path_to_append)
