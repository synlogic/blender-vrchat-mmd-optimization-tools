import bpy

bl_info = {"name": "VRChat MMD Bone Fix",
           "category": "Rigging",
           "author": "SynLogic",
           "version": (0, 1),
           "description": "Correctly parents MMD Bones for use in VRChat"}

class BoneFix(bpy.types.Operator):
    """Reparents bones in an optimal way for VRChat use"""
    bl_idname = "rigging.bonefix"
    bl_label = "VRChat MMD Bone Fix"
    bl_options = {'REGISTER', 'UNDO'}
        
    def execute(self, context):
        print('executed')
        #initialize lists
        bone_list = ['Shoulder_R', 'Arm_R', 'Elbow_R', 'Wrist_R', 'Shoulder_L', 'Arm_L', 'Elbow_L', 'Wrist_L']
        parent_list = ['UpperBody2']
        for item in bone_list: 
            parent_list.append(item)
            
        # Grab selected object information
        obj = bpy.context.object
        
        #raise exception if selected object is not an armature
        if obj.type != 'ARMATURE':
            raise TypeError('Object selected must be of type ARMATURE')
        
        #auto set mode to edit and deselect all objects
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.select_all(action='DESELECT')
        
        #Iterate through list of bones and reparent bones to the optimal format for VRChat
        arm = obj.data
        for bone in arm.bones:
            if bone.name in bone_list:
                
                bpy.ops.armature.select_all(action='DESELECT')
                parent_bone = arm.edit_bones[parent_list[ bone_list.index( bone.name ) ] ]
                child_bone = arm.edit_bones[bone.name]
                
                print( "Parenting {0} to {1}".format(child_bone.name, parent_bone.name) )
                
                parent_bone.select = True
                child_bone.select = True
                
                child_bone.parent = parent_bone
                
        return {"FINISHED"}

class GUIPanel(bpy.types.Panel):
    bl_label = "VRChat MMD Bone Fix"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "VRChat MMD Bone Fix"
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator('rigging.bonefix', text='Fix Bones')

    
def register():
    bpy.utils.register_class(BoneFix)
    bpy.utils.register_class(GUIPanel)

def unregister():
    bpy.utils.unregister_class(BoneFix)
    bpy.utils.unregister_class(GUIPanel)

if __name__ == "__main__":
    register()
    print("MMD Bone Fix loaded")


