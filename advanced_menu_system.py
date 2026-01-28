"""
Advanced Menu System with Script Management
Designed for managing utility scripts and complex CLI tools similar to moltbot.
"""

from menu_system import Menu, ConsoleApp, MenuItem
from typing import List, Dict, Optional, Callable
import subprocess
import os
import json


class ScriptRunner:
    """Manages and executes shell/cli scripts."""
    
    def __init__(self, script_dir: str = "."):
        """Initialize script runner."""
        self.script_dir = script_dir
        self.scripts: Dict[str, Dict] = {}
    
    def register_script(self, key: str, name: str, script_path: str, 
                       description: str = "", args: List[str] = None):
        """
        Register a script to be executed.
        
        Args:
            key: Unique identifier
            name: Display name
            script_path: Path to script file
            description: Script description
            args: Default arguments
        """
        self.scripts[key] = {
            'name': name,
            'path': script_path,
            'description': description,
            'args': args or []
        }
    
    def execute_script(self, key: str, extra_args: List[str] = None) -> bool:
        """
        Execute a registered script.
        
        Args:
            key: Script identifier
            extra_args: Additional arguments to pass
        
        Returns:
            True to continue menu
        """
        if key not in self.scripts:
            print(f"\n❌ Script '{key}' not found")
            return True
        
        script_info = self.scripts[key]
        script_path = os.path.join(self.script_dir, script_info['path'])
        
        if not os.path.exists(script_path):
            print(f"\n❌ Script file not found: {script_path}")
            return True
        
        print(f"\n▶️  Running: {script_info['name']}")
        print(f"📝 Path: {script_path}")
        
        if script_info['description']:
            print(f"📖 Description: {script_info['description']}")
        
        args = script_info['args'].copy()
        if extra_args:
            args.extend(extra_args)
        
        try:
            # For demonstration - in real use, execute actual script
            print(f"\n⚙️  Executing with args: {args if args else 'none'}")
            print("\n[Script output would appear here in actual execution]")
            return True
        except Exception as e:
            print(f"\n❌ Error executing script: {e}")
            return True


class CategoryMenu:
    """Organizes scripts by category."""
    
    def __init__(self, name: str, description: str = ""):
        """Initialize category."""
        self.name = name
        self.description = description
        self.scripts: Dict[str, Dict] = {}
    
    def add_script(self, key: str, name: str, script_path: str, 
                   description: str = ""):
        """Add script to category."""
        self.scripts[key] = {
            'name': name,
            'path': script_path,
            'description': description
        }


class AdvancedConsoleApp(ConsoleApp):
    """Extended console app with script management capabilities."""
    
    def __init__(self, name: str = "Script Manager"):
        """Initialize advanced app."""
        super().__init__(name)
        self.script_runner = ScriptRunner()
        self.categories: Dict[str, CategoryMenu] = {}
    
    def add_category(self, key: str, name: str, description: str = "") -> CategoryMenu:
        """Add a category for organizing scripts."""
        category = CategoryMenu(name, description)
        self.categories[key] = category
        return category
    
    def setup_script_menu(self):
        """Populate menu with scripts from categories."""
        main_menu = self.main_menu
        
        for cat_key, category in self.categories.items():
            cat_menu = main_menu.add_submenu(cat_key, f"📁 {category.name}")
            
            for script_key, script_info in category.scripts.items():
                script_runner = self.script_runner
                script_runner.register_script(
                    script_key,
                    script_info['name'],
                    script_info['path'],
                    script_info['description']
                )
                
                # Create closure to capture script_key
                def make_executor(key):
                    return lambda: script_runner.execute_script(key)
                
                cat_menu.add_item(
                    script_key,
                    f"▶️  {script_info['name']}",
                    make_executor(script_key)
                )


class ScriptLibrary:
    """Pre-configured script library similar to moltbot scripts."""
    
    @staticmethod
    def create_moltbot_like_app() -> AdvancedConsoleApp:
        """Create an app similar to moltbot's script organization."""
        app = AdvancedConsoleApp("Moltbot Script Manager")
        
        # Build & Release Scripts
        build_cat = app.add_category(
            "build",
            "Build & Release",
            "Building, bundling, and releasing applications"
        )
        build_cat.add_script(
            "build_mac", "Build macOS App",
            "build-and-run-mac.sh",
            "Build and run application on macOS"
        )
        build_cat.add_script(
            "bundle", "Bundle A2UI",
            "bundle-a2ui.sh",
            "Bundle the A2UI assets"
        )
        build_cat.add_script(
            "codesign", "Code Sign macOS App",
            "codesign-mac-app.sh",
            "Sign the macOS application"
        )
        build_cat.add_script(
            "dmg", "Create DMG Distribution",
            "create-dmg.sh",
            "Create DMG disk image for distribution"
        )
        build_cat.add_script(
            "notarize", "Notarize macOS Artifact",
            "notarize-mac-artifact.sh",
            "Notarize macOS build with Apple"
        )
        build_cat.add_script(
            "package", "Package macOS Distribution",
            "package-mac-dist.sh",
            "Package application for distribution"
        )
        
        # Testing Scripts
        test_cat = app.add_category(
            "testing",
            "Testing & Validation",
            "Running tests and quality checks"
        )
        test_cat.add_script(
            "test_docker", "Test Cleanup Docker",
            "test-cleanup-docker.sh",
            "Clean up Docker test environment"
        )
        test_cat.add_script(
            "test_install", "Test Installation (Docker)",
            "test-install-sh-docker.sh",
            "Test installation process in Docker"
        )
        test_cat.add_script(
            "test_e2e", "Test E2E (Docker)",
            "test-install-sh-e2e-docker.sh",
            "Run end-to-end tests in Docker"
        )
        test_cat.add_script(
            "test_models", "Test Live Models",
            "test-live-models-docker.sh",
            "Test live model integration"
        )
        test_cat.add_script(
            "test_gateway", "Test Gateway Models",
            "test-live-gateway-models-docker.sh",
            "Test gateway model functionality"
        )
        test_cat.add_script(
            "test_parallel", "Run Parallel Tests",
            "test-parallel.mjs",
            "Execute tests in parallel mode"
        )
        
        # Authentication & System
        auth_cat = app.add_category(
            "auth",
            "Authentication & System",
            "Authentication and system management"
        )
        auth_cat.add_script(
            "auth_monitor", "Auth Monitor",
            "auth-monitor.sh",
            "Monitor authentication status"
        )
        auth_cat.add_script(
            "claude_auth", "Check Claude Auth Status",
            "claude-auth-status.sh",
            "Check Claude authentication status"
        )
        auth_cat.add_script(
            "mobile_reauth", "Mobile Re-authentication",
            "mobile-reauth.sh",
            "Re-authenticate mobile devices"
        )
        auth_cat.add_script(
            "termux_auth", "Termux Auth Widget",
            "termux-auth-widget.sh",
            "Authentication widget for Termux"
        )
        auth_cat.add_script(
            "termux_quick", "Termux Quick Auth",
            "termux-quick-auth.sh",
            "Quick authentication for Termux"
        )
        auth_cat.add_script(
            "setup_auth", "Setup Auth System",
            "setup-auth-system.sh",
            "Initialize authentication system"
        )
        
        # Development & Tools
        dev_cat = app.add_category(
            "development",
            "Development Tools",
            "Development utilities and debugging"
        )
        dev_cat.add_script(
            "debug_usage", "Debug Claude Usage",
            "debug-claude-usage.ts",
            "Debug Claude API usage"
        )
        dev_cat.add_script(
            "bench_model", "Benchmark Model",
            "bench-model.ts",
            "Benchmark AI model performance"
        )
        dev_cat.add_script(
            "check_loc", "Check TypeScript LOC",
            "check-ts-max-loc.ts",
            "Check TypeScript lines of code"
        )
        dev_cat.add_script(
            "proto_gen", "Generate Protocol (Swift)",
            "protocol-gen-swift.ts",
            "Generate Swift protocol definitions"
        )
        dev_cat.add_script(
            "proto_gen_ts", "Generate Protocol",
            "protocol-gen.ts",
            "Generate protocol definitions"
        )
        dev_cat.add_script(
            "write_build_info", "Write Build Info",
            "write-build-info.ts",
            "Write build metadata"
        )
        
        # Documentation
        docs_cat = app.add_category(
            "documentation",
            "Documentation",
            "Generate and manage documentation"
        )
        docs_cat.add_script(
            "build_docs", "Build Docs List",
            "build-docs-list.mjs",
            "Generate documentation index"
        )
        docs_cat.add_script(
            "changelog", "Convert Changelog to HTML",
            "changelog-to-html.sh",
            "Convert changelog to HTML format"
        )
        docs_cat.add_script(
            "sync_moonshot", "Sync Moonshot Docs",
            "sync-moonshot-docs.ts",
            "Synchronize Moonshot documentation"
        )
        docs_cat.add_script(
            "update_contrib", "Update Contributors",
            "update-clawtributors.ts",
            "Update contributor information"
        )
        
        # Maintenance
        maint_cat = app.add_category(
            "maintenance",
            "Maintenance & Setup",
            "System maintenance and configuration"
        )
        maint_cat.add_script(
            "setup_hooks", "Setup Git Hooks",
            "setup-git-hooks.js",
            "Configure git hooks"
        )
        maint_cat.add_script(
            "sync_labels", "Sync GitHub Labels",
            "sync-labels.ts",
            "Synchronize GitHub issue labels"
        )
        maint_cat.add_script(
            "sync_plugins", "Sync Plugin Versions",
            "sync-plugin-versions.ts",
            "Synchronize plugin versions"
        )
        maint_cat.add_script(
            "restart", "Restart macOS",
            "restart-mac.sh",
            "Restart macOS system"
        )
        
        return app


def create_demo_app() -> AdvancedConsoleApp:
    """Create a demo script management application."""
    app = ScriptLibrary.create_moltbot_like_app()
    
    # Add utility menu
    main_menu = app.main_menu
    utils_menu = main_menu.add_submenu("utils", "🔧 Utilities")
    utils_menu.add_item("release_check", "Release Check", 
                       lambda: print("\n✅ Release check passed") or True)
    utils_menu.add_item("smoke_test", "Run Smoke Test",
                       lambda: print("\n✅ Smoke tests completed") or True)
    
    # Add help menu
    help_menu = main_menu.add_submenu("help", "❓ Help")
    help_menu.add_item("about", "About Script Manager",
                      lambda: _show_about())
    help_menu.add_item("usage", "How to Use",
                      lambda: _show_usage())
    
    return app


def _show_about():
    """Show about information."""
    print("\n" + "=" * 60)
    print("  SCRIPT MANAGER - Advanced Multi-Level Menu System")
    print("=" * 60)
    print("\nThis application demonstrates a script management system")
    print("inspired by moltbot's script organization structure.")
    print("\nFeatures:")
    print("  • Organize scripts by category (Build, Test, Auth, etc.)")
    print("  • Multi-level menu navigation")
    print("  • Script descriptions and metadata")
    print("  • Easy to extend with new scripts")
    print("=" * 60)
    return True


def _show_usage():
    """Show usage instructions."""
    print("\n" + "=" * 60)
    print("  HOW TO USE SCRIPT MANAGER")
    print("=" * 60)
    print("\n1. Navigate to a category (e.g., 'Build & Release')")
    print("2. Select a script to run")
    print("3. The script description appears")
    print("4. Script executes with configured parameters")
    print("5. Use 'Back' to return to previous menu")
    print("\nExample Path:")
    print("  Main → Build & Release → Build macOS App")
    print("      → Testing → Run Parallel Tests")
    print("      → Authentication → Check Claude Auth")
    print("\nCategories Available:")
    print("  • Build & Release")
    print("  • Testing & Validation")
    print("  • Authentication & System")
    print("  • Development Tools")
    print("  • Documentation")
    print("  • Maintenance & Setup")
    print("=" * 60)
    return True


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  INITIALIZING ADVANCED SCRIPT MANAGER...")
    print("=" * 60)
    
    app = create_demo_app()
    app.setup_script_menu()
    app.run()
