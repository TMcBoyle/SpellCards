import drawsvg as draw
import textwrap
import text_justify
from PIL import Image, ImageDraw, ImageFont
from dataclasses import dataclass

style_box = {
    "fill": "#fafafa",
    "stroke": "#000000",
    "stroke_width": "1.88976",
    "stroke_linejoin": "bevel"
}
style_line = {
    "fill": "none",
    "stroke": "#000000",
    "stroke_width": "1.88976",
    "stroke_linejoin": "bevel"
}
style_header = {
    "font_size": "14pt",
    "font_family": "Cambria",
    "text_align": "justify",
    "text_anchor": "middle",
    "fill": "#000000"
}
style_body = {
    "font_size": "8pt",
    "font_family": "Cambria",
    "text_align": "justify",
    "text_anchor": "middle",
    "fill": "#000000"
}
style_body_faint = {
    **style_body,
    "fill_opacity": "0.1"
}
style_body_big = {
    "font_size": "12pt",
    "font_family": "Cambria",
    "text_align": "center",
    "text_anchor": "middle",
    "fill": "#000000"
}
style_body_big_faint = {
    **style_body_big,
    "fill_opacity": "0.1"
}
style_rules = {
    "font_size": "8pt",
    "font_family": "Cambria",
    "text_align": "justify",
    "text_anchor": "start",
    "xml:space": "preserve",
    "fill": "#000000"
}
style_footer = {
    "font_size": "8pt",
    "font_family": "Cambria",
    "text_align": "justify",
    "text_anchor": "end",
    "fill": "#000000"
}

def build_paragraph(text: str, text_width, parent_args, style, margin=4):
    text_x = parent_args['x'] + margin
    text_y = parent_args['y'] + float(style['font_size'][:-2]) + margin
    wrapped_text = text_justify.wrap(text, style["font_family"], float(style["font_size"][:-2]) / 0.75, text_width - margin * 2)
    return draw.Text(wrapped_text, x=text_x, y=text_y, **style)

def build_centered_text(text: str, parent_args, style):
    text_x = parent_args['x'] + parent_args['width'] / 2
    text_y = parent_args['y'] + (float(style['font_size'][:-2]) + parent_args['height']) / 2
    return draw.Text(text, x=text_x, y=text_y, **style)

def build_label_text(text: str, parent_args, style):
    text_x = parent_args['x'] + parent_args['width'] / 2
    text_y = parent_args['y'] - float(style['font_size'][:-2]) / 2
    return draw.Text(text, x=text_x, y=text_y, **style)

@dataclass
class Spell:
    name: str = ""
    level: int = 0
    school: str = ""
    casting_time: str = ""
    range: str = ""
    verbal: bool = False
    somatic: bool = False
    material: bool = False
    reaction: str = ""
    materials: str = ""
    duration: str = ""
    ritual: bool = False
    concentration: bool = False
    rules: str = ""

class Card:
    origin_xy = (0, 0)
    width    = 241.88977
    height   = 336.37796
    footer_x = 203.00000 +32.0
    footer_y = 285.35736 +44.5

    base_cols = [-24.440945 +32.0, -16.881889 +32.0, 54.929138 +32.0, 134.29922 +32.0, 158.86617 +32.0, 183.43311 +32.0]
    base_rows = [-36.940945 +44.5,  8.4133873 +44.5, 31.090555 +44.5, 49.988194 +44.5, 80.224411 +44.5, 106.68111 +44.5]

    def __init__(self, spell: Spell=Spell()):
        self.spell = spell
        self.svg = draw.Drawing(Card.width, Card.height, Card.origin_xy)
        self.components = {}

        self.boxes = {
            "title":    { "width": 226.77167, "height": 30.236221 },
            "wide":     { "width": 211.65355, "height": 15.118111 },
            "large":    { "width": 226.77167, "height": 166.29924 },
            "standard": { "width": 68.031502, "height": 18.897638 },
            "small":    { "width": 18.897638, "height": 18.897638 },
            "tiny":     { "width": 14.000000, "height": 14.000000 },
        }
        self.wrap_width = self.boxes["large"]["width"]
        self.cols = Card.base_cols.copy()
        self.rows = Card.base_rows.copy()

        row_count = len(Card.base_rows)
        offset = Card.base_rows[3] - Card.base_rows[2]
        reaction_connector_v = 11.338583
        material_connector_v = 30.236221
        if self.spell.reaction == "":
            row_count -= 1
            material_connector_v -= offset
            self.rows[3] -= offset
            self.rows[4] -= offset
            self.rows[5] -= offset
            self.boxes["large"]["height"] += offset
        if self.spell.materials == "":
            row_count -= 1
            self.rows[4] -= offset
            self.rows[5] -= offset
            self.boxes["large"]["height"] += offset

        self.reaction_path = f"m {-20.661417 +32.0},{27.311026 +44.5} v {reaction_connector_v} h 3.779528"
        self.material_path = f"m {198.55119 +32.0},{27.311026 +44.5} v {material_connector_v} h -3.77953"
    
    def __build_svg_template(self, background):
        # Background
        self.components['background'] = draw.Rectangle(
            Card.origin_xy[0], Card.origin_xy[1], 
            Card.width, Card.height,
            fill=background
        )
        # Spell Name
        self.components['spell_name_container'] = draw.Rectangle(
            self.cols[0], self.rows[0], **self.boxes["title"], **style_box
        )
        # Level
        self.components['level_container'] = draw.Rectangle(
            self.cols[0], self.rows[0], **self.boxes["tiny"], **style_box
        )
        # Casting Time
        self.components['casting_time_container'] = draw.Rectangle(
            self.cols[0], self.rows[1], **self.boxes["standard"], **style_box
        )
        self.components['casting_time_label'] = build_label_text(
            "Casting Time", self.components['casting_time_container'].args, style_body
        )
        # Range
        self.components['range_container'] = draw.Rectangle(
            self.cols[2], self.rows[1], **self.boxes["standard"], **style_box
        )
        self.components['range_label'] = build_label_text(
            "Range", self.components['range_container'].args, style_body
        )
        # Components
        self.components['verbal_container'] = draw.Rectangle(
            self.cols[3], self.rows[1], **self.boxes["small"], **style_box
        )
        self.components['somatic_container'] = draw.Rectangle(
            self.cols[4], self.rows[1], **self.boxes["small"], **style_box
        )
        self.components['material_container'] = draw.Rectangle(
            self.cols[5], self.rows[1], **self.boxes["small"], **style_box
        )
        self.components['components_label'] = build_label_text(
            "Components", self.components['somatic_container'].args, style_body
        )
        # Reaction details
        if self.spell.reaction != "":
            self.components['reaction_container'] = draw.Rectangle(
                self.cols[1], self.rows[2], **self.boxes["wide"], **style_box
            )
            self.components['reaction_connector'] = draw.Path(
                self.reaction_path, **style_line
            )
        # Material details
        if self.spell.materials != "":
            self.components['material_detail_container'] = draw.Rectangle(
                self.cols[1], self.rows[3], **self.boxes["wide"], **style_box
            )
            self.components['material_detail_connector'] = draw.Path(
                self.material_path, **style_line
            )
        # Duration
        self.components['duration_container'] = draw.Rectangle(
            self.cols[0], self.rows[4], **self.boxes["standard"], **style_box
        )
        self.components['duration_label'] = build_label_text(
            "Duration", self.components['duration_container'].args, style_body
        )
        # Attributes
        self.components['ritual_container'] = draw.Rectangle(
            self.cols[2], self.rows[4], **self.boxes["standard"], **style_box
        )
        self.components['concentration_container'] = draw.Rectangle(
            self.cols[3], self.rows[4], **self.boxes["standard"], **style_box
        )
        self.components['attributes_label'] = build_label_text(
            "Attributes", 
            {
                'x': (self.cols[2] + self.cols[3] + self.boxes["standard"]["width"]) / 2,
                'y': self.rows[4],
                'width': 0,
                'height': 0
            },
            style_body
        )
        # Rules
        self.components['rules_container'] = draw.Rectangle(
            self.cols[0], self.rows[5], **self.boxes["large"], **style_box
        )

    def __populate_values(self):
        # Spell Name
        self.components['spell_name'] = build_centered_text(
            self.spell.name,
            self.components['spell_name_container'].args,
            style_header
        )
        # Level
        self.components['level'] = build_centered_text(
            "C" if self.spell.level == 0 else str(self.spell.level),
            self.components['level_container'].args,
            style_body
        )
        # Casting Time
        self.components['casting_time'] = build_centered_text(
            self.spell.casting_time,
            self.components['casting_time_container'].args,
            style_body
        )
        # Range
        self.components['range'] = build_centered_text(
            self.spell.range,
            self.components['range_container'].args,
            style_body
        )
        # Components
        self.components['verbal'] = build_centered_text(
            "V",
            self.components['verbal_container'].args,
            style_body if self.spell.verbal else style_body_big_faint
        )
        self.components['somatic'] = build_centered_text(
            "S",
            self.components['somatic_container'].args,
            style_body if self.spell.somatic else style_body_big_faint
        )
        self.components['material'] = build_centered_text(
            "M",
            self.components['material_container'].args,
            style_body if self.spell.material else style_body_big_faint
        )
        # Reaction Detail
        if self.spell.reaction != "":
            self.components['reaction'] = build_centered_text(
                self.spell.reaction,
                self.components['reaction_container'].args,
                style_body
            )
        # Material Detail
        if self.spell.materials != "":
            self.components['material_detail'] = build_centered_text(
                self.spell.materials,
                self.components['material_detail_container'].args,
                style_body
            )
        # Duration
        self.components['duration'] = build_centered_text(
            self.spell.duration,
            self.components['duration_container'].args,
            style_body
        )
        # Attributes
        self.components['ritual'] = build_centered_text(
            "Ritual",
            self.components['ritual_container'].args,
            style_body if self.spell.ritual else style_body_faint
        )
        self.components['concentration'] = build_centered_text(
            "Concentration",
            self.components['concentration_container'].args,
            style_body if self.spell.concentration else style_body_faint
        )
        # Rules
        self.components['rules'] = build_paragraph(
            self.spell.rules,
            self.wrap_width,
            self.components['rules_container'].args,
            style_rules
        )
        # Footer
        self.components['footer'] = draw.Text(
            self.spell.school, x=Card.footer_x, y=Card.footer_y, **style_footer
        )

    def to_svg(self, background="#ffffff"):
        self.__build_svg_template(background)
        self.__populate_values()

        svg = draw.Drawing(Card.width, Card.height, Card.origin_xy)
        for key, value in self.components.items():
            svg.append(value)
        return svg
    
    def __str__(self):
        return str(self.to_svg())
