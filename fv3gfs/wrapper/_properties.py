import os
import json

DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(DIR, "dynamics_properties.json"), "r") as f:
    DYNAMICS_PROPERTIES = json.load(f)

with open(os.path.join(DIR, "physics_properties.json"), "r") as f:
    PHYSICS_PROPERTIES = json.load(f)

DIM_NAMES = {
    properties["name"]: properties["dims"]
    for properties in DYNAMICS_PROPERTIES + PHYSICS_PROPERTIES
}
