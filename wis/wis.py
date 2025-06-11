import pygame
import sys


pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whispers in the Shadows")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (30, 30, 30)
DARK_HALL = (20, 20, 20)
DARK_ROOM = (10, 10, 10)
LIGHT_ROOM = (60, 60, 60)
RITUAL_ROOM = (15, 10, 20)

font = pygame.font.SysFont("Arial", 20)
title_font = pygame.font.SysFont("Arial", 40, bold=True) # For start screen

clock = pygame.time.Clock()

game_state = {
    "current_chapter": "start_screen", 
    "message": "",
    "inventory": set(), 

    "ch1_door_open": False,

    "ch2_unlocked": False,
    "ch2_found_memories": set(),

    "ch3_room": "selection", # "selection", "living", "unlocked"
    "ch3_drawer_unlocked": False,
    "ch3_code_input": "",
    "ch3_correct_code": "347",
    "ch3_buttons": {
        "living": pygame.Rect(100, 200, 200, 50),
        "kitchen": pygame.Rect(100, 300, 200, 50),
        "stairs": pygame.Rect(100, 400, 200, 50)
    },

    "ch4_curtains_closed": False,
    "ch4_mirror_revealed": False,
    "ch4_book_unlocked": False,

    "ch5_clicked_sequence": [],
    "ch5_correct_sequence": [1, 0, 2],
    "ch5_puzzle_solved": False,
    "ch5_ending_triggered": False,
    "ch5_bad_attempts": 0,
    "ch5_final_message_shown": False # To control transition after final message
}

ch1_objects = {
    "toy": pygame.Rect(150, 400, 60, 60),
    "photo": pygame.Rect(300, 300, 80, 60),
    "diary": pygame.Rect(500, 350, 80, 60),
    "door": pygame.Rect(700, 250, 60, 120)
}

ch2_portraits = [pygame.Rect(100, 150, 60, 100), pygame.Rect(600, 150, 60, 100)]
ch2_memory_fragments = [pygame.Rect(200, 400, 40, 40), pygame.Rect(500, 450, 40, 40)]
ch2_door = pygame.Rect(700, 250, 60, 120)

ch3_objects = {
    "bookshelf": pygame.Rect(100, 150, 100, 200),
    "candle": pygame.Rect(300, 200, 40, 40),
    "drawer": pygame.Rect(500, 400, 100, 60),
    "door": pygame.Rect(700, 250, 60, 120)
}

ch4_objects = {
    "curtains": pygame.Rect(100, 100, 120, 300),
    "mirror": pygame.Rect(300, 150, 120, 180),
    "book": pygame.Rect(550, 400, 120, 60),
    "door": pygame.Rect(700, 250, 60, 120)
}

ch5_symbols = [
    pygame.Rect(200, 300, 60, 60),
    pygame.Rect(370, 250, 60, 60),
    pygame.Rect(540, 300, 60, 60)
]
ch5_candles = pygame.Rect(370, 150, 60, 60)
ch5_door = pygame.Rect(700, 500, 80, 80)



def reset_chapter_state(chapter_name):
    """Resets specific state variables for a given chapter."""
    global game_state
    if chapter_name == "chapter1":
        game_state["ch1_door_open"] = False
        game_state["inventory"].discard("key") 
    elif chapter_name == "chapter2":
        game_state["ch2_unlocked"] = False
        game_state["ch2_found_memories"].clear()
    elif chapter_name == "chapter3":
        game_state["ch3_room"] = "selection"
        game_state["ch3_drawer_unlocked"] = False
        game_state["ch3_code_input"] = ""
        game_state["inventory"].discard("key") 
    elif chapter_name == "chapter4":
        game_state["ch4_curtains_closed"] = False
        game_state["ch4_mirror_revealed"] = False
        game_state["ch4_book_unlocked"] = False
    elif chapter_name == "chapter5":
        game_state["ch5_clicked_sequence"].clear()
        game_state["ch5_puzzle_solved"] = False
        game_state["ch5_ending_triggered"] = False
        game_state["ch5_bad_attempts"] = 0
        game_state["ch5_final_message_shown"] = False

def draw_message():
    """Draws the current game message on the screen."""
    if game_state["message"]:
        text_surface = font.render(game_state["message"], True, WHITE)
        screen.blit(text_surface, (20, 20))


def chapter_start_screen(event):
    """Handles logic and drawing for the start screen."""
    screen.fill(BLACK)
    title_text = title_font.render("Whispers in the Shadows", True, WHITE)
    start_text = font.render("Click anywhere to begin...", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 20))

    if event.type == pygame.MOUSEBUTTONDOWN:
        game_state["current_chapter"] = "chapter1"
        game_state["message"] = "" 

def chapter1_logic(event):
    """Handles logic for Chapter 1."""
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        game_state["message"] = ""

        if ch1_objects["toy"].collidepoint(pos):
            game_state["message"] = "The stuffed toy feels familiar..."
        elif ch1_objects["photo"].collidepoint(pos):
            game_state["message"] = "A family photo... all faces scratched out."
        elif ch1_objects["diary"].collidepoint(pos):
            game_state["message"] = "The diary reads: 'Shadows whisper truths you dare not face...'"
            game_state["inventory"].add("key")
        elif ch1_objects["door"].collidepoint(pos):
            if "key" in game_state["inventory"]:
                game_state["message"] = "You unlock the door. A hallway awaits..."
                game_state["ch1_door_open"] = True
            else:
                game_state["message"] = "The door is locked tight."

def chapter1_draw():
    """Draws elements for Chapter 1."""
    screen.fill(DARK_GRAY)

    pygame.draw.rect(screen, (200, 100, 100), ch1_objects["toy"])
    pygame.draw.rect(screen, (100, 200, 100), ch1_objects["photo"])
    pygame.draw.rect(screen, (100, 100, 200), ch1_objects["diary"])
    pygame.draw.rect(screen, (150, 150, 150), ch1_objects["door"])

    # Labels
    screen.blit(font.render("Stuffed Toy", True, WHITE), (ch1_objects["toy"].x, ch1_objects["toy"].y - 20))
    screen.blit(font.render("Photo", True, WHITE), (ch1_objects["photo"].x, ch1_objects["photo"].y - 20))
    screen.blit(font.render("Diary", True, WHITE), (ch1_objects["diary"].x, ch1_objects["diary"].y - 20))
    screen.blit(font.render("Door", True, WHITE), (ch1_objects["door"].x, ch1_objects["door"].y - 20))

    if game_state["ch1_door_open"]:
        game_state["message"] = "Entering the hallway..."
        draw_message() 
        pygame.display.flip()
        pygame.time.wait(1000)
        game_state["current_chapter"] = "chapter2"
        game_state["message"] = "" 

def chapter2_logic(event):
    """Handles logic for Chapter 2."""
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        game_state["message"] = ""

        for i, m in enumerate(ch2_memory_fragments):
            if m.collidepoint(pos) and i not in game_state["ch2_found_memories"]:
                game_state["ch2_found_memories"].add(i)
                game_state["message"] = "A memory returns... pain, then silence."

        if ch2_door.collidepoint(pos):
            if len(game_state["ch2_found_memories"]) == len(ch2_memory_fragments):
                game_state["message"] = "The door creaks open, inviting you forward..."
                game_state["ch2_unlocked"] = True
            else:
                game_state["message"] = "It won't budge. Something is missing..."

        for p in ch2_portraits:
            if p.collidepoint(pos):
                game_state["message"] = "The eyes... are they moving?"

def chapter2_draw():
    """Draws elements for Chapter 2."""
    screen.fill(DARK_HALL)

    for p in ch2_portraits:
        pygame.draw.rect(screen, (80, 80, 120), p)
        screen.blit(font.render("Portrait", True, WHITE), (p.x, p.y - 20))


    for i, m in enumerate(ch2_memory_fragments):
        if i not in game_state["ch2_found_memories"]:
            pygame.draw.rect(screen, (180, 180, 80), m)
            screen.blit(font.render(f"Fragment {i+1}", True, WHITE), (m.x, m.y - 20))

    pygame.draw.rect(screen, (100, 100, 100), ch2_door)
    screen.blit(font.render("Door", True, WHITE), (ch2_door.x, ch2_door.y - 20))

    if game_state["ch2_unlocked"]:
        game_state["message"] = "Moving to the next room..."
        draw_message()
        pygame.display.flip()
        pygame.time.wait(1000)
        game_state["current_chapter"] = "chapter3"
        game_state["message"] = ""

def chapter3_logic(event):
    """Handles logic for Chapter 3."""
    current_ch3_room = game_state["ch3_room"]

    if current_ch3_room == "selection":
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if game_state["ch3_buttons"]["living"].collidepoint(pos):
                game_state["ch3_room"] = "living"
                game_state["message"] = ""
            elif game_state["ch3_buttons"]["kitchen"].collidepoint(pos):
                game_state["message"] = "Kitchen not available yet."
            elif game_state["ch3_buttons"]["stairs"].collidepoint(pos):
                game_state["message"] = "You feel a chill… not yet."

    elif current_ch3_room == "living":
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            game_state["message"] = ""
            if ch3_objects["bookshelf"].collidepoint(pos):
                game_state["message"] = "Dusty books... One has a number: 3"
            elif ch3_objects["candle"].collidepoint(pos):
                game_state["message"] = "The flame flickers violently... 4?"
            elif ch3_objects["drawer"].collidepoint(pos):
                if game_state["ch3_drawer_unlocked"]:
                    game_state["message"] = "The drawer is open. A key lies inside."
                    game_state["inventory"].add("key")
                else:
                    game_state["message"] = f"Enter 3-digit code: {game_state['ch3_code_input']}"
            elif ch3_objects["door"].collidepoint(pos):
                if "key" in game_state["inventory"]:
                    game_state["message"] = "The door opens with a creak... onward to Chapter 4."
                    game_state["ch3_room"] = "unlocked"
                else:
                    game_state["message"] = "Locked. A key is needed."

        elif event.type == pygame.KEYDOWN:
            if not game_state["ch3_drawer_unlocked"]:
                if event.unicode.isdigit() and len(game_state["ch3_code_input"]) < 3:
                    game_state["ch3_code_input"] += event.unicode
                    game_state["message"] = f"Enter 3-digit code: {game_state['ch3_code_input']}"
                elif event.key == pygame.K_BACKSPACE: # Allow backspace
                    game_state["ch3_code_input"] = game_state["ch3_code_input"][:-1]
                    game_state["message"] = f"Enter 3-digit code: {game_state['ch3_code_input']}"
                elif event.key == pygame.K_RETURN and game_state["ch3_code_input"]:
                    if game_state["ch3_code_input"] == game_state["ch3_correct_code"]:
                        game_state["ch3_drawer_unlocked"] = True
                        game_state["message"] = "The drawer clicks open."
                    else:
                        game_state["message"] = "Wrong code..."
                        game_state["ch3_code_input"] = ""

def chapter3_draw():
    """Draws elements for Chapter 3."""
    screen.fill(DARK_ROOM)

    current_ch3_room = game_state["ch3_room"]

    if current_ch3_room == "selection":
        title = font.render("Where would you like to go?", True, WHITE)
        screen.blit(title, (100, 100))
        for name, rect in game_state["ch3_buttons"].items():
            pygame.draw.rect(screen, (100, 100, 200), rect)
            screen.blit(font.render(name.capitalize(), True, WHITE), (rect.x + 10, rect.y + 10))

    elif current_ch3_room == "living":
        pygame.draw.rect(screen, (80, 60, 50), ch3_objects["bookshelf"])
        pygame.draw.rect(screen, (200, 200, 100), ch3_objects["candle"])
        pygame.draw.rect(screen, (120, 120, 120), ch3_objects["drawer"])
        pygame.draw.rect(screen, (150, 150, 150), ch3_objects["door"])

        screen.blit(font.render("Bookshelf", True, WHITE), (ch3_objects["bookshelf"].x, ch3_objects["bookshelf"].y - 20))
        screen.blit(font.render("Candle", True, WHITE), (ch3_objects["candle"].x, ch3_objects["candle"].y - 20))
        screen.blit(font.render("Drawer", True, WHITE), (ch3_objects["drawer"].x, ch3_objects["drawer"].y - 20))
        screen.blit(font.render("Exit Door", True, WHITE), (ch3_objects["door"].x, ch3_objects["door"].y - 20))

    elif current_ch3_room == "unlocked":
        screen.blit(font.render("Chapter 3 complete. Ready for Chapter 4?", True, WHITE), (100, 250))
        game_state["message"] = "The path ahead is clear..."
        draw_message()
        pygame.display.flip()
        pygame.time.wait(1000)
        game_state["current_chapter"] = "chapter4"
        game_state["message"] = ""

def chapter4_logic(event):
    """Handles logic for Chapter 4."""
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        game_state["message"] = ""

        if ch4_objects["curtains"].collidepoint(pos):
            if not game_state["ch4_curtains_closed"]:
                game_state["ch4_curtains_closed"] = True
                game_state["message"] = "You draw the heavy curtains. The room darkens..."
        elif ch4_objects["mirror"].collidepoint(pos):
            if game_state["ch4_curtains_closed"] and not game_state["ch4_mirror_revealed"]:
                game_state["ch4_mirror_revealed"] = True
                game_state["message"] = "The mirror shows words: 'The truth is written... not spoken.'"
            elif not game_state["ch4_curtains_closed"]:
                game_state["message"] = "Only moonlight reflects back..."
        elif ch4_objects["book"].collidepoint(pos):
            if game_state["ch4_mirror_revealed"]:
                game_state["ch4_book_unlocked"] = True
                game_state["message"] = "The ancient book opens. The pages whisper."
            else:
                game_state["message"] = "It won’t open… Something is missing."
        elif ch4_objects["door"].collidepoint(pos):
            if game_state["ch4_book_unlocked"]:
                game_state["message"] = "The air shifts. A presence guides you to the next room..."
              
                game_state["current_chapter"] = "chapter5"
            else:
                game_state["message"] = "The door is sealed by some unseen force."

def chapter4_draw():
    """Draws elements for Chapter 4."""
    screen.fill(DARK_ROOM if game_state["ch4_curtains_closed"] else LIGHT_ROOM)

    pygame.draw.rect(screen, (50, 50, 100), ch4_objects["curtains"])
    pygame.draw.rect(screen, (180, 180, 255) if game_state["ch4_mirror_revealed"] else (120, 120, 150), ch4_objects["mirror"])
    pygame.draw.rect(screen, (200, 180, 120) if game_state["ch4_book_unlocked"] else (80, 60, 40), ch4_objects["book"])
    pygame.draw.rect(screen, (130, 130, 130), ch4_objects["door"])

    screen.blit(font.render("Curtains", True, WHITE), (ch4_objects["curtains"].x, ch4_objects["curtains"].y - 20))
    screen.blit(font.render("Mirror", True, WHITE), (ch4_objects["mirror"].x, ch4_objects["mirror"].y - 20))
    screen.blit(font.render("Book", True, WHITE), (ch4_objects["book"].x, ch4_objects["book"].y - 20))
    screen.blit(font.render("Exit", True, WHITE), (ch4_objects["door"].x, ch4_objects["door"].y - 20))

    if game_state["current_chapter"] == "chapter5": 
        game_state["message"] = "A new presence..."
        draw_message()
        pygame.display.flip()
        pygame.time.wait(1000)
        game_state["message"] = ""

def chapter5_logic(event):
    """Handles logic for Chapter 5."""
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        game_state["message"] = ""

        if ch5_candles.collidepoint(pos):
            game_state["message"] = "The flames whisper a warning."

        for i, sym in enumerate(ch5_symbols):
            if sym.collidepoint(pos) and i not in game_state["ch5_clicked_sequence"]:
                game_state["ch5_clicked_sequence"].append(i)
                if len(game_state["ch5_clicked_sequence"]) == 3:
                    if game_state["ch5_clicked_sequence"] == game_state["ch5_correct_sequence"]:
                        game_state["ch5_puzzle_solved"] = True
                        game_state["message"] = "The sigils glow... the path is revealed."
                    else:
                        game_state["ch5_bad_attempts"] += 1
                        game_state["ch5_clicked_sequence"].clear()
                        game_state["message"] = "A cold wind pushes back. Try again..."

        if ch5_door.collidepoint(pos):
            if game_state["ch5_puzzle_solved"]:
                if not game_state["ch5_ending_triggered"]:
                    game_state["message"] = "The final memory floods back... The truth is yours."
                    game_state["ch5_ending_triggered"] = True
                    game_state["ch5_final_message_shown"] = True
                elif game_state["ch5_ending_triggered"] and game_state["ch5_final_message_shown"]:
                    return "quit" 
            else:
                game_state["message"] = "It remains shut. The ritual must be completed."
    return None 

def chapter5_draw():
    """Draws elements for Chapter 5."""
    screen.fill(RITUAL_ROOM)

    pygame.draw.rect(screen, (250, 210, 60), ch5_candles)
    screen.blit(font.render("Candles", True, WHITE), (ch5_candles.x, ch5_candles.y - 25))

    for i, sym in enumerate(ch5_symbols):
        color = (100, 100, 200)
        if i in game_state["ch5_clicked_sequence"]:
            color = (200, 200, 100)
        pygame.draw.rect(screen, color, sym)
        screen.blit(font.render(f"Symbol {i+1}", True, WHITE), (sym.x, sym.y - 25))

    pygame.draw.rect(screen, (180, 80, 80), ch5_door)
    screen.blit(font.render("Final Door", True, WHITE), (ch5_door.x - 20, ch5_door.y - 25))

    if game_state["ch5_ending_triggered"]:
        final_text_surface = font.render(game_state["message"], True, (255, 255, 255))
        screen.blit(final_text_surface, (WIDTH // 2 - final_text_surface.get_width() // 2, HEIGHT // 2 - 50))
        prompt_text = font.render("Click the door again to face your destiny...", True, WHITE)
        screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 + 20))
    else:
        draw_message() 

def chapter_ending_screen():
    """Draws the final ending screen."""
    screen.fill(BLACK)
    ending_text = title_font.render("The Shadows Recede...", True, WHITE)
    thank_you_text = font.render("Thank you for playing 'Whispers in the Shadows'", True, WHITE)
    screen.blit(ending_text, (WIDTH // 2 - ending_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(thank_you_text, (WIDTH // 2 - thank_you_text.get_width() // 2, HEIGHT // 2 + 20))
    pygame.display.flip()
    pygame.time.wait(3000) 
    return "quit" 


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state["current_chapter"] == "start_screen":
            chapter_start_screen(event)
        elif game_state["current_chapter"] == "chapter1":
            chapter1_logic(event)
        elif game_state["current_chapter"] == "chapter2":
            chapter2_logic(event)
        elif game_state["current_chapter"] == "chapter3":
            chapter3_logic(event)
        elif game_state["current_chapter"] == "chapter4":
            chapter4_logic(event)
        elif game_state["current_chapter"] == "chapter5":
            action = chapter5_logic(event)
            if action == "quit":
                running = False 

    if game_state["current_chapter"] == "start_screen":
        chapter_start_screen(pygame.event.Event(pygame.NOEVENT)) 
    elif game_state["current_chapter"] == "chapter1":
        chapter1_draw()
    elif game_state["current_chapter"] == "chapter2":
        chapter2_draw()
    elif game_state["current_chapter"] == "chapter3":
        chapter3_draw()
    elif game_state["current_chapter"] == "chapter4":
        chapter4_draw()
    elif game_state["current_chapter"] == "chapter5":
        chapter5_draw()

    if game_state["current_chapter"] not in ["start_screen", "chapter5"]: 
        draw_message()

    pygame.display.flip()
    clock.tick(60)

if game_state["current_chapter"] == "chapter5" and game_state["ch5_ending_triggered"]:
    chapter_ending_screen()

pygame.quit()
sys.exit()