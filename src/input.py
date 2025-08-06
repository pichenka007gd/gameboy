class Input:
    def __init__(self):
        self.button_states = {
            'up': False,
            'down': False,
            'left': False,
            'right': False,
            'a': False,
            'b': False,
            'start': False,
            'select': False
        }
    
    def press(self, button: str):
        """Нажатие кнопки"""
        if button in self.button_states:
            self.button_states[button] = True
            
    def release(self, button: str):
        """Отпускание кнопки"""
        if button in self.button_states:
            self.button_states[button] = False
