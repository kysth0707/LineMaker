import pygame
from Functions import DrawMap, GetMapDots, DrawDots, NearestDotLoc, Abs, SizeX, SizeY
import time
import os
import keyboard
import math
# print(keyboard._canonical_names.canonical_names)
On = True
Off = False

# print(pygame.font.get_fonts())

def ReturnPos(loc : str):
	return os.getcwd() + loc


# ===================== 여기를 변경
DebugMode = Off

EditorMode = On

with open(ReturnPos(f"\\config.txt"), "r", encoding="utf-8") as f:
	data = f.readlines()
	StartLoc = (int(data[0][:-1]), int(data[1][:-1]))
	StartAngle = int(data[2])
# ↑   0
# ←   1
# ↓   2
# →   3
# ====================== 여기를 변경


MapDots = GetMapDots()
# print(MapDots)

if EditorMode:
	if not StartLoc in MapDots:
		print("StartPos 의 값이 이상합니다! 재 확인 부탁드립니다")
		print("> StartLocCheckMode 를 활성화한 후, 스페이스 바 눌렀을 때 나온 값이 맞나요?")
		raise ""

def GetDistance(xy1, xy2):
	x1, y1 = xy1[0], xy1[1]
	x2, y2 = xy2[0], xy2[1]
	return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def DirFF():
	global LastDir
	if LastDir != "FF":
		AddData("dir(FF);")
		LastDir = "FF"
	pass

def DirBB():
	global LastDir
	if LastDir != "BB":
		AddData("dir(BB);")
		LastDir = "BB"
	pass

def GoBackward(GUIMOVE = True, AddCommand = True):
	global DebugNum, LineTracerLoc, AngleVector
	if AddCommand:
		DirBB()
		AddData(f"FFT({DebugNum});")
		DebugNum += 1
	if GUIMOVE:
		LineTracerLoc = (LineTracerLoc[0] + SizeX * -AngleVector[0], LineTracerLoc[1] + SizeY * AngleVector[1])
	pass

def GoForward(GUIMOVE = True, AddCommand = True):
	global DebugNum, LineTracerLoc, AngleVector
	if AddCommand:
		DirFF()
		AddData(f"FFT({DebugNum});")
		DebugNum += 1
	if GUIMOVE:
		LineTracerLoc = (LineTracerLoc[0] + SizeX * AngleVector[0], LineTracerLoc[1] + SizeY * -AngleVector[1])
	pass

def TurnLeft():
	global DebugNum, AngleVector
	DirFF()
	AddData(f"LLT({DebugNum});")
	DebugNum += 1
	if AngleVector == (0, 1):
		AngleVector = (-1, 0)
	elif AngleVector == (-1, 0):
		AngleVector = (0, -1)
	elif AngleVector == (0, -1):
		AngleVector = (1, 0)
	elif AngleVector == (1, 0):
		AngleVector = (0, 1)
	pass

def TurnRight():
	global DebugNum, AngleVector
	DirFF()
	AddData(f"RRT({DebugNum});")
	DebugNum += 1
	if AngleVector == (0, 1):
		AngleVector = (1, 0)
	elif AngleVector == (1, 0):
		AngleVector = (0, -1)
	elif AngleVector == (0, -1):
		AngleVector = (-1, 0)
	elif AngleVector == (-1, 0):
		AngleVector = (0, 1)
	pass

def AddData(Data):
	global ExportData
	ExportData.append(Data)
	print(Data)

pygame.init()

ScreenWidth = 1000
ScreenHeight = 600
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
pygame.display.set_caption('LineMaker v2.1')

LastAngle = StartAngle
angle = StartAngle
AngleText = ["↑", "←", "↓", "→"]
AngleTextFont = []
LineTracerLoc = StartLoc
if StartAngle == 0:
	AngleVector = (0, 1)
elif StartAngle == 1:
	AngleVector = (-1, 0)
elif StartAngle == 2:
	AngleVector = (0, -1)
elif StartAngle == 3:
	AngleVector = (1, 0)
LastDir = "FF"

MyFont = pygame.font.SysFont("malgungothic", 15)
for i in range(4):
	AngleTextFont.append(MyFont.render(AngleText[i], True, (0, 0, 0)))
TutorialText = MyFont.render("Space 바 : GET ( 한 칸 뒤에서 실행 ) / 키보드 위 숫자 1 ~ 0 : PUT1 ~ 10 ( 한 칸 뒤에서 실행 ) / i, o : OLD_PUT8, OLD_PUT9 / P : PAUSE", True, (0, 0, 0))
TutorialText2 = MyFont.render("↑↓ : 앞 뒤 이동 / ←→ : 좌우 이동 / s : 추출하기 ( 현재 시간으로 저장됨 ) / 백스페이스 : 재시작 / 클릭 : 박스 추가", True, (0, 0, 0))
TutorialText3 = MyFont.render("ctrl + 화살표 : 시작 각도 설정 / ctrl + 좌클릭 : 시작 좌표 설정 및 해당 설정 저장 ( 각도 설정 이후 필수로 사용해야 함 ) [ 설정 변경 후, 백스페이스 ]", True, (0, 0, 0))

BoxList = []
BoxHolding = False

DebugNum = 0
ExportData = []
AddData("dir(FF);")
clock = pygame.time.Clock()
Run = True
while Run:

	screen.fill((230, 230, 230))

	DrawMap(pygame, screen, MyFont)
	if DebugMode:
		DrawDots(pygame, screen, MapDots)

	NearestLoc = NearestDotLoc(pygame.mouse.get_pos(), MapDots)
	pygame.draw.circle(screen, (0, 255, 0), NearestLoc, 6)
	screen.blit(MyFont.render(str(NearestLoc), True, (0, 0, 0)), (pygame.mouse.get_pos()[0] - 20, pygame.mouse.get_pos()[1] + 20))

	for i in range(len(BoxList)):
		pygame.draw.rect(screen, (50, 50, 50), [BoxList[i][0] - 5, BoxList[i][1] - 5, 10, 10], 2)

	if EditorMode:
		pygame.draw.circle(screen, (0, 0, 0), LineTracerLoc, 6)
		AngleLoc = (LineTracerLoc[0] + AngleVector[0] * 20, LineTracerLoc[1] + -AngleVector[1] * 20)
		
		pygame.draw.circle(screen, (255, 0, 255), AngleLoc, 6)
		if BoxHolding:
			pygame.draw.rect(screen, (50, 50, 50), [AngleLoc[0] - 5, AngleLoc[1] - 5, 10, 10], 2)
			# pygame.draw.circle(screen, (255, 0, 255), AngleLoc, 6)

	screen.blit(TutorialText, (20, 500))
	screen.blit(TutorialText2, (20, 530))
	screen.blit(TutorialText3, (20, 560))
	pygame.display.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			Run = False
			pygame.quit()

		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				if keyboard.is_pressed("left control"):
					NearestLoc = NearestDotLoc(pygame.mouse.get_pos(), MapDots)
					with open(ReturnPos(f"\\config.txt"), "w", encoding="utf-8") as f:
						f.write(f"{NearestLoc[0]}\n{NearestLoc[1]}\n{StartAngle}")
				else:
					NearestLoc = NearestDotLoc(pygame.mouse.get_pos(), MapDots)
					if NearestLoc in BoxList:
						BoxList.remove(NearestLoc)
					else:
						BoxList.append(NearestLoc)
			
		elif event.type == pygame.KEYDOWN:
			# 움직임 제어
			if EditorMode:
				# if not(event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
				# 	continue

				if keyboard.is_pressed("left control"):
					if event.key == pygame.K_UP:
						StartAngle = 0
						angle = 0
						AngleVector = (0, 1)
						continue

					elif event.key == pygame.K_DOWN:
						StartAngle = 2
						angle = 2
						AngleVector = (0, -1)
						continue

					elif event.key == pygame.K_LEFT:
						StartAngle = 1
						angle = 1
						AngleVector = (-1, 0)
						continue

					elif event.key == pygame.K_RIGHT:
						StartAngle = 3
						angle = 3
						AngleVector = (1, 0)
						continue

				if event.key == pygame.K_UP:
					# angle = "↑"
					angle = 0
					ForwardLoc = (LineTracerLoc[0] + SizeX * AngleVector[0], LineTracerLoc[1] + SizeY * -AngleVector[1])
					# if not ForwardLoc in BoxList:
					GoForward()

				elif event.key == pygame.K_DOWN:
					# angle = "↓"
					angle = 2
					BackwardLoc = (LineTracerLoc[0] + SizeX * -AngleVector[0], LineTracerLoc[1] + SizeY * AngleVector[1])
					# if not BackwardLoc in BoxList:
					GoBackward()

				elif event.key == pygame.K_LEFT:
					# angle = "←"
					angle = 1
					TurnLeft()
				elif event.key == pygame.K_RIGHT:
					# angle = "→"
					angle = 3
					TurnRight()
				
				elif event.key == pygame.K_1:
					if BoxHolding:
						BoxHolding = False
						AddData("PUT1;")
						ForwardLoc = (LineTracerLoc[0] + SizeX * AngleVector[0], LineTracerLoc[1] + SizeY * -AngleVector[1])
						BoxList.append(ForwardLoc)
						GoBackward(True, False)
				elif event.key == pygame.K_2:
					if BoxHolding:
						BoxHolding = False
						AddData("PUT2;")
						ForwardLoc = (LineTracerLoc[0] + 0.92 * SizeX * AngleVector[0], LineTracerLoc[1] + 0.92 * SizeY * -AngleVector[1])
						BoxList.append(ForwardLoc)
						GoBackward(True, False)
				elif event.key == pygame.K_3:
					if BoxHolding:
						BoxHolding = False
						AddData("PUT3;")
						ForwardLoc = (LineTracerLoc[0] + 0.87 * SizeX * AngleVector[0], LineTracerLoc[1] + 0.87 * SizeY * -AngleVector[1])
						BoxList.append(ForwardLoc)
						GoBackward(True, False)
				elif event.key == pygame.K_4:
					if BoxHolding:
						BoxHolding = False
						AddData("PUT4;")
						ForwardLoc = (LineTracerLoc[0] + 0.7 * SizeX * AngleVector[0], LineTracerLoc[1] + 0.7 * SizeY * -AngleVector[1])
						BoxList.append(ForwardLoc)
						GoBackward(True, False)
				elif event.key == pygame.K_5:
					if BoxHolding:
						BoxHolding = False
						AddData("PUT5;")
						ForwardLoc = (LineTracerLoc[0] + 0.45 * SizeX * AngleVector[0], LineTracerLoc[1] + 0.45 * SizeY * -AngleVector[1])
						BoxList.append(ForwardLoc)
						GoBackward(True, False)
				elif event.key == pygame.K_6:
					if BoxHolding:
						BoxHolding = False
						AddData("PUT6;")
						if AngleVector == (0, 1):
							ForwardLoc = (LineTracerLoc[0] + -0.45 * SizeX * (AngleVector[0] + 0.5), LineTracerLoc[1] + 0.55 * SizeY * -AngleVector[1])
						elif AngleVector == (-1, 0):
							ForwardLoc = (LineTracerLoc[0] + -0.45 * SizeX * -(AngleVector[0]), LineTracerLoc[1] + 0.55 * SizeY * -(AngleVector[1] - 0.5))
						elif AngleVector == (0, -1):
							ForwardLoc = (LineTracerLoc[0] + -0.45 * SizeX * (AngleVector[0] - 0.5), LineTracerLoc[1] + 0.55 * SizeY * -AngleVector[1])
						elif AngleVector == (1, 0):
							ForwardLoc = (LineTracerLoc[0] + -0.45 * SizeX * -(AngleVector[0]), LineTracerLoc[1] + 0.55 * SizeY * -(AngleVector[1] + 0.5))
						BoxList.append(ForwardLoc)
						GoBackward(True, False)
				elif event.key == pygame.K_7:
					if BoxHolding:
						BoxHolding = False
						AddData("PUT7;")
						if AngleVector == (0, 1):
							ForwardLoc = (LineTracerLoc[0] + -0.45 * SizeX * (AngleVector[0] - 0.5), LineTracerLoc[1] + 0.55 * SizeY * -AngleVector[1])
						elif AngleVector == (-1, 0):
							ForwardLoc = (LineTracerLoc[0] + -0.45 * SizeX * -(AngleVector[0]), LineTracerLoc[1] + 0.55 * SizeY * -(AngleVector[1] + 0.5))
						elif AngleVector == (0, -1):
							ForwardLoc = (LineTracerLoc[0] + -0.45 * SizeX * (AngleVector[0] + 0.5), LineTracerLoc[1] + 0.55 * SizeY * -AngleVector[1])
						elif AngleVector == (1, 0):
							ForwardLoc = (LineTracerLoc[0] + -0.45 * SizeX * -(AngleVector[0]), LineTracerLoc[1] + 0.55 * SizeY * -(AngleVector[1] - 0.5))
						BoxList.append(ForwardLoc)
						GoBackward(True, False)
				
				elif event.key == pygame.K_8:
					BoxHolding = False
					ForwardLoc = (LineTracerLoc[0] + SizeX * AngleVector[0], LineTracerLoc[1] + SizeY * -AngleVector[1])
					i = 0
					for _ in range(len(BoxList)):
						if GetDistance(BoxList[i],ForwardLoc) <= 15:
							BoxList.remove(BoxList[i])
							i -= 1
						i += 1

					ForwardLoc = (LineTracerLoc[0] + SizeX * AngleVector[0] * 2, LineTracerLoc[1] + SizeY * -AngleVector[1] * 2)
					BoxList.append(ForwardLoc)
					
				elif event.key == pygame.K_9:
					BoxHolding = False
					ForwardLoc = (LineTracerLoc[0] + SizeX * AngleVector[0], LineTracerLoc[1] + SizeY * -AngleVector[1])
					i = 0
					for _ in range(len(BoxList)):
						if GetDistance(BoxList[i],ForwardLoc) <= 15:
							BoxList.remove(BoxList[i])
							i -= 1
						i += 1

					ForwardLoc = (LineTracerLoc[0] + SizeX * AngleVector[0] * 1.7, LineTracerLoc[1] + SizeY * -AngleVector[1] * 1.7)
					BoxList.append(ForwardLoc)

				elif event.key == pygame.K_0:
					ForwardLoc = (LineTracerLoc[0] + SizeX * AngleVector[0], LineTracerLoc[1] + SizeY * -AngleVector[1])
					i = 0
					for _ in range(len(BoxList)):
						if GetDistance(BoxList[i],ForwardLoc) <= 15:
							BoxList.remove(BoxList[i])
							i -= 1
						i += 1

					ForwardLoc = (LineTracerLoc[0] + SizeX * AngleVector[0] * 1.45, LineTracerLoc[1] + SizeY * -AngleVector[1] * 1.45)
					BoxList.append(ForwardLoc)


				elif event.key == pygame.K_i:
					if BoxHolding:
						BoxHolding = False
						AddData("OLD_PUT8;")
						ForwardLoc = (LineTracerLoc[0] + 1.35 * SizeX * AngleVector[0], LineTracerLoc[1] + 1.35 * SizeY * -AngleVector[1])
						BoxList.append(ForwardLoc)
						GoBackward(True, False)
				elif event.key == pygame.K_o:
					if BoxHolding:
						BoxHolding = False
						AddData("OLD_PUT9;")
						ForwardLoc = (LineTracerLoc[0] + 1.55 * SizeX * AngleVector[0], LineTracerLoc[1] + 1.55 * SizeY * -AngleVector[1])
						BoxList.append(ForwardLoc)
						GoBackward(True, False)

				elif event.key == pygame.K_p:
					AddData("PAUSE;")

				elif event.key == pygame.K_BACKSPACE:
					print("============= RESTART =============")
					with open(ReturnPos(f"\\config.txt"), "r", encoding="utf-8") as f:
						data = f.readlines()
						StartLoc = (int(data[0][:-1]), int(data[1][:-1]))
						StartAngle = int(data[2])
					BoxHolding = False
					LastAngle = StartAngle
					angle = StartAngle
					LineTracerLoc = StartLoc
					if StartAngle == 0:
						AngleVector = (0, 1)
					elif StartAngle == 1:
						AngleVector = (-1, 0)
					elif StartAngle == 2:
						AngleVector = (0, -1)
					elif StartAngle == 3:
						AngleVector = (1, 0)
					LastDir = "FF"

					BoxList = []
					BoxHolding = False

					DebugNum = 0
					ExportData = []
					AddData("dir(FF);")

				elif event.key == pygame.K_SPACE:
					ForwardLoc = (LineTracerLoc[0] + SizeX * AngleVector[0], LineTracerLoc[1] + SizeY * -AngleVector[1])
					# if ForwardLoc in BoxList:
					if not BoxHolding:
						BoxHolding = True
						AddData(f"GET({DebugNum});")
						DebugNum += 1
						# LineTracerLoc = (LineTracerLoc[0] + SizeX * -AngleVector[0], LineTracerLoc[1] + SizeY * AngleVector[1])
						i = 0
						for _ in range(len(BoxList)):
							if BoxList[i] == ForwardLoc:
								BoxList.remove(BoxList[i])
								i -= 1
							i += 1

				elif event.key == pygame.K_s: # 숫자 패드
					with open(ReturnPos(f"\\export\\{time.strftime('%Y-%m-%d_%H_%M_%S')}.txt"), "w", encoding="utf-8") as f:
						f.write('\n'.join(ExportData))
					print("Export")
					

				# if angle == 0 or angle == 2:
				# 	if LastAngle != angle:
				# 		print("dir(FF);" if angle == 0 else "dir(BB);")
				# 		LastAngle = angle

				# AngleVector = (AngleVector[0], -AngleVector[1])


			# if StartLocCheckMode:
			# 	if event.key == pygame.K_SPACE:
			# 		print(NearestDotLoc(pygame.mouse.get_pos(), MapDots))


	clock.tick(60)

	
