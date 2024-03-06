STD_FRAME = 10
COLL_SOURCE = "WCfV source Collection"
OBJ_SOURCE = "WCfVsourceArmature"
path_base = os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons") # LOCAL
PATH = os.path.join(path_base, "weight_checker_for_VRC", "source", f"{OBJ_SOURCE}.fbx")

ACTION_NAMES = ["0 base",
    "1 Open Close",
    "2 Left Right",
    "3 Roll Left Right",
    "4 In Out",
    "5 Roll In Out",
    "6 Finger Open Close",
    "7 Finger In Out",
    ]

MARROW_NAMES = {
    "Hips": ["Hips"],
    "Spine": ["Spine"],
    "LowerChest": ["LowerChest", "Lower_Chest", "Chest", "Spine1"],
    "UpperChest": ["UpperChest", "Upper_Chest", "Spine2"],
    "Neck": ["Neck"],
    "Head": ["Head"],
}

ARM_NAMES = {
    "Shoulder": ["Shoulder"],
    "UpperArm": ["UpperArm", "Upper_Arm", "Arm"],
    "LowerArm": ["LowerArm", "Lower_Arm", "ForeArm", "Arm"],
    "Hand": ["Hand", "Wrist"],
}

LEG_NAMES = {
    "UpperLeg": ["UpperLeg", "Upper_Leg", "Thigh", "UpLeg", "Leg"],
    "LowerLeg": ["LowerLeg", "Lower_Leg", "Knee", "Leg"],
    "Foot": ["Foot", "Ankle"],
    "Toes": ["Toes", "ToeBase", "Toe"],
}

FINGER_NAMES = {
    "Thumb": ["Thumb"],
    "Index": ["Index"],
    "Middle": ["Middle"],
    "Ring": ["Ring"],
    "Little": ["Little", "Pinky"],
}

FINGER_JOINT_NAMES = {
    "Proximal": ["Proximal"],
    "Intermediate": ["Intermediate"],
    "Distal": ["Distal"],
}

BONES_LIST = []
BONES_LIST = BONES_LIST + list(MARROW_NAMES.keys())
for j in ["_L", "_R"]:
    for k in list(ARM_NAMES.keys()) + list(LEG_NAMES.keys()):
        BONES_LIST.append(k+j)
for j in ["_L", "_R"]:
    for k in FINGER_NAMES.keys():
        for i in FINGER_JOINT_NAMES.keys():
            BONES_LIST.append(k+i+j)
