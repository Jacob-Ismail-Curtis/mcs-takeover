import pygame

# Initialize Pygame
pygame.init()

# Set the password
password = "secret"

# Set the font size
font_size = 20

# Set the font color
font_color = (0, 0, 0)

# Set the font type
font_type = pygame.font.Font(None, font_size)

# Set the window size
window_size = (400, 300)

# Create the window
window = pygame.display.set_mode(window_size)

# Set the window title
pygame.display.set_caption("Password Input")

# Set the initial value of the user input
user_input = ""

# Set the initial value of the password check
password_check = False

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.unicode.isalpha() or event.unicode.isdigit() or event.unicode == " ":
                user_input += event.unicode
            if event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            if event.key == pygame.K_RETURN:
                if user_input == password:
                    password_check = True
                    running = False
                else:
                    user_input = "Password incorrect"

    # Render the user input
    text = font_type.render(user_input, True, font_color)

    # Clear the window
    window.fill((255, 255, 255))

    # Display the user input
    window.blit(text, [10, 10])

    # Update the window
    pygame.display.update()

    # If the password is incorrect, clear the user input
    if user_input == "Password incorrect":
        pygame.time.wait(1000)
        user_input = ""

# Quit Pygame
pygame.quit()
