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

import bpy
import os
from sys import platform

bl_info = {
    "name": "Swiftly",
    "description": "additional commands for a faster workflow",
    "author": "BlendyBlend",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh",
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_url": "none",
    "tracker_url": "https://twitter.com/blendyblend",
    "support": "COMMUNITY",
    "category": "Add Mesh"
}


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


# CopySceneSettings -> UI
class CopySceneSettingsPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Swiftly: Copy scene settings to other scenes"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.scale_y = 2.0
        row.operator("view3d.swiftlycopyscene", text="copy CURRENT scene render/output *")
        layout.label(text="* but not: frame-start/end/remap, resolutions/border")


# CopySceneSettings -> Operator
class SWIFTLY_OT_CopySceneSettings(bpy.types.Operator):
    """CopyOver Scene Settings"""
    bl_label = "CopyOver Operator"
    bl_idname = "view3d.swiftlycopyscene"

    def execute(self, context):        # execute() is called when running the operator.
        # mainsc = bpy.data.scenes[0]
        mainsc = bpy.context.scene
        print("++++ copy settings from " + mainsc.name + "++++")
        # copy over settings from current scene
        # advice, keep an (empty) scene on top, by name for settings

        # everything should copy over BUT not this, as it is scene depended (in my eyes)
        # scene.frame_start and ..._end
        # scene.render.frame_map_new and ..._old
        # resolutions and borders (but resolution percentage is synced for fast preview)
        for sc in bpy.data.scenes:
            if str(sc.name) != str(mainsc.name):
                # sc.render.as_pointer() = mainsc.render.as_pointer()
                # # sc.render.bake = mainsc.render.bake
                sc.render.bake_bias = mainsc.render.bake_bias
                sc.render.bake_margin = mainsc.render.bake_margin
                sc.render.bake_samples = mainsc.render.bake_samples
                sc.render.bake_type = mainsc.render.bake_type
                sc.render.bake_user_scale = mainsc.render.bake_user_scale
                # # sc.render.bl_rna = mainsc.render.bl_rna
                # sc.render.bl_rna_get_subclass() = mainsc.render.bl_rna_get_subclass()
                # sc.render.bl_rna_get_subclass_py( = mainsc.render.bl_rna_get_subclass_py()
                # sc.render.border_max_x = mainsc.render.border_max_x
                # sc.render.border_max_y = mainsc.render.border_max_y
                # sc.render.border_min_x = mainsc.render.border_min_x
                # sc.render.border_min_y = mainsc.render.border_min_y
                sc.render.dither_intensity = mainsc.render.dither_intensity
                # sc.render.driver_add() = mainsc.render.driver_add()
                # sc.render.driver_remove() = mainsc.render.driver_remove()
                sc.render.engine = mainsc.render.engine
                # # sc.render.ffmpeg = mainsc.render.ffmpeg
                # # sc.render.file_extension = mainsc.render.file_extension
                sc.render.filepath = mainsc.render.filepath
                sc.render.film_transparent = mainsc.render.film_transparent
                sc.render.filter_size = mainsc.render.filter_size
                sc.render.fps = mainsc.render.fps
                sc.render.fps_base = mainsc.render.fps_base
                # ! sc.render.frame_map_new = mainsc.render.frame_map_new
                # ! sc.render.frame_map_old = mainsc.render.frame_map_old
                # sc.render.frame_path() = mainsc.render.frame_path()
                # sc.render.get() = mainsc.render.get()
                sc.render.hair_subdiv = mainsc.render.hair_subdiv
                sc.render.hair_type = mainsc.render.hair_type
                # # sc.render.has_multiple_engines = mainsc.render.has_multiple_engines
                # sc.render.id_data = mainsc.render.id_data
                # # sc.render.image_settings = mainsc.render.image_settings

                sc.render.image_settings.cineon_black = mainsc.render.image_settings.cineon_black
                sc.render.image_settings.cineon_gamma = mainsc.render.image_settings.cineon_gamma
                sc.render.image_settings.cineon_white = mainsc.render.image_settings.cineon_white
                try:
                    sc.render.image_settings.color_depth = mainsc.render.image_settings.color_depth
                except Exception:
                    print('')

                sc.render.image_settings.color_mode = mainsc.render.image_settings.color_mode
                sc.render.image_settings.compression = mainsc.render.image_settings.compression
                # sc.render.image_settings.display_settings = mainsc.render.image_settings.display_settings
                sc.render.image_settings.exr_codec = mainsc.render.image_settings.exr_codec
                sc.render.image_settings.file_format = mainsc.render.image_settings.file_format
                sc.render.image_settings.jpeg2k_codec = mainsc.render.image_settings.jpeg2k_codec
                sc.render.image_settings.quality = mainsc.render.image_settings.quality
                sc.render.image_settings.cineon_black = mainsc.render.image_settings.cineon_black
                # sc.render.image_settings.rna_type = mainsc.render.image_settings.rna_type
                # sc.render.image_settings.stereo_3d_format = mainsc.render.image_settings.stereo_3d_format
                sc.render.image_settings.tiff_codec = mainsc.render.image_settings.tiff_codec
                sc.render.image_settings.use_cineon_log = mainsc.render.image_settings.use_cineon_log
                sc.render.image_settings.use_jpeg2k_cinema_48 = mainsc.render.image_settings.use_jpeg2k_cinema_48
                sc.render.image_settings.use_jpeg2k_cinema_preset = mainsc.render.image_settings.use_jpeg2k_cinema_preset
                sc.render.image_settings.use_jpeg2k_cinema_preset = mainsc.render.image_settings.use_jpeg2k_cinema_preset
                sc.render.image_settings.use_preview = mainsc.render.image_settings.use_preview
                sc.render.image_settings.use_zbuffer = mainsc.render.image_settings.use_zbuffer
                # sc.render.image_settings.view_settings = mainsc.render.image_settings.view_settings
                sc.render.image_settings.views_format = mainsc.render.image_settings.views_format

                # # sc.render.is_movie_format = mainsc.render.is_movie_format
                # sc.render.is_property_hidden() = mainsc.render.is_property_hidden()
                # sc.render.is_property_overridable_library() = mainsc.render.is_property_overridable_library()
                # sc.render.is_property_readonly() = mainsc.render.is_property_readonly()
                # sc.render.is_property_set() = mainsc.render.is_property_set()
                # sc.render.items() = mainsc.render.items()
                # sc.render.keyframe_delete() = mainsc.render.keyframe_delete(
                # sc.render.keyframe_insert() = mainsc.render.keyframe_insert()
                # sc.render.keys() = mainsc.render.keys()
                sc.render.line_thickness = mainsc.render.line_thickness
                sc.render.line_thickness_mode = mainsc.render.line_thickness_mode
                sc.render.motion_blur_shutter = mainsc.render.motion_blur_shutter
                # # sc.render.motion_blur_shutter_curve = mainsc.render.motion_blur_shutter_curve
                # sc.render.path_from_id() = mainsc.render.path_from_id()
                # sc.render.path_resolve() = mainsc.render.path_resolve()
                # sc.render.pixel_aspect_x = mainsc.render.pixel_aspect_x
                # sc.render.pixel_aspect_y = mainsc.render.pixel_aspect_y
                # sc.render.pop() = mainsc.render.pop()
                sc.render.preview_pixel_size = mainsc.render.preview_pixel_size
                sc.render.preview_start_resolution = mainsc.render.preview_start_resolution
                # sc.render.property_overridable_library_set() = mainsc.render.property_overridable_library_set()
                # sc.render.property_unset() = mainsc.render.property_unset()
                sc.render.resolution_percentage = mainsc.render.resolution_percentage
                # sc.render.resolution_x = mainsc.render.resolution_x
                # sc.render.resolution_y = mainsc.render.resolution_y
                # # sc.render.rna_type = mainsc.render.rna_type
                sc.render.sequencer_gl_preview = mainsc.render.sequencer_gl_preview
                sc.render.simplify_child_particles = mainsc.render.simplify_child_particles
                sc.render.simplify_child_particles_render = mainsc.render.simplify_child_particles_render
                sc.render.simplify_gpencil = mainsc.render.simplify_gpencil
                sc.render.simplify_gpencil_blend = mainsc.render.simplify_gpencil_blend
                sc.render.simplify_gpencil_onplay = mainsc.render.simplify_gpencil_onplay
                sc.render.simplify_gpencil_remove_lines = mainsc.render.simplify_gpencil_remove_lines
                sc.render.simplify_gpencil_shader_fx = mainsc.render.simplify_gpencil_shader_fx
                sc.render.simplify_gpencil_tint = mainsc.render.simplify_gpencil_tint
                sc.render.simplify_gpencil_view_fill = mainsc.render.simplify_gpencil_view_fill
                sc.render.simplify_gpencil_view_modifier = mainsc.render.simplify_gpencil_view_modifier
                sc.render.simplify_subdivision = mainsc.render.simplify_subdivision
                sc.render.simplify_subdivision_render = mainsc.render.simplify_subdivision_render
                sc.render.stamp_background = mainsc.render.stamp_background
                sc.render.stamp_font_size = mainsc.render.stamp_font_size
                sc.render.stamp_foreground = mainsc.render.stamp_foreground
                sc.render.stamp_note_text = mainsc.render.stamp_note_text
                # # sc.render.stereo_views = mainsc.render.stereo_views
                sc.render.threads = mainsc.render.threads
                sc.render.threads_mode = mainsc.render.threads_mode
                sc.render.tile_x = mainsc.render.tile_x
                sc.render.tile_y = mainsc.render.tile_y
                # sc.render.type_recast() = mainsc.render.type_recast()
                sc.render.use_bake_clear = mainsc.render.use_bake_clear
                sc.render.use_bake_lores_mesh = mainsc.render.use_bake_lores_mesh
                sc.render.use_bake_multires = mainsc.render.use_bake_multires
                sc.render.use_bake_selected_to_active = mainsc.render.use_bake_selected_to_active
                sc.render.use_bake_user_scale = mainsc.render.use_bake_user_scale
                sc.render.use_border = mainsc.render.use_border
                sc.render.use_compositing = mainsc.render.use_compositing
                sc.render.use_crop_to_border = mainsc.render.use_crop_to_border
                sc.render.use_file_extension = mainsc.render.use_file_extension
                sc.render.use_freestyle = mainsc.render.use_freestyle
                sc.render.use_full_sample = mainsc.render.use_full_sample
                sc.render.use_lock_interface = mainsc.render.use_lock_interface
                sc.render.use_motion_blur = mainsc.render.use_motion_blur
                sc.render.use_multiview = mainsc.render.use_multiview
                sc.render.use_overwrite = mainsc.render.use_overwrite
                sc.render.use_persistent_data = mainsc.render.use_persistent_data
                sc.render.use_placeholder = mainsc.render.use_placeholder
                sc.render.use_render_cache = mainsc.render.use_render_cache
                sc.render.use_save_buffers = mainsc.render.use_save_buffers
                sc.render.use_sequencer = mainsc.render.use_sequencer
                sc.render.use_sequencer_override_scene_strip = mainsc.render.use_sequencer_override_scene_strip
                sc.render.use_simplify = mainsc.render.use_simplify
                sc.render.use_simplify_smoke_highres = mainsc.render.use_simplify_smoke_highres
                sc.render.use_single_layer = mainsc.render.use_single_layer
                # # sc.render.use_spherical_stereo = mainsc.render.use_spherical_stereo
                sc.render.use_stamp = mainsc.render.use_stamp
                sc.render.use_stamp_camera = mainsc.render.use_stamp_camera
                sc.render.use_stamp_date = mainsc.render.use_stamp_date
                sc.render.use_stamp_filename = mainsc.render.use_stamp_filename
                sc.render.use_stamp_frame = mainsc.render.use_stamp_frame
                sc.render.use_stamp_frame_range = mainsc.render.use_stamp_frame_range
                sc.render.use_stamp_hostname = mainsc.render.use_stamp_hostname
                sc.render.use_stamp_labels = mainsc.render.use_stamp_labels
                sc.render.use_stamp_lens = mainsc.render.use_stamp_lens
                sc.render.use_stamp_marker = mainsc.render.use_stamp_marker
                sc.render.use_stamp_memory = mainsc.render.use_stamp_memory
                sc.render.use_stamp_note = mainsc.render.use_stamp_note
                sc.render.use_stamp_render_time = mainsc.render.use_stamp_render_time
                sc.render.use_stamp_scene = mainsc.render.use_stamp_scene
                sc.render.use_stamp_sequencer_strip = mainsc.render.use_stamp_sequencer_strip
                sc.render.use_stamp_strip_meta = mainsc.render.use_stamp_strip_meta
                sc.render.use_stamp_time = mainsc.render.use_stamp_time
                # sc.render.values( = mainsc.render.values()
                # # sc.render.views = mainsc.render.views
                sc.render.views_format = mainsc.render.views_format

                sc.cycles.aa_samples = mainsc.cycles.aa_samples
                sc.cycles.ao_bounces = mainsc.cycles.ao_bounces
                sc.cycles.ao_bounces_render = mainsc.cycles.ao_bounces_render
                sc.cycles.ao_samples = mainsc.cycles.ao_samples
                # sc.cycles.as_pointer() = mainsc.cycles.as_pointer()
                sc.cycles.bake_type = mainsc.cycles.bake_type
                sc.cycles.bl_rna = mainsc.cycles.bl_rna
                # sc.cycles.bl_rna_get_subclass() = mainsc.cycles.bl_rna_get_subclass()
                # sc.cycles.bl_rna_get_subclass_py() = mainsc.cycles.bl_rna_get_subclass_py()
                sc.cycles.blur_glossy = mainsc.cycles.blur_glossy
                sc.cycles.camera_cull_margin = mainsc.cycles.camera_cull_margin
                sc.cycles.caustics_reflective = mainsc.cycles.caustics_reflective
                sc.cycles.caustics_refractive = mainsc.cycles.caustics_refractive
                sc.cycles.debug_bvh_layout = mainsc.cycles.debug_bvh_layout
                sc.cycles.debug_bvh_time_steps = mainsc.cycles.debug_bvh_time_steps
                sc.cycles.debug_bvh_type = mainsc.cycles.debug_bvh_type
                sc.cycles.debug_cancel_timeout = mainsc.cycles.debug_cancel_timeout
                sc.cycles.debug_opencl_device_type = mainsc.cycles.debug_opencl_device_type
                sc.cycles.debug_opencl_kernel_type = mainsc.cycles.debug_opencl_kernel_type
                sc.cycles.debug_opencl_mem_limit = mainsc.cycles.debug_opencl_mem_limit
                sc.cycles.debug_optix_cuda_streams = mainsc.cycles.debug_optix_cuda_streams
                sc.cycles.debug_reset_timeout = mainsc.cycles.debug_reset_timeout
                sc.cycles.debug_text_timeout = mainsc.cycles.debug_text_timeout
                sc.cycles.debug_tile_size = mainsc.cycles.debug_tile_size
                sc.cycles.debug_use_cpu_avx = mainsc.cycles.debug_use_cpu_avx
                sc.cycles.debug_use_cpu_avx2 = mainsc.cycles.debug_use_cpu_avx2
                sc.cycles.debug_use_cpu_split_kernel = mainsc.cycles.debug_use_cpu_split_kernel
                sc.cycles.debug_use_cpu_sse2 = mainsc.cycles.debug_use_cpu_sse2
                sc.cycles.debug_use_cpu_sse3 = mainsc.cycles.debug_use_cpu_sse3
                sc.cycles.debug_use_cpu_sse41 = mainsc.cycles.debug_use_cpu_sse41
                sc.cycles.debug_use_cuda_adaptive_compile = mainsc.cycles.debug_use_cuda_adaptive_compile
                sc.cycles.debug_use_cuda_split_kernel = mainsc.cycles.debug_use_cuda_split_kernel
                sc.cycles.debug_use_hair_bvh = mainsc.cycles.debug_use_hair_bvh
                sc.cycles.debug_use_opencl_debug = mainsc.cycles.debug_use_opencl_debug
                sc.cycles.debug_use_spatial_splits = mainsc.cycles.debug_use_spatial_splits
                sc.cycles.device = mainsc.cycles.device
                sc.cycles.dicing_camera = mainsc.cycles.dicing_camera
                sc.cycles.dicing_rate = mainsc.cycles.dicing_rate
                sc.cycles.diffuse_bounces = mainsc.cycles.diffuse_bounces
                sc.cycles.diffuse_samples = mainsc.cycles.diffuse_samples
                sc.cycles.distance_cull_margin = mainsc.cycles.distance_cull_margin
                # sc.cycles.driver_add() = mainsc.cycles.driver_add()
                # sc.cycles.driver_remove() = mainsc.cycles.driver_remove()
                sc.cycles.feature_set = mainsc.cycles.feature_set
                sc.cycles.film_exposure = mainsc.cycles.film_exposure
                sc.cycles.film_transparent_glass = mainsc.cycles.film_transparent_glass
                sc.cycles.film_transparent_roughness = mainsc.cycles.film_transparent_roughness
                sc.cycles.filter_type = mainsc.cycles.filter_type
                sc.cycles.filter_width = mainsc.cycles.filter_width
                # sc.cycles.get() = mainsc.cycles.get()
                sc.cycles.glossy_bounces = mainsc.cycles.glossy_bounces
                sc.cycles.glossy_samples = mainsc.cycles.glossy_samples
                # # sc.cycles.id_data = mainsc.cycles.id_data
                # sc.cycles.is_property_hidden() = mainsc.cycles.is_property_hidden()
                # sc.cycles.is_property_overridable_library() = mainsc.cycles.is_property_overridable_library()
                # sc.cycles.is_property_readonly() = mainsc.cycles.is_property_readonly()
                # sc.cycles.is_property_set() = mainsc.cycles.is_property_set()
                # sc.cycles.items() = mainsc.cycles.items()
                # sc.cycles.keyframe_delete() = mainsc.cycles.keyframe_delete()
                # sc.cycles.keyframe_insert() = mainsc.cycles.keyframe_insert()
                # sc.cycles.keys() = mainsc.cycles.keys()
                sc.cycles.light_sampling_threshold = mainsc.cycles.light_sampling_threshold
                sc.cycles.max_bounces = mainsc.cycles.max_bounces
                sc.cycles.max_subdivisions = mainsc.cycles.max_subdivisions
                sc.cycles.mesh_light_samples = mainsc.cycles.mesh_light_samples
                sc.cycles.min_light_bounces = mainsc.cycles.min_light_bounces
                sc.cycles.min_transparent_bounces = mainsc.cycles.min_transparent_bounces
                sc.cycles.motion_blur_position = mainsc.cycles.motion_blur_position
                sc.cycles.name = mainsc.cycles.name
                sc.cycles.offscreen_dicing_scale = mainsc.cycles.offscreen_dicing_scale
                # sc.cycles.path_from_id() = mainsc.cycles.path_from_id()
                # sc.cycles.path_resolve() = mainsc.cycles.path_resolve()
                sc.cycles.pixel_filter_type = mainsc.cycles.pixel_filter_type
                # sc.cycles.pop() = mainsc.cycles.pop()
                sc.cycles.preview_aa_samples = mainsc.cycles.preview_aa_samples
                sc.cycles.preview_dicing_rate = mainsc.cycles.preview_dicing_rate
                sc.cycles.preview_pause = mainsc.cycles.preview_pause
                sc.cycles.preview_samples = mainsc.cycles.preview_samples
                sc.cycles.preview_start_resolution = mainsc.cycles.preview_start_resolution
                sc.cycles.progressive = mainsc.cycles.progressive
                # sc.cycles.property_overridable_library_set() sc.cycles.property_overridable_library_set()
                # sc.cycles.property_unset() = mainsc.cycles.property_unset()
                # sc.cycles.register() = mainsc.cycles.register()
                # # sc.cycles.rna_type = mainsc.cycles.rna_type
                sc.cycles.rolling_shutter_duration = mainsc.cycles.rolling_shutter_duration
                sc.cycles.rolling_shutter_type = mainsc.cycles.rolling_shutter_type
                sc.cycles.sample_all_lights_direct = mainsc.cycles.sample_all_lights_direct
                sc.cycles.sample_all_lights_indirect = mainsc.cycles.sample_all_lights_indirect
                sc.cycles.sample_clamp_direct = mainsc.cycles.sample_clamp_direct
                sc.cycles.sample_clamp_indirect = mainsc.cycles.sample_clamp_indirect
                sc.cycles.samples = mainsc.cycles.samples
                sc.cycles.sampling_pattern = mainsc.cycles.sampling_pattern
                sc.cycles.seed = mainsc.cycles.seed
                sc.cycles.shading_system = mainsc.cycles.shading_system
                sc.cycles.subsurface_samples = mainsc.cycles.subsurface_samples
                sc.cycles.texture_limit = mainsc.cycles.texture_limit
                sc.cycles.texture_limit_render = mainsc.cycles.texture_limit_render
                sc.cycles.tile_order = mainsc.cycles.tile_order
                sc.cycles.transmission_bounces = mainsc.cycles.transmission_bounces
                sc.cycles.transmission_samples = mainsc.cycles.transmission_samples
                sc.cycles.transparent_max_bounces = mainsc.cycles.transparent_max_bounces
                # sc.cycles.type_recast() = mainsc.cycles.type_recast()
                # sc.cycles.unregister() = mainsc.cycles.unregister()
                sc.cycles.use_animated_seed = mainsc.cycles.use_animated_seed
                sc.cycles.use_bvh_embree = mainsc.cycles.use_bvh_embree
                sc.cycles.use_camera_cull = mainsc.cycles.use_camera_cull
                sc.cycles.use_distance_cull = mainsc.cycles.use_distance_cull
                sc.cycles.use_layer_samples = mainsc.cycles.use_layer_samples
                sc.cycles.use_progressive_refine = mainsc.cycles.use_progressive_refine
                sc.cycles.use_square_samples = mainsc.cycles.use_square_samples
                # sc.cycles.values() = mainsc.cycles.values()
                sc.cycles.volume_bounces = mainsc.cycles.volume_bounces
                sc.cycles.volume_max_steps = mainsc.cycles.volume_max_steps
                sc.cycles.volume_samples = mainsc.cycles.volume_samples
                sc.cycles.volume_step_size = mainsc.cycles.volume_step_size

                sc.display_settings.display_device = mainsc.display_settings.display_device
                sc.view_settings.view_transform = mainsc.view_settings.view_transform
                sc.view_settings.look = mainsc.view_settings.look
                sc.view_settings.exposure = mainsc.view_settings.exposure
                sc.view_settings.gamma = mainsc.view_settings.gamma
                # # sc.diplay_setting.view_settings.use_curve_mapping = mainsc..view_settings.use_curve_mapping

                # # sc.sequencer_colorspace_settings = mainsc.sequencer_colorspace_settings
                print("++++ to " + sc.name + "++++")
        print("++++ finished ++++")
        print(" ")
        # Lets Blender know the operator finished successfully.
        return {'FINISHED'}


# Registration and Unregistration
def register():
    # RiggingHelper
    bpy.utils.register_class(SWIFTLY_OT_AddEmptyRigHlp)
    bpy.types.VIEW3D_MT_mesh_add.append(AddEmptyRigHlp_button)
    # GPU info
    bpy.utils.register_class(SWIFTLY_OT_GetGPUinfo)
    bpy.utils.register_class(GpuPanel)
    # Copy Scene Settings
    bpy.utils.register_class(CopySceneSettingsPanel)
    bpy.utils.register_class(SWIFTLY_OT_CopySceneSettings)


def unregister():
    # RiggingHelper
    bpy.utils.unregister_class(SWIFTLY_OT_AddEmptyRigHlp)
    bpy.types.VIEW3D_MT_mesh_add.remove(AddEmptyRigHlp_button)
    # GPU info
    bpy.utils.unregister_class(SWIFTLY_OT_GetGPUinfo)
    bpy.utils.unregister_class(GpuPanel)
    # Copy Scene Settings
    bpy.utils.unregister_class(CopySceneSettingsPanel)
    bpy.utils.unregister_class(SWIFTLY_OT_CopySceneSettings)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
