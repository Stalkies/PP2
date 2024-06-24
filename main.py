
import time
import threading
from pywinauto import Desktop
from pywinauto.keyboard import send_keys
from pynput import keyboard, mouse
#(106, 265)
# Список заголовков окон, для которых нужно нажимать "Enter"
target_windows = ["Komunikat błędu"]

class BarcodeScanner:
    def __init__(self):
        self.prefix = "BLC"
        self.current_input = ""
        self.matching_index = 0
        self.collecting_data = False
        self.click_position_komplet = (671, 170)
        self.click_position_komplet_check = (106, 265)
        self.mouse_controller = mouse.Controller()

    def on_press(self, key):
        try:
            char = key.char
            if char:
                if not self.collecting_data:
                    self.current_input += char
                    self.check_input(char)
                else:
                    self.current_input += char
        except AttributeError:
            pass

    def check_input(self, char):
        if char.upper() == self.prefix[self.matching_index]:
            self.matching_index += 1
            if self.matching_index == len(self.prefix):
                print(f"Detected prefix {self.prefix}")
                self.collecting_data = True
                self.current_input = ""
                self.matching_index = 0
        else:
            print(f"Character '{char}' did not match, resetting input.")
            self.current_input = ""
            self.matching_index = 0

    def on_release(self, key):
        if self.collecting_data and key == keyboard.Key.enter:
            print(f"Complete input: BLC{self.current_input}")
            time.sleep(2)
            self.click_at_position()
            self.current_input = ""
            self.collecting_data = False

        if key == keyboard.Key.esc:
            return False

    def click_at_position(self):
        self.mouse_controller.position = self.click_position_komplet_check
        self.mouse_controller.click(mouse.Button.left, 1)
        self.mouse_controller.position = self.click_position_komplet_check
        self.mouse_controller.click(mouse.Button.left, 1)
        self.mouse_controller.position = self.click_position_komplet
        self.mouse_controller.click(mouse.Button.left, 1)

    def start(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
def get_mouse_position():
    from pynput.mouse import Controller
    import time

    mouse = Controller()
    try:
        while True:
            print(f"Current mouse position: {mouse.position}")
            time.sleep(1)
    except KeyboardInterrupt:
        pass


def watch_windows():
    counter = 0
    while True:
        if counter >= 3:
            for i in range(3):
                send_keys("+{TAB}")
            counter = 0
        # Получаем все активные окна на рабочем столе
        windows = Desktop(backend="uia").windows()
        for window in windows:
            # Проверяем, есть ли окно в списке целевых
            if window.window_text() in target_windows:
                print(f"Detected target window: {window.window_text()}")
                # Активируем окно и нажимаем "Enter"
                window.set_focus()
                send_keys("{ENTER}")
                counter += 1
        # Ждем перед следующим циклом
        time.sleep(1)

if __name__ == "__main__":
    get_mouse_position()
    scanner = BarcodeScanner()
        # Создаем и запускаем поток для сканера штрих-кодов
    scanner_thread = threading.Thread(target=scanner.start)
    scanner_thread.start()
    
    # Создаем и запускаем поток для отслеживания окон
    window_thread = threading.Thread(target=watch_windows)
    window_thread.start()
    
    # Ожидаем завершения обоих потоков
    scanner_thread.join()
    window_thread.join()
    
