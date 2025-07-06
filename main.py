# En main.py
def handle_gamepad():
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:  # Botón A (Saltar)
                samus.jump()
            elif event.button == 2:  # Botón X (Disparar)
                samus.shoot()
        elif event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:  # Eje horizontal (Movimiento)
                samus.move_x(event.value * 5)