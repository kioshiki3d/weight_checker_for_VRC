from math import sin, cos
from mathutils import Quaternion
import bpy
from bpy.types import Operator
from bpy.props import FloatProperty, EnumProperty
from .settings import *
from .linkbones import KJ_link_ang


def set_ani_items():
    items = [("", "", "")]
    for act_name in ACTION_NAMES[1:]:
        items.append((act_name, act_name, ""))
    return items


class KJ_weight_checker(KJ_link_ang):
    bl_idname = "kjweightcheck.operator"
    bl_label = "weight_checker"
    bl_description = "weight check dialog menu"
    bl_options = {"REGISTER", "UNDO"}

    PropAni: EnumProperty(
        name="pattern",
        description="animation list",
        items=set_ani_items(),
    )
    PropSlider: FloatProperty(
        name="slider",
        default=0,
        min=-1,
        max=1,
        options={"SKIP_SAVE"},
    )


    @classmethod
    def poll(cls, context):
        return context.scene.KjwcLinkBool


    def weight_checker(self, context):
        scene = context.scene
        objects = bpy.data.objects
        actions = bpy.data.actions
        src_obj = objects[OBJ_SOURCE]
        dmy_obj = objects[f"{OBJ_SOURCE}Roll"]
        tgt_obj = objects[scene.KjwcTargetArmature.name]

        src_obj.select_set(True)
        context.view_layer.objects.active = src_obj
        ani_params = self.PropAni if self.PropAni!="" else ACTION_NAMES[0]
        src_obj.animation_data.action = actions[f"{OBJ_SOURCE}|{ani_params}|Base Layer"]
        frm = int(self.PropSlider * STD_FRAME)
        scene.frame_current = STD_FRAME + frm
        if ani_params in ACTION_NAMES[1:]:
            try:
                bpy.ops.object.mode_set(mode = "OBJECT")
            except:
                pass
            src_obj.select_set(False)
            dmy_obj.select_set(True)
            self.reset_pose(context, dmy_obj)
            context.view_layer.objects.active = dmy_obj
            bpy.ops.object.mode_set(mode = "POSE")
            for bname in BONES_LIST:
                src_bone = src_obj.pose.bones.get(bname)
                dmy_bone = dmy_obj.pose.bones.get(bname)
                tgt_bname = getattr(scene, f"Kjwc{bname}")
                if (tgt_bname=="") or (tgt_bname=="None"):
                    continue

                ang_std = dmy_bone.rotation_quaternion
                ang_move = src_bone.rotation_quaternion
                d_roll = self.src_roll[bname] - self.tgt_roll[tgt_bname]
                ang_roll = Quaternion((0, 1, 0), d_roll)
                ang_roll_v = Quaternion((0, -1, 0), d_roll)
                ang = ang_roll @ ang_move @ ang_roll_v
                dmy_bone.rotation_mode = "QUATERNION"
                dmy_bone.rotation_quaternion = ang
                """
                if dmy_bone_name=="Hips":
                    loc_move = list(src_bone.location)
                    x = loc_move[0]*sin(d_roll)
                    y = loc_move[1]
                    z = -loc_move[2]*cos(d_roll)
                    dmy_bone.location = (x, y, z)
                """
            bpy.ops.object.mode_set(mode = "OBJECT")


    def execute(self, context):
        self.collection_exclude(context, False)
        self.weight_checker(context)
        self.collection_exclude(context, True)
        return {"FINISHED"}
