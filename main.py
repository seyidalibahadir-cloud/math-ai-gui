import customtkinter as ctk
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

# Modern Koyu Tema
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MathAIChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Windows Pencere Ayarları
        self.title("Math AI — Matematik Sohbet Asistanı")
        self.geometry("650x750")

        # SymPy Ayarları
        self.x, self.y, self.z = sp.symbols('x y z')
        self.transformations = (standard_transformations + (implicit_multiplication_application,))

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Başlık Paneli
        self.header_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1e1e2e")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="🧮 Math AI Assistant", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#89b4fa"
        )
        self.title_label.pack(pady=12)

        # Sohbet Ekranı
        self.chat_frame = ctk.CTkScrollableFrame(self, corner_radius=15, fg_color="#181825")
        self.chat_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # Karşılama Mesajı
        self.add_bot_message(
            "Selam! Ben senin matematik yapay zekâ asistanınım. 🤖✨\n"
            "Bana çözmemi istediğin denklemi yazabilirsin.\n\n"
            "Örnekler:\n"
            "• 3x + 2 = 11\n"
            "• x^2 - 5x + 6 = 0\n"
            "• diff(x^3 + 2x, x)"
        )

        # Girdi Paneli
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="Matematiksel bir ifade veya denklem yazın...",
            font=ctk.CTkFont(size=14),
            height=45,
            corner_radius=10
        )
        self.entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.entry.bind("<Return>", lambda event: self.send_message())

        self.send_btn = ctk.CTkButton(
            self.input_frame, 
            text="Gönder 🚀", 
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            corner_radius=10,
            command=self.send_message
        )
        self.send_btn.grid(row=0, column=1)

    def add_user_message(self, text):
        msg_box = ctk.CTkTextbox(
            self.chat_frame, font=ctk.CTkFont(size=13), 
            fg_color="#313244", text_color="#cdd6f4", corner_radius=12, wrap="word", height=50
        )
        msg_box.pack(anchor="e", padx=10, pady=5, fill="x")
        msg_box.insert("1.0", f"Sen: {text}")
        msg_box.configure(state="disabled")

    def add_bot_message(self, text):
        msg_box = ctk.CTkTextbox(
            self.chat_frame, font=ctk.CTkFont(size=13), 
            fg_color="#1e1e2e", text_color="#a6e3a1", corner_radius=12, wrap="word", height=90
        )
        msg_box.pack(anchor="w", padx=10, pady=5, fill="x")
        msg_box.insert("1.0", f"Math AI:\n{text}")
        msg_box.configure(state="disabled")

    def send_message(self):
        query = self.entry.get().strip()
        if not query:
            return

        self.add_user_message(query)
        self.entry.delete(0, "end")

        response = self.process_math(query)
        self.add_bot_message(response)

    def process_math(self, query):
        query_fixed = query.replace("^", "**")

        try:
            if "=" in query_fixed:
                sol_str, sag_str = query_fixed.split("=")
                sol = parse_expr(sol_str, transformations=self.transformations)
                sag = parse_expr(sag_str, transformations=self.transformations)
                
                denklem = sp.Eq(sol, sag)
                cozum = sp.solve(denklem)
                return f"Bu denklemin çözümü: {cozum}"
            
            elif query_fixed.startswith("diff"):
                ic_ifade = query_fixed[5:-1]
                parcalar = ic_ifade.split(",")
                expr = parse_expr(parcalar[0], transformations=self.transformations)
                var = sp.Symbol(parcalar[1].strip())
                sonuc = sp.diff(expr, var)
                return f"Türev sonucu: {sonuc}"
            
            else:
                expr = parse_expr(query_fixed, transformations=self.transformations)
                sade = sp.simplify(expr)
                if expr == sade:
                    return f"Sonuç: {expr}"
                return f"Sonuç: {expr}\nSadeleşmiş Hali: {sade}"

        except Exception as e:
            return f"Bunu tam anlayamadım dostum. İfadeyi kontrol edebilir misin?\n(Hata: {e})"

if __name__ == "__main__":
    app = MathAIChatApp()
    app.mainloop()
