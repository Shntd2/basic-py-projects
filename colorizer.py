from PIL import Image
from PIL import ImageColor


class Color:
    def __init__(self, red, green, blue):
        self.red = min(max(red, 0), 255)
        self.green = min(max(green, 0), 255)
        self.blue = min(max(blue, 0), 255)

    def add_color(self, other_color):
        new_red = self.red + other_color.red
        new_green = self.green + other_color.green
        new_blue = self.blue + other_color.blue

        return Color(new_red, new_green, new_blue)

    def subtract_color(self, other_color):
        new_red = self.red - other_color.red
        new_green = self.green - other_color.green
        new_blue = self.blue - other_color.blue

        return Color(new_red, new_green, new_blue)

    def get_hex_string(self):
        hex_list = ['{:02x}'.format(x) for x in (self.red, self.green, self.blue)]
        return '#' + ''.join(hex_list)


def create_image(com_color):
	image = Image.new(mode='RGB', size=(500, 500), color=(com_color.red, com_color.green, com_color.blue))
	image.show()


blue_color = Color(*ImageColor.getrgb('blue'))
green_color = Color(*ImageColor.getrgb('green'))
red_color = Color(*ImageColor.getrgb('red'))

specific_operation = input("Press 'A' to add colors or 'S' to subtract colors: ").upper()
operations_variety = {'A': Color.add_color, 'S': Color.subtract_color}
color_combinations = {
	'red + green': (red_color, green_color),
	'red - green': (red_color, green_color),
	'green + red': (red_color, green_color),
	'green - red': (green_color, red_color),
	'red + blue': (red_color, blue_color),
	'red - blue': (red_color, blue_color),
	'blue + red': (red_color, blue_color),
	'blue - red': (blue_color, red_color),
	'green + blue': (green_color, blue_color),
	'green - blue': (green_color, blue_color),
	'blue + green': (green_color, blue_color),
	'blue - green': (blue_color, green_color)
}

if specific_operation == 'A':
	specific_colors = input("You have three colors ('red', 'green' and 'blue'), "
	                        "choose which two of them you want to add (e.g., 'red + green'): ").lower()
	if specific_colors in color_combinations:
		color1, color2 = color_combinations[specific_colors]
		combined_color = operations_variety[specific_operation](color1, color2)
	else:
		print('Invalid color combination')

elif specific_operation == 'S':
	specific_colors = input("You have three colors ('red', 'green' and 'blue'), "
	                        "choose which two of them you want to add (e.g., 'red - green'): ").lower()
	if specific_colors in color_combinations:
		color1, color2 = color_combinations[specific_colors]
		combined_color = operations_variety[specific_operation](color1, color2)
	else:
		print('Invalid color combination')
else:
	print("Invalid operation. Please enter 'A' to add colors or 'S' to subtract colors")
	exit()

print(f'Combined color: RGB ({combined_color.red}, {combined_color.green}, {combined_color.blue})'
      f'\nHexadecimal mark: {combined_color.get_hex_string()}')
create_image(combined_color)
