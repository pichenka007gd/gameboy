data = "\n".join(open("gameboy_opcodes.txt", "r").read().splitlines()[1:])

data = [x.splitlines() for x in [x[1:-2] for x in data.split("x")[1:]]]

items = []
for i in range(len(data)):
	for j in range(len(data[i])):
		if j > 1 and (j) % 2 == 0:
			items.append(data[i][j][0:7])
			items.append(data[i][j][8:])

		else:
			items.append(data[i][j])
items = [x for x in items if x != ""]
opcodes = []
for i in range(0, len(items), 3):
	opcodes.append(items[i:i+3])
opcodes = [[x[0], " ".join(x[1].split()), x[2]] for x in opcodes]

print("\n".join(["# "+ " # ".join(x) for x in opcodes]))

with open("opcodes_paste.py", "w") as file:
	q = 0
	for i in range(2**8):
		if i in [0xD3, 0xDB, 0xDD, 0xE3, 0xE4, 0xEB, 0xEC, 0xED, 0xF4, 0xFC, 0xFD]:
			q += 1
			continue
		opcodes[i-q][0] = opcodes[i-q][0].ljust(11)
		opcodes[i-q][1] = opcodes[i-q][1].replace("  ", " ")
		opcodes[i-q][2] = "".join(opcodes[i-q][2].split())

		file.write(f"if opcode == 0x{i:02X}: # {" | ".join([opcodes[i-q][0], opcodes[i-q][2], opcodes[i-q][1]])}\n    cycles({opcodes[i-q][1][-2:].replace(" ", "").replace("/", "")})\n")



