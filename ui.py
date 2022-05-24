import pygame_gui as pgg
import pygame


class MenuWindow(pgg.elements.UIWindow):
    def __init__(self, manager, app):
        self.app = app
        super().__init__(pygame.Rect((50, 50), (200, 300)), manager,
                         window_display_title="Menu", object_id="#menu_window")
        self.timescale_slider = pgg.elements.UIHorizontalSlider(pygame.Rect(
            self.rect.width*0.1, 10, self.rect.width*0.7, 20), app.time_scale, (0.0, 2.0), manager, self)

    def process_event(self, event):
        handled = super().process_event(event)
        if event.type == pgg.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.timescale_slider:
                self.app.time_scale = self.timescale_slider.get_current_value()
                handled = True
        return handled
