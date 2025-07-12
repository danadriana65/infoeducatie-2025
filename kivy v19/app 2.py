import kivy
from session import UserSession
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from PIL import Image as PILImage, ImageDraw
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.video import Video
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import webbrowser
from kivy.uix.popup import Popup
import os
import sys
import json
from kivy.uix.image import Image as KivyImage
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.floatlayout import FloatLayout
from kivy.resources import resource_find

def load_user_credentials():
    try:
        with open("user_credentials.json","r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
            return {}
def store_user_info(username, password, email):
    user_data = load_user_credentials()
    if username in user_data:
        return "User already exists"
    else:
        user_data[username] = {"username": username, "password": password, "email": email}  
        with open("user_credentials.json", "w") as f:
            json.dump(user_data, f, indent=4)
        return "Account created successfully"

def verify_user(username, password):
    user_data = load_user_credentials()
    return username in user_data and user_data[username]["password"] == password

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(Label(text="Welcome to App!", font_size=24))

        start_button = Button(text="Start")
        start_button.bind(on_press=self.go_to_image)
        layout.add_widget(start_button)

        self.add_widget(layout)

    def go_to_image(self, instance):
        self.manager.current = "image_screen"

class ImageScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical")
        self.default_image_path = r"videos/WhatsApp Image 2025-07-02 at 21.02.56_71248b74(1).png"  # imagine implicită
        self.add_widget(self.layout)

        if not os.path.exists(self.default_image_path):
            self.layout.add_widget(Label(text="Imaginea implicită nu a fost găsită!"))

            self.file_chooser = FileChooserListView(filters=["*.png", "*.jpg", "*.jpeg"])
            self.layout.add_widget(self.file_chooser)

            select_button = Button(text="Selectează imagine")
            select_button.bind(on_press=self.select_custom_image)
            self.layout.add_widget(select_button)
        else:
            self.show_image(self.default_image_path)
        skip_button = Button(
            text="Continue to Login",
            size_hint=(0.4, 0.1),
            pos_hint={"center_x": 0.5, "y": 0.05},
            on_press=self.skip_to_login
        )
        self.layout.add_widget(skip_button)

    def skip_to_login(self, instance):
        self.manager.current = "login_screen"
    def select_custom_image(self, instance):
        if self.file_chooser.selection:
            selected = self.file_chooser.selection[0]
            self.show_image(selected)

    def show_image(self, image_path):
        self.layout.clear_widgets()

        if isinstance(image_path, list):
            image_path = image_path[0]

        self.image_widget = Image(source=image_path, allow_stretch=True, keep_ratio=True)
        self.layout.add_widget(self.image_widget)

        # După 3 secunde, trecem la ecranul de login
        Clock.schedule_once(self.go_to_login, 10)

    def go_to_login(self, dt):
        self.manager.current = "login_screen"

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # 🎬 Video pe fundal
        self.image_path = r"videos/WhatsApp Image 2025-07-02 at 21.05.20_a0c9f2ee.png"
        if os.path.exists(self.image_path):
           self.image_widget = Image(source=self.image_path, allow_stretch=True, keep_ratio=True)
           self.layout.add_widget(self.image_widget)

        # 🔤 Etichete și input-uri
        self.layout.add_widget(Label(text="Welcome to Cosmiccode!", font_size=24,
                                     pos_hint={"center_x": 0.5, "center_y": 0.85}))

        self.username = TextInput(hint_text="Username", size_hint=(0.5, 0.1),
                                  pos_hint={"center_x": 0.5, "center_y": 0.65})
        self.email = TextInput(hint_text="Your Email", size_hint=(0.5, 0.1),
                               pos_hint={"center_x": 0.5, "center_y": 0.55})
        self.password = TextInput(hint_text="Password", password=True, size_hint=(0.5, 0.1),
                                  pos_hint={"center_x": 0.5, "center_y": 0.45})

        self.layout.add_widget(self.username)
        self.layout.add_widget(self.email)
        self.layout.add_widget(self.password)

        self.message_label = Label(text="", pos_hint={"center_x": 0.5, "center_y": 0.35})
        self.layout.add_widget(self.message_label)

        # 🔘 Butoane
        submit_button = Button(text="Create Account", size_hint=(0.3, 0.1),
                               pos_hint={"center_x": 0.5, "center_y": 0.25})
        submit_button.bind(on_press=self.submit_username)
        self.layout.add_widget(submit_button)

        login_button = Button(text="Login", size_hint=(0.3, 0.1),
                              pos_hint={"center_x": 0.5, "center_y": 0.15})
        login_button.bind(on_press=self.login)
        self.layout.add_widget(login_button)

    def submit_username(self, instance):
        entered_username = self.username.text.strip()
        entered_password = self.password.text.strip()
        entered_email = self.email.text.strip()

        if not entered_username or not entered_password or not entered_email:
            self.message_label.text = "Error: Please fill all fields!"
        else:
            result = store_user_info(entered_username, entered_password, entered_email)
            self.message_label.text = result

    def login(self, instance):
        entered_username = self.username.text.strip()
        entered_password = self.password.text.strip()

        if verify_user(entered_username, entered_password):
            # ✅ Salvăm utilizatorul activ
            with open("active_user.txt", "w") as f:
                f.write(entered_username)

            # 👉 Transmitem datele către grid_screen dacă există
            if self.manager.has_screen("grid_screen"):
                self.manager.get_screen("grid_screen").set_user_details(entered_username)

            # 🛰️ Tranziție către ecranul principal
            self.manager.current = "main"
        else:
            self.message_label.text = "Invalid credentials!"
    
class GridScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        self.video_path = r"videos/WhatsApp Video 2025-04-05 at 20.39.03_78657a3f.mp4"
        if os.path.exists(self.video_path):
            self.video_player = VideoPlayer(source=self.video_path, play=True, options={"eos": "loop"}, size_hint=(1, 1), pos_hint={"x": 0, "y": 0})
            self.video_player.allow_fullscreen = False
            self.video_player.allow_stretch = True
            self.layout.add_widget(self.video_player)

        # 🔹 Elemente UI deasupra videoclipului
        self.welcome_label = Label(
            text="Welcome, User!",
            font_size=24,
            pos_hint={"center_x": 0.5, "center_y": 0.85}
        )
        self.layout.add_widget(self.welcome_label)

        sign_out_button = Button(
            text="Continue",
            size_hint=(0.3, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.15},
            on_press=self.sign_out
        )
        self.layout.add_widget(sign_out_button)

        self.add_widget(self.layout)
    def switch_to_navigate(self, option):
      app = App.get_running_app()
      screen_name = f"navigate_screen_{option}"

      if not self.manager.has_screen(screen_name):
        self.manager.add_widget(NavigateScreen(
            option,
            app.session.user_data,
            app.session.username,
            app.session.email,
            name=screen_name
        ))

      self.manager.current = screen_name
    def set_user_details(self, username):
        self.welcome_label.text = f"Welcome, {username}!"

    def sign_out(self, instance):
        self.manager.current = "login_screen"
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        self.layout = BoxLayout(orientation="vertical", spacing=20, padding=40)
        self.add_widget(self.layout)

        # Adaugă conținut în layout
        # 🎥 Video pe fundal
        self.image_path = r"videos\WhatsApp Image 2025-07-02 at 21.05.20_a0c9f2ee.png"
        if os.path.exists(self.image_path):
           self.image_widget = Image(source=self.image_path, allow_stretch=True, keep_ratio=True)
           self.layout.add_widget(self.image_widget)
        
        # 📍 Sigle și butoane
        languages = [
            ("C++", "images/ISO_C++_Logo.svg(1).png"), 
            ("Python", "images/Python.svg(1).png"),
            ("JavaScript", "images/1698604163003(1).png")
        ]
        x_positions = [0.15, 0.4, 0.65]

        for idx, (lang, sticker) in enumerate(languages):
            btn = Button(
                text=lang,
                size_hint=(0.2, 0.1),
                pos_hint={"x": x_positions[idx], "y": 0.2}
            )
            img = Image(
                source=sticker,
                size_hint=(None, None),
                size=(80, 80),
                pos_hint={"x": x_positions[idx] + 0.03, "y": 0.33}
            )

            btn.bind(on_press=lambda instance, language=lang: self.switch_to_navigate(language))

            layout.add_widget(btn)
            layout.add_widget(img)

        # 🏆 Clasament
        ranking_button = Button(text="Clasament", size_hint=(0.2, 0.1), pos_hint={"x": 0.7, "y": 0.85})
        ranking_button.bind(on_press=self.go_to_ranking)
        layout.add_widget(ranking_button)

        # 🔙 Undo
        undo_button = Button(
            text="Undo",
            size_hint=(0.2, 0.1),
            pos_hint={"x": 0.1, "y": 0.05},
            on_press=self.undo
        )
        layout.add_widget(undo_button)

        # ⚙️ Settings
        setting_button = Button(
            text="Settings",
            size_hint=(0.2, 0.1),
            pos_hint={"x": 0.7, "y": 0.05},
            on_press=self.settings
        )
        layout.add_widget(setting_button)

        self.add_widget(layout)

    def switch_to_navigate(self, option):
        app = App.get_running_app()
        screen_name = f"navigate_screen_{option}"

        if not self.manager.has_screen(screen_name):
            self.manager.add_widget(NavigateScreen(
                option,
                {"profile_picture": app.session.profile_picture},
                app.session.username,
                app.session.email,
                name=screen_name
            ))

        self.manager.current = screen_name

    def settings(self, instance):
        self.manager.current = "settings_screen"

    def undo(self, instance):
        self.manager.current = "login_screen"

    def go_to_ranking(self, instance):
        self.manager.current = "ranking_screen"

class UserDataManager:
    def __init__(self, file_path="user_data.json"):
        self.file_path = file_path

    def load_user_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return {}

    def save_user_data(self, data):
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)
user_data_manager = UserDataManager()
def load_active_user():
    try:
        with open("active_user.txt", "r") as f:
            username = f.read().strip()
        all_users = load_user_credentials()
        return all_users.get(username, {})
    except FileNotFoundError:
        return {}

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        self.add_widget(self.layout)

        session = load_active_user()

        self.profile_label = Label(text="No profile picture selected")
        self.layout.add_widget(Label(text="Settings", font_size=24))
        self.layout.add_widget(Label(text=f"Username: {session.get('username', '(necunoscut)')}", font_size=18))
        self.layout.add_widget(Label(text=f"Email: {session.get('email', '(necunoscut)')}", font_size=18))
        self.layout.add_widget(self.profile_label)

        profile_path = session.get("profile_picture", "")
        if profile_path and os.path.exists(profile_path):
            self.update_profile_picture(profile_path)

        choose_button = Button(text="Alege poza de profil", size_hint=(None, None), width=200, height=50)
        choose_button.bind(on_press=self.choose_profile_picture)
        self.layout.add_widget(choose_button)

        remove_button = Button(text="Șterge poza de profil", size_hint=(None, None), width=200, height=50)
        remove_button.bind(on_press=self.remove_profile_picture)
        self.layout.add_widget(remove_button)

        self.session_data = session  # păstrezi datele în obiect pentru salvări viitoare

    def choose_profile_picture(self, instance):
        content = BoxLayout(orientation="vertical", spacing=10, padding=10)
        chooser = FileChooserListView(filters=["*.png", "*.jpg", "*.jpeg"], size_hint=(1, 0.9))
        confirm_btn = Button(text="Folosește această imagine", size_hint=(1, 0.1))
        content.add_widget(chooser)
        content.add_widget(confirm_btn)
        popup = Popup(title="Alege poza de profil", content=content, size_hint=(0.9, 0.9))
        popup.open()

        def set_image(_):
            if chooser.selection:
                selected = chooser.selection[0]
                self.session_data["profile_picture"] = selected
                all_users = load_user_credentials()
                username = self.session_data.get("username")
                if username in all_users:
                    all_users[username]["profile_picture"] = selected
                    with open("user_credentials.json", "w") as f:
                        import json
                        json.dump(all_users, f, indent=4)
                self.update_profile_picture(selected)
                popup.dismiss()

        confirm_btn.bind(on_press=set_image)

    def update_profile_picture(self, image_path):
        if hasattr(self, "profile_img"):
            self.layout.remove_widget(self.profile_img)

        try:
            pil_image = PILImage.open(image_path).convert("RGBA")
            size = min(pil_image.size)
            mask = PILImage.new("L", (size, size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size, size), fill=255)
            cropped = pil_image.crop((0, 0, size, size))
            cropped.putalpha(mask)
            cropped = cropped.resize((100, 100))
            img_data = cropped.tobytes()
            texture = Texture.create(size=cropped.size, colorfmt='rgba')
            texture.blit_buffer(img_data, colorfmt='rgba', bufferfmt='ubyte')
            self.profile_img = Image(texture=texture, size_hint=(None, None), size=(100, 100))
            self.layout.add_widget(self.profile_img)
            self.profile_label.text = ""
        except Exception as e:
            self.profile_label.text = f"Eroare: {e}"

    def remove_profile_picture(self, instance):
        self.session_data["profile_picture"] = ""
        all_users = load_user_credentials()
        username = self.session_data.get("username")
        if username in all_users:
            all_users[username]["profile_picture"] = ""
            with open("user_credentials.json", "w") as f:
                import json
                json.dump(all_users, f, indent=4)

        if hasattr(self, "profile_img"):
            self.layout.remove_widget(self.profile_img)
        self.profile_label.text = "No profile picture selected"
class NavigateScreen(Screen):
    def __init__(self, option, user_data, user_input, user_mail, **kwargs):
        super().__init__(**kwargs)
        self.option = option

        # 🌌 Root layout
        self.root_layout = FloatLayout()
        self.add_widget(self.root_layout)

        # 🌄 Background image
        self.image_path = r"videos/WhatsApp Image 2025-07-02 at 21.05.20_a0c9f2ee.png"
        if os.path.exists(self.image_path):
            bg_image = Image(
                source=self.image_path,
                allow_stretch=True,
                keep_ratio=False,
                size_hint=(1, 1),
                pos_hint={"x": 0, "y": 0}
            )
            self.root_layout.add_widget(bg_image)

        # 📦 Foreground layout (everything else)
        self.foreground = BoxLayout(orientation="vertical", spacing=20, padding=40, size_hint=(1, 1), pos_hint={"x": 0, "y": 0})
        self.root_layout.add_widget(self.foreground)

        # 🔘 Top buttons
        top_buttons = BoxLayout(size_hint=(1, 0.1))
        progress_btn = Button(text="Progress", size_hint=(None, None), width=150, height=50)
        progress_btn.bind(on_press=lambda x: show_progress_kivy())
        leaderboard_btn = Button(text="LeaderBoard", size_hint=(None, None), width=150, height=50)
        leaderboard_btn.bind(on_press=lambda x: show_leaderboard())
        profile_btn = Button(text="Profile", size_hint=(None, None), width=150, height=50)
        profile_btn.bind(on_press=lambda x: open_profile_popup())
        top_buttons.add_widget(progress_btn)
        top_buttons.add_widget(leaderboard_btn)
        top_buttons.add_widget(profile_btn)
        self.foreground.add_widget(top_buttons)

        # 📚 Theory button
        link_map = {
            "C++": "https://www.w3schools.com/cpp/cpp_syntax.asp",
            "Python": "https://www.w3schools.com/python/default.asp",
            "JavaScript": "https://www.w3schools.com/js/default.asp"
        }
        if self.option in link_map:
            theory_btn = Button(text=f"Teorie {self.option}", size_hint=(None, None), width=200, height=50)
            theory_btn.bind(on_press=lambda instance: webbrowser.open(link_map[self.option]))
            self.foreground.add_widget(theory_btn)

        # 🪐 Planet buttons
        planet_images = {
            "Uranus": "images/Uranus(1).png",
            "Venus": "images/Venus.png",
            "Saturn": "images/Saturn.png"
        }
        planet_buttons = BoxLayout(size_hint=(1, 0.3))
        for planet_name, image_path in planet_images.items():
            if os.path.exists(image_path):
                img = Image(source=image_path, size_hint=(None, None), width=100, height=100)
                btn = Button(text=planet_name, size_hint=(None, None), width=100, height=100)
                btn.bind(on_press=lambda instance, name=planet_name: self.switch_to_navigate(name))
                planet_buttons.add_widget(img)
                planet_buttons.add_widget(btn)
        self.foreground.add_widget(planet_buttons)

        # 🔙 Undo button
        undo_button = Button(text="Undo", size_hint=(None, None), width=200, height=50)
        undo_button.bind(on_press=lambda instance: setattr(self.manager, "current", "main_screen"))
        self.foreground.add_widget(undo_button)

    def switch_to_navigate(self, planet_name):
        screen_name = f"options_screen_{planet_name}_{self.option}"
        if not self.manager.has_screen(screen_name):
            self.manager.add_widget(OptionsScreen(planet_name, self.option, name=screen_name))
        self.manager.current = screen_name

class OptionsScreen(Screen):
    def __init__(self, planet_name, selected_option, **kwargs):
        super().__init__(**kwargs)
        self.planet_name = planet_name
        self.selected_option = selected_option

        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        title = Label(text=f"Options for {planet_name}", font_size=24, size_hint=(1, None), height=60)
        main_layout.add_widget(title)

        # Scrollable grid for exercise buttons
        scroll = ScrollView(size_hint=(1, 1))
        grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        for i in range(7):
           btn_text = f"Exercițiu {i + 1}"
           btn = Button(text=btn_text, size_hint_y=None, height=80)
           btn.bind(on_press=self.create_handler(i))
           grid.add_widget(btn)


        scroll.add_widget(grid)
        main_layout.add_widget(scroll)

        # Undo button
        undo = Button(text="Undo", size_hint=(None, None), size=(200, 50))
        undo.bind(on_press=lambda x: setattr(self.manager, "current", "navigate_screen_" + self.selected_option))
        main_layout.add_widget(undo)

        self.add_widget(main_layout)
    def create_handler(self, index):
       def handler(instance):
           self.handle_exercise(index)
       return handler


    def handle_exercise(self, i):
      print(f"Exercițiu {i + 1} selectat pentru {self.planet_name} - {self.selected_option}")
      question = ""
      code = ""
      answers = []
      correct = ""
      if self.planet_name == "Saturn" and self.selected_option == "C++":
        question = questions_cpp1[i]
        code = code_cpp1[i]
        answers = answers_cpp1[i]
        correct = answers[i]  
      elif self.planet_name == "Uranus" and self.selected_option == "C++":
          question = questions_cpp[i]
          answers = answers_cpp[i]
          correct = correct_answers_cpp[i]
      elif self.planet_name == "Venus" and self.selected_option == "C++":
          question = questions_cpp_code[i]
          answers = answers_cpp_code[i]
          correct = correct_answers_cpp[i]
      elif self.planet_name == "Uranus" and self.selected_option == "Python":
          question = questions_python[i]
          answers = answers_python[i]
          correct = correct_answers_python[i]
      elif self.planet_name == "Venus" and self.selected_option == "Python":
          question = questions_python_b[i]
          answers = answers_python_b[i]
          correct = correct_answers_python_b[i]
      elif self.planet_name == "Saturn" and self.selected_option == "Python":
        question = questions_python_c[i]
        code = code_samples_python_c[i]
        answers = answers_python_c[i]
        correct = correct_answers_python_c[i]  
      elif self.planet_name == "Uranus" and self.selected_option == "JavaScript":
          question = questions_javascript_a[i]
          answers = answers_javascript_a[i]
          correct = correct_answers_javascript_a[i]
      elif self.planet_name == "Venus" and self.selected_option == "JavaScript":
          question = questions_javascript_code[i]
          answers = answers_javascript_code[i]
          correct = correct_answers_javascript_code[i]
      elif self.planet_name == "Saturn" and self.selected_option == "JavaScript":
        question = questions_javascript_error[i]
        code = code_samples_javascript_error[i]
        answers = answers_javascript_error[i]
        correct = correct_answers_javascript_error[i]
      else:
        print("❌ Nicio întrebare disponibilă pentru combinația selectată.")
        return

      full_question = question + ("\n\n" + code if code else "")
      question_data = {
            'question': full_question,
            'answers': answers,
            'correct': correct,
            'planet': self.planet_name,
            'option': self.selected_option
        }

      if self.manager.has_screen("question"):
         self.manager.remove_widget(self.manager.get_screen("question"))

      question_screen = QuestionScreen(question_data, name="question")
      self.manager.add_widget(question_screen)
      self.manager.current = "question"
questions_javascript_code = [
    "Cum declarăm o funcție anonimă în JavaScript?",
    "Care este sintaxa corectă pentru Arrow Function?",
    "Cum definim un obiect JavaScript?",
    "Care este modul corect de a itera printr-o listă cu `forEach`?",
    "Cum verificăm dacă un element există într-un array?",
    "Cum facem destructurarea unui obiect?",
    "Cum adăugăm un nou element într-un array?"
]

answers_javascript_code = [
    ["let func = function() {}", "let func() {}", "function = func() {}"],
    ["const add = (a, b) => a + b;", "add = (a, b) { return a + b; }", "function add(a, b) => a + b;"],
    ["let obj = object { name: 'Alex', age: 25 };", "object obj = { 'name': 'Alex', 'age': 25 }", "const obj = { name: 'Alex', age: 25 }"],
    ["array.forEach(item => console.log(item));", "for (item in array) { console.log(item); }", "array.each(item => console.log(item));"],
    ["array.has(5)", "array.includes(5)", "array.exists(5)"],
    ["const { name, age } = obj;", "destructure(obj).get('name', 'age');", "let name, age = obj.extract();"],
    ["array.add('newItem')", "array.push('newItem')", "array.insert('newItem')"]
]

correct_answers_javascript_code = [
    "let func = function() {}",
    "const add = (a, b) => a + b;",
    "const obj = { name: 'Alex', age: 25 }",
    "array.forEach(item => console.log(item));",
    "array.includes(5)",
    "const { name, age } = obj;",
    "array.push('newItem')"
]
questions_javascript_a = [
    "Cum declarăm o variabilă în JavaScript?",
    "Care dintre următoarele NU este un mod valid de a declara o funcție?",
    "Cum verificăm tipul unei variabile în JavaScript?",
    "Ce va afișa `console.log(2 + '2')`?",
    "Care dintre următoarele structuri de date NU există în JavaScript?",
    "Cum iterăm peste un array folosind `map()`?",
    "Cum facem o copie superficială a unui obiect în JavaScript?"
]

answers_javascript_a = [
    ["var x = 10;", "let x = 10;", "const x = 10;", "int x = 10;"],
    ["function myFunc() {}", "const myFunc = function() {}", "myFunc = () => {}", "def myFunc() {}"],
    ["typeof x", "x.type()", "getType(x)", "x.kind"],
    ["22", "'22'", "4", "Error"],
    ["Array", "Set", "Tuple", "Map"],
    ["array.map(x => x * 2)", "map(array, x => x * 2)", "array.map(function(x) { return x * 2 })", "array.forEach(x => x * 2)"],
    ["Object.assign({}, obj)", "obj.copy()", "{...obj}", "clone(obj)"]
]

correct_answers_javascript_a = [
    "int x = 10;",  # Varianta greșită (to test knowledge)
    "def myFunc() {}",  # Varianta greșită (nu există în JS)
    "typeof x",
    "'22'",
    "Tuple",
    "array.map(x => x * 2)",
    "{...obj}"
]
questions_python_b = [
    "Cum declari o funcție în Python?",
    "Cum citești un fișier în Python?",
    "Cum iterăm peste o listă folosind list comprehension?",
    "Cum creezi o clasă în Python?",
    "Cum verifici dacă un element există într-un dicționar?",
    "Cum folosești `try-except` pentru gestionarea erorilor?",
    "Cum sortezi o listă în Python?"
]

answers_python_b = [
    ["def my_function():\n    print('Hello!')", "function my_function():\n    print('Hello!')", "def myFunction() print('Hello!')", "fun my_function():\n    print('Hello!')"],
    ["with open('file.txt', 'r') as f:\n    data = f.read()", "file = open('file.txt', 'r')\n    file.read()", "open('file.txt', 'read')", "readfile('file.txt')"],
    ["[x**2 for x in range(10)]", "for x in range(10):\n    x**2", "[for x in range(10): x**2]", "map(lambda x: x**2, range(10))"],
    ["class MyClass:\n    def __init__(self):\n        self.name = 'Example'", "def MyClass:\n    self.name = 'Example'", "new Class MyClass:\n    name = 'Example'", "class = MyClass()"],
    ["if 'key' in my_dict:", "my_dict.has_key('key')", "my_dict.contains('key')", "my_dict.find('key')"],
    ["try:\n    x = int(input('Număr:'))\nexcept ValueError:\n    print('Eroare!')", "try x = int(input('Număr')) except ValueError: print('Eroare!')", "except ValueError:\n    x = int(input('Număr'))", "catch ValueError:\n    x = int(input('Număr'))"],
    ["sorted(my_list)", "my_list.sort()", "sort(my_list)", "my_list.sorted()"]
]

correct_answers_python_b = [
    "def my_function():\n    print('Hello!')",
    "with open('file.txt', 'r') as f:\n    data = f.read()",
    "[x**2 for x in range(10)]",
    "class MyClass:\n    def __init__(self):\n        self.name = 'Example'",
    "if 'key' in my_dict:",
    "try:\n    x = int(input('Număr:'))\nexcept ValueError:\n    print('Eroare!')",
    "sorted(my_list)"
]
questions_python = [
    "Ce este metoda __new__() în Python?",
    "Ce face @staticmethod în Python?",
    "Care este diferența dintre deepcopy() și copy()?",
    "Ce va returna list(map(lambda x: x**2, range(3)))?",
    'Ce face expresia if __name__ == "__main__": în Python?',
    "Care dintre următoarele NU este o metodă validă pentru sincronizarea thread-urilor în Python?",
    "Ce rezultat va avea print(bool([]) == False)?" ]
  

answers_python = [
    ["O metodă care creează o instanță înainte de __init__()", "O metodă folosită doar în moștenirea multiplă", "O metodă specială care returnează self", "O metodă de conversie între tipuri de date"],
    ["Creează o metodă care poate fi apelată doar de alte clase", "Definește o metodă statică care nu are acces la self", "Permite accesul la metodele private din clasă", "Transformă metoda într-o variabilă de clasă"],
    ["deepcopy() face conversia tipurilor de date", "copy() elimină referințele către obiectele originale", "deepcopy() este mai rapid decât copy()", "copy() creează o copie superficială, iar deepcopy() copiază recursiv obiectele"],
    ["[1, 4, 9]", "[0, 2, 4]", "[0, 1, 4]", "[1, 2, 3]"],
    ["Creează o variabilă globală numită __main__", "Permite executarea în paralel a mai multor funcții", "Determină dacă scriptul este executat direct", "Verifică dacă scriptul este importat din alt modul"],
    ["threading.Event()", "threading.pause()", "threading.Lock()", "threading.Semaphore()"],
    ["True", "False", "Va genera o eroare", "None"]
]

correct_answers_python = ["O metodă care creează o instanță înainte de __init__()", "Definește o metodă statică care nu are acces la self", "copy() creează o copie superficială, iar deepcopy() copiază recursiv obiectele", "[0, 1, 4]", "Determină dacă scriptul este executat direct", "threading.pause()", "True"]
questions_cpp = [
    "Care dintre următoarele este un mod corect de a declara o variabilă în C++?",
    "Ce cuvânt-cheie folosim pentru a aloca dinamic memorie în C++?",
    "Ce tip de date folosim pentru a stoca un singur caracter în C++?",
    "Care dintre următoarele bucle NU există în C++?",
    "Care dintre următoarele operatori este folosit pentru accesarea membrilor unei structuri sau clase?",
    "Care este scopul funcției `main()` în C++?",
    "Ce se întâmplă când apelăm `delete` pe un pointer valid?"
]

answers_cpp = [
    ["int x;", "variable x;", "x = 5;", "declare x;"],
    ["alloc", "new", "malloc", "allocate"],
    ["char", "string", "character", "text"],
    ["for", "while", "repeat-until", "do-while"],
    [".", "->", "*", "&"],
    ["Inițializarea tuturor variabilelor", "Stabilirea punctului de intrare al programului", "Afișarea rezultatelor", "Crearea de obiecte"],
    ["Memoria asociată cu pointerul este eliberată", "Pointerul se șterge automat din cod", "Programul se oprește imediat", "Pointerul este resetat la zero"]
]

correct_answers_cpp = [
    "int x;", "new", "char", "repeat-until", ".", "Stabilirea punctului de intrare al programului", "Memoria asociată cu pointerul este eliberată"
]
questions_cpp_code = [
    "Care dintre următoarele declară corect o funcție în C++?",
    "Care dintre următoarele este sintaxa corectă pentru un `for loop`?",
    "Care este modul corect de a accesa un element dintr-un vector?",
    "Care dintre următoarele alocă corect memorie dinamică?",
    "Care dintre următoarele clase implementează corect moștenirea?",
    "Care este forma corectă de a citi un număr de la tastatură?",
    "Care dintre următoarele definește corect un destructor?"
]

answers_cpp_code = [
    ["function myFunction();", "void myFunction();", "func myFunction();"],
    ["for (i = 0; i < n; i++)", "for i in range(0, n)", "loop (i; i < n; i++)"],
    ["vector[2]", "vector(2)", "vector -> 2"],
    ["alloc<int> ptr;", "int ptr = malloc(sizeof(int));", "int *ptr = new int;"],
    ["class Child : Parent {}", "class Parent -> Child {}", "inherit Parent -> Child {}"],
    ["cin >> x;", "input(x);", "x = scan();"],
    ["~MyClass() {}", "destructor MyClass() {}", "destroy MyClass();"]
]

correct_answers_cpp_code = [
    "void myFunction();",
    "for (i = 0; i < n; i++)",
    "vector[2]",
    "int *ptr = new int;",
    "class Child : Parent {}",
    "cin >> x;",
    "~MyClass() {}"
]

questions_cpp1 = [
    "Unde este eroarea?",
    "Unde este eroarea?",
    "Unde este eroarea?",
    "Unde este eroarea?",
    "Unde este eroarea?",
    "Unde este eroarea?",
    "Unde este eroarea? "
]

# Vectorul de cod Python asociat fiecărei întrebări
code_cpp1 = [
    "#include <iostream> \nusing namespace std; \nint main() { \nint *ptr; \n*ptr = 10; \ncout << *ptr << endl; \nreturn 0;}",
    "#include <iostream> \nusing namespace std; \nint main() { \nint matrice[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}; \ncout << matrice[3][0] << endl; \n return 0;}",
    '#include <iostream> \nusing namespace std; \nint main() { \nstring mesaj = "Salut!"; \ncout << mesaj; \nreturn 0;}',
    "#include <iostream> \nusing namespace std; \nint main() { \nint v[5] = {1, 2, 3, 4, 5}; \ncout << v[5] << endl; \n return 0;}",
    '#include <iostream> \n#include <cstring> \n using namespace std; \nint main() { \nchar sir[6] = "Salut"; \nstrcat(sir, "!"); \ncout << sir << endl; \nreturn 0;}',
    "#include <iostream> \n #include <stack>\n using namespace std;\n int main() {\nstack<int> s; \n s.pop(); \n return 0;",
    "#include <iostream> \n #include <queue> \n using namespace std; \nint main() {\n queue<int> q; \nq.push(10);\n q.push(20);\n q.push(30);\n cout << q.back() << endl;\n q.pop();\n cout << q.front() << endl;\n q.pop();q.pop();\n cout << q.front() << endl;\nreturn 0;}"
]
answers_cpp1 = [
    ["Linia 5", "Linia 2", "Linia 3", "Nicio eroare"],
    ["Linia 4", "Linia 5", "Linia 3", "Nicio eroare"],
    ["Linia 1", "Linia 2", "Linia 3", "E bun, dar poate fi imbunatatit"],
    ["Linia 2", "Linia 5", "Linia 8", "Nicio eroare"],
    ["Linia 6", "Linia 2", "Linia 8", "Nicio eroare"],
    ["Linia 5", "Linia 2", "Linia 6", "Nicio eroare"],
    ["Linia 14", "Linia 2", "Linia 9", "Nicio eroare"]
]
questions_python_c = [
    "În ce linie apare eroarea de indentare?",
    "Unde este eroarea?",
    "Pe ce linie se află eroarea?",
    "Unde este eroarea de import?",
    "Pe ce linie este eroarea de index?",
    "Unde este eroarea de sintaxă?",
    "Pe ce linie este eroarea?"
]

code_samples_python_c = [
    "def my_function():\nprint('Hello!')\n  print('Indentation Error!')",
    'data = {"name": "Alice", "age": 25} \nprint(data["city"])',
    "stack = [] \n stack.append(3) \nstack.append(5) \nstack.pop(1) \nprint(stack)",
    "import non_existent_module\nprint('This should fail')",
    "my_list = [1, 2, 3]\nprint(my_list[5])",
    'class Animal: \ndef __init__(self, name): \nself.name = name \ndef speak(): \nprint("Sunet necunoscut!")\ndog = Animal("Rex") \ndog.speak()',
    'class Parent: \ndef __init__(self):\n print("Parent initialized") \nclass Child(Parent): \ndef __init__(self): \nprint("Child initialized") \nobj = Child()'
]

answers_python_c = [
    ["Linia 2", "Linia 3", "Linia 1", "Nicio eroare"],
    ["Linia 1", "Linia 2", "Tot", "Nicio eroare"],
    ["Linia 1", "Linia 4", "Linia 3", "Nicio eroare"],
    ["Linia 1", "Linia 2", "Linia 3", "Nicio eroare"],
    ["Linia 2", "Linia 3", "Linia 1", "Nicio eroare"],
    ["Linia 1", "Linia 2", "Linia 4", "Nicio eroare"],
    ["Linia 4", "Linia 5", "Linia 3", "Nicio eroare"]
]

correct_answers_python_c = [
    "Linia 2",
    "Linia 2",
    "Linia 4",
    "Linia 1",
    "Linia 2",
    "Linia 4",
    "Linia 5"
]
questions_javascript_error = [
    "Unde este eroarea de sintaxă?",
    "În ce linie apare eroarea de tip?",
    "Unde se află eroarea de referință?",
    "Pe ce linie se află eroarea de index?",
    "Unde apare eroarea de funcție nedefinită?",
    "Pe ce linie este eroarea de acces la obiect?",
    "În ce linie este eroarea de scoping?"
]

code_samples_javascript_error = [
    "console.log('Hello World'\nconsole.log('JS Error')",   # Lipsă paranteză închidere
    "let x = 'text' + 5;\nconsole.log(x);",                # Concatenare greșită
    "console.log(y);\nlet y = 10;",                         # Variabilă folosită înainte de declarare
    "let array = [1, 2, 3];\nconsole.log(array[5]);",       # Acces invalid la index
    "myFunction();\nfunction notDeclared() { \nconsole.log('Error') }",  # Apelare înainte de definire
    "let obj = { name: 'Alice' };\nconsole.log(obj.age.length);",      # Acces invalid la proprietăți
    "function test() {\n    let x = 10;\n}\nconsole.log(x);"  # Variabilă în afara scoping-ului funcției
]

answers_javascript_error = [
    ["Linia 2", "Linia 1", "Linia 3", "Nicio eroare"],
    ["Linia 1", "Linia 2", "Linia 3", "Nicio eroare"],
    ["Linia 3", "Linia 2", "Linia 1", "Nicio eroare"],
    ["Linia 2", "Linia 3", "Linia 1", "Nicio eroare"],
    ["Linia 1", "Linia 2", "Linia 3", "Nicio eroare"],
    ["Linia 1", "Linia 2", "Linia 3", "Nicio eroare"],
    ["Linia 1", "Linia 2", "Linia 3", "Nicio eroare"]
]

correct_answers_javascript_error = [
    "Linia 1",
    "Linia 1",
    "Linia 1",
    "Linia 2",
    "Linia 1",
    "Linia 2",
    "Linia 3"
]

class Image2Screen(Screen):
    def __init__(self, image_path, next_screen, question_data, **kwargs):
        super().__init__(**kwargs)
        self.next_screen = next_screen
        self.question_data = question_data

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.add_widget(layout)

        if os.path.exists(image_path):
            img = Image(source=image_path, allow_stretch=True, keep_ratio=True)
            layout.add_widget(img)
        else:
            layout.add_widget(Label(text="Imaginea nu a fost găsită."))

        continue_btn = Button(text="Continuă", size_hint=(0.4, 0.1), pos_hint={"center_x": 0.5})
        continue_btn.bind(on_press=self.go_next)
        layout.add_widget(continue_btn)

    def go_next(self, *args):
        if self.manager.has_screen(self.next_screen):
            self.manager.current = self.next_screen
        else:
            print(f"Eroare: ecranul '{self.next_screen}' nu este înregistrat în ScreenManager.")
        self.manager.remove_widget(self)
# Screen to display the question and handle answers
user_progress ={}
class QuestionScreen(Screen):
    def __init__(self, question_data, **kwargs):
        super().__init__(**kwargs)
        self.question_data = question_data
        self.buttons = []
        # În handle_answer, în loc să creezi din nou:
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        q_label = Label(text=question_data['question'], font_size=22, size_hint_y=0.2)
        layout.add_widget(q_label)

        for answer in question_data['answers']:
            btn = Button(text=answer, size_hint_y=None, height=60)
            btn.bind(on_press=lambda instance, a=answer, b=btn: self.handle_answer(a, b))
            layout.add_widget(btn)
            self.buttons.append(btn)

        back_btn = Button(text="Undo", size_hint_y=None, height=50)
        back_btn.bind(on_press=lambda x: setattr(self.manager, "current", "options_screen"))
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def handle_answer(self, selected, button):
        for b in self.buttons:
            b.disabled = True

        correct = self.question_data['correct']
        planet = self.question_data['planet']
        option = self.question_data['option']

        if selected == correct:
         button.background_color = (0, 1, 0, 1)
         user_progress.setdefault(option, {}).setdefault(planet, 0)
         user_progress[option][planet] += 1
         image_path = r"videos/WhatsApp Image 2025-07-02 at 21.05.19_cbdddd93.png"
        else:
         button.background_color = (1, 0, 0, 1)
         image_path = r"videos/WhatsApp Image 2025-07-02 at 21.05.16_69541a07.png"

         save_progress()

# Tranziție către ecranul cu imagine
        image_screen = Image2Screen(image_path, 'options_screen', self.question_data, name='feedback_image')
        self.manager.add_widget(image_screen)
        self.manager.current = 'feedback_image'

def save_progress():
    global user_progress

    print("Progres salvat:", user_progress)

    active = load_active_user()
    username = active.get("username")
    if not username:
        print("❌ Niciun utilizator activ!")
        return

    all_users = load_user_credentials()
    if username in all_users:
        all_users[username]["progress"] = user_progress
        with open("user_credentials.json", "w") as f:
            json.dump(all_users, f, indent=4)
        print(f"✅ Progres salvat pentru: {username}")
    else:
        print(f"❌ Utilizatorul {username} nu există în baza de date.")
def show_progress_kivy():
    global user_progress
    progress_message = "Progresul tău:\n"
    for option, planets in user_progress.items():
        progress_message += f"\n{option}:\n"
        for planet, correct_count in planets.items():
            progress_message += f"  {planet}: {correct_count} întrebări corecte\n"

    # Conținutul popupului
    content = BoxLayout(orientation='vertical', padding=20, spacing=10)
    label = Label(text=progress_message, halign="left", valign="top", color=(1, 1, 1, 1))
    label.bind(size=label.setter('text_size'))  # pentru wrap la text

    close_button = Button(text="Închide", size_hint=(1, None), height=40)
    content.add_widget(label)
    content.add_widget(close_button)

    # Popup-ul propriu-zis
    popup = Popup(title="Progres",
                  content=content,
                  size_hint=(0.8, 0.8),
                  background_color=(0, 0.137, 0.4, 1),  # echivalentul "#002366"
                  title_color=(1, 1, 1, 1),
                  auto_dismiss=False)

    close_button.bind(on_release=popup.dismiss)
    popup.open()

def show_leaderboard():
    total_correct = sum(c for planets in user_progress.values() for c in planets.values())
    if total_correct >= 21:
        award = "🏆 Aur"
    elif total_correct >= 14:
        award = "🥈 Argint"
    elif total_correct >= 7:
        award = "🥉 Bronz"
    else:
        award = "🔹 Fără medalie - mai încearcă!"

    message = f"Premiul tău: {award}\nAi răspuns corect la {total_correct} întrebări!"

    content = BoxLayout(orientation='vertical', padding=20, spacing=10)
    label = Label(text=message, color=(1, 1, 1, 1), halign='center')
    label.bind(size=label.setter('text_size'))
    close_btn = Button(text="Închide", size_hint=(1, None), height=40)
    content.add_widget(label)
    content.add_widget(close_btn)

    popup = Popup(title="Leaderboard",
                  content=content,
                  size_hint=(0.8, 0.5),
                  background_color=(0, 0.137, 0.4, 1),
                  title_color=(1, 1, 1, 1),
                  auto_dismiss=False)
    close_btn.bind(on_release=popup.dismiss)
    popup.open()
def open_profile_popup():
    session = load_active_user()

    layout = BoxLayout(orientation='vertical', spacing=15, padding=20)
    title = Label(text="Profile", font_size=24)
    layout.add_widget(title)

    image_path = session.get("profile_picture", "")
    if image_path and os.path.exists(image_path):
        try:
            pil_image = PILImage.open(image_path).convert("RGBA")
            size = min(pil_image.size)
            mask = PILImage.new('L', (size, size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size, size), fill=255)
            cropped = pil_image.crop((0, 0, size, size))
            cropped.putalpha(mask)
            cropped = cropped.resize((100, 100))

            img_data = cropped.tobytes()
            texture = Texture.create(size=cropped.size, colorfmt='rgba')
            texture.blit_buffer(img_data, colorfmt='rgba', bufferfmt='ubyte')

            img_widget = KivyImage(texture=texture, size_hint=(None, None), size=(100, 100))
            layout.add_widget(img_widget)
        except Exception as e:
            layout.add_widget(Label(text=f"⚠️ Eroare la poză: {e}"))
    else:
        layout.add_widget(Label(text="(Nicio poză de profil selectată)"))

    layout.add_widget(Label(text=f"Username: {session.get('username', '(necunoscut)')}", font_size=18))
    layout.add_widget(Label(text=f"E-mail: {session.get('email', '(necunoscut)')}", font_size=18))

    close_btn = Button(text="Închide", size_hint=(1, None), height=40)
    popup = Popup(title="Profil", content=layout, size_hint=(0.8, 0.8), auto_dismiss=False)
    close_btn.bind(on_release=popup.dismiss)
    layout.add_widget(close_btn)

    popup.open()

class RankingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)
        layout.add_widget(Label(text="🏆 Clasament Utilizatori", font_size=24))

        user_data = load_user_credentials()
        active = load_active_user()
        active_username = active.get("username")

        ranked_users = []

        for username, data in user_data.items():
            progress = data.get("progress", {})  # tip: {'Python': {'Venus': 2, 'Saturn': 1}, ...}
            total_score = 0
            for planet_data in progress.values():  # parcurge fiecare limbaj (Python, C++)
                total_score += sum(planet_data.values())
            ranked_users.append((username, data.get("email", ""), total_score))

        # sortează descrescător după punctaj
        ranked_users.sort(key=lambda x: x[2], reverse=True)

        for idx, (username, email, score) in enumerate(ranked_users, start=1):
            label = Label(text=f"{idx}. {username} — {score} puncte", font_size=18)
            if username == active_username:
                label.color = (1, 0.84, 0, 1)  # evidențiază utilizatorul activ cu galben
            layout.add_widget(label)

        back_btn = Button(text="Înapoi", size_hint=(0.3, 0.1))
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = "main_screen"

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        app = App.get_running_app()
        self.session = UserSession()
        self.session.load()
        sm = ScreenManager(transition=FadeTransition())
        self.user_input = ""          # va fi setat din LoginScreen
        self.user_mail = ""
        self.user_data = {}   
        self.cale_imagine_selectata = "" 
        sm.add_widget(WelcomeScreen(name="welcome_screen"))
        sm.add_widget(ImageScreen(name="image_screen"))
        sm.add_widget(GridScreen(name="grid_screen"))
        sm.add_widget(OptionsScreen(planet_name="Uranus", selected_option="Python", name="options_screen"))
        sm.add_widget(OptionsScreen(planet_name="Venus", selected_option="Python", name="options_screen"))
        sm.add_widget(OptionsScreen(planet_name="Saturn", selected_option="Python", name="options_screen"))
  # or whatever your class is
        sm.add_widget(OptionsScreen(planet_name="Uranus", selected_option="C++", name="options_screen"))
        sm.add_widget(OptionsScreen(planet_name="Venus", selected_option="C++", name="options_screen"))
        sm.add_widget(OptionsScreen(planet_name="Saturn", selected_option="C++", name="options_screen"))
        sm.add_widget(OptionsScreen(planet_name="Uranus", selected_option="JavaScript", name="options_screen"))
        sm.add_widget(OptionsScreen(planet_name="Venus", selected_option="JavaScript", name="options_screen"))
        sm.add_widget(OptionsScreen(planet_name="Saturn", selected_option="JavaScript", name="options_screen"))
        
        sm.add_widget(LoginScreen(name="login_screen"))
        sm.add_widget(MainScreen(name="main_screen"))
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(SettingsScreen(name="settings_screen"))
        sm.add_widget(RankingScreen(name="ranking_screen"))
        sm.current = "welcome_screen"
        return sm

MyApp().run()
