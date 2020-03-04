import bpy

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


# RiggingHelper -> UI
def AddEmptyRigHlp_button(self, context):
    self.layout.operator(
        SWIFTLY_OT_AddEmptyRigHlp.bl_idname,
        text="Swiftly: add RiggingHelper",
        icon='OUTLINER_OB_EMPTY')


# RiggingHelper -> Operator
class SWIFTLY_OT_AddEmptyRigHlp(bpy.types.Operator):
    """Add Empty to current selected location"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "view3d.swiftlyemptyadd"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Swiftly: Add Empty to current selected location"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.

        bpy.ops.view3d.snap_cursor_to_selected()

        empt = bpy.data.objects.new("empty", None)

        empt.location = bpy.context.scene.cursor.location
        empt.name = "RiggingHelper"
        empt.empty_display_size = 0.08
        empt.empty_display_type = 'SPHERE'

        # create new collection
        coll = bpy.data.collections.new('RiggingHelpers')
        # or find the existing collection
        coll = bpy.data.collections['RiggingHelpers']

        # link the newCol to the scene
        try:
            bpy.context.scene.collection.children.link(coll)
        except Exception:
            print("")

        # link the object to collection
        coll.objects.link(empt)

        # Lets Blender know the operator finished successfully.
        return {'FINISHED'}


# Registration and Unregistration
def register():
    bpy.utils.register_class(SWIFTLY_OT_AddEmptyRigHlp)
    bpy.types.VIEW3D_MT_mesh_add.append(AddEmptyRigHlp_button)


def unregister():
    bpy.utils.unregister_class(SWIFTLY_OT_AddEmptyRigHlp)
    bpy.types.VIEW3D_MT_mesh_add.remove(AddEmptyRigHlp_button)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
