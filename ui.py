import pygame_gui as pgg
import pygame


class MenuWindow(pgg.elements.UIWindow):
    def __init__(self, manager, app):
        self.manager = manager
        self.app = app
        super().__init__(pygame.Rect((0, 0), (200, 300)), manager,
                         window_display_title="Menu", object_id="#menu_window")                  
        self.container_rect = self.get_container().get_rect()
        self.sliders = []
        self.add_slider(pygame.Rect(4, 24, self.container_rect.width-8, 20), (0.0, 2.0), self.app, "time_scale")
        self.add_slider(pygame.Rect(4, 64, self.container_rect.width-8, 20), (self.app.camera_group.MIN_ZOOM, self.app.camera_group.MAX_ZOOM), self.app.camera_group, "zoom_scale")

    def add_slider(self, rect, value_range, obj, attr):
        if not hasattr(obj, attr):
            return
        slider = pgg.elements.UIHorizontalSlider(rect, getattr(obj, attr), value_range, self.manager, self, self)
        label = pgg.elements.UILabel(pygame.Rect(rect.x, rect.y-rect.height+2, rect.width, rect.height), "",  self.manager, self, self)
        self.sliders.append({
            "slider": slider,
            "obj": obj,
            "attr": attr,
            "label": label,
        })
        
    def process_event(self, event):
        handled = super().process_event(event)
        if event.type == pgg.UI_HORIZONTAL_SLIDER_MOVED:
            for i in self.sliders:
                if event.ui_element == i["slider"]:
                    setattr(i["obj"], i["attr"], i["slider"].get_current_value())
                    handled = True
        return handled

    def update(self, time_delta: float):
        for i in self.sliders:
            i["slider"].set_current_value(getattr(i["obj"], i["attr"]))
            i["label"].set_text(f"{i['attr'].replace('_', ' ').capitalize()}: {getattr(i['obj'], i['attr']):.2f}")
        return super().update(time_delta)

