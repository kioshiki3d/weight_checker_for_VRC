import bpy
from bpy.types import Operator
from .settings import *
from .propsetting import read_path, remove_objects


class KJ_link_ang(Operator):
    src_roll = {}
    tgt_roll = {}


    def collection_exclude(self, context, exclude=False):
        layer_coll = context.view_layer.layer_collection.children[COLL_SOURCE]
        layer_coll.exclude = exclude
        return layer_coll


    def reset_pose(self, context, obj):
        context.view_layer.objects.active = obj
        for bone in obj.data.bones:
            bone.select = True
        bpy.ops.object.mode_set(mode = "POSE")
        bpy.ops.pose.rot_clear()
        bpy.ops.object.mode_set(mode = "OBJECT")


class KJ_link_bones(KJ_link_ang):
    bl_idname = "kjlinkbones.operator"
    bl_label = "link_bones"
    bl_description = "link target bones"


    def generate_source(self, context):
        collections = bpy.data.collections
        objects = bpy.data.objects
        actions = bpy.data.actions
        armatures = bpy.data.armatures
        action_names_full = [f"{OBJ_SOURCE}|{name}|Base Layer" for name in ACTION_NAMES]
        # objects check
        fbx_data = 0
        for act in actions:
            if act.name in action_names_full:
                fbx_data+=1
        for amt in armatures:
            if OBJ_SOURCE==amt.name:
                fbx_data+=1
        if fbx_data < 9:
            remove_objects()

        # create collection
        if not(COLL_SOURCE in collections):
            new_coll = collections.new(COLL_SOURCE)
            context.scene.collection.children.link(new_coll)
        # active collection
        layer_coll = self.collection_exclude(context, False)
        context.view_layer.active_layer_collection = layer_coll

        # import FBX
        obj_list = [ob.name for ob in objects]
        if not OBJ_SOURCE in obj_list:
            bpy.ops.import_scene.fbx(filepath=read_path())
            src_obj = objects[OBJ_SOURCE]
        else:
            src_obj = objects[OBJ_SOURCE]
            coll_list = [c.name for c in src_obj.users_collection]
            if not COLL_SOURCE in coll_list:
                collections[COLL_SOURCE].objects.link(src_obj)
                for name in coll_list:
                    collections[name].objects.unlink(src_obj)
        # copy sourceOBJ
        if not objects.get(f"{OBJ_SOURCE}Roll"):
            src_dat = src_obj.data.copy()
            src_dat.name = f"{OBJ_SOURCE}Roll"
            dmy_obj = objects.new(f"{OBJ_SOURCE}Roll", src_dat)
            collections[COLL_SOURCE].objects.link(dmy_obj)
            src_obj.rotation_mode = "XYZ"
            src_obj_rot = src_obj.rotation_euler
            src_obj_scl = src_obj.scale
            dmy_obj.rotation_mode = "XYZ"
            dmy_obj.rotation_euler = src_obj_rot
            dmy_obj.scale = src_obj_scl
        #layer_coll.exclude = True


    def read_roll(self, context, obj, dct):
        context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode = "EDIT")
        for bone in obj.data.edit_bones:
            dct[bone.name] = bone.roll
        bpy.ops.object.mode_set(mode = "OBJECT")


    def set_constraint(self, context, tgt_obj, src_obj=None):
        scene = context.scene
        context.view_layer.objects.active = tgt_obj
        bpy.ops.object.mode_set(mode = "POSE")
        for bname in BONES_LIST:
            tgt_bname = getattr(scene, f"Kjwc{bname}")
            if (tgt_bname=="") or (tgt_bname=="None"):
                continue
            tgt_data_bone = tgt_obj.data.bones.get(tgt_bname)
            context.object.data.bones.active = tgt_data_bone
            tgt_data_bone.select = True
            tgt_bone = tgt_obj.pose.bones.get(tgt_bname)
            # remove constraints
            copyLocConstraints = [c for c in tgt_bone.constraints if c.type=="COPY_ROTATION"]
            for c in copyLocConstraints:
                tgt_bone.constraints.remove(c)
            # atatch constraints
            if src_obj:
                constraint = tgt_bone.constraints.new(type="COPY_ROTATION")
                constraint.target = src_obj
                constraint.subtarget = bname
        bpy.ops.object.mode_set(mode = "OBJECT")


    def unlink_bones(self, context):
        scene = context.scene
        objects = bpy.data.objects
        src_obj = objects[OBJ_SOURCE]
        dmy_obj = objects[f"{OBJ_SOURCE}Roll"]
        tgt_obj = objects[scene.KjwcTargetArmature.name]
        self.reset_pose(context, src_obj)
        self.reset_pose(context, dmy_obj)
        self.reset_pose(context, tgt_obj)
        self.set_constraint(context, tgt_obj)


    def link_bones(self, context):
        scene = context.scene
        objects = bpy.data.objects
        actions = bpy.data.actions
        src_obj = objects[OBJ_SOURCE]
        dmy_obj = objects[f"{OBJ_SOURCE}Roll"]
        tgt_obj = objects[scene.KjwcTargetArmature.name]
        src_obj.animation_data.action = actions[f"{OBJ_SOURCE}|{ACTION_NAMES[0]}|Base Layer"]
        # pose reset
        self.reset_pose(context, src_obj)
        self.reset_pose(context, dmy_obj)
        self.reset_pose(context, tgt_obj)
        # read roll
        self.read_roll(context, tgt_obj, self.tgt_roll)
        self.read_roll(context, src_obj, self.src_roll)
        # atatch roll to source_dummy
        context.view_layer.objects.active = dmy_obj
        bpy.ops.object.mode_set(mode = "EDIT")
        for bname in BONES_LIST:
            dmy_bone = dmy_obj.data.edit_bones.get(bname)
            tgt_bname = getattr(scene, f"Kjwc{bname}")
            if (tgt_bname=="") or (tgt_bname=="None"):
                continue
            dmy_bone.roll = self.tgt_roll[tgt_bname]
        bpy.ops.object.mode_set(mode = "OBJECT")
        # constraint
        self.set_constraint(context, tgt_obj, dmy_obj)
        bpy.ops.object.mode_set(mode = "OBJECT")
        tgt_obj.select_set(True)


    def execute(self, context):
        scene = context.scene
        wm = context.window_manager
        try:
            bpy.ops.object.mode_set(mode = "OBJECT")
        except:
            pass
        # Link to Unlink
        if scene.KjwcLinkBool:
            # bone unlink
            self.collection_exclude(context, False)
            self.unlink_bones(context)
            scene.frame_current = 0

            rpt_txt = "unlink bones"
            scene.KjwcLinkBool = False
        # Unlink to Link
        else:
            wm.KjwcBody = False
            wm.KjwcArms = False
            wm.KjwcLegs = False
            wm.KjwcFingerR = False
            wm.KjwcFingerL = False
            # generate source
            self.generate_source(context)
            # bone link
            self.link_bones(context)
            scene.frame_current = STD_FRAME

            rpt_txt = "link bones"
            scene.KjwcLinkBool = True

        self.collection_exclude(context, True)
        self.report({"INFO"}, rpt_txt)
        return {"FINISHED"}
