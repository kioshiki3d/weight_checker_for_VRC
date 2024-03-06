import os
import glob
import bpy
from bpy.types import PropertyGroup
from bpy.props import PointerProperty, BoolProperty, FloatProperty, EnumProperty
from .settings import *


def read_path():
    path_base = os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons") # LOCAL
    addon_path = glob.glob(os.path.join(path_base, "weight_checker_for_VRC*"))
    PATH = os.path.join(addon_path[0], "source", f"{OBJ_SOURCE}.fbx")
    return PATH


def set_allbones_items(obj_name):
    items = [("", "", "")]
    if obj_name=="":
        return items
    obj = bpy.data.objects[obj_name]
    items.append(("None", "None", ""))
    for bone in obj.data.bones:
        items.append((bone.name, bone.name, ""))
    return items


def set_prop_allbones(obj_name):
    bpy.types.Scene.KjwcBoneNames = EnumProperty(
        name="all bones",
        items=set_allbones_items(obj_name)
        )


def set_unselected_bone_items():
    items = bpy.types.Scene.KjwcBoneNames.keywords["items"]
    return items


def set_props_bones():
    scene = bpy.types.Scene
    for k in BONES_LIST:
        setattr(
            scene,
            f"Kjwc{k}",
            EnumProperty(
                name=f"bones list {k}",
                description="select bone",
                items=set_unselected_bone_items(),
            )
        )


def remove_objects():
    actions = bpy.data.actions
    armatures = bpy.data.armatures
    meshes = bpy.data.meshes
    collections = bpy.data.collections
    for act in actions:
        act_name = act.name
        act_name = act_name.replace(f"{OBJ_SOURCE}|", "")
        act_name = act_name.replace("|Base Layer", "")
        if act_name in ACTION_NAMES:
            actions.remove(act)
    if armatures.get(OBJ_SOURCE):
        armatures.remove(armatures[OBJ_SOURCE])
    if meshes.get(f"{OBJ_SOURCE}Mesh"):
        meshes.remove(meshes[f"{OBJ_SOURCE}Mesh"])
    if armatures.get(f"{OBJ_SOURCE}Roll"):
        armatures.remove(armatures[f"{OBJ_SOURCE}Roll"])
    if collections.get(COLL_SOURCE):
        collections.remove(collections[COLL_SOURCE])


def filter_armature(self, object):
    return (object.type=="ARMATURE") and (object.name!=OBJ_SOURCE)


def set_props():
    scene = bpy.types.Scene
    scene.KjwcTargetArmature = PointerProperty(
        name="TargetArmature",
        type=bpy.types.Object,
        poll=filter_armature,
        )
    scene.KjwcLinkBool = BoolProperty(default=False)
    set_prop_allbones("")
    set_props_bones()

    wm = bpy.types.WindowManager
    wm.KjwcBody = BoolProperty(default=False)
    wm.KjwcArms = BoolProperty(default=False)
    wm.KjwcLegs = BoolProperty(default=False)
    wm.KjwcFingerR = BoolProperty(default=False)
    wm.KjwcFingerL = BoolProperty(default=False)


def clear_props():
    remove_objects()
    bpy.context.scene.KjwcLinkBool = False
    del bpy.types.Scene.KjwcTargetArmature
    del bpy.types.Scene.KjwcLinkBool
    del bpy.types.Scene.KjwcBoneNames
    for k in BONES_LIST:
        delattr(bpy.types.Scene, f"Kjwc{k}")

    del bpy.types.WindowManager.KjwcBody
    del bpy.types.WindowManager.KjwcArms
    del bpy.types.WindowManager.KjwcLegs
    del bpy.types.WindowManager.KjwcFingerR
    del bpy.types.WindowManager.KjwcFingerL
