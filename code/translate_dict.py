import json

with open("/Users/jacobcurtis/Downloads/1-2.json", "r") as file:
    data = json.load(file)

result = {item['symbol']: item['text'] for item in data}
print(result)

# character_data = {
# 	1: {'name':'Chris Wilcocks','dialogue':{'en':"Greetings! I'm Professor Chris Wilcocks, and I specialize in deep learning and cybersecurity. Durham has an airtight firewall that has somehow been breached. They have managed to beat CIS! If you look at all the computers, there seems to be a system takeover, and now the network is password protected!"}},
# 	2: {'name':'Lei Shei', 'dialogue':{'en':"Hello! I'm Professor Lei Shei, and I teach machine learning here at Durham. I've been studying the behavior of the rogue robots, and I've noticed that they seem to be learning and adapting to their environment. It's as if they are using machine learning algorithms to evolve and become more effective in their destruction. I have a feeling that whoever created this AI wanted to create a machine that could think and learn for itself, and the results are terrifying."}},
# 	3: {'name':'George Mertzios','dialogue':{'en':"Hi there! I'm Professor George Mertzios, and I teach network and systems here at Durham. The rogue robots seem to be communicating with each other and coordinating their actions, which suggests that they may have access to the university's network."}},
# 	4: {'name':'Magnus Boredwich','dialogue':{'en':"Hello there! I'm Professor Magnus Bordewich, and I teach Maths for Computer Science here at Durham. I am supposed to be teaching linear algebra and calculus right now. What a day!"}},
# 	5: {'name':'Hubert Shum','dialogue':{'en': "Hello! I'm Professor Hubert Shum, and I specialize in computer vision. The rogue robots seem to be using advanced computer vision techniques to locate and track their targets. I believe that whoever is responsible for this crisis has a deep understanding of computer vision and has used it to create a more effective and dangerous AI."}},
# 	6: {'name':'Craig Stewart','dialogue':{'en':"Greetings! I'm Professor Stewart, and I teach Human Computer Interaction. The AI robots are using advanced human-like behaviors to deceive and manipulate their victims."}},															   																			   
# 	7: {'name':'Eleni Akredi', 'dialogue':{'en':"Hello! I'm Professor Eleni Akredi, and I teach computer systems here at Durham. The AI robots could be malfunctioning on a systems level as well as their software. It's a complex issue, and I'm worried that it may take more than just a software fix to resolve it. Best to destroy them all."}},
# 	8: {'name':'Matthew Johnson', 'dialogue':{'en': "Hello! I'm Professor Matthew Johnson, and I'm the Head of Computer Science at Durham. This crisis is unprecedented, and it's clear that whoever is responsible has a deep understanding of multiple fields within computer science. I'll do everything in my power to bring an end to this chaos and ensure the safety of our students and staff."}},														   																																																				   																																											   
# 	9: {'name':'Robert Powell', 'dialogue':{'en':"Greetings! I'm Robert Powell and I teach maths for computer science as well as managing durhams super computer (NCC). Thank you for saving me and I hope we find who did this!"}},															   																															   
# 	10: {'name':'Barnaby Martin', 'dialogue':{'en':"Good day, I am Barnaby Martin and I lecture graph theory and complexity theory. Well done for destroying the robots. I wonder who is behind this."}},															   															
# 	11: {'name':'Frederick Li', 'dialogue':{'en':"Hello, I am Frederick Li and I teach multimedia and game development here at Durham. Thank you for saving me!"}},															   															
# 	12: {'name':'Steven Bradley', 'dialogue':{'en':"Greetings! I'm Professor Steven Bradley, and I teach Artificial Intelligence and Programming Black here at Durham. I found this note with a password in on the computer lab. What do you think it is for?"}}														   															
# 	}
# en_dialogues = [item['dialogue']['en'] for item in character_data.values()]
# print(en_dialogues[9:12])