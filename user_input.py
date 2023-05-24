import pygame

import instance as inst
import network

text_input = str()

def mouse_canvas_pos():
    pos = pygame.mouse.get_pos()

    pos = (pos[0] - inst.renderer.hor_offset,
           pos[1] - inst.renderer.vert_offset)

    pos = (pos[0] * (1 / inst.renderer.scale_factor),
           pos[1] * (1 / inst.renderer.scale_factor))

    return pos

def handle_event(e:pygame.event.Event):
    global text_input

    if e.type == pygame.MOUSEMOTION:
        return

    if e.type == pygame.MOUSEBUTTONDOWN:
        if e.button == 1:
            inst.state.mouse_event(mouse_canvas_pos(), True)

    if e.type == pygame.MOUSEBUTTONUP:
        if e.button == 1:
            inst.state.mouse_event(mouse_canvas_pos(), False)

    if e.type == pygame.TEXTINPUT:
        text_input += e.text

    if e.type == pygame.KEYDOWN:
        if e.key == pygame.K_ESCAPE:
            inst.screen_closed = True
        elif e.key == pygame.K_BACKSPACE:
            text_input = text_input[:-1]
        elif e.key == pygame.K_EQUALS:
            tmp = network.get_incoming_drop_chance() + 5
            if tmp <= 100:
                print('Set incoming drop chance to ', tmp)
                network.set_incoming_drop_chance(tmp)
        elif e.key == pygame.K_MINUS:
            tmp = network.get_incoming_drop_chance() - 5
            if tmp >= 0:
                print('Set incoming drop chance to ', tmp)
                network.set_incoming_drop_chance(tmp)
        elif e.key == pygame.K_RIGHTBRACKET:
            tmp = network.get_outgoing_drop_chance() + 5
            if tmp <= 100:
                print('Set outgoing drop chance to ', tmp)
                network.set_outgoing_drop_chance(tmp)
        elif e.key == pygame.K_LEFTBRACKET:
            tmp = network.get_outgoing_drop_chance() - 5
            if tmp >= 0:
                print('Set outgoing drop chance to ', tmp)
                network.set_outgoing_drop_chance(tmp)
        elif e.key == pygame.K_p:
            network.set_outgoing_drop_chance(100)
            network.set_incoming_drop_chance(100)
            print('Dropping all incoming and outgoing packets')

        if inst.state.uses_key_events:
            inst.state.key_events.put(e)

    if e.type == pygame.KEYUP:
        if e.key == pygame.K_p:
            network.set_outgoing_drop_chance(0)
            network.set_incoming_drop_chance(0)
            print('Restored drop chances to 0')