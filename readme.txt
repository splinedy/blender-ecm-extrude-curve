Extrude Curve (ECM) — Non-destructive curve extrusion (Geometry Nodes)

Description:
ECM extrudes any curve into a 3D mesh in a fully non-destructive way, powered by Geometry Nodes.
Keep curves editable, generate clean extrusions in real time, and avoid mesh conversion until final output.

Requirements:
- Blender 4.2.0 or newer.

Installation:
1. Edit → Preferences → Add-ons → Install... → select the addon .zip
2. Enable "Extrude Curve (ECM)" and Save Preferences.

Usage:
1. Select a Curve object.
2. Properties → Modifiers → Add Modifier → SplineDynamics Tools → Extrude Curve (ECM).
3. Adjust parameters:
   - Height = extrusion distance
   - Segments = divisions
   - Caps = toggle top/bottom faces

Node Group:
The node group "ECM_ExtrudeCurve" is included.
It can also be added in the Geometry Nodes Editor:
Add → SplineDynamics Tools → Extrude Curve (ECM).

Note about "Unassigned":
When first used, Blender may place "ECM_ExtrudeCurve" under the "Unassigned" category.
To move it:
1. Outliner → Blender File → Node Groups.
2. Right-click ECM_ExtrudeCurve → Mark as Asset.
3. In the Asset Browser, drag it from Unassigned into a catalog (e.g. SplineDynamics Tools).
This removes it from Unassigned.

Troubleshooting:
- Extrusion sideways: Ensure the curve lies flat on its local XY plane. Rotate in Edit Mode if necessary.

Support & donations:
- Docs: https://www.splinedynamics.com/blender/extrude-curve-modifier-ecm
- Gumroad (support): <GUMROAD_LINK>
- PayPal (direct): <PAYPAL_LINK>

Author: Hernán Alexis Rodenstein — Spline Dynamics
License: See LICENSE file included.
