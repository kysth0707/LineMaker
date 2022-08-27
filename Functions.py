
MapColor = (150, 150, 150)
StartX, StartY = 50, 50
SizeX, SizeY = 70, 70

def DrawMap(pygame, screen):
	for x in range(6):
		for y in range(6):
			if (x == 5 and y == 5) or (x == 5 and y == 4) or (x == 4 and y == 5) or (x == 4 and y == 4):
				continue
			pygame.draw.rect(screen, MapColor, [StartX + x * SizeX, StartY + y * SizeY, SizeX, SizeY], 2)
	for x in range(6):
		for y in range(6):
			if (x == 0 and y == 5) or (x == 0 and y == 4) or (x == 1 and y == 5) or (x == 1 and y == 4):
				continue
			pygame.draw.rect(screen, MapColor, [StartX + x * SizeX + 70 * 7, StartY + y * SizeY, SizeX, SizeY], 2)

	pygame.draw.line(screen, MapColor, (StartX + SizeX * 5, StartY + SizeY * 4), 
									   (StartX + SizeX * 5, StartY + SizeY * 6))
	
	pygame.draw.line(screen, MapColor, (StartX + SizeX * 8, StartY + SizeY * 4), 
									   (StartX + SizeX * 8, StartY + SizeY * 6))
	
	pygame.draw.line(screen, MapColor, (StartX + SizeX * 6, StartY + SizeY * 3), 
									   (StartX + SizeX * 7, StartY + SizeY * 3))

	pygame.draw.circle(screen, (255, 0, 0), (120, 120), 70 * 0.2, 1)
	pygame.draw.circle(screen, (0, 255, 0), (120, 120), 70 * 0.4, 1)
	pygame.draw.circle(screen, (0, 0, 255), (120, 120), 70 * 0.6, 1)

	pygame.draw.circle(screen, (255, 0, 0), (890, 120), 70 * 0.2, 1)
	pygame.draw.circle(screen, (0, 255, 0), (890, 120), 70 * 0.4, 1)
	pygame.draw.circle(screen, (0, 0, 255), (890, 120), 70 * 0.6, 1)

	pygame.draw.circle(screen, (222, 135, 45), (120, 400), 70 * 0.1)
	pygame.draw.circle(screen, (222, 135, 45), (890, 400), 70 * 0.1)

def GetMapDots():
	ReturnList = []
	for x in range(7):
		for y in range(7):
			if (x == 6 and y == 6) or (x == 6 and y == 5) or (x == 5 and y == 6) or (x == 5 and y == 5):
				continue
			ReturnList.append((StartX + x * SizeX, StartY + y * SizeY))
	
	for x in range(7):
		for y in range(7):
			if (x == 1 and y == 6) or (x == 1 and y == 5) or (x == 0 and y == 6) or (x == 0 and y == 5):
				continue
			ReturnList.append((StartX + x * SizeX + 70 * 7, StartY + y * SizeY))

	ReturnList.append((StartX + 5 * SizeX, StartY + 5 * SizeY))
	ReturnList.append((StartX + 8 * SizeX, StartY + 5 * SizeY))

	return ReturnList

def DrawDots(pygame, screen, MapDots):
	for i in range(len(MapDots)):
		pygame.draw.circle(screen, (255, 0, 0), [MapDots[i][0], MapDots[i][1]], 4)

def NearestDotLoc(MousePos, MapDots):
	NearestDotPosition = None
	NearestDotDistance = 10000000000
	for i in range(len(MapDots)):
		DistanceSquare = ((MousePos[0] - MapDots[i][0]) ** 2 + (MousePos[1] - MapDots[i][1]) ** 2)
		if DistanceSquare < NearestDotDistance:
			NearestDotPosition = MapDots[i]
			NearestDotDistance = DistanceSquare

	return NearestDotPosition

def Abs(value):
	return value if value >= 0 else value * -1