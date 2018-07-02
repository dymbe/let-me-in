from wifi import Cell, Scheme

all_cells = Cell.all('wlan0')

all_cells_list = list(all_cells)

for cell in all_cells_list:
	print(cell)
