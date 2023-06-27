# game setup
import os

#Game parameters
MAP_WIDTH=2240
MAP_HEIGHT=2464

WIDTH    = 1440	
HEIGHT   = 880
FPS      = 32
TILESIZE = 32
LANGUAGE = "en"
DIFFICULTY=0

#Font and Colours
font_name = os.path.dirname(__file__)+'/'+'../graphics/font/joystix.ttf'
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
BACKGROUND_COLOUR, TEXT_COLOUR=(180,180,196), (54, 54, 59)

#UI settings
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
HEALTH_COLOR = 'red'
ABILITY_COLOR = (176,224,230)
BOX_COLOR = (82, 82, 82)

UI_FONT = os.path.dirname(__file__)+'/'+'../graphics/font/joystix.ttf'
UI_FONT_SIZE = 18
UI_BG_COLOR = (164,164,164)
UI_BORDER_COLOR = '#111111'

#sound
AUDIO_PATH=os.path.dirname(__file__)+'/../audio/'
GRAPHICS_PATH=os.path.dirname(__file__)+'/../graphics/'
#Fog
NIGHT_COLOR = (5, 5, 5)
LIGHT_RADIUS = (1500, 1500)
LIGHT_MASK = os.path.dirname(__file__)+'/'+'../graphics/particles/light.png'

#Gun Data
gun_data = {
	'Pistol': {'cooldown': 300, 'damage':20,'graphic':'../graphics/guns/pistol.png'},
	'Revolver': {'cooldown': 700, 'damage': 60,'graphic':'../graphics/guns/revolver.png'},
	'Shotgun': {'cooldown': 900, 'damage': 50, 'graphic':'../graphics/guns/shotgun.png'},
	'Machine Gun':{'cooldown': 50, 'damage': 10, 'graphic':'../graphics/guns/machine_gun.png'}}

gun1_data = {
	'Pistol': {'cooldown': 500, 'damage':20,'graphic':'../graphics/guns1/pistol.png'},
	'Revolver': {'cooldown': 1000, 'damage': 50,'graphic':'../graphics/guns1/revolver.png'},
	'Shotgun': {'cooldown': 1200, 'damage': 40, 'graphic':'../graphics/guns1/shotgun.png'},
	'Machine Gun':{'cooldown': 50, 'damage': 8, 'graphic':'../graphics/guns1/machine_gun.png'}}


level_data={
	1:{'robot_count': 11, 'npc_count':4, 'map':'map2_boundaries.csv', 'robot_spawns':'map2_robot_spawns_1.csv','npc_spawns':'map2_npc_spawns_1.csv',"computer_dialogue":"clue 1. There was a lecturer that was working late last night. His office is on the third floor."},
	2:{'robot_count': 2, 'npc_count':4, 'map':'map2_boundaries.csv', 'robot_spawns':'map2_robot_spawns_2.csv','npc_spawns':'map2_npc_spawns_2.csv',"computer_dialogue":"clue 1. There was a lecturer that was working late last night. His office is on the third floor."},
	3:{'robot_count': 2, 'npc_count':4, 'map':'map2_boundaries.csv', 'robot_spawns':'map2_robot_spawns_3.csv','npc_spawns':'map2_npc_spawns_3.csv',"computer_dialogue":"clue 1. There was a lecturer that was working late last night. His office is on the third floor."}
}

#Robot Data
robot_data = {
	1: {'health': 40,'damage':20,'attack_sound':os.path.dirname(__file__)+'/'+'../audio/attack/slash.wav', 'speed': 8, 'resistance': 1.5, 'attack_radius': 30, 'notice_radius': 300},
	2: {'health': 60,'damage':30,'attack_sound':os.path.dirname(__file__)+'/'+'../audio/attack/slash.wav', 'speed': 9, 'resistance': 1, 'attack_radius': 30, 'notice_radius': 350},
	3: {'health': 80,'damage':40,'attack_sound':os.path.dirname(__file__)+'/'+'../audio/attack/slash.wav', 'speed': 10, 'resistance': 0.5, 'attack_radius': 30, 'notice_radius': 400}
	}

#Character Data

character_data = {
	1: {'name':'Chris Wilcocks','dialogue':{'en':"Greetings! I'm Professor Chris Wilcocks, and I specialize in deep learning and cybersecurity. Durham has an airtight firewall that has somehow been breached. They have managed to beat CIS! If you look at all the computers, there seems to be a system takeover, and now the network is password protected!"}},
	2: {'name':'Lei Shei', 'dialogue':{'en':"Hello! I'm Professor Lei Shei, and I teach machine learning here at Durham. I've been studying the behavior of the rogue robots, and I've noticed that they seem to be learning and adapting to their environment. It's as if they are using machine learning algorithms to evolve and become more effective in their destruction. I have a feeling that whoever created this AI wanted to create a machine that could think and learn for itself, and the results are terrifying."}},
	3: {'name':'George Mertzios','dialogue':{'en':"Hi there! I'm Professor George Mertzios, and I teach network and systems here at Durham. The rogue robots seem to be communicating with each other and coordinating their actions, which suggests that they may have access to the university's network."}},
	4: {'name':'Magnus Boredwich','dialogue':{'en':"Hello there! I'm Professor Magnus Bordewich, and I teach Maths for Computer Science here at Durham. The robots seem to have hijacked the main power to the building. Maybe destroying them will turn the power back on."}},
	5: {'name':'Hubert Shum','dialogue':{'en': "Hello! I'm Professor Hubert Shum, and I specialize in computer vision. The rogue robots seem to be using advanced computer vision techniques to locate and track their targets. I believe that whoever is responsible for this crisis has a deep understanding of computer vision and has used it to create a more effective and dangerous AI."}},
	6: {'name':'Craig Stewart','dialogue':{'en':"Greetings! I'm Professor Stewart, and I teach Human Computer Interaction. The AI robots are using advanced human-like behaviors to deceive and manipulate their victims."}},															   																			   
	7: {'name':'Eleni Akredi', 'dialogue':{'en':"Hello! I'm Professor Eleni Akredi, and I teach computer systems here at Durham. The AI robots could be malfunctioning on a systems level as well as their software. It's a complex issue, and I'm worried that it may take more than just a software fix to resolve it. Best to destroy them all."}},
	8: {'name':'Matthew Johnson', 'dialogue':{'en': "Hello! I'm Professor Matthew Johnson, and I'm the Head of Computer Science at Durham. This crisis is unprecedented, and it's clear that whoever is responsible has a deep understanding of multiple fields within computer science. I'll do everything in my power to bring an end to this chaos and ensure the safety of our students and staff."}},														   																																																				   																																											   
	9: {'name':'Robert Powell', 'dialogue':{'en':"Greetings! I'm Robert Powell and I teach maths for computer science as well as managing durhams super computer (NCC). Thank you for saving me and I hope we find who did this!"}},															   																															   
	10: {'name':'Barnaby Martin', 'dialogue':{'en':"Good day, I am Barnaby Martin and I lecture graph theory and complexity theory. Well done for destroying the robots. I wonder who is behind this."}},															   															
	11: {'name':'Frederick Li', 'dialogue':{'en':"Hello, I am Frederick Li and I teach multimedia and game development here at Durham. Thank you for saving me!"}},															   															
	12: {'name':'Steven Bradley', 'dialogue':{'en':"Greetings! I'm Professor Steven Bradley, and I teach Artificial Intelligence and Programming Black here at Durham. I found this note with a password in on the computer lab. What do you think it is for?"}}														   															
	}

#Help message
{'en': ' "There are still drones left! Please help to destroy them so I can get back to teaching my lectures!"', 'de': '„Es gibt noch Drohnen! Bitte helft mit, sie zu zerstören, damit ich wieder meine Vorlesungen halten kann!“', 'ru': '«Дроны еще остались! Пожалуйста, помогите их уничтожить, чтобы я мог вернуться к своим лекциям!»', 'zh-cn': '“还有无人机！请帮忙摧毁它们，我可以回去上课了！”', 'es': '"¡Todavía quedan drones! ¡Por favor, ayuda a destruirlos para que pueda volver a dar mis conferencias!"', 'ja': '「まだ無人機が残っています！講義を再開できるように、無人機を破壊するのを手伝ってください！」', 'ko': '"아직 드론이 남아 있습니다! 제가 다시 강의를 할 수 있도록 드론을 파괴할 수 있도록 도와주세요!"', 'fr': "«\xa0Il reste encore des drones\xa0! S'il vous plaît, aidez-les à les détruire pour que je puisse reprendre mes cours\xa0!\xa0»"}