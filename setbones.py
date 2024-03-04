import re
import bpy
from bpy.types import Operator
from .settings import *
from .propsetting import set_prop_allbones, set_props_bones


class KJ_set_bones(Operator):
    bl_idname = "kjsetupbones.operator"
    bl_label = "set_bones"
    bl_description = "Setup target bones"
    rpt_txt = "WARNING: set armature"


    def rl_re_search(self, hits, j):
        if j=="":
            return hits
        elif j=="_R":
            p = r"_R|Right"
        elif j=="_L":
            p = r"_L|Left"
        return [name for name in hits if bool(re.search(p, name, flags=re.IGNORECASE))]


    def name_re_search(self, scene, bnames, x, v, j=""):
        p = r""
        for id, s in enumerate(v):
            if id==0:
                p = p + s
            else:
                p = p + "|" + s
        hits = [name for name in bnames if bool(re.search(p, name, flags=re.IGNORECASE))]
        hits = self.rl_re_search(hits, j)
        if hits:
            setattr(scene, f"Kjwc{x}", hits[0])
            bnames.remove(hits[0])
        else:
            setattr(scene, f"Kjwc{x}", "None")


    def bones_mapping(self, context, bnames, names, rl=[""], fings={"":""}):
        for j in rl:
            for k,v in names.items():
                for i in fings.keys():
                    x = k+i+j
                    self.name_re_search(context.scene, bnames, x, v, j)


    def execute(self, context):
        scene = context.scene
        wm = context.window_manager
        objects = bpy.data.objects
        tgt_obj = objects[scene.KjwcTargetArmature.name]
        # set props
        if not scene.KjwcTargetArmature:
            self.report({"WARNING"}, self.rpt_txt)
            return {"FINISHED"}

        obj_name = scene.KjwcTargetArmature.name
        set_prop_allbones(obj_name)
        set_props_bones()
        wm.KjwcBody = True
        wm.KjwcArms = True
        wm.KjwcLegs = True
        wm.KjwcFingerR = True
        wm.KjwcFingerL = True

        bnames = [bone.name for bone in tgt_obj.data.bones]
        rl = ["_L", "_R"]
        self.bones_mapping(context, bnames, MARROW_NAMES)
        self.bones_mapping(context, bnames, ARM_NAMES, rl=rl)
        self.bones_mapping(context, bnames, LEG_NAMES, rl=rl)
        self.bones_mapping(context, bnames, FINGER_NAMES, rl=rl, fings=FINGER_JOINT_NAMES)

        self.rpt_txt = "Bones setup finished"
        self.report({"INFO"}, self.rpt_txt)
        return {"FINISHED"}
