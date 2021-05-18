# creates fitzgap data Report
import sys, os
from datetime import datetime

sys.path.append("/opt/homebrew/lib/python3.9/site-packages")

from fpdf import FPDF

WIDTH = 210
HEIGHT = 297
SIZE = 100

my_path = "/Users/david/Dropbox/Computing/Linux/Python/fitzgap_data/website/"
my_image1 = "fgap_website_text_history.png"
my_image2 = "fgap_website_text_hope.png"
my_image3 = "fgap_website_text_gid.png"
my_image4 = "fgap_website_stats.png"


day = datetime.today().strftime("%d/%m/%y")

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.set_text_color(68, 118, 171)
pdf.set_draw_color(68, 118, 171)

pdf.image(my_path + "Warren St Logo_Final.jpg", 10, 5, 12.5, 25)

pdf.cell(
    0,
    15,
    "FitzGAP Website Data Report:   " + day,
    border=0,
    ln=1,
    align="C",
    fill=False,
)
pdf.set_font("Arial", "", 12)
pdf.set_text_color(68, 118, 171)

pdf.cell(
    20,
    25,
    "Outline of history; most common words   ",
    border=0,
    ln=1,
    align="L",
    fill=False,
)

pdf.image(my_path + my_image1, x=30, y=50, w=SIZE, h=SIZE)  # 20  # 30

pdf.cell(
    20,
    220,
    "Outline of hope; most common words   ",
    border=0,
    ln=1,
    align="L",
    fill=False,
)

pdf.image(my_path + my_image2, x=30, y=170, w=SIZE, h=SIZE)
pdf.add_page()

pdf.cell(
    0,
    25,
    "Gender identity; most common words   ",
    border=0,
    ln=1,
    align="L",
    fill=False,
)

pdf.image(my_path + my_image3, x=30, y=30, w=SIZE, h=SIZE)

pdf.cell(
    0,
    210,
    "Word frequency   ",
    border=0,
    ln=1,
    align="L",
    fill=False,
)

pdf.image(my_path + my_image4, x=30, y=160, w=150, h=SIZE)

pdf.output(my_path + "fgap_website_data_report.pdf", "F")