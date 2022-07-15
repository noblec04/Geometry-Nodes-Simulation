# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# This addon was created with the Serpens - Visual Scripting Addon.
# This code is generated from nodes and is not intended for manual editing.
# You can find out more about Serpens at <https://blendermarket.com/products/serpens>.


bl_info = {
    "name": "GN Simulation add-on",
    "description": "Use GeoNodes to perform simulations by passing data between frames",
    "author": "Zeus",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"
}


###############   IMPORTS
import bpy
from bpy.utils import previews
import os
import math  
from bpy.app.handlers import frame_change_post

###############   IMPERATIVE CODE
###############   EVALUATED CODE
#######   Easy Fog add-on

class runSim(bpy.types.Operator):
    bl_idname = "object.runsim"
    bl_label = "GNSim"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
  
        frame_change_post.append(self.simulation)
        bpy.ops.screen.animation_play()

        return {"FINISHED"}

    def step(self,context, ob):
        depsgraph = context.evaluated_depsgraph_get()
        old_mesh = ob.data
        ob.data = bpy.data.meshes.new_from_object(ob.evaluated_get(depsgraph))
        bpy.data.meshes.remove(old_mesh)

    def simulation(self,scene,ob):    
        context = bpy.context
        ob_sim = bpy.data.objects.get("Sim")
        self.step(context, ob_sim)

class resetSim(bpy.types.Operator):
    bl_idname = "object.resetsim"
    bl_label = "GNSim_reset"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        frame_change_post.clear()
        depsgraph = context.evaluated_depsgraph_get()  
        ob_base = bpy.data.objects.get("Base")
        ob_sim = bpy.data.objects.get("Sim")
        ob_sim.data = bpy.data.meshes.new_from_object(ob_base.evaluated_get(depsgraph))

        return {"FINISHED"}


class Sim_PT_Panel(bpy.types.Panel):
    bl_label = "Geometry Nodes Simulation"
    bl_idname = "GNSim_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'GN simulation'
    bl_order = 0
    bl_info = ""

    def draw(self, context):
        layout = self.layout
        layout.operator(operator=runSim.bl_idname, text="Run Simulation")
        layout.operator(operator=resetSim.bl_idname, text="Reset Simulation")


###############   REGISTER ADDON
def register():
    bpy.utils.register_class(Sim_PT_Panel)
    bpy.utils.register_class(runSim)
    bpy.utils.register_class(resetSim)

###############   UNREGISTER ADDON
def unregister():
    bpy.utils.unregister_class(Sim_PT_Panel)
    bpy.utils.unregister_class(runSim)
    bpy.utils.unregister_class(resetSim)
