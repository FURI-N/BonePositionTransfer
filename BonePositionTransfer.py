import bpy

bl_info = {
    "name": "Bone Position and Rotation Transfer",
    "blender": (3, 3, 0),
    "category": "Object",
}

class BoneTransferOperator(bpy.types.Operator):
    bl_idname = "object.bone_transfer_operator"
    bl_label = "Start Transfer"
    bl_description = "Transfer bone positions and rotations from Armature A to Armature B based on matching bone names"
    
    transfer_position: bpy.props.BoolProperty(name="Transfer Position", default=True)
    transfer_rotation: bpy.props.BoolProperty(name="Transfer Rotation", default=True)

    def execute(self, context):
        source_armature = context.scene.source_armature
        dest_armature = context.scene.dest_armature

        if not source_armature or not dest_armature:
            self.report({'ERROR'}, "Source or Destination Armature not specified")
            return {'CANCELLED'}

        # オブジェクトモードに切り替え
        bpy.context.view_layer.objects.active = source_armature
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.context.view_layer.objects.active = dest_armature
        bpy.ops.object.mode_set(mode='EDIT')

        # EditBoneへの参照を取得
        source_bones = source_armature.data.edit_bones
        dest_bones = dest_armature.data.edit_bones

        # ボーンの名前が一致する場合、位置と回転を転送
        for source_bone in source_bones:
            self.report({'INFO'}, source_bone.name)
            if source_bone.name in dest_bones:
                dest_bone = dest_bones[source_bone.name]
                self.report({'INFO'}, dest_bone.name)

                # 位置の転送
                if self.transfer_position:
                    dest_bone.head = source_bone.head
                    dest_bone.tail = source_bone.tail

                # 回転の転送
                if self.transfer_rotation:
                    dest_bone.roll = source_bone.roll

        self.report({'INFO'}, "Bone transfer completed")
        return {'FINISHED'}

class BoneTransferPanel(bpy.types.Panel):
    bl_label = "Bone Transfer"
    bl_idname = "VIEW3D_PT_bone_transfer_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Edit'

    def draw(self, context):
        layout = self.layout

        layout.prop(context.scene, "source_armature")
        layout.prop(context.scene, "dest_armature")
        
        layout.label(text="Transfer Options:")
        layout.prop(context.scene, "transfer_position")
        layout.prop(context.scene, "transfer_rotation")

        layout.operator("object.bone_transfer_operator", text="Start Transfer")

# プロパティの登録
def register():
    bpy.utils.register_class(BoneTransferOperator)
    bpy.utils.register_class(BoneTransferPanel)

    bpy.types.Scene.source_armature = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.dest_armature = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.transfer_position = bpy.props.BoolProperty(name="Transfer Position", default=True)
    bpy.types.Scene.transfer_rotation = bpy.props.BoolProperty(name="Transfer Rotation", default=True)

# プロパティの解除
def unregister():
    bpy.utils.unregister_class(BoneTransferOperator)
    bpy.utils.unregister_class(BoneTransferPanel)

    del bpy.types.Scene.source_armature
    del bpy.types.Scene.dest_armature
    del bpy.types.Scene.transfer_position
    del bpy.types.Scene.transfer_rotation

if __name__ == "__main__":
    register()
