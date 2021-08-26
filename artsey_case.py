from math import *
from openpyscad import *

PRINT_MARGIN = 0.4

# all sizes in mm
plate_width = 102.1
plate_height = 39.55
plate_depth = 1.65
plate_border_thickness = 1.5

plate_component_depth = 6.65 - plate_depth

case_thickness = 3
wall_size = 2
side_panel_spacing = wall_size
keyboard_spacing = 2

# 0.05 extra margin
case_inside_width = plate_width + 0.05 + side_panel_spacing * 2
case_inside_height = plate_height + 0.05
case_inside_depth = plate_component_depth + 0.05 + case_thickness + wall_size + plate_depth


case_outside_width = case_inside_width + case_thickness
case_outside_height = case_inside_height + case_thickness
# 0.05 extra margin
case_outside_depth = (
    plate_component_depth + 0.05 + case_thickness + plate_depth + wall_size
)

usb_port_pokes_out = 3
usb_port_distance_left = 33
usb_port_width = 7.5  + 2.5
usb_port_height = 9
# 0.05 extra margin
usb_port_depth = 3.8 + 0.05

reset_button_hole_radius = 4 / 2
reset_button_distance_right = 14 + reset_button_hole_radius
reset_button_distance_bottom = 3.6
reset_button_depth = plate_component_depth

keyboard_space_width = 73.2 + PRINT_MARGIN * 2
keyboard_space_height = case_inside_height - case_thickness - keyboard_spacing + PRINT_MARGIN * 2

case_top_width = case_outside_width
case_top_height = case_outside_height
case_top_depth = plate_depth

side_panel_height = case_top_height - case_thickness - wall_size * 2 - PRINT_MARGIN * 2
side_panel_width = wall_size - PRINT_MARGIN
side_panel_depth = case_inside_depth - plate_depth -PRINT_MARGIN



def plate(remove_wall=False, reset_cut=False, usb_cut=False):
    total = Union()
    if usb_cut:
        usb = (
            Cube(
                [usb_port_width, 10, usb_port_depth + plate_depth + wall_size]
            )
            .translate(
                [
                    usb_port_distance_left + case_thickness / 2,
                    plate_height - (usb_port_height - usb_port_pokes_out),
                    0 - usb_port_depth,
                ]
            )
            .color("blue")
        )
    else:
        usb = (
            Cube(
                [usb_port_width, 10, usb_port_depth]
            )
            .translate(
                [
                    usb_port_distance_left + wall_size,
                    plate_height - (usb_port_height - usb_port_pokes_out),
                    -usb_port_depth,
                ]
            )
            .color("blue")
        )

    reset_button = Cylinder(
        h=reset_button_depth + (5 if reset_cut else 0), r=reset_button_hole_radius
    ).translate(
        [
            plate_width - reset_button_distance_right + case_thickness / 2 + wall_size,
            reset_button_distance_bottom + case_thickness / 2,
            -reset_button_depth - (plate_depth + 5 if reset_cut else 0),
        ]
    )
    total.append(usb)
    total.append(reset_button)
    total.append(Cube([plate_width, plate_height, plate_depth + (wall_size if remove_wall else 0)]).color("green"))
    return total


def case_bottom():
    bottom_case = Difference()
    outside = Cube([case_outside_width, case_outside_height + 2, case_outside_depth])
    inside = Cube(
        [case_inside_width, case_inside_height - wall_size * 2, case_inside_depth]
    ).translate(
        [case_thickness / 2, case_thickness / 2 + wall_size, case_thickness / 2]
    )
    bottom_case.append(outside)
    bottom_case.append(inside)

    bottom_case.append(
        plate(remove_wall=True, reset_cut=True, usb_cut=True).translate(
            [
                case_thickness / 2 + side_panel_spacing,
                case_thickness / 2,
                case_thickness / 2 + plate_component_depth + plate_depth,
            ]
        )
    )

    return bottom_case


def side_panel():
    sidepanel = Union()
    sidepanel.append(Cube([side_panel_width, side_panel_height, side_panel_depth]))
    return sidepanel


def case_top():
    top_case = Difference()

    top_case.append(Cube([case_top_width, case_top_height + 2, case_top_depth]))
    top_case.append(Cube([keyboard_space_width, keyboard_space_height, case_top_depth + 3]).translate(
        [wall_size + side_panel_spacing + keyboard_spacing, wall_size + keyboard_spacing - PRINT_MARGIN, 0]
    ))

    top_case_complete = Union()

    panel_left = side_panel().translate(
        [case_thickness / 2 + PRINT_MARGIN / 2, case_thickness / 2 + wall_size + PRINT_MARGIN, -side_panel_depth]
    )
    panel_right = side_panel().translate(
        [case_outside_width - wall_size - case_thickness / 2 - PRINT_MARGIN / 2, case_thickness / 2 + wall_size + PRINT_MARGIN, -side_panel_depth]
    )
    top_case_complete.append(top_case)
    top_case_complete.append(panel_left)
    top_case_complete.append(panel_right)

    # Top USB piece
    #top_case_complete.append(Cube([usb_port_width, case_thickness, plate_depth]).translate(
    #        [
    #            usb_port_distance_left + case_thickness * 2,
    #            case_outside_height - case_thickness,
    #            -case_top_depth,
    #        ]
    #    ))

    # bottom mounted row
    top_case_complete.append(Cube([plate_width, wall_size, plate_depth]).translate(
        [wall_size + case_thickness / 2, case_thickness / 2 + PRINT_MARGIN, -plate_depth]
    ))
    # bottom mounted row
    top_case_complete.append(Cube([plate_width, wall_size, plate_depth]).translate(
        [wall_size + case_thickness / 2, plate_height - wall_size + case_thickness / 2 - PRINT_MARGIN, -plate_depth]
    ))
    return top_case_complete


def place_holes(case, case_top):
    case_diff = Difference()
    case_top_diff = Difference()

    plug1 = Cube(
        [3, 3, wall_size + case_thickness / 2]
    )
    plug2 = Cube(
        [3, 3, wall_size + case_thickness / 2]
    )

    case_diff.append(case)
    case_top_diff.append(case_top)

    case_diff.append(plug1.rotate([0, 90, 0]).translate(
        [0, case_outside_height / 2, case_outside_depth -2]
    ))
    case_diff.append(plug2.rotate([0, 90, 0]).translate(
        [case_outside_width - wall_size - case_thickness / 2, case_outside_height / 2, case_outside_depth -2]
    ))

    case_top_diff.append(plug1.rotate([0, 90, 0]).translate(
        [0, case_outside_height / 2, case_outside_depth -2]
    ))
    case_top_diff.append(plug2.rotate([0, 90, 0]).translate(
        [case_outside_width - wall_size - case_thickness / 2, case_outside_height / 2, case_outside_depth -2]
    ))

    return case_diff, case_top_diff, plug1, plug2


def translate_for_print(top, plug1, plug2, move_away=False):
    scale = 0.96
    if move_away:
        plug1 = plug1.translate([20, case_outside_height + 20, 0]).scale([scale, scale, scale])
        plug2 = plug2.translate([20 + 10, case_outside_height + 20, 0]).scale([scale, scale, scale])
        top = top.rotate([180, 0, 0]).translate([0, case_outside_height * 2 + 5, case_outside_depth + case_top_depth])
    else:
        plug1 = plug1.translate([0, 0, 0]).scale([scale, scale, scale])
        plug2 = plug2.translate([10, 0, 0]).scale([scale, scale, scale])
        top = top.rotate([180, 0, 0]).translate([0, case_outside_height, case_outside_depth + case_top_depth])
    return top, plug1, plug2


if __name__ == "__main__":
    case_top = case_top().translate(
        [0, 0, case_outside_depth]
    )

    items = Union()
    items.append(case_bottom())

    plate = plate().translate(
        [
            case_thickness / 2 + side_panel_spacing,
            case_thickness / 2,
            case_thickness / 2 + plate_component_depth + plate_depth,
        ]
    )
    #items.append(plate.translate([0,0,10]))

    #items, case_top, plug1, plug2 = place_holes(items, case_top)

    case_top, plug1, plug2 = translate_for_print(case_top, Cube(), Cube(), move_away=False)

    #(items + case_top.translate([0,0,10]) + plug1 + plug2).write("case.scad")
    #(items + case_top.translate([0,0,30])).write("case.scad")

    def seperate():
        items.write("bottom_case.scad")
        #(plug1 + plug2).write("plug.scad")
        (case_top).write("top_case.scad")
    seperate()
