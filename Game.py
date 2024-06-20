import sys
import os
import pygame
import pygame_menu


pygame.init()

size = width, height = 512, 512
speed_ball = [0, 0]
speed_hoop = [1, 0]
black = 0, 0, 0
white = 255, 255, 255
strip_color = (255, 128, 0, 200) 

current_dir = os.path.dirname(os.path.abspath(__file__))
menu_music = os.path.join(current_dir, ".assets", "menu_music.mp3")
game_music = os.path.join(current_dir, ".assets", "game_music.mp3")
wn_music = os.path.join(current_dir, ".assets", "Win.mp3")

count_sound = os.path.join(current_dir, ".assets", "countdown.wav")
basket_sound = os.path.join(current_dir, ".assets", "baskethit.wav")
lose_sound = os.path.join(current_dir, ".assets", "lose.wav")


pygame.mixer.music.load(menu_music)
pygame.mixer.music.play(-1)


countdown_sound = pygame.mixer.Sound(count_sound)
basket_hit = pygame.mixer.Sound(basket_sound)
lose_sound = pygame.mixer.Sound(lose_sound)

icon = pygame.image.load(os.path.join(current_dir, ".assets", "icon.png"))
pygame.display.set_icon(icon) 

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Basketball Air")



bg_path = os.path.join(current_dir, ".assets", "field.jpeg")
bg_menu_path = os.path.join(current_dir, ".assets", "menu_bg.png")

bg = pygame.image.load(bg_path).convert()
bg_image = pygame_menu.BaseImage(image_path=bg_menu_path)


ball_path = os.path.join(current_dir, ".assets", "ball.png")
hoop_path = os.path.join(current_dir, ".assets", "hoopnobg.png")
r_sdsh_path = os.path.join(current_dir, ".assets", "player_rsh.png")
l_sdsh_path = os.path.join(current_dir, ".assets", "player_lsh.png")
r_side_path = os.path.join(current_dir, ".assets", "player_r.png")
l_side_path = os.path.join(current_dir, ".assets", "player_l.png")

ball = pygame.image.load(ball_path)
hoop = pygame.image.load(hoop_path)

r_sideshadow = pygame.image.load(r_sdsh_path).convert_alpha()
l_sideshadow = pygame.image.load(l_sdsh_path).convert_alpha()

r_side = pygame.image.load(r_side_path).convert_alpha()
l_side = pygame.image.load(l_side_path).convert_alpha()



player = r_side


hooprect = hoop.get_rect(top=75)
playerrect = player.get_rect(center=(width //2, height-120))



clock = pygame.time.Clock()  # Let's add a Clock object to control the frame rate

game_running = False



def isWin(running,misses):
    result = ""
    speed_hoop[0]=2
    delay = 0
    pygame.mixer.music.stop()
    if misses<3:
        result = "You win!"
        delay = 10000
        pygame.mixer.music.load(wn_music)
        pygame.mixer.music.play()
    else:
        result = "You lose!"
        delay = 3000
        lose_sound.play() 

    font = pygame.font.Font(pygame_menu.font.FONT_NEVIS, 50)
    strip_height = 100
    strip_rect = pygame.Rect(0, (height - strip_height) // 2, width, strip_height)
    strip_surface = pygame.Surface((width, strip_height), pygame.SRCALPHA)
    strip_surface.fill(strip_color)  
    screen.fill(black)
    screen.blit(bg, (0, 0))
    screen.blit(strip_surface, strip_rect.topleft)
        
    text = font.render(result, True, black)
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(delay) 
    
    running = False
    return running

def display_text(surface, text, pos):
    font = pygame.font.Font(pygame_menu.font.FONT_NEVIS, 30)
    text_surface = font.render(text, True, white)
    surface.blit(text_surface, pos)
def show_countdown():
    pygame.mixer.music.stop()
    font = pygame.font.Font(pygame_menu.font.FONT_NEVIS, 50)
    strip_height = 100
    strip_rect = pygame.Rect(0, (height - strip_height) // 2, width, strip_height)
    strip_surface = pygame.Surface((width, strip_height), pygame.SRCALPHA)
    strip_surface.fill(strip_color)
    countdown_sound.play()
    for count in ["3", "2", "1", "Let's Go!"]:
        screen.fill(black)
        screen.blit(bg, (0, 0))
        screen.blit(strip_surface, strip_rect.topleft)
        
        text = font.render(count, True, black)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)  # 1 second delay
def start_game():
    global game_running
    game_running = True

def main_game(hooprect, playerrect):
 show_countdown()
 countdown_sound.stop()

 running = True
 score = 0
 pre_score=0
 misses  = 0
 isHit = False
 isThrown = False  
 isUp = False

 pygame.mixer.music.load(game_music)
 pygame.mixer.music.play(-1)
 while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit the loop if the window close button is pressed
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.mixer.music.load(menu_music)
                    pygame.mixer.music.play(-1)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    playerrect.x-=5
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    playerrect.x+=5

    if keys[pygame.K_SPACE]:
          isThrown = True
 
    if playerrect.x < 150:
        if isThrown is not True:
          player = l_side
        else:
          player = l_sideshadow
    else:
        if isThrown is False:
          player = r_side
        else:
          player = r_sideshadow
    

    if playerrect.left < 60:
            playerrect.left = 60
    if playerrect.right > 460:
            playerrect.right = 460
    if playerrect.top < 0:
            playerrect.top = 0
    if playerrect.bottom > height:
            playerrect.bottom = height

    if isThrown is True:
          speed_ball[1] = -10
    else:
          speed_ball[1] = 0
          ballrect = ball.get_rect(topleft=(playerrect.left+50, playerrect.top-14))
        
    hooprect = hooprect.move(speed_hoop)
    ballrect = ballrect.move(speed_ball)
    
   
    if ballrect.top < 0 or isHit is True:
        isThrown = False
    elif ballrect.top < 10:
         misses += 1

    if hooprect.left < 0 or hooprect.right > width:
            speed_hoop[0] = -speed_hoop[0]
    if hooprect.top < 0 or hooprect.bottom > height:
            speed_hoop[1] = -speed_hoop[1]  

    hoop_target_area = pygame.Rect(hooprect.left+90, hooprect.top+72, hooprect.width-180, hooprect.height -180)
   
    ball_area = pygame.Rect(ballrect.left+30, ballrect.top+18, ballrect.width-60, ballrect.height-50)
 
    

    if ball_area.colliderect(hoop_target_area):
        if not isHit:  # Checking to see if there has already been a hit
          isHit = True
          if isUp is False:
            score += 1
          else:
            score += 2
        basket_hit.set_volume(0.1)
        basket_hit.play()
    else:
        isHit = False 
        pre_score=score
    


    if score < 10 or isUp is True: 

       if speed_hoop[0]>0:   
            if pre_score < score:
                speed_hoop[0]+=1
       else:
           if pre_score > score:
                speed_hoop[0]-=1

    else:
        isUp = True
        hooprect.y =+15     
        

    

    if score >=25 or misses >3:
       running = isWin(running, misses)
       pygame.mixer.music.stop()
       pygame.mixer.music.load(menu_music)
       pygame.mixer.music.play(-1)
         
    
        
    screen.fill(white)
    
    
    screen.blit(bg, (0, 0))
    screen.blit(hoop, hooprect)
    screen.blit(ball, ballrect)
    screen.blit(player, playerrect)

    
    
    display_text(screen, f'Score: {score}', (360, 50))
    display_text(screen, f'Fails: {misses}', (360, 80))

    pygame.display.flip()
    clock.tick(60)




custom_theme = pygame_menu.themes.Theme(
    title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE,
    #title_font=pygame_menu.font.FONT_8BIT,
    background_color=bg_image,
    #title_offset=(50, -50),
    widget_offset=(0, 75),
    widget_font_size=45,
    widget_font=pygame_menu.font.FONT_8BIT,
    widget_font_color=black,
    widget_selection_effect = pygame_menu.widgets.HighlightSelection(border_width=0),  # Removing the rectangular selection
)




menu = pygame_menu.Menu('', width, height, theme=custom_theme)




menu.add.button('Play', start_game)
menu.add.button('Quit', pygame_menu.events.EXIT)




while True:
    if game_running:
        main_game(hooprect, playerrect)      
        game_running = False
    else:
        screen.fill(black)
        menu.update(pygame.event.get())
        menu.draw(screen)
        
        
    pygame.display.flip()
    clock.tick(60)

 
