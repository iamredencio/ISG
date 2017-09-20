## Adopted from http://variable-scope.com/posts/hexagon-tilings-with-python

import math
from PIL import Image, ImageDraw


class HexagonGenerator(object):
  """Returns a hexagon generator for hexagons of the specified size."""
  def __init__(self, edge_length):
    self.edge_length = edge_length

  @property
  def col_width(self):
    return self.edge_length * 3

  @property
  def row_height(self):
    return math.sin(math.pi / 3) * self.edge_length

  def __call__(self, row, col):
    x = (col + 0.5 * (row % 2)) * self.col_width
    y = row * self.row_height
    for angle in range(0, 360, 60):
      x += math.cos(math.radians(angle)) * self.edge_length
      y += math.sin(math.radians(angle)) * self.edge_length
      yield x
      yield y

def main():
  image = Image.new('RGB', (375, 380), 'white')
  draw = ImageDraw.Draw(image)
  hexagon_generator = HexagonGenerator(20)
  r = 10
  x = 20
  y = 20
  
  for row in range(22):
	for col in range(11):
		if not ( (row % 2 == 0 and col == 0) | (row < 3 and col == 1) | \
			((row < 4 or row == 17) and col == 0) |\
			((row == 0 or row > 19) and col == 2) |\
			(row > 17 and row < 22 and col < 2) |\
			((row == 0 or row == 1) and col > 3) |\
			((row == 2 or row == 3) and col == 5) |\
			(col > 5) |\
			(row >= 17 and col > 4) | (row > 18 and col > 3) | (row > 20 and col > 1) ):
      			hexagon = hexagon_generator(row, col)
      			draw.polygon(list(hexagon), outline='red', fill='white')
  movePiece(draw, 0, 5)
  image.show()

def movePiece(canvas, row, col):
	r = 10
	if col % 2 == 0:
		x = 20 + row * 40
	else:
		x = 20 + row * 33
	y = 40 + col * 30
	canvas.ellipse((y-r, x-r, y+r, x+r), fill=(0,0,0,255))

main()


  # Rest of class as previously defined
 # def rows(self, canvas_height):
 #   """Returns the number of rows required to fill the canvas height."""
   # return int(math.ceil(canvas_height / self.row_height))
