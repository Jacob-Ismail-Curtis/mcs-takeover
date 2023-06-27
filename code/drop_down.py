import pygame

# Initialize pygame
pygame.init()

# Set screen size and caption
size = (400, 300)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Language Selection")

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create a list of language options
languages = ["English", "Spanish", "French", "German"]

# Initialize variables for menu
menu_font = pygame.font.Font(None, 30)
selected_language = 0
drop_down_open = False

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            # elif drop_down_open:
            #     # Check if user clicks on a language option
            #     if event.pos[1] > 150 and event.pos[1] < 150 + 30*len(languages):
            #         selected_language = (event.pos[1] - 150) // 30
            #         drop_down_open = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN] and drop_down_open:
        selected_language = (selected_language + 1) % len(languages)
    elif keys[pygame.K_UP] and drop_down_open:
        selected_language = (selected_language - 1) % len(languages)
    elif keys[pygame.K_RETURN] and drop_down_open:
        drop_down_open = False
    elif keys[pygame.K_RETURN] and not drop_down_open:
        drop_down_open = True
    # Clear the screen
    screen.fill(WHITE)

    # Draw the language selection button
    pygame.draw.rect(screen, BLACK, (50, 100, 300, 50))
    language_text = menu_font.render("Select Language", True, WHITE)
    screen.blit(language_text, (150, 110))

    # Draw the drop-down menu
    if drop_down_open:
        for i, language in enumerate(languages):
            pygame.draw.rect(screen, BLACK, (50, 150 + 30*i, 300, 30))
            language_text = menu_font.render(language, True, WHITE)
            screen.blit(language_text, (150, 160 + 30*i))
            if i == selected_language:
                pygame.draw.rect(screen, (0,0,255), (50, 150 + 30*i, 300, 30), 2)
    # Display the selected language
    selected_language_text = menu_font.render("Selected Language: " + languages[selected_language], True, BLACK)
    screen.blit(selected_language_text, (50, 250))
    
    # Update the screen
    pygame.display.flip()

# Quit pygame
pygame.quit()