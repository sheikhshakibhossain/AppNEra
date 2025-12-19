#!/usr/bin/env python3

"""
AppNEra - A new era for web apps on Linux
Modern GUI for creating lightweight web app wrappers
"""

import os
import shutil
import subprocess
import threading
from pathlib import Path
from tkinter import filedialog
from typing import Optional

import customtkinter as ctk

# Color Palette
COLORS = {
    "bg_primary": "#1a1b26",
    "bg_secondary": "#24283b",
    "accent": "#7aa2f7",
    "success": "#9ece6a",
    "danger": "#f7768e",
    "text_primary": "#c0caf5",
    "text_secondary": "#565f89",
    "border": "#414868",
    "input_bg": "#1f2335",
}


class AppNEraGUI(ctk.CTk):
    """Main AppNEra application window"""

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("AppNEra")
        self.geometry("1500x950")
        # self.minsize(1200, 800)

        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configure colors
        self._configure_colors()

        # Font size multiplier (default 1.2 = Large)
        self.font_multiplier = 1.2
        self._load_settings()

        # Build UI
        self._create_header()
        self._create_tabview()

        # Track created apps
        self.apps_dir = Path.home() / ".local"
        
        # Loading overlay (initially hidden)
        self.loading_overlay = None

    def _configure_colors(self):
        """Configure custom color theme"""
        self.configure(fg_color=COLORS["bg_primary"])

    def _create_header(self):
        """Create the header section with title and tagline"""
        header_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_primary"], corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=(0, 24))

        title = ctk.CTkLabel(
            header_frame,
            text="AppNEra",
            font=("Ubuntu", int(28 * self.font_multiplier), "bold"),
            text_color=COLORS["accent"],
        )
        title.pack(pady=(24, 4))

        tagline = ctk.CTkLabel(
            header_frame,
            text="A new era for web apps on Linux",
            font=("Ubuntu", int(13 * self.font_multiplier)),
            text_color=COLORS["text_secondary"],
        )
        tagline.pack(pady=(0, 16))

    def _create_tabview(self):
        """Create the main tabbed interface"""
        self.tabview = ctk.CTkTabview(
            self,
            fg_color=COLORS["bg_primary"],
            segmented_button_fg_color=COLORS["bg_secondary"],
            segmented_button_selected_color=COLORS["accent"],
            segmented_button_selected_hover_color=COLORS["accent"],
            segmented_button_unselected_color=COLORS["bg_secondary"],
            text_color=COLORS["text_primary"],
        )
        self.tabview.pack(fill="both", expand=True, padx=32, pady=(0, 32))
        
        # Configure tab label font size
        try:
            self.tabview._segmented_button.configure(font=("Ubuntu", int(13 * self.font_multiplier)))
        except:
            pass

        # Create tabs
        self.tabview.add("Create App")
        self.tabview.add("Manage Apps")
        self.tabview.add("Settings")
        self.tabview.add("Help")
        self.tabview.add("About")

        # Build tab contents
        self._build_create_tab()
        self._build_manage_tab()
        self._build_settings_tab()
        self._build_help_tab()
        self._build_about_tab()

    def _build_create_tab(self):
        """Build the Create App tab UI"""
        self._build_create_tab_content()
    
    def _build_create_tab_content(self):
        """Build the Create App tab content (separated for rebuilding)"""
        tab = self.tabview.tab("Create App")

        # Main card container
        card = ctk.CTkFrame(
            tab,
            fg_color=COLORS["bg_secondary"],
            corner_radius=12,
        )
        card.pack(fill="both", expand=True, padx=80, pady=24)

        # Form container
        form_frame = ctk.CTkFrame(card, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=32, pady=32)

        # App URL field
        url_label = ctk.CTkLabel(
            form_frame,
            text="Web App URL *",
            font=("Ubuntu", int(12 * self.font_multiplier), "bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        )
        url_label.pack(fill="x", pady=(0, 8))

        self.url_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="https://website.com/login",
            height=44,
            fg_color=COLORS["input_bg"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            placeholder_text_color=COLORS["text_secondary"],
            border_width=1,
            corner_radius=6,
            font=("Ubuntu", int(12 * self.font_multiplier)),
        )
        self.url_entry.pack(fill="x", pady=(0, 24))

        # App Name field
        name_label = ctk.CTkLabel(
            form_frame,
            text="App Name *",
            font=("Ubuntu", int(12 * self.font_multiplier), "bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        )
        name_label.pack(fill="x", pady=(0, 8))

        self.name_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Notion",
            height=44,
            fg_color=COLORS["input_bg"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            placeholder_text_color=COLORS["text_secondary"],
            border_width=1,
            corner_radius=6,
            font=("Ubuntu", int(12 * self.font_multiplier)),
        )
        self.name_entry.pack(fill="x", pady=(0, 24))

        # App Icon field (required)
        icon_label = ctk.CTkLabel(
            form_frame,
            text="App Icon *",
            font=("Ubuntu", int(12 * self.font_multiplier), "bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        )
        icon_label.pack(fill="x", pady=(0, 8))

        # Icon selection button
        self.selected_icon_path = None
        self.icon_btn = ctk.CTkButton(
            form_frame,
            text="🖼️  Select Icon",
            height=44,
            fg_color=COLORS["input_bg"],
            hover_color=COLORS["border"],
            border_color=COLORS["border"],
            border_width=1,
            text_color=COLORS["text_secondary"],
            anchor="w",
            command=self._select_icon,
        )
        self.icon_btn.pack(fill="x", pady=(0, 32))

        # Create button
        self.create_btn = ctk.CTkButton(
            form_frame,
            text="Create App",
            height=48,
            fg_color=COLORS["accent"],
            hover_color="#5a7fc7",
            text_color="white",
            font=("Ubuntu", int(14 * self.font_multiplier), "bold"),
            corner_radius=8,
            command=self._create_app,
        )
        self.create_btn.pack(fill="x", pady=(0, 16))

        # Status label
        self.status_label = ctk.CTkLabel(
            form_frame,
            text="",
            font=("Ubuntu", int(12 * self.font_multiplier)),
            text_color=COLORS["text_secondary"],
        )
        self.status_label.pack()

    def _build_manage_tab(self):
        """Build the Manage Apps tab UI"""
        self._build_manage_tab_content()
    
    def _build_manage_tab_content(self):
        """Build the Manage Apps tab content (separated for rebuilding)"""
        tab = self.tabview.tab("Manage Apps")

        # Container with two panels
        container = ctk.CTkFrame(tab, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=0, pady=0)

        # Left panel - Apps list
        left_panel = ctk.CTkFrame(
            container,
            fg_color=COLORS["bg_secondary"],
            corner_radius=12,
            width=300,
        )
        left_panel.pack(side="left", fill="both", padx=(0, 16), pady=0)
        left_panel.pack_propagate(False)

        list_title = ctk.CTkLabel(
            left_panel,
            text="Created Apps",
            font=("Ubuntu", int(16 * self.font_multiplier), "bold"),
            text_color=COLORS["text_primary"],
        )
        list_title.pack(pady=(16, 8), padx=16, anchor="w")

        # Scrollable apps list
        self.apps_list_frame = ctk.CTkScrollableFrame(
            left_panel,
            fg_color="transparent",
        )
        self.apps_list_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        # Right panel - App details
        self.right_panel = ctk.CTkFrame(
            container,
            fg_color=COLORS["bg_secondary"],
            corner_radius=12,
        )
        self.right_panel.pack(side="right", fill="both", expand=True, pady=0)

        # Empty state
        self.empty_state = ctk.CTkLabel(
            self.right_panel,
            text="No app selected\n\nSelect an app from the list\nor create your first app",
            font=("Ubuntu", int(14 * self.font_multiplier)),
            text_color=COLORS["text_secondary"],
            justify="center",
        )
        self.empty_state.pack(expand=True)

        # Refresh apps list
        self._refresh_apps_list()

    def _select_icon(self):
        """Open file dialog to select an icon"""
        filename = filedialog.askopenfilename(
            title="Select App Icon",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.svg *.ico"),
                ("All files", "*.*"),
            ],
        )
        if filename:
            self.selected_icon_path = filename
            # Update button to show selected file
            icon_name = Path(filename).name
            if len(icon_name) > 30:
                icon_name = icon_name[:27] + "..."
            self.icon_btn.configure(
                text=f"✓  {icon_name}",
                fg_color=COLORS["accent"],
                text_color="white",
            )

    def _create_app(self):
        """Handle app creation"""
        # Get values
        url = self.url_entry.get().strip()
        name = self.name_entry.get().strip()
        icon_path = self.selected_icon_path

        # Validate
        if not url:
            self._show_status("❌ Please enter a web app URL", COLORS["danger"])
            return

        if not name:
            self._show_status("❌ Please enter an app name", COLORS["danger"])
            return

        if not icon_path:
            self._show_status("❌ Please select an app icon", COLORS["danger"])
            return

        if not url.startswith(("http://", "https://")):
            self._show_status("❌ URL must start with http:// or https://", COLORS["danger"])
            return

        # Show loading overlay
        self._show_loading("Creating your app...")
        self.create_btn.configure(state="disabled")
        self.update()

        # Run app creation in a separate thread to keep UI responsive
        def build_thread():
            try:
                self._build_app(url, name, icon_path)
                
                # Schedule UI updates on main thread
                self.after(0, self._on_build_success)
                
            except Exception as e:
                # Schedule error handling on main thread
                self.after(0, lambda: self._on_build_error(str(e)))
        
        # Start the build process in background
        thread = threading.Thread(target=build_thread, daemon=True)
        thread.start()
    
    def _on_build_success(self):
        """Called on main thread when build succeeds"""
        self._hide_loading()
        self._show_status("✅ App created successfully!", COLORS["success"])
        
        # Clear form
        self.url_entry.delete(0, "end")
        self.name_entry.delete(0, "end")
        self.selected_icon_path = None
        self.icon_btn.configure(
            text="🖼️  Select Icon",
            fg_color=COLORS["input_bg"],
            text_color=COLORS["text_secondary"],
        )
        
        # Refresh manage tab
        self._refresh_apps_list()
        self.create_btn.configure(state="normal")
    
    def _on_build_error(self, error_msg: str):
        """Called on main thread when build fails"""
        self._hide_loading()
        self._show_status(f"❌ Error: {error_msg}", COLORS["danger"])
        self.create_btn.configure(state="normal")

    def _build_app(self, url: str, name: str, icon_path: Optional[str]):
        """Build the web app using the template"""
        app_id = name.lower().replace(" ", "-")
        app_dir = Path.home() / ".local" / name
        template_dir = Path(__file__).parent / "template"

        # Check if app already exists
        if app_dir.exists():
            raise ValueError(f"App '{name}' already exists")

        # Create app directory
        self.after(0, lambda: self._update_loading_message("Creating app directory..."))
        app_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Copy template files
            self.after(0, lambda: self._update_loading_message("Copying template files..."))
            shutil.copy(template_dir / "app.py", app_dir / "app.py")
            shutil.copy(template_dir / "uninstall.sh", app_dir / "uninstall.sh")
            os.chmod(app_dir / "uninstall.sh", 0o755)

            # Copy selected icon
            self.after(0, lambda: self._update_loading_message("Setting up icon..."))
            if not Path(icon_path).exists():
                raise ValueError("Selected icon file not found")
            shutil.copy(icon_path, app_dir / "icon.png")

            # Create isolated venv
            self.after(0, lambda: self._update_loading_message("Creating Python environment..."))
            subprocess.run(
                ["python3", "-m", "venv", str(app_dir / "venv")],
                check=True,
                capture_output=True,
            )

            # Install PyQt5 dependencies in venv (fully self-contained, no system packages needed)
            self.after(0, lambda: self._update_loading_message("Installing dependencies (this may take a moment)..."))
            pip_path = app_dir / "venv" / "bin" / "pip"
            subprocess.run(
                [str(pip_path), "install", "PyQt5", "PyQtWebEngine"],
                check=True,
                capture_output=True,
            )

            # Create launcher script
            self.after(0, lambda: self._update_loading_message("Creating launcher..."))
            launcher_path = app_dir / "run.sh"
            launcher_content = f"""#!/usr/bin/env bash
set -euo pipefail

export APPNERA_APP_NAME="{name}"
export APPNERA_APP_ID="{app_id}"
export APPNERA_URL="{url}"

exec "{app_dir / 'venv' / 'bin' / 'python'}" "{app_dir / 'app.py'}"
"""
            launcher_path.write_text(launcher_content)
            os.chmod(launcher_path, 0o755)

            # Create .desktop entry
            self.after(0, lambda: self._update_loading_message("Registering app..."))
            desktop_content = f"""[Desktop Entry]
Name={name}
Comment={name}
Exec={app_dir / 'run.sh'}
Icon={app_dir / 'icon.png'}
Terminal=false
Type=Application
Categories=Network;WebBrowser;
"""
            desktop_path = app_dir / f"{app_id}.desktop"
            desktop_path.write_text(desktop_content)

            # Link to user applications
            desktop_dir = Path.home() / ".local" / "share" / "applications"
            desktop_dir.mkdir(parents=True, exist_ok=True)
            desktop_link = desktop_dir / f"{app_id}.desktop"
            
            if desktop_link.exists():
                desktop_link.unlink()
            desktop_link.symlink_to(desktop_path)

            # Link icon
            icon_dir = Path.home() / ".local" / "share" / "icons"
            icon_dir.mkdir(parents=True, exist_ok=True)
            icon_link = icon_dir / f"{app_id}.png"
            
            if icon_link.exists():
                icon_link.unlink()
            icon_link.symlink_to(app_dir / "icon.png")
            
            self.after(0, lambda: self._update_loading_message("Finalizing..."))

        except Exception as e:
            # Cleanup on failure
            if app_dir.exists():
                shutil.rmtree(app_dir)
            raise e

    def _build_settings_tab(self):
        """Build the Settings tab"""
        tab = self.tabview.tab("Settings")

        # Main card container
        card = ctk.CTkFrame(
            tab,
            fg_color=COLORS["bg_secondary"],
            corner_radius=12,
        )
        card.pack(fill="both", expand=True, padx=80, pady=24)

        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=32, pady=32)

        # Title
        title = ctk.CTkLabel(
            content_frame,
            text="Settings",
            font=("Ubuntu", int(24 * self.font_multiplier), "bold"),
            text_color=COLORS["accent"],
            anchor="w",
        )
        title.pack(anchor="w", pady=(0, 24))

        # Font Size Section
        font_section = ctk.CTkFrame(
            content_frame,
            fg_color=COLORS["input_bg"],
            corner_radius=8,
        )
        font_section.pack(fill="x", pady=(0, 16))

        font_title = ctk.CTkLabel(
            font_section,
            text="Font Size",
            font=("Ubuntu", int(16 * self.font_multiplier), "bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        )
        font_title.pack(anchor="w", padx=16, pady=(16, 8))

        font_desc = ctk.CTkLabel(
            font_section,
            text="Adjust the font size for better readability",
            font=("Ubuntu", int(12 * self.font_multiplier)),
            text_color=COLORS["text_secondary"],
            anchor="w",
        )
        font_desc.pack(anchor="w", padx=16, pady=(0, 12))

        # Slider container
        slider_frame = ctk.CTkFrame(font_section, fg_color="transparent")
        slider_frame.pack(fill="x", padx=16, pady=(0, 16))

        # Current size label
        self.font_size_label = ctk.CTkLabel(
            slider_frame,
            text=f"Size: {int(self.font_multiplier * 100)}%",
            font=("Ubuntu", int(12 * self.font_multiplier), "bold"),
            text_color=COLORS["accent"],
            width=100,
        )
        self.font_size_label.pack(side="right", padx=(16, 0))

        # Font size slider
        self.font_slider = ctk.CTkSlider(
            slider_frame,
            from_=0.8,
            to=1.5,
            number_of_steps=14,
            command=self._on_font_size_change,
            fg_color=COLORS["border"],
            progress_color=COLORS["accent"],
            button_color=COLORS["accent"],
            button_hover_color="#5a7fc7",
        )
        self.font_slider.set(self.font_multiplier)
        self.font_slider.pack(side="left", fill="x", expand=True)

        # Preset buttons
        preset_frame = ctk.CTkFrame(font_section, fg_color="transparent")
        preset_frame.pack(fill="x", padx=16, pady=(0, 16))

        preset_label = ctk.CTkLabel(
            preset_frame,
            text="Quick presets:",
            font=("Ubuntu", int(11 * self.font_multiplier)),
            text_color=COLORS["text_secondary"],
        )
        preset_label.pack(side="left", padx=(0, 8))

        for label, value in [("Small", 0.9), ("Normal", 1.0), ("Large", 1.2), ("Extra Large", 1.4)]:
            btn = ctk.CTkButton(
                preset_frame,
                text=label,
                width=80,
                height=28,
                fg_color=COLORS["bg_secondary"],
                hover_color=COLORS["border"],
                text_color=COLORS["text_primary"],
                font=("Ubuntu", int(11 * self.font_multiplier)),
                command=lambda v=value: self._set_font_size(v),
            )
            btn.pack(side="left", padx=4)

        # Info note
        info_frame = ctk.CTkFrame(
            content_frame,
            fg_color=COLORS["border"],
            corner_radius=8,
        )
        info_frame.pack(fill="x", pady=(16, 0))

        ctk.CTkLabel(
            info_frame,
            text="💡 Note: Font size changes are saved automatically and will persist across sessions.",
            font=("Ubuntu", int(12 * self.font_multiplier)),
            text_color=COLORS["text_secondary"],
            anchor="w",
            wraplength=600,
        ).pack(anchor="w", padx=16, pady=12)

    def _on_font_size_change(self, value):
        """Handle font size slider change"""
        self.font_multiplier = value
        self.font_size_label.configure(text=f"Size: {int(value * 100)}%")
        self._save_settings()
        self._apply_font_changes()
        
    def _set_font_size(self, value):
        """Set font size to a specific value"""
        self.font_multiplier = value
        self.font_slider.set(value)
        self.font_size_label.configure(text=f"Size: {int(value * 100)}%")
        self._save_settings()
        self._apply_font_changes()
    
    def _apply_font_changes(self):
        """Apply font size changes to all tabs by rebuilding them"""
        # Remember current tab
        current_tab = self.tabview.get()
        
        # Rebuild header
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget != self.tabview and widget != self.loading_overlay:
                widget.destroy()
                break
        self._create_header()
        
        # Destroy and recreate entire tabview to apply font size to tab labels
        if hasattr(self, 'tabview'):
            self.tabview.destroy()
        
        self._create_tabview()
        
        # Restore current tab
        try:
            self.tabview.set(current_tab)
        except:
            pass
    
    def _load_settings(self):
        """Load settings from config file"""
        config_file = Path.home() / ".config" / "appnera" / "settings.conf"
        try:
            if config_file.exists():
                with open(config_file, "r") as f:
                    for line in f:
                        if line.startswith("font_multiplier="):
                            self.font_multiplier = float(line.split("=")[1].strip())
        except Exception:
            pass
    
    def _save_settings(self):
        """Save settings to config file"""
        config_dir = Path.home() / ".config" / "appnera"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / "settings.conf"
        
        try:
            with open(config_file, "w") as f:
                f.write(f"font_multiplier={self.font_multiplier}\n")
        except Exception:
            pass

    def _refresh_apps_list(self):
        """Refresh the list of created apps"""
        # Clear existing list
        for widget in self.apps_list_frame.winfo_children():
            widget.destroy()

        # Find all apps
        apps = self._get_created_apps()

        if not apps:
            empty_label = ctk.CTkLabel(
                self.apps_list_frame,
                text="No apps created yet\n\nGo to Create App tab\nto build your first app",
                font=("Ubuntu", int(12 * self.font_multiplier)),
                text_color=COLORS["text_secondary"],
                justify="center",
            )
            empty_label.pack(pady=32)
            return

        # Display apps
        for app in apps:
            # Create a frame for each app item
            app_frame = ctk.CTkFrame(
                self.apps_list_frame,
                fg_color="transparent",
            )
            app_frame.pack(fill="x", pady=2, padx=4)
            
            # Try to load and display the app icon
            icon_image = None
            try:
                from PIL import Image
                icon_path = app["path"] / "icon.png"
                if icon_path.exists():
                    img = Image.open(icon_path)
                    img = img.resize((32, 32), Image.Resampling.LANCZOS)
                    icon_image = ctk.CTkImage(light_image=img, dark_image=img, size=(32, 32))
            except Exception:
                pass
            
            # Create button with icon and text
            app_btn = ctk.CTkButton(
                app_frame,
                text=f"  {app['name']}" if icon_image else app["name"],
                image=icon_image if icon_image else None,
                compound="left",
                height=48,
                anchor="w",
                fg_color="transparent",
                hover_color=COLORS["input_bg"],
                text_color=COLORS["text_primary"],
                font=("Ubuntu", int(13 * self.font_multiplier)),
                command=lambda a=app: self._show_app_details(a),
            )
            app_btn.pack(fill="x")
            
            # Keep reference to prevent garbage collection
            if icon_image:
                app_btn.icon_image = icon_image

    def _get_created_apps(self) -> list:
        """Get list of created apps"""
        apps = []
        local_dir = Path.home() / ".local"

        if not local_dir.exists():
            return apps

        for item in local_dir.iterdir():
            if item.is_dir() and (item / "app.py").exists() and (item / "run.sh").exists():
                apps.append({
                    "name": item.name,
                    "path": item,
                    "id": item.name.lower().replace(" ", "-"),
                })

        return sorted(apps, key=lambda x: x["name"])

    def _show_app_details(self, app: dict):
        """Show details for selected app"""
        # Clear right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()

        details_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        details_frame.pack(fill="both", expand=True, padx=24, pady=24)

        # Top section with icon and name
        header_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        header_frame.pack(anchor="w", pady=(0, 16), fill="x")
        
        # App icon (larger version)
        try:
            from PIL import Image
            icon_path = app["path"] / "icon.png"
            if icon_path.exists():
                img = Image.open(icon_path)
                img = img.resize((64, 64), Image.Resampling.LANCZOS)
                icon_image = ctk.CTkImage(light_image=img, dark_image=img, size=(64, 64))
                
                icon_label = ctk.CTkLabel(
                    header_frame,
                    image=icon_image,
                    text="",
                )
                icon_label.pack(side="left", padx=(0, 16))
                icon_label.icon_image = icon_image  # Keep reference
        except Exception:
            pass
        
        # App name next to icon
        name_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        name_container.pack(side="left", fill="both", expand=True)
        
        name_label = ctk.CTkLabel(
            name_container,
            text=app["name"],
            font=("Ubuntu", int(24 * self.font_multiplier), "bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        )
        name_label.pack(anchor="w")

        # App path
        path_label = ctk.CTkLabel(
            details_frame,
            text=f"Location: {app['path']}",
            font=("Ubuntu", int(12 * self.font_multiplier)),
            text_color=COLORS["text_secondary"],
            anchor="w",
        )
        path_label.pack(anchor="w", pady=4)

        # Calculate size
        total_size = sum(f.stat().st_size for f in app["path"].rglob("*") if f.is_file())
        size_mb = total_size / (1024 * 1024)
        size_label = ctk.CTkLabel(
            details_frame,
            text=f"Size: {size_mb:.1f} MB",
            font=("Ubuntu", int(12 * self.font_multiplier)),
            text_color=COLORS["text_secondary"],
            anchor="w",
        )
        size_label.pack(anchor="w", pady=4)

        # Spacer
        ctk.CTkFrame(details_frame, fg_color="transparent", height=32).pack()

        # Uninstall button
        uninstall_btn = ctk.CTkButton(
            details_frame,
            text="🗑️  Uninstall App",
            height=48,
            fg_color=COLORS["danger"],
            hover_color="#c75a6f",
            text_color="white",
            font=("Ubuntu", int(14 * self.font_multiplier), "bold"),
            corner_radius=8,
            command=lambda: self._uninstall_app(app),
        )
        uninstall_btn.pack(fill="x", pady=(16, 0))

    def _uninstall_app(self, app: dict):
        """Uninstall an app"""
        # Confirm dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirm Uninstall")
        dialog.geometry("400x200")
        dialog.transient(self)
        
        # Wait for window to be viewable before grabbing focus
        dialog.after(100, dialog.grab_set)

        ctk.CTkLabel(
            dialog,
            text=f"Uninstall {app['name']}?",
            font=("Ubuntu", int(16 * self.font_multiplier), "bold"),
        ).pack(pady=(24, 8))

        ctk.CTkLabel(
            dialog,
            text="This will remove all app data\nand cannot be undone.",
            font=("Ubuntu", int(12 * self.font_multiplier)),
            text_color=COLORS["text_secondary"],
        ).pack(pady=8)

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=(24, 0))

        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=120,
            fg_color=COLORS["bg_secondary"],
            hover_color=COLORS["border"],
            command=dialog.destroy,
        ).pack(side="left", padx=8)

        def confirm_uninstall():
            dialog.destroy()
            self._do_uninstall(app)

        ctk.CTkButton(
            btn_frame,
            text="Uninstall",
            width=120,
            fg_color=COLORS["danger"],
            hover_color="#c75a6f",
            command=confirm_uninstall,
        ).pack(side="left", padx=8)

    def _do_uninstall(self, app: dict):
        """Actually perform the uninstallation"""
        try:
            # Remove desktop entry
            desktop_dir = Path.home() / ".local" / "share" / "applications"
            desktop_file = desktop_dir / f"{app['id']}.desktop"
            if desktop_file.exists():
                desktop_file.unlink()

            # Remove icon link
            icon_dir = Path.home() / ".local" / "share" / "icons"
            icon_file = icon_dir / f"{app['id']}.png"
            if icon_file.exists():
                icon_file.unlink()

            # Remove app directory
            if app["path"].exists():
                shutil.rmtree(app["path"])

            # Refresh UI
            self._refresh_apps_list()
            
            # Clear right panel
            for widget in self.right_panel.winfo_children():
                widget.destroy()
            self.empty_state = ctk.CTkLabel(
                self.right_panel,
                text="App uninstalled successfully!",
                font=("Ubuntu", int(14 * self.font_multiplier)),
                text_color=COLORS["success"],
            )
            self.empty_state.pack(expand=True)

        except Exception as e:
            # Show error
            for widget in self.right_panel.winfo_children():
                widget.destroy()
            error_label = ctk.CTkLabel(
                self.right_panel,
                text=f"Error uninstalling:\n{str(e)}",
                font=("Ubuntu", int(14 * self.font_multiplier)),
                text_color=COLORS["danger"],
            )
            error_label.pack(expand=True)

    def _build_help_tab(self):
        """Build the Help tab with troubleshooting information"""
        self._build_help_tab_content()
    
    def _build_help_tab_content(self):
        """Build the Help tab content (separated for rebuilding)"""
        tab = self.tabview.tab("Help")

        # Scrollable container for help content
        scroll_frame = ctk.CTkScrollableFrame(
            tab,
            fg_color=COLORS["bg_secondary"],
            corner_radius=12,
        )
        scroll_frame.pack(fill="both", expand=True, padx=40, pady=24)
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            scroll_frame._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        # Bind mouse wheel events to the scrollable frame and its canvas
        scroll_frame.bind_all("<MouseWheel>", _on_mousewheel)  # Windows/MacOS
        scroll_frame.bind_all("<Button-4>", lambda e: scroll_frame._parent_canvas.yview_scroll(-1, "units"))  # Linux scroll up
        scroll_frame.bind_all("<Button-5>", lambda e: scroll_frame._parent_canvas.yview_scroll(1, "units"))  # Linux scroll down

        content_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=32, pady=24)

        # Title
        title = ctk.CTkLabel(
            content_frame,
            text="Why my App says Invalid URL or something like this?",
            font=("Ubuntu", int(20 * self.font_multiplier), "bold"),
            text_color=COLORS["text_primary"],
            wraplength=800,
        )
        title.pack(anchor="w", pady=(0, 16))

        # Pro Tip at the beginning
        protip_frame = ctk.CTkFrame(
            content_frame,
            fg_color=COLORS["border"],
            corner_radius=8,
        )
        protip_frame.pack(fill="x", pady=(0, 24))

        ctk.CTkLabel(
            protip_frame,
            text="💡 Pro Tip",
            font=("Ubuntu", int(14 * self.font_multiplier), "bold"),
            text_color=COLORS["accent"],
            anchor="w",
        ).pack(anchor="w", padx=16, pady=(12, 4))

        ctk.CTkLabel(
            protip_frame,
            text="Open the website in your browser, log in if needed, then copy the exact URL from the address bar. This ensures you're using the correct entry point for your web app.",
            font=("Ubuntu", int(12 * self.font_multiplier)),
            text_color=COLORS["text_secondary"],
            anchor="w",
            wraplength=800,
        ).pack(anchor="w", padx=16, pady=(0, 12))

        # URL Format Examples at the beginning
        section_examples_title = ctk.CTkLabel(
            content_frame,
            text="Correct URL Format Examples:",
            font=("Ubuntu", int(16 * self.font_multiplier), "bold"),
            text_color=COLORS["accent"],
            anchor="center",
        )
        section_examples_title.pack(anchor="center", pady=(0, 12))

        # Examples container (two columns)
        examples_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        examples_container.pack(fill="x", pady=(0, 16))

        # Left column - Correct examples
        examples_left = ctk.CTkFrame(examples_container, fg_color="transparent")
        examples_left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        correct_examples = [
            ("✓ Correct", "https://website.com/login"),
            ("✓ Correct", "https://app.service.com/dashboard"),
        ]

        for label, url in correct_examples:
            example_frame = ctk.CTkFrame(
                examples_left,
                fg_color=COLORS["input_bg"],
                corner_radius=6,
            )
            example_frame.pack(fill="x", pady=4)

            ctk.CTkLabel(
                example_frame,
                text=f"{label}: {url}",
                font=("Ubuntu", int(12 * self.font_multiplier), "bold"),
                text_color=COLORS["success"],
                anchor="w",
            ).pack(anchor="w", padx=16, pady=12)

        # Right column - Wrong examples
        examples_right = ctk.CTkFrame(examples_container, fg_color="transparent")
        examples_right.pack(side="right", fill="both", expand=True, padx=(8, 0))

        wrong_examples = [
            ("✗ Wrong", "website.com"),
            ("✗ Wrong", "http://website.com"),
        ]

        for label, url in wrong_examples:
            example_frame = ctk.CTkFrame(
                examples_right,
                fg_color=COLORS["input_bg"],
                corner_radius=6,
            )
            example_frame.pack(fill="x", pady=4)

            ctk.CTkLabel(
                example_frame,
                text=f"{label}: {url}",
                font=("Ubuntu", int(12 * self.font_multiplier)),
                text_color=COLORS["danger"],
                anchor="w",
            ).pack(anchor="w", padx=16, pady=12)

        # Two-column container
        columns_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        columns_container.pack(fill="both", expand=True)

        # Left column
        left_column = ctk.CTkFrame(columns_container, fg_color="transparent")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 8))

        # Section 1: Common causes (Left column)
        section1_title = ctk.CTkLabel(
            left_column,
            text="Common Causes:",
            font=("Ubuntu", int(16 * self.font_multiplier), "bold"),
            text_color=COLORS["accent"],
            anchor="w",
        )
        section1_title.pack(anchor="w", pady=(0, 12))

        causes_text = [
            "1. The URL doesn't include the login page",
            "   → Some websites require you to be logged in to access the homepage",
            "   → Solution: Use the full login URL (e.g., https://website.com/login)",
            "",
            "2. The URL is incomplete or incorrect",
            "   → Missing https:// or http:// prefix",
            "   → Typo in the domain name",
            "   → Solution: Double-check the URL format",
            "",
            "3. The website requires special authentication",
            "   → Some sites block automated browsers or require specific headers",
            "   → Solution: Try accessing the login page directly",
        ]

        for line in causes_text:
            ctk.CTkLabel(
                left_column,
                text=line,
                font=("Ubuntu", int(12 * self.font_multiplier)),
                text_color=COLORS["text_primary"] if not line.startswith("   →") else COLORS["text_secondary"],
                anchor="w",
                wraplength=450,
            ).pack(anchor="w", pady=2)

        # Right column
        right_column = ctk.CTkFrame(columns_container, fg_color="transparent")
        right_column.pack(side="right", fill="both", expand=True, padx=(8, 0))

        # Section 2: How to fix (Right column)
        section2_title = ctk.CTkLabel(
            right_column,
            text="How to Fix:",
            font=("Ubuntu", int(16 * self.font_multiplier), "bold"),
            text_color=COLORS["accent"],
            anchor="w",
        )
        section2_title.pack(anchor="w", pady=(0, 12))

        fix_text = [
            "✓ Always use the complete URL including protocol (https://)",
            "",
            "✓ For login-required sites, use the login page URL:",
            "   • Notion: https://notion.so/login",
            "   • WhatsApp: https://web.whatsapp.com",
            "   • Discord: https://discord.com/login",
            "   • Slack: https://slack.com/signin",
            "",
            "✓ Test the URL in your regular browser first",
            "   → Make sure the page loads correctly before creating the app",
            "",
            "✓ If the app was created with wrong URL:",
            "   1. Go to 'Manage Apps' tab",
            "   2. Uninstall the app",
            "   3. Create it again with the correct URL",
        ]

        for line in fix_text:
            ctk.CTkLabel(
                right_column,
                text=line,
                font=("Ubuntu", int(12 * self.font_multiplier)),
                text_color=COLORS["text_primary"] if line.startswith("✓") else COLORS["text_secondary"],
                anchor="w",
                wraplength=450,
            ).pack(anchor="w", pady=2)

    def _build_about_tab(self):
        """Build the About tab with author information"""
        self._build_about_tab_content()
    
    def _build_about_tab_content(self):
        """Build the About tab content (separated for rebuilding)"""
        tab = self.tabview.tab("About")

        # Scrollable container for about content
        scroll_frame = ctk.CTkScrollableFrame(
            tab,
            fg_color=COLORS["bg_secondary"],
            corner_radius=12,
        )
        scroll_frame.pack(fill="both", expand=True, padx=40, pady=24)

        # Main container with two columns
        main_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=32, pady=24)
        
        # Configure grid columns (40% left, 60% right)
        main_container.grid_columnconfigure(0, weight=25)
        main_container.grid_columnconfigure(1, weight=75)

        # Left column - Author image (40%)
        left_column = ctk.CTkFrame(main_container, fg_color="transparent")
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        # Author image
        try:
            from PIL import Image
            author_img_path = Path(__file__).parent / "about" / "author.png"
            if author_img_path.exists():
                img = Image.open(author_img_path)
                # Resize to circular display size
                img = img.resize((200, 200), Image.Resampling.LANCZOS)
                photo = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 200))
                
                img_label = ctk.CTkLabel(
                    left_column,
                    image=photo,
                    text="",
                )
                img_label.pack(pady=(0, 16))
                
                # Store reference to prevent garbage collection
                img_label.image = photo
        except Exception:
            pass

        # Author name below image
        name_label = ctk.CTkLabel(
            left_column,
            text="Sheikh Shakib\nHossain",
            font=("Ubuntu", int(14 * self.font_multiplier), "bold"),
            text_color=COLORS["text_primary"],
            justify="center",
        )
        name_label.pack(pady=(0, 16))

        # Links section under profile
        links_frame = ctk.CTkFrame(
            left_column,
            fg_color=COLORS["input_bg"],
            corner_radius=8,
        )
        links_frame.pack(fill="x", pady=(8, 0))

        links_title = ctk.CTkLabel(
            links_frame,
            text="Connect",
            font=("Ubuntu", int(14 * self.font_multiplier), "bold"),
            text_color=COLORS["accent"],
            anchor="w",
        )
        links_title.pack(anchor="w", padx=16, pady=(16, 8))

        # GitHub link
        github_label = ctk.CTkLabel(
            links_frame,
            text="GitHub: github.com/sheikhshakibhossain",
            font=("Ubuntu", int(12 * self.font_multiplier)),
            text_color=COLORS["text_primary"],
            anchor="w",
            cursor="hand2",
        )
        github_label.pack(anchor="w", padx=16, pady=4)
        github_label.bind("<Button-1>", lambda e: self._open_url("https://github.com/sheikhshakibhossain"))

        # Portfolio link
        portfolio_label = ctk.CTkLabel(
            links_frame,
            text="Portfolio: sheikhshakibhossain.github.io",
            font=("Ubuntu", int(12 * self.font_multiplier)),
            text_color=COLORS["text_primary"],
            anchor="w",
            cursor="hand2",
        )
        portfolio_label.pack(anchor="w", padx=16, pady=(4, 16))
        portfolio_label.bind("<Button-1>", lambda e: self._open_url("https://sheikhshakibhossain.github.io"))

        # Right column - Content (60%)
        right_column = ctk.CTkFrame(main_container, fg_color="transparent")
        right_column.grid(row=0, column=1, sticky="nsew", padx=(12, 0))

        # Title
        title = ctk.CTkLabel(
            right_column,
            text="About the Author",
            font=("Ubuntu", int(24 * self.font_multiplier), "bold"),
            text_color=COLORS["accent"],
        )
        title.pack(anchor="w", pady=(0, 24))

        # Author bio - paragraph 1
        bio1 = ctk.CTkLabel(
            right_column,
            text="Sheikh Shakib Hossain is a Linux-first developer, researcher, and systems enthusiast focused on building practical, transparent, and user-respecting software. His work spans Linux desktop tooling, automation, Flutter apps, robotics, networking, and applied security research. He is especially interested in systems that run locally, remain offline-capable when possible, and give full control to the user rather than the platform.",
            font=("Ubuntu", int(12 * self.font_multiplier)),
            text_color=COLORS["text_primary"],
            anchor="w",
            wraplength=520,
            justify="left",
        )
        bio1.pack(anchor="w", pady=(0, 16))

        # Author bio - paragraph 2
        bio2 = ctk.CTkLabel(
            right_column,
            text="Over the years, he has worked on a wide range of projects—from notification systems and academic automation tools to ROS 2–based autonomous rover stacks, sensor-fusion algorithms, and research prototypes aligned with green computing and efficient system design. Alongside development, he is actively involved in teaching programming and problem-solving, translating complex technical ideas into simple, practical knowledge.",
            font=("Ubuntu", int(12 * self.font_multiplier)),
            text_color=COLORS["text_primary"],
            anchor="w",
            wraplength=520,
            justify="left",
        )
        bio2.pack(anchor="w", pady=(0, 16))

        # Philosophy section
        philosophy_title = ctk.CTkLabel(
            right_column,
            text="Development Philosophy",
            font=("Ubuntu", int(16 * self.font_multiplier), "bold"),
            text_color=COLORS["accent"],
            anchor="w",
        )
        philosophy_title.pack(anchor="w", pady=(16, 12))

        philosophy = ctk.CTkLabel(
            right_column,
            text="His development philosophy is rooted in Unix and Linux principles: lightweight design, clarity over abstraction, and performance without unnecessary dependencies. He prefers native solutions, clean architectures, and open standards, avoiding bloat, telemetry, and opaque frameworks whenever possible.",
            font=("Ubuntu", int(12 * self.font_multiplier)),
            text_color=COLORS["text_primary"],
            anchor="w",
            wraplength=520,
            justify="left",
        )
        philosophy.pack(anchor="w", pady=(0, 16))

        # AppNEra description
        appnera_desc = ctk.CTkLabel(
            right_column,
            text="AppNEra reflects this mindset. It is designed to empower Linux users to build and manage applications locally, with full ownership of their system and data—open-source, efficient, and built with care.",
            font=("Ubuntu", int(12 * self.font_multiplier), "italic"),
            text_color=COLORS["text_secondary"],
            anchor="w",
            wraplength=520,
            justify="left",
        )
        appnera_desc.pack(anchor="w", pady=(0, 24))

    def _open_url(self, url: str):
        """Open URL in default browser"""
        import webbrowser
        webbrowser.open(url)

    def _show_status(self, message: str, color: str):
        """Show status message"""
        self.status_label.configure(text=message, text_color=color)

    def _show_loading(self, message: str = "Creating app..."):
        """Show loading overlay with animation"""
        if self.loading_overlay is not None:
            return
        
        # Create overlay frame that covers entire window
        self.loading_overlay = ctk.CTkFrame(
            self,
            fg_color=COLORS["bg_primary"],
            corner_radius=0,
        )
        self.loading_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Container for centered content
        content_frame = ctk.CTkFrame(
            self.loading_overlay,
            fg_color=COLORS["bg_secondary"],
            corner_radius=16,
            border_width=2,
            border_color=COLORS["accent"],
        )
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Inner padding frame
        inner_frame = ctk.CTkFrame(
            content_frame,
            fg_color="transparent",
        )
        inner_frame.pack(padx=48, pady=40)
        
        # Loading spinner (using progress bar in indeterminate mode)
        self.loading_progress = ctk.CTkProgressBar(
            inner_frame,
            mode="indeterminate",
            width=300,
            height=6,
            fg_color=COLORS["border"],
            progress_color=COLORS["accent"],
        )
        self.loading_progress.pack(pady=(0, 20))
        self.loading_progress.start()
        
        # Loading message
        self.loading_label = ctk.CTkLabel(
            inner_frame,
            text=message,
            font=("Ubuntu", int(16 * self.font_multiplier), "bold"),
            text_color=COLORS["text_primary"],
        )
        self.loading_label.pack(pady=(0, 8))
        
        # Subtitle
        self.loading_subtitle = ctk.CTkLabel(
            inner_frame,
            text="This may take a moment...",
            font=("Ubuntu", int(12 * self.font_multiplier)),
            text_color=COLORS["text_secondary"],
        )
        self.loading_subtitle.pack()
        
        # Raise overlay to top
        self.loading_overlay.lift()
        self.update()
    
    def _hide_loading(self):
        """Hide loading overlay"""
        if self.loading_overlay is not None:
            if hasattr(self, 'loading_progress'):
                self.loading_progress.stop()
            self.loading_overlay.destroy()
            self.loading_overlay = None
    
    def _update_loading_message(self, message: str):
        """Update loading message - safe to call from any thread"""
        if hasattr(self, 'loading_label') and self.loading_label.winfo_exists():
            self.loading_label.configure(text=message)


def main():
    """Main entry point"""
    app = AppNEraGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
