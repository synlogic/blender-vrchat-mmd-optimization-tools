import bpy

bl_info = {"name": "VRChat MMD Optimization Tools",
           "category": "Rigging",
           "author": "SynLogic",
           "version": (0, 1),
           "description": "Optimizes MMD models imported through MMD-Tools for use in VRChat"}

class BoneFix(bpy.types.Operator):
    """Reparents bones in an optimal way for VRChat use"""
    bl_idname = "rigging.bonefix"
    bl_label = "VRChat MMD Bone Fix"
    bl_options = {'REGISTER', 'UNDO'}
        
    def execute(self, context):
        print('====Executing MMD Bone Fix====')
        #initialize lists
        bone_list = ['Shoulder_R', 'Arm_R', 'Elbow_R', 'Wrist_R', 'Shoulder_L', 'Arm_L', 'Elbow_L', 'Wrist_L']
        parent_list = ['UpperBody2']
        remove_list = ['ParentNode', 'Center', 'Groove', 'CenterTip']
        for item in bone_list: 
            if item != 'Wrist_L' and item != 'Wrist_R':
                parent_list.append(item)
            if item == 'Wrist_R':
                parent_list.append('UpperBody2')
        print(parent_list)
        print(bone_list)
            
        # Find Armature within the scene
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.context.scene.objects:
            if obj.type == 'ARMATURE':
                arm = obj.data
                obj.select = True
                bpy.context.scene.objects.active = obj
                break
        #auto set mode to edit and deselect all objects
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.select_all(action='DESELECT')
        #Iterate through list of bones and reparent bones to the optimal format for VRChat
        for bone in arm.bones:
            if bone.name in bone_list:
                
                bpy.ops.armature.select_all(action='DESELECT')
                parent_bone = arm.edit_bones[parent_list[ bone_list.index( bone.name ) ] ]
                child_bone = arm.edit_bones[bone.name]
                
                print( "Parenting {0} to {1}".format(child_bone.name, parent_bone.name) )
                
                parent_bone.select = True
                child_bone.select = True
                
                child_bone.parent = parent_bone
                
            if bone.name in remove_list:
                arm.edit_bones.remove( arm.edit_bones[bone.name] )
        
        bpy.ops.object.mode_set(mode='OBJECT')
        return {"FINISHED"}

class MergeMeshes(bpy.types.Operator):
    bl_idname = "mesh.mesh_merge"
    bl_label = "VRChat MMD Mesh Merge"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        print('====MergeMeshes executed====')
        
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except:
            print("Already in OBJECT mode!")
        bpy.ops.object.select_all(action='DESELECT')
        mesh_count = 0
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                mesh_count += 1
                print("Mesh Count: ", mesh_count)
                bpy.context.scene.objects.active = obj
                obj.select = True
            try:
                bpy.ops.object.join()
            except:
                print("Minor Error Occured, continuing")
        
        return {'FINISHED'}

class Optimize(bpy.types.Operator):
    """Executes all optimization functions"""
    bl_idname = "object.optimize_for_vrchat"
    bl_label = "VRChat MMD Optimize"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        print('====Executing MMD Optimization====')
        BoneFix.execute(self, context)
        MergeMeshes.execute(self, context)
        
        #Delete joints and rigidbodys
        
        return {"FINISHED"}
        
        

class GUIPanel(bpy.types.Panel):
    """GUIPanel to show in blender's UI"""
    bl_label = "MMD VRChat Optimization"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "MMD VRChat Optimization"
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column()
        col.operator('object.optimize_for_vrchat', text='Optimize')
        col.operator('rigging.bonefix', text='Fix Bones')
        col.operator('mesh.mesh_merge', text='Merge Meshes')
        

    
def register():
    bpy.utils.register_class(BoneFix)
    bpy.utils.register_class(Optimize)
    bpy.utils.register_class(MergeMeshes)
    bpy.utils.register_class(GUIPanel)

def unregister():
    bpy.utils.unregister_class(BoneFix)
    bpy.utils.unregister_class(Optimize)
    bpy.utils.unregister_class(MergeMeshes)
    bpy.utils.unregister_class(GUIPanel)

if __name__ == "__main__":
    register()
    print("====VRChat MMD Optimization Tools Loaded====")


