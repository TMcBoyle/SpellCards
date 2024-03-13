import textwrap
import random
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont

def justify(string, width):
    wrapped = textwrap.wrap(string, width=width)
    diffs = [width - len(s) for s in wrapped]
    
    result = []
    for i in range(len(wrapped)):
        tokens = wrapped[i].split(" ")
        if len(wrapped[i]) < width * 0.6 or len(tokens) == 1:
            result.append(wrapped[i])
            continue
        new_spaces = [diffs[i] // (len(tokens) - 1)] * (len(tokens) - 1)
        remainder = width - (len(wrapped[i]) + sum(new_spaces))
        while remainder > 0:
            new_spaces[random.randint(0, len(new_spaces) - 1)] += 1
            remainder -= 1

        justified = ""
        for i in range(len(tokens) - 1):
            justified += tokens[i] + " " * (1 + new_spaces[i])
        justified += tokens[-1]
        result.append(justified)

    return result

def wrap(text: str, font_family: str, font_size: float, width: int):
    image = Image.new("RGBA", (0, 0))
    font_file = font_manager.findfont(font_manager.FontProperties(family=font_family))
    font = ImageFont.truetype(font_file, font_size)
    draw = ImageDraw.Draw(image)

    result_lines = []
    for line in text.splitlines():
        if line in ("\n", "\r\n"):
            result_lines.extend(line)
            return
        
        words = line.split(" ")
        current = [""]
        for word in words:
            if draw.textlength(current[-1] + word, font=font) <= width:
                current[-1] += f" {word}"
                continue
            current[-1] = current[-1].lstrip()
            current.append(word)

        result_lines.extend(current)
    return result_lines
