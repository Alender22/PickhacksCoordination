import pygame


import sys
import os
import google.generativeai as genai

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro-latest') 

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NPC Chatbot")

# Colors
WHITE = (255, 255, 255)
CHAOS = (0, 175, 0)
BLACK = (0, 0, 0)
PLAYER_COLOR = (0, 0, 255)
NPC_COLOR = (255, 0, 0)

# Player and NPC settings
PLAYER_SIZE = 50
NPC_SIZE = 50
player_pos = [WIDTH // 2, HEIGHT // 2]
npc_pos = [WIDTH // 4, HEIGHT // 4]
player_speed = 1

# Font
font = pygame.font.Font(None, 36)

# Chatbot state
chat_active = False
while player_response != "n":
    def get_npc_response(player_input):
        response = model.generate(prompt=player_input)
        return response['text']
'''npc_message = "Greetings, I am The Ghost Miner"
player_response = input("Add response here: ")
while player_response != "n":
    npc_message = " "
    npc_message = "would you like to say anything else (y/n)?"
    player_response = input(" ")
    if player_response == "y":
        npc_message = "What would you like to say?" 
        player_response = input(" ")
    else: 
        npc_message = "Goodbye"
        break 
'''


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if chat_active:
                if event.key == pygame.K_RETURN:
                    print(f"Player: {player_response}")
                    player_response = ""
                elif event.key == pygame.K_BACKSPACE:
                    player_response = player_response[:-1]
                else:
                    player_response += event.unicode

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed

    # Check distance between player and NPC
    distance = ((player_pos[0] - npc_pos[0]) ** 2 + (player_pos[1] - npc_pos[1]) ** 2) ** 0.5
    if distance < 150:
        chat_active = True
    else:
        chat_active = False

    # Drawing
    screen.fill(CHAOS)
    pygame.draw.rect(screen, PLAYER_COLOR, (*player_pos, PLAYER_SIZE, PLAYER_SIZE))
    pygame.draw.rect(screen, NPC_COLOR, (*npc_pos, NPC_SIZE, NPC_SIZE))

    if chat_active:
        npc_text = font.render(npc_message, True, BLACK)
        screen.blit(npc_text, (npc_pos[0], npc_pos[1] - 30))
        player_text = font.render(player_response, True, BLACK)
        screen.blit(player_text, (player_pos[0], player_pos[1] - 30))

    pygame.display.flip()

pygame.quit()
sys.exit()