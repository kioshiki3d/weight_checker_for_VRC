import bpy
from bpy.types import Panel, Menu
from .settings import *
from .setbones import KJ_set_bones
from .linkbones import KJ_link_bones
from .weightchecker import KJ_weight_checker


class KJ_WCfV_Panel(Panel):
    bl_label = "weight checker for VRC"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "kjtools"


    def draw(self, context):
        layout = self.layout
        scene = context.scene
        wm = context.window_manager

        layout.prop_search(scene, "KjwcTargetArmature", bpy.data, "objects", text="", icon="ARMATURE_DATA")
        layout.separator()

        link_bool = scene.KjwcLinkBool
        link_text = "Linked" if link_bool else "Link"

        row_setup = layout.row(align=True)
        row_setup.enabled = not link_bool
        row_setup.operator(KJ_set_bones.bl_idname, text="Setup")
        layout.operator(KJ_link_bones.bl_idname, text=link_text, depress=link_bool)
        row_check = layout.row(align=True)
        row_check.enabled = link_bool
        row_check.operator(KJ_weight_checker.bl_idname, text="Check")
        # layout.prop(scene,"KjwcBoneNames")

        # marrow
        row_body = layout.row(align = True)
        row_body.enabled = not link_bool
        row_body.alignment = "LEFT"
        row_body.prop(wm, "KjwcBody", icon="TRIA_DOWN" if wm.KjwcBody else "TRIA_RIGHT", text="Body", emboss=False)
        if wm.KjwcBody:
            for k in MARROW_NAMES.keys():
                layout.prop(scene, f"Kjwc{k}", text=k)
        # arms
        row_arms = layout.row(align = True)
        row_arms.enabled = not link_bool
        row_arms.alignment = "LEFT"
        row_arms.prop(wm, "KjwcArms", icon="TRIA_DOWN" if wm.KjwcArms else "TRIA_RIGHT", text="Arms", emboss=False)
        if wm.KjwcArms:
            for j in ["_L", "_R"]:
                for k in ARM_NAMES.keys():
                    x = k+j
                    layout.prop(scene, f"Kjwc{x}", text=x)
        # legs
        row_legs = layout.row(align = True)
        row_legs.enabled = not link_bool
        row_legs.alignment = "LEFT"
        row_legs.prop(wm, "KjwcLegs", icon="TRIA_DOWN" if wm.KjwcLegs else "TRIA_RIGHT", text="Legs", emboss=False)
        if wm.KjwcLegs:
            for j in ["_L", "_R"]:
                for k in LEG_NAMES.keys():
                    x = k+j
                    layout.prop(scene, f"Kjwc{x}", text=x)
        # finger Left
        row_fngl = layout.row(align = True)
        row_fngl.enabled = not link_bool
        row_fngl.alignment = "LEFT"
        row_fngl.prop(wm, "KjwcFingerL", icon="TRIA_DOWN" if wm.KjwcFingerL else "TRIA_RIGHT", text="Finger Left ", emboss=False)
        if wm.KjwcFingerL:
            for k in FINGER_NAMES.keys():
                for i in FINGER_JOINT_NAMES.keys():
                    x = k+i+"_L"
                    layout.prop(scene, f"Kjwc{x}", text=x)
        # finger Right
        row_fngr = layout.row(align = True)
        row_fngr.enabled = not link_bool
        row_fngr.alignment = "LEFT"
        row_fngr.prop(wm, "KjwcFingerR", icon="TRIA_DOWN" if wm.KjwcFingerR else "TRIA_RIGHT", text="Finger Right", emboss=False)
        if wm.KjwcFingerR:
            for k in FINGER_NAMES.keys():
                for i in FINGER_JOINT_NAMES.keys():
                    x = k+i+"_R"
                    layout.prop(scene, f"Kjwc{x}", text=x)
