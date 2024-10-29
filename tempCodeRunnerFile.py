def main(screen):
    clock = pygame.time.Clock()
    block_size = 96
    floor = [Block(i * block_size, HEIGHT - block_size + 50, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    background = Background()
    player = Player(100, 100, 32, 32)
    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        player.loop(FPS)
        handle_move(player, floor)        
        background.draw(screen)
        player.draw(screen, offset_x)
        draw(screen ,floor, offset_x)

        if((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel >0) or (
            (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel


        # Update the display
        pygame.display.flip()

    pygame.quit()
    quit()