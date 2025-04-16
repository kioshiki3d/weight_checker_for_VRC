import bpy
from .propsetting import set_props, clear_props
from .ui import KJ_WCfV_Panel
from .setbones import KJ_set_bones
from .linkbones import KJ_link_bones
from .weightchecker import KJ_weight_checker

if "bpy" in locals():
    from importlib import reload
    import sys
    for k, v in list(sys.modules.items()):
        if k.startswith("weight_checker_for_VRC."):
            reload(v)

bl_info = {
    "name": "weight checker for VRC",
    "author": "Kageji",
    "version": (0, 0, 3),
    "blender": (3, 3, 0),
    "location": "3D View > Sidebar",
    "description": "weight checker for VRC",
    "warning": "",
    "support": "COMMUNITY",
    "wiki_url": "https://github.com/kioshiki3d/weight_checker_for_VRC",
    "tracker_url": "https://twitter.com/shadow003min",
    "category": "Object",
}

classes = [
    KJ_WCfV_Panel,
    KJ_set_bones,
    KJ_link_bones,
    KJ_weight_checker,
    ]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    set_props()
    print(f"{bl_info['name']} is active")


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    clear_props()
    print(f"{bl_info['name']} is inactive")
