import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
from customtkinter import CTkImage
from datetime import datetime

from src.core.encryption import generate_key, encrypt_message, decrypt_message, save_key
from src.core.steganography import encode_message, decode_message


class SteganoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🕶️ Stegano Tool - Secure Key Edition")
        self.geometry("940x640")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.image_path = None
        self.preview_ctk_image = None

        os.makedirs("data/output", exist_ok=True)
        os.makedirs("data/secret", exist_ok=True)

        self.create_ui()

    def create_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="#0F172A", height=60, corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(
            header, text="🕵️‍♂️ Stegano Tool", font=("Segoe UI", 22, "bold"), text_color="#38BDF8"
        ).pack(side="left", padx=20, pady=10)
        ctk.CTkLabel(
            header, text="Secure Key Edition", font=("Consolas", 13, "italic"), text_color="#94A3B8"
        ).pack(side="left", padx=(0, 12), pady=10)

        # Main layout
        main_frame = ctk.CTkFrame(self, fg_color="#111827", corner_radius=12)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        main_frame.grid_columnconfigure((0, 1), weight=1)

        # LEFT COLUMN
        self.preview_card = ctk.CTkFrame(main_frame, fg_color="#1E293B", corner_radius=12)
        self.preview_card.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        ctk.CTkLabel(
            self.preview_card, text="Preview Image", font=("Segoe UI", 15, "bold"), text_color="#38BDF8"
        ).pack(pady=(12, 8))
        self.preview_label = ctk.CTkLabel(
            self.preview_card,
            text="No image selected",
            width=380,
            height=300,
            fg_color="#0F172A",
            corner_radius=10,
            anchor="center",
        )
        self.preview_label.pack(padx=12, pady=8)
        self.select_btn = ctk.CTkButton(
            self.preview_card,
            text="📂 Select Image",
            command=self.select_image,
            width=180,
            height=38,
            fg_color="#2563EB",
            hover_color="#1E40AF",
        )
        self.select_btn.pack(pady=10)

        # RIGHT COLUMN
        control_frame = ctk.CTkFrame(main_frame, fg_color="#1E293B", corner_radius=12)
        control_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        ctk.CTkLabel(
            control_frame, text="💬 Secret Message", font=("Segoe UI", 15, "bold"), text_color="#38BDF8"
        ).pack(pady=(12, 8))

        self.message_entry = ctk.CTkTextbox(control_frame, width=400, height=150, corner_radius=10)
        self.message_entry.pack(pady=8)

        # INPUT KEY AREA (for extraction)
        ctk.CTkLabel(
            control_frame, text="🔑 Enter Key for Decryption", font=("Segoe UI", 13, "bold"), text_color="#38BDF8"
        ).pack(pady=(10, 5))
        self.key_entry = ctk.CTkEntry(control_frame, width=400, placeholder_text="Paste your key here...")
        self.key_entry.pack(pady=5)

        # Buttons
        btn_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        btn_frame.pack(pady=10)

        self.embed_btn = ctk.CTkButton(
            btn_frame,
            text="🔒 Embed Message",
            command=self.embed_message,
            width=160,
            height=38,
            fg_color="#10B981",
            hover_color="#059669",
        )
        self.embed_btn.grid(row=0, column=0, padx=10)

        self.extract_btn = ctk.CTkButton(
            btn_frame,
            text="🔓 Extract Message",
            command=self.extract_message,
            width=160,
            height=38,
            fg_color="#F59E0B",
            hover_color="#B45309",
        )
        self.extract_btn.grid(row=0, column=1, padx=10)

        self.reset_btn = ctk.CTkButton(
            control_frame,
            text="♻️ Reset",
            command=self.reset_ui,
            width=150,
            height=36,
            fg_color="#475569",
            hover_color="#334155",
        )
        self.reset_btn.pack(pady=12)

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.bmp")])
        if not file_path:
            return
        try:
            with Image.open(file_path) as img:
                img = img.copy()
                img.thumbnail((380, 300))
            ctk_img = CTkImage(light_image=img, size=img.size)
            self.preview_ctk_image = ctk_img
            self.preview_label.configure(image=self.preview_ctk_image, text="")
            self.preview_label.image = ctk_img
            self.image_path = file_path
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image:\n{e}")

    def embed_message(self):
        if not self.image_path:
            messagebox.showwarning("⚠️ Warning", "Please select an image first.")
            return

        message = self.message_entry.get("0.0", "end").strip()
        if not message:
            messagebox.showwarning("⚠️ Warning", "Please enter a secret message.")
            return

        try:
            # ambil nama dasar dari file (tanpa ekstensi)
            base_name = os.path.splitext(os.path.basename(self.image_path))[0]

            # output file = data/output/gambar1.png
            output_img = os.path.join("data/output", f"{base_name}.png")

            # generate key + enkripsi pesan
            key = generate_key()
            key_str = key.decode()
            encrypted = encrypt_message(message, key)

            # encode pesan ke gambar output
            encode_message(self.image_path, output_img, encrypted.decode())

            # simpan key dengan nama data/secret/key_gambar1.key
            key_filename = os.path.join("data/secret", f"key_{base_name}.key")
            save_key(key, key_filename)

            # Pop-up window untuk menampilkan key
            popup = ctk.CTkToplevel(self)
            popup.title("🔑 Secret Key")
            popup.geometry("580x280")
            popup.grab_set()
            popup.focus()

            ctk.CTkLabel(
                popup, text="✅ Message Embedded Successfully!", font=("Segoe UI", 16, "bold"), text_color="#10B981"
            ).pack(pady=(15, 5))

            ctk.CTkLabel(
                popup, text=f"Saved to:\n{output_img}", font=("Consolas", 12), text_color="#94A3B8"
            ).pack(pady=(0, 10))

            ctk.CTkLabel(
                popup, text="Your Secret Key:", font=("Segoe UI", 14, "bold"), text_color="#38BDF8"
            ).pack(pady=(10, 5))

            key_box = ctk.CTkTextbox(popup, width=520, height=80, corner_radius=8)
            key_box.pack(pady=(0, 10))
            key_box.insert("0.0", key_str)
            key_box.configure(state="disabled")

            def copy_key():
                self.clipboard_clear()
                self.clipboard_append(key_str)
                messagebox.showinfo("📋 Copied", "Key copied to clipboard!")

            ctk.CTkButton(
                popup, text="📋 Copy Key", command=copy_key, width=150, fg_color="#2563EB", hover_color="#1E40AF"
            ).pack(pady=8)

            ctk.CTkButton(
                popup, text="Close", command=popup.destroy, width=100, fg_color="#475569", hover_color="#334155"
            ).pack(pady=(5, 15))

            self.reset_ui()

        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to embed message:\n{e}")

    def extract_message(self):
        if not self.image_path:
            messagebox.showwarning("⚠️ Warning", "Please select an image first.")
            return

        key_input = self.key_entry.get().strip()
        if not key_input:
            messagebox.showwarning("⚠️ Warning", "Please enter the decryption key.")
            return

        try:
            hidden = decode_message(self.image_path)
            decrypted = decrypt_message(hidden.encode(), key_input.encode())
            self.message_entry.delete("0.0", "end")
            self.message_entry.insert("0.0", decrypted)
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to extract message:\nInvalid key or corrupted image.\n\nDetails: {e}")

    def reset_ui(self):
        self.message_entry.delete("0.0", "end")
        self.key_entry.delete(0, "end")
        self.preview_label.configure(image="", text="No image selected")
        self.preview_label.image = None
        self.preview_ctk_image = None
        self.image_path = None


if __name__ == "__main__":
    app = SteganoApp()
    app.mainloop()
