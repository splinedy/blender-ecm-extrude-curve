bl_info = {
    "name": "Extrude Curve (ECM)",
    "description": "Non-destructive Curve Extrusion through Geometry Nodes modifier",
    "author": "SplineDynamics",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location" : "Properties > Modifiers > Add Modifier > Spline Dynamics Tools > Extrude Curve (ECM)",    
    "category": "Object",
}


import bpy


# ------------------------------------------------------------------------
# Operator to add the modifier
# ------------------------------------------------------------------------
class ECM_ExtrudeCurve(bpy.types.Operator):
    """Add Extrude Curve (ECM) Modifier"""
    bl_idname = "object.ecm_extrudecurve"
    bl_label = "Extrude Curve (ECM)"
    bl_description = "Create a non-destructive extrusion of curve objects using Geometry Nodes"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.object
        if obj is None or obj.type != 'CURVE':
            self.report({'ERROR'}, "Please select a curve object")
            return {'CANCELLED'}

        node_group = ecm_extrudecurve_node_group()
        mod = obj.modifiers.new(name="Extrude Curve (ECM)", type="NODES")
        mod.node_group = node_group
        return {"FINISHED"}


# ------------------------------------------------------------------------
# Geometry Nodes Group Definition
# ------------------------------------------------------------------------
def ecm_extrudecurve_node_group():
    """Return or create the ECM_ExtrudeCurve Geometry Node group"""
    if "ECM_ExtrudeCurve" in bpy.data.node_groups:
        return bpy.data.node_groups["ECM_ExtrudeCurve"]

    node_group = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "ECM_ExtrudeCurve")

    node_group.color_tag = 'NONE'
    node_group.description = ""
    node_group.default_group_node_width = 140
    node_group.is_modifier = True

    #node_group interface
    #Socket Geometry
    geometry_socket = node_group.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'

    #Socket Geometry
    geometry_socket_1 = node_group.interface.new_socket(name = "Geometry", in_out='INPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket_1.attribute_domain = 'POINT'

    #Panel Extrusion
    extrusion_panel = node_group.interface.new_panel("Extrusion")
    #Socket Height
    height_socket = node_group.interface.new_socket(name = "Height", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = extrusion_panel)
    height_socket.default_value = 1.0
    height_socket.min_value = -3.4028234663852886e+38
    height_socket.max_value = 3.4028234663852886e+38
    height_socket.subtype = 'NONE'
    height_socket.default_attribute_name = "height"
    height_socket.attribute_domain = 'POINT'
    height_socket.description = "Extrusion distance in Z"

    #Socket Segments
    segments_socket = node_group.interface.new_socket(name = "Segments", in_out='INPUT', socket_type = 'NodeSocketInt', parent = extrusion_panel)
    segments_socket.default_value = 1
    segments_socket.min_value = 1
    segments_socket.max_value = 1000
    segments_socket.subtype = 'NONE'
    segments_socket.default_attribute_name = "segments"
    segments_socket.attribute_domain = 'POINT'
    segments_socket.description = "Divisions along the extrusion"

    #Panel Caps
    caps_panel = node_group.interface.new_panel("Caps")
    #Socket Top Cap
    top_cap_socket = node_group.interface.new_socket(name = "Top Cap", in_out='INPUT', socket_type = 'NodeSocketBool', parent = caps_panel)
    top_cap_socket.default_value = True   # cambiado a True
    top_cap_socket.default_attribute_name = "top_cap"
    top_cap_socket.attribute_domain = 'POINT'
    top_cap_socket.description = "Close the top end"

    #Socket Bottom Cap
    bottom_cap_socket = node_group.interface.new_socket(name = "Bottom Cap", in_out='INPUT', socket_type = 'NodeSocketBool', parent = caps_panel)
    bottom_cap_socket.default_value = True   # cambiado a True
    bottom_cap_socket.default_attribute_name = "bottom_cap"
    bottom_cap_socket.attribute_domain = 'POINT'
    bottom_cap_socket.description = "Close the bottom end"

   #initialize node_group nodes
    #node Group Input
    group_input = node_group.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    #node Group Output
    group_output = node_group.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    #node Fill Curve
    fill_curve = node_group.nodes.new("GeometryNodeFillCurve")
    fill_curve.label = "Fill Curve - Side"
    fill_curve.name = "Fill Curve"
    fill_curve.mode = 'NGONS'
    #Group ID
    fill_curve.inputs[1].default_value = 0

    #node Extrude Mesh
    extrude_mesh = node_group.nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh.name = "Extrude Mesh"
    extrude_mesh.mode = 'FACES'
    #Selection
    extrude_mesh.inputs[1].default_value = True
    #Offset
    extrude_mesh.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Individual
    extrude_mesh.inputs[4].default_value = False

    #node Delete Geometry
    delete_geometry = node_group.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"
    delete_geometry.domain = 'FACE'
    delete_geometry.mode = 'ALL'

    #node Fill Curve.001
    fill_curve_001 = node_group.nodes.new("GeometryNodeFillCurve")
    fill_curve_001.label = "Fill Curve - Bottom"
    fill_curve_001.name = "Fill Curve.001"
    fill_curve_001.mode = 'NGONS'
    #Group ID
    fill_curve_001.inputs[1].default_value = 0

    #node Fill Curve.002
    fill_curve_002 = node_group.nodes.new("GeometryNodeFillCurve")
    fill_curve_002.label = "Fill Curve  - Top"
    fill_curve_002.name = "Fill Curve.002"
    fill_curve_002.mode = 'NGONS'
    #Group ID
    fill_curve_002.inputs[1].default_value = 0

    #node Join Geometry
    join_geometry = node_group.nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"

    #node Switch
    switch = node_group.nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.input_type = 'GEOMETRY'

    #node Switch.001
    switch_001 = node_group.nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.input_type = 'GEOMETRY'

    #node Extrude Mesh.001
    extrude_mesh_001 = node_group.nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_001.name = "Extrude Mesh.001"
    extrude_mesh_001.mode = 'FACES'
    #Selection
    extrude_mesh_001.inputs[1].default_value = True
    #Offset
    extrude_mesh_001.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Individual
    extrude_mesh_001.inputs[4].default_value = True

    #node Delete Geometry.001
    delete_geometry_001 = node_group.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_001.name = "Delete Geometry.001"
    delete_geometry_001.domain = 'FACE'
    delete_geometry_001.mode = 'ALL'

    #node Merge by Distance
    merge_by_distance = node_group.nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance.name = "Merge by Distance"
    merge_by_distance.mode = 'ALL'
    #Selection
    merge_by_distance.inputs[1].default_value = True
    #Distance
    merge_by_distance.inputs[2].default_value = 0.0010000000474974513

    #node Flip Faces
    flip_faces = node_group.nodes.new("GeometryNodeFlipFaces")
    flip_faces.name = "Flip Faces"
    #Selection
    flip_faces.inputs[1].default_value = True

    #node Math
    math = node_group.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'DIVIDE'
    math.use_clamp = False

    #node Instance on Points
    instance_on_points = node_group.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    #Pick Instance
    instance_on_points.inputs[3].default_value = False
    #Instance Index
    instance_on_points.inputs[4].default_value = 0
    #Rotation
    instance_on_points.inputs[5].default_value = (0.0, 0.0, 0.0)
    #Scale
    instance_on_points.inputs[6].default_value = (1.0, 1.0, 1.0)

    #node Geometry to Instance
    geometry_to_instance = node_group.nodes.new("GeometryNodeGeometryToInstance")
    geometry_to_instance.name = "Geometry to Instance"

    #node Mesh Line
    mesh_line = node_group.nodes.new("GeometryNodeMeshLine")
    mesh_line.name = "Mesh Line"
    mesh_line.count_mode = 'TOTAL'
    mesh_line.mode = 'END_POINTS'
    #Start Location
    mesh_line.inputs[2].default_value = (0.0, 0.0, 0.0)

    #node Combine XYZ
    combine_xyz = node_group.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.name = "Combine XYZ"
    #X
    combine_xyz.inputs[0].default_value = 0.0
    #Y
    combine_xyz.inputs[1].default_value = 0.0

    #node Math.001
    math_001 = node_group.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'ADD'
    math_001.use_clamp = False
    #Value_001
    math_001.inputs[1].default_value = 1.0

    #node Compare
    compare = node_group.nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.data_type = 'INT'
    compare.mode = 'ELEMENT'
    compare.operation = 'LESS_THAN'

    #node Index
    index = node_group.nodes.new("GeometryNodeInputIndex")
    index.name = "Index"

    #node Realize Instances
    realize_instances = node_group.nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    #Selection
    realize_instances.inputs[1].default_value = True
    #Realize All
    realize_instances.inputs[2].default_value = True
    #Depth
    realize_instances.inputs[3].default_value = 0

    #node Flip Faces.001
    flip_faces_001 = node_group.nodes.new("GeometryNodeFlipFaces")
    flip_faces_001.name = "Flip Faces.001"
    #Selection
    flip_faces_001.inputs[1].default_value = True

    #node Switch.002
    switch_002 = node_group.nodes.new("GeometryNodeSwitch")
    switch_002.name = "Switch.002"
    switch_002.input_type = 'GEOMETRY'

    #node Compare.001
    compare_001 = node_group.nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.data_type = 'FLOAT'
    compare_001.mode = 'ELEMENT'
    compare_001.operation = 'LESS_THAN'
    #B
    compare_001.inputs[1].default_value = 0.0

    
    #Set locations
    group_input.location = (-914.1019287109375, -214.44473266601562)
    group_output.location = (2496.602294921875, -107.43557739257812)
    fill_curve.location = (-410.20501708984375, 43.73919677734375)
    extrude_mesh.location = (62.53750991821289, 86.04241180419922)
    delete_geometry.location = (288.0355529785156, 96.89566040039062)
    fill_curve_001.location = (-135.30230712890625, -231.11346435546875)
    fill_curve_002.location = (-136.7638702392578, -394.2537841796875)
    join_geometry.location = (1657.5579833984375, -56.1291389465332)
    switch.location = (327.56903076171875, -109.78105926513672)
    switch_001.location = (463.58636474609375, -290.51336669921875)
    extrude_mesh_001.location = (47.495262145996094, -382.26019287109375)
    delete_geometry_001.location = (262.5473937988281, -360.5662841796875)
    merge_by_distance.location = (1887.29931640625, -72.58911895751953)
    flip_faces.location = (128.00955200195312, -227.7783203125)
    math.location = (-206.6744842529297, -40.98670959472656)
    instance_on_points.location = (1271.6912841796875, 255.62095642089844)
    geometry_to_instance.location = (551.1242065429688, 38.29910659790039)
    mesh_line.location = (765.3663940429688, 338.7535095214844)
    combine_xyz.location = (561.1982421875, 198.4735565185547)
    math_001.location = (373.308349609375, 310.4452819824219)
    compare.location = (1028.47705078125, 99.3311767578125)
    index.location = (767.3814086914062, 80.76202392578125)
    realize_instances.location = (1477.8134765625, 130.27734375)
    flip_faces_001.location = (2119.72802734375, -260.9518127441406)
    switch_002.location = (2295.09228515625, -103.82646179199219)
    compare_001.location = (1890.8580322265625, -255.4117431640625)

    #Set dimensions
    group_input.width, group_input.height = 140.0, 100.0
    group_output.width, group_output.height = 140.0, 100.0
    fill_curve.width, fill_curve.height = 140.0, 100.0
    extrude_mesh.width, extrude_mesh.height = 140.0, 100.0
    delete_geometry.width, delete_geometry.height = 140.0, 100.0
    fill_curve_001.width, fill_curve_001.height = 140.0, 100.0
    fill_curve_002.width, fill_curve_002.height = 140.0, 100.0
    join_geometry.width, join_geometry.height = 140.0, 100.0
    switch.width, switch.height = 140.0, 100.0
    switch_001.width, switch_001.height = 140.0, 100.0
    extrude_mesh_001.width, extrude_mesh_001.height = 140.0, 100.0
    delete_geometry_001.width, delete_geometry_001.height = 140.0, 100.0
    merge_by_distance.width, merge_by_distance.height = 140.0, 100.0
    flip_faces.width, flip_faces.height = 140.0, 100.0
    math.width, math.height = 140.0, 100.0
    instance_on_points.width, instance_on_points.height = 140.0, 100.0
    geometry_to_instance.width, geometry_to_instance.height = 160.0, 100.0
    mesh_line.width, mesh_line.height = 140.0, 100.0
    combine_xyz.width, combine_xyz.height = 140.0, 100.0
    math_001.width, math_001.height = 140.0, 100.0
    compare.width, compare.height = 140.0, 100.0
    index.width, index.height = 140.0, 100.0
    realize_instances.width, realize_instances.height = 140.0, 100.0
    flip_faces_001.width, flip_faces_001.height = 140.0, 100.0
    switch_002.width, switch_002.height = 140.0, 100.0
    compare_001.width, compare_001.height = 140.0, 100.0

    #initialize node_group links
    #fill_curve.Mesh -> extrude_mesh.Mesh
    node_group.links.new(fill_curve.outputs[0], extrude_mesh.inputs[0])
    #extrude_mesh.Top -> delete_geometry.Selection
    node_group.links.new(extrude_mesh.outputs[1], delete_geometry.inputs[1])
    #extrude_mesh.Mesh -> delete_geometry.Geometry
    node_group.links.new(extrude_mesh.outputs[0], delete_geometry.inputs[0])
    #extrude_mesh_001.Mesh -> delete_geometry_001.Geometry
    node_group.links.new(extrude_mesh_001.outputs[0], delete_geometry_001.inputs[0])
    #fill_curve_002.Mesh -> extrude_mesh_001.Mesh
    node_group.links.new(fill_curve_002.outputs[0], extrude_mesh_001.inputs[0])
    #extrude_mesh_001.Side -> delete_geometry_001.Selection
    node_group.links.new(extrude_mesh_001.outputs[2], delete_geometry_001.inputs[1])
    #group_input.Height -> extrude_mesh_001.Offset Scale
    node_group.links.new(group_input.outputs[1], extrude_mesh_001.inputs[3])
    #group_input.Top Cap -> switch_001.Switch
    node_group.links.new(group_input.outputs[3], switch_001.inputs[0])
    #group_input.Bottom Cap -> switch.Switch
    node_group.links.new(group_input.outputs[4], switch.inputs[0])
    #delete_geometry_001.Geometry -> switch_001.True
    node_group.links.new(delete_geometry_001.outputs[0], switch_001.inputs[2])
    #switch_001.Output -> join_geometry.Geometry
    node_group.links.new(switch_001.outputs[0], join_geometry.inputs[0])
    #join_geometry.Geometry -> merge_by_distance.Geometry
    node_group.links.new(join_geometry.outputs[0], merge_by_distance.inputs[0])
    #fill_curve_001.Mesh -> flip_faces.Mesh
    node_group.links.new(fill_curve_001.outputs[0], flip_faces.inputs[0])
    #flip_faces.Mesh -> switch.True
    node_group.links.new(flip_faces.outputs[0], switch.inputs[2])
    #group_input.Height -> math.Value
    node_group.links.new(group_input.outputs[1], math.inputs[0])
    #group_input.Segments -> math.Value
    node_group.links.new(group_input.outputs[2], math.inputs[1])
    #math.Value -> extrude_mesh.Offset Scale
    node_group.links.new(math.outputs[0], extrude_mesh.inputs[3])
    #delete_geometry.Geometry -> geometry_to_instance.Geometry
    node_group.links.new(delete_geometry.outputs[0], geometry_to_instance.inputs[0])
    #geometry_to_instance.Instances -> instance_on_points.Instance
    node_group.links.new(geometry_to_instance.outputs[0], instance_on_points.inputs[2])
    #mesh_line.Mesh -> instance_on_points.Points
    node_group.links.new(mesh_line.outputs[0], instance_on_points.inputs[0])
    #math_001.Value -> mesh_line.Count
    node_group.links.new(math_001.outputs[0], mesh_line.inputs[0])
    #combine_xyz.Vector -> mesh_line.Offset
    node_group.links.new(combine_xyz.outputs[0], mesh_line.inputs[3])
    #group_input.Height -> combine_xyz.Z
    node_group.links.new(group_input.outputs[1], combine_xyz.inputs[2])
    #group_input.Segments -> math_001.Value
    node_group.links.new(group_input.outputs[2], math_001.inputs[0])
    #index.Index -> compare.A
    node_group.links.new(index.outputs[0], compare.inputs[2])
    #compare.Result -> instance_on_points.Selection
    node_group.links.new(compare.outputs[0], instance_on_points.inputs[1])
    #group_input.Segments -> compare.B
    node_group.links.new(group_input.outputs[2], compare.inputs[3])
    #instance_on_points.Instances -> realize_instances.Geometry
    node_group.links.new(instance_on_points.outputs[0], realize_instances.inputs[0])
    #group_input.Geometry -> fill_curve.Curve
    node_group.links.new(group_input.outputs[0], fill_curve.inputs[0])
    #group_input.Geometry -> fill_curve_001.Curve
    node_group.links.new(group_input.outputs[0], fill_curve_001.inputs[0])
    #group_input.Geometry -> fill_curve_002.Curve
    node_group.links.new(group_input.outputs[0], fill_curve_002.inputs[0])
    #flip_faces_001.Mesh -> switch_002.True
    node_group.links.new(flip_faces_001.outputs[0], switch_002.inputs[2])
    #group_input.Height -> compare_001.A
    node_group.links.new(group_input.outputs[1], compare_001.inputs[0])
    #compare_001.Result -> switch_002.Switch
    node_group.links.new(compare_001.outputs[0], switch_002.inputs[0])
    #merge_by_distance.Geometry -> flip_faces_001.Mesh
    node_group.links.new(merge_by_distance.outputs[0], flip_faces_001.inputs[0])
    #switch_002.Output -> group_output.Geometry
    node_group.links.new(switch_002.outputs[0], group_output.inputs[0])
    #merge_by_distance.Geometry -> switch_002.False
    node_group.links.new(merge_by_distance.outputs[0], switch_002.inputs[1])
    #switch.Output -> join_geometry.Geometry
    node_group.links.new(switch.outputs[0], join_geometry.inputs[0])
    #realize_instances.Geometry -> join_geometry.Geometry
    node_group.links.new(realize_instances.outputs[0], join_geometry.inputs[0])
    
    return node_group


# ------------------------------------------------------------------------
#  Add Modifier Menu Registration
# ------------------------------------------------------------------------

class OBJECT_MT_splinedynamics_menu(bpy.types.Menu):
    """SplineDynamics Object Menu"""
    bl_label = "Spline Dynamics Tools"
    bl_idname = "OBJECT_MT_splinedynamics_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.ecm_extrudecurve", text="Extrude Curve (ECM)", icon="MOD_SOLIDIFY")


def menu_func(self, context):
    layout = self.layout
    layout.separator()
    layout.menu(OBJECT_MT_splinedynamics_menu.bl_idname, icon="MODIFIER")
    

# ------------------------------------------------------------------------
# Node Editor Menu Registration
# ------------------------------------------------------------------------

class NODE_OT_add_ecm_group(bpy.types.Operator):
    """Add Extrude Curve (ECM) Node Group"""
    bl_idname = "node.add_ecm_extrudecurve"
    bl_label = "Extrude Curve (ECM)"
    bl_description = "Create a non-destructive extrusion of curve objects using Geometry Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ng = ecm_extrudecurve_node_group()
        tree = context.space_data.edit_tree
        node = tree.nodes.new("GeometryNodeGroup")
        node.node_tree = ng
        node.location = context.space_data.cursor_location
        return {'FINISHED'}


class NODE_MT_ecm_nodes_menu(bpy.types.Menu):
    """Extrude Curve Node Group Menu"""
    bl_idname = "NODE_MT_ecm_nodes_menu"
    bl_label = "Spline Dynamics Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator("node.add_ecm_extrudecurve", icon="MOD_SOLIDIFY")


def add_ecm_menu(self, context):
    layout = self.layout
    layout.menu("NODE_MT_ecm_nodes_menu", icon="MODIFIER")


# ------------------------------------------------------------------------
#  Registration
# ------------------------------------------------------------------------

classes = (
    ECM_ExtrudeCurve,
    OBJECT_MT_splinedynamics_menu,
    NODE_OT_add_ecm_group,
    NODE_MT_ecm_nodes_menu,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.NODE_MT_add.append(add_ecm_menu)
    bpy.types.OBJECT_MT_modifier_add.append(menu_func)


def unregister():
    bpy.types.OBJECT_MT_modifier_add.remove(menu_func)
    bpy.types.NODE_MT_add.remove(add_ecm_menu)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()


# ------------------------------------------------------------------------
# Credits
# ------------------------------------------------------------------------
# Developed by SplineDynamics - https://SplineDynamics.com
