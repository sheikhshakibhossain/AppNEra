#!/usr/bin/env python3

"""
AppNEra - A new era for web apps on Linux
Modern GUI for creating lightweight web app wrappers
"""

import os
import shutil
import subprocess
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
        self.geometry("1400x900")
        # self.minsize(1200, 800)

        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configure colors
        self._configure_colors()

        # Build UI
        self._create_header()
        self._create_tabview()

        # Track created apps
        self.apps_dir = Path.home() / ".local"

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
            font=("Ubuntu", 28, "bold"),
            text_color=COLORS["accent"],
        )
        title.pack(pady=(24, 4))

        tagline = ctk.CTkLabel(
            header_frame,
            text="A new era for web apps on Linux",
            font=("Ubuntu", 13),
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

        # Create tabs
        self.tabview.add("Create App")
        self.tabview.add("Manage Apps")
        self.tabview.add("Help")
        self.tabview.add("About")

        # Build tab contents
        self._build_create_tab()
        self._build_manage_tab()
        self._build_help_tab()
        self._build_about_tab()

    def _build_create_tab(self):
        """Build the Create App tab UI"""
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
            font=("Ubuntu", 12, "bold"),
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
        )
        self.url_entry.pack(fill="x", pady=(0, 24))

        # App Name field
        name_label = ctk.CTkLabel(
            form_frame,
            text="App Name *",
            font=("Ubuntu", 12, "bold"),
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
        )
        self.name_entry.pack(fill="x", pady=(0, 24))

        # App Icon field (required)
        icon_label = ctk.CTkLabel(
            form_frame,
            text="App Icon *",
            font=("Ubuntu", 12, "bold"),
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
            font=("Ubuntu", 14, "bold"),
            corner_radius=8,
            command=self._create_app,
        )
        self.create_btn.pack(fill="x", pady=(0, 16))

        # Status label
        self.status_label = ctk.CTkLabel(
            form_frame,
            text="",
            font=("Ubuntu", 12),
            text_color=COLORS["text_secondary"],
        )
        self.status_label.pack()

    def _build_manage_tab(self):
        """Build the Manage Apps tab UI"""
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
            font=("Ubuntu", 16, "bold"),
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
            font=("Ubuntu", 14),
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

        # Show progress
        self._show_status("⏳ Creating app...", COLORS["accent"])
        self.create_btn.configure(state="disabled")
        self.update()

        try:
            self._build_app(url, name, icon_path)
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
            
        except Exception as e:
            self._show_status(f"❌ Error: {str(e)}", COLORS["danger"])
        finally:
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
        app_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Copy template files
            shutil.copy(template_dir / "app.py", app_dir / "app.py")
            shutil.copy(template_dir / "uninstall.sh", app_dir / "uninstall.sh")
            os.chmod(app_dir / "uninstall.sh", 0o755)

            # Copy selected icon
            if not Path(icon_path).exists():
                raise ValueError("Selected icon file not found")
            shutil.copy(icon_path, app_dir / "icon.png")

            # Create isolated venv
            subprocess.run(
                ["python3", "-m", "venv", str(app_dir / "venv")],
                check=True,
                capture_output=True,
            )

            # Install PyQt5 dependencies in venv (fully self-contained, no system packages needed)
            pip_path = app_dir / "venv" / "bin" / "pip"
            subprocess.run(
                [str(pip_path), "install", "PyQt5", "PyQtWebEngine"],
                check=True,
                capture_output=True,
            )

            # Create launcher script
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

        except Exception as e:
            # Cleanup on failure
            if app_dir.exists():
                shutil.rmtree(app_dir)
            raise e

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
                font=("Ubuntu", 12),
                text_color=COLORS["text_secondary"],
                justify="center",
            )
            empty_label.pack(pady=32)
            return

        # Display apps
        for app in apps:
            app_btn = ctk.CTkButton(
                self.apps_list_frame,
                text=app["name"],
                height=48,
                anchor="w",
                fg_color="transparent",
                hover_color=COLORS["input_bg"],
                text_color=COLORS["text_primary"],
                command=lambda a=app: self._show_app_details(a),
            )
            app_btn.pack(fill="x", pady=2, padx=4)

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

        # App name
        name_label = ctk.CTkLabel(
            details_frame,
            text=app["name"],
            font=("Ubuntu", 24, "bold"),
            text_color=COLORS["text_primary"],
        )
        name_label.pack(anchor="w", pady=(0, 16))

        # App path
        path_label = ctk.CTkLabel(
            details_frame,
            text=f"Location: {app['path']}",
            font=("Ubuntu", 12),
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
            font=("Ubuntu", 12),
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
            font=("Ubuntu", 14, "bold"),
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
            font=("Ubuntu", 16, "bold"),
        ).pack(pady=(24, 8))

        ctk.CTkLabel(
            dialog,
            text="This will remove all app data\nand cannot be undone.",
            font=("Ubuntu", 12),
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
                font=("Ubuntu", 14),
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
                font=("Ubuntu", 14),
                text_color=COLORS["danger"],
            )
            error_label.pack(expand=True)

    def _build_help_tab(self):
        """Build the Help tab with troubleshooting information"""
        tab = self.tabview.tab("Help")

        # Scrollable container for help content
        scroll_frame = ctk.CTkScrollableFrame(
            tab,
            fg_color=COLORS["bg_secondary"],
            corner_radius=12,
        )
        scroll_frame.pack(fill="both", expand=True, padx=40, pady=24)

        content_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=32, pady=24)

        # Title
        title = ctk.CTkLabel(
            content_frame,
            text="Why my App says Invalid URL or something like this?",
            font=("Ubuntu", 20, "bold"),
            text_color=COLORS["text_primary"],
            wraplength=600,
        )
        title.pack(anchor="w", pady=(0, 24))

        # Section 1: Common causes
        section1_title = ctk.CTkLabel(
            content_frame,
            text="Common Causes:",
            font=("Ubuntu", 16, "bold"),
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
                content_frame,
                text=line,
                font=("Ubuntu", 12),
                text_color=COLORS["text_primary"] if not line.startswith("   →") else COLORS["text_secondary"],
                anchor="w",
            ).pack(anchor="w", pady=2)

        # Section 2: How to fix
        section2_title = ctk.CTkLabel(
            content_frame,
            text="How to Fix:",
            font=("Ubuntu", 16, "bold"),
            text_color=COLORS["accent"],
            anchor="w",
        )
        section2_title.pack(anchor="w", pady=(24, 12))

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
                content_frame,
                text=line,
                font=("Ubuntu", 12),
                text_color=COLORS["text_primary"] if line.startswith("✓") else COLORS["text_secondary"],
                anchor="w",
            ).pack(anchor="w", pady=2)

        # Section 3: URL format examples
        section3_title = ctk.CTkLabel(
            content_frame,
            text="Correct URL Format Examples:",
            font=("Ubuntu", 16, "bold"),
            text_color=COLORS["accent"],
            anchor="w",
        )
        section3_title.pack(anchor="w", pady=(24, 12))

        # Examples in boxes
        examples = [
            ("✓ Correct", "https://website.com/login", COLORS["success"]),
            ("✓ Correct", "https://app.service.com/dashboard", COLORS["success"]),
            ("✗ Wrong", "website.com", COLORS["danger"]),
            ("✗ Wrong", "http://website.com", COLORS["danger"]),
        ]

        for label, url, color in examples:
            example_frame = ctk.CTkFrame(
                content_frame,
                fg_color=COLORS["input_bg"],
                corner_radius=6,
            )
            example_frame.pack(fill="x", pady=4)

            ctk.CTkLabel(
                example_frame,
                text=f"{label}: {url}",
                font=("Ubuntu", 12, "bold" if "Correct" in label else "normal"),
                text_color=color,
                anchor="w",
            ).pack(anchor="w", padx=16, pady=12)

        # Note section
        note_frame = ctk.CTkFrame(
            content_frame,
            fg_color=COLORS["border"],
            corner_radius=8,
        )
        note_frame.pack(fill="x", pady=(24, 0))

        ctk.CTkLabel(
            note_frame,
            text="💡 Pro Tip",
            font=("Ubuntu", 14, "bold"),
            text_color=COLORS["accent"],
            anchor="w",
        ).pack(anchor="w", padx=16, pady=(12, 4))

        ctk.CTkLabel(
            note_frame,
            text="Open the website in your browser, log in if needed, then copy the exact URL from the address bar. This ensures you're using the correct entry point for your web app.",
            font=("Ubuntu", 12),
            text_color=COLORS["text_secondary"],
            anchor="w",
            wraplength=550,
        ).pack(anchor="w", padx=16, pady=(0, 12))

    def _build_about_tab(self):
        """Build the About tab with author information"""
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

        # Left column - Author image
        left_column = ctk.CTkFrame(main_container, fg_color="transparent", width=220)
        left_column.pack(side="left", fill="y", padx=(0, 24))
        left_column.pack_propagate(False)

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
            font=("Ubuntu", 14, "bold"),
            text_color=COLORS["text_primary"],
            justify="center",
        )
        name_label.pack()

        # Right column - Content
        right_column = ctk.CTkFrame(main_container, fg_color="transparent")
        right_column.pack(side="right", fill="both", expand=True)

        # Title
        title = ctk.CTkLabel(
            right_column,
            text="About the Author",
            font=("Ubuntu", 24, "bold"),
            text_color=COLORS["accent"],
        )
        title.pack(anchor="w", pady=(0, 24))

        # Author bio - paragraph 1
        bio1 = ctk.CTkLabel(
            right_column,
            text="Sheikh Shakib Hossain is a Linux-first developer, researcher, and systems enthusiast focused on building practical, transparent, and user-respecting software. His work spans Linux desktop tooling, automation, Flutter apps, robotics, networking, and applied security research. He is especially interested in systems that run locally, remain offline-capable when possible, and give full control to the user rather than the platform.",
            font=("Ubuntu", 12),
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
            font=("Ubuntu", 12),
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
            font=("Ubuntu", 16, "bold"),
            text_color=COLORS["accent"],
            anchor="w",
        )
        philosophy_title.pack(anchor="w", pady=(16, 12))

        philosophy = ctk.CTkLabel(
            right_column,
            text="His development philosophy is rooted in Unix and Linux principles: lightweight design, clarity over abstraction, and performance without unnecessary dependencies. He prefers native solutions, clean architectures, and open standards, avoiding bloat, telemetry, and opaque frameworks whenever possible.",
            font=("Ubuntu", 12),
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
            font=("Ubuntu", 12, "italic"),
            text_color=COLORS["text_secondary"],
            anchor="w",
            wraplength=520,
            justify="left",
        )
        appnera_desc.pack(anchor="w", pady=(0, 24))

        # Links section
        links_frame = ctk.CTkFrame(
            right_column,
            fg_color=COLORS["input_bg"],
            corner_radius=8,
        )
        links_frame.pack(fill="x", pady=(8, 0))

        links_title = ctk.CTkLabel(
            links_frame,
            text="Connect",
            font=("Ubuntu", 14, "bold"),
            text_color=COLORS["accent"],
            anchor="w",
        )
        links_title.pack(anchor="w", padx=16, pady=(16, 8))

        # GitHub link
        github_label = ctk.CTkLabel(
            links_frame,
            text="GitHub: github.com/sheikhshakibhossain",
            font=("Ubuntu", 12),
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
            font=("Ubuntu", 12),
            text_color=COLORS["text_primary"],
            anchor="w",
            cursor="hand2",
        )
        portfolio_label.pack(anchor="w", padx=16, pady=(4, 16))
        portfolio_label.bind("<Button-1>", lambda e: self._open_url("https://sheikhshakibhossain.github.io"))

    def _open_url(self, url: str):
        """Open URL in default browser"""
        import webbrowser
        webbrowser.open(url)

    def _show_status(self, message: str, color: str):
        """Show status message"""
        self.status_label.configure(text=message, text_color=color)


def main():
    """Main entry point"""
    app = AppNEraGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
