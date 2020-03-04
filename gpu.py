import bpy
import os
from sys import platform

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


# GPU Panel -> UI
class GpuPanel(bpy.types.Panel):
    bl_idname = "SWIFTLY_PANEL1_PT_gpuinfo"
    bl_label = "GPU info"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Swiftly"

    _gpuinfo1 = ""
    _gpuinfo2 = ""

    def draw(self, context):
        layout = self.layout

        layout.operator(operator="view3d.swiftlygetgpuinfo", text="update", icon="RECOVER_LAST")

        layout.label(text=self._gpuinfo1, icon="OUTLINER_OB_FORCE_FIELD")
        layout.label(text=self._gpuinfo2, icon="OUTLINER_OB_FORCE_FIELD")

        # col = layout.column(align=True)

        # temparr = NVsmi_getinfo()

        # row = col.row(align=True)
        # row.label(text=temparr[0] + " C", icon="OUTLINER_OB_FORCE_FIELD")
        # row.label(text=temparr[1], icon="FORCE_WIND")

        # row.label(text=self._gputemp, icon="OUTLINER_OB_FORCE_FIELD")
        # row.label(text=self._fanspeed, icon="FORCE_WIND")
        # row.operator("view3d.swiftlygpuinfoget", text="Essential Menu", icon="OUTLINER_OB_FORCE_FIELD")
        # self.layout.label(text=temparr[0], icon="OUTLINER_OB_FORCE_FIELD")
        # self.layout.label(text=temparr[1], icon="FORCE_WIND")


# GPUinfo -> Operator
class SWIFTLY_OT_GetGPUinfo(bpy.types.Operator):
    """get gpu info from sys command"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "view3d.swiftlygetgpuinfo"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Get GPU info"         # Display name in the interface.

    def execute(self, context):        # execute() is called when running the operator.
        # self.report({"INFO"}, "button pressed")
        # gpuinfostr = str.split(NVsmi_getinfo(), "/n")
        gpuinfostr = NVsmi_getinfo().splitlines()
        print(len(gpuinfostr))
        if len(gpuinfostr) == 1:
            GpuPanel._gpuinfo1 = gpuinfostr[0]
        else:
            GpuPanel._gpuinfo1 = gpuinfostr[0]
            GpuPanel._gpuinfo2 = gpuinfostr[1]

        # GpuPanel._gputemp = temparr[0] + " C"
        # GpuPanel._fanspeed = temparr[1]

        return {'FINISHED'}


# slow system call
def NVsmi_getinfo():
    # system call
    # timeline = (datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    # print(timeline)

    if platform == "linux" or platform == "linux2":
        # linux
        gpuinfo = str(os.popen(r'nvidia-smi --query-gpu=temperature.gpu,fan.speed,memory.used,memory.free --format=csv,noheader').read())
    elif platform == "darwin":
        # OS X
        print("! no osx command, yet here !")
    elif platform == "win32":
        gpuinfo = str(os.popen(r'"C:\Program Files\NVIDIA Corporation\NVSMI\nvidia-smi.exe" --query-gpu=temperature.gpu,fan.speed,memory.used,memory.free --format=csv,noheader').read())
    else:
        print("unknown platform:" + platform)

    # temparr = str.split(temp, ", ")
    return gpuinfo.replace('\n', '\r\n')


# Registration and Unregistration
def register():
    bpy.utils.register_class(SWIFTLY_OT_GetGPUinfo)
    bpy.utils.register_class(GpuPanel)


def unregister():
    bpy.utils.unregister_class(SWIFTLY_OT_GetGPUinfo)
    bpy.utils.unregister_class(GpuPanel)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
