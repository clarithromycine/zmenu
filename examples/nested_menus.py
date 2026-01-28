"""
Advanced example demonstrating nested menus at multiple depth levels.
"""

from zmenu import Menu, MenuItem


# Action functions
def view_profile():
    """View user profile."""
    print("\n" + "=" * 50)
    print("USER PROFILE")
    print("=" * 50)
    print("Name: John Doe")
    print("Email: john.doe@example.com")
    print("Role: Administrator")


def change_password():
    """Change password action."""
    print("\nPassword change functionality")
    old_pwd = input("Enter old password: ")
    new_pwd = input("Enter new password: ")
    confirm_pwd = input("Confirm new password: ")
    
    if new_pwd == confirm_pwd:
        print("\n✓ Password changed successfully!")
    else:
        print("\n✗ Passwords don't match!")


def update_email():
    """Update email action."""
    new_email = input("\nEnter new email address: ")
    print(f"\n✓ Email updated to: {new_email}")


def view_notifications():
    """View notifications."""
    print("\n" + "=" * 50)
    print("NOTIFICATIONS")
    print("=" * 50)
    print("1. Welcome to zmenu!")
    print("2. New feature available")
    print("3. System update completed")


def notification_settings():
    """Configure notification settings."""
    print("\nNotification Settings")
    print("- Email notifications: Enabled")
    print("- Push notifications: Disabled")
    print("- SMS notifications: Enabled")


def list_files():
    """List files action."""
    print("\nFiles:")
    print("- document1.txt")
    print("- document2.pdf")
    print("- image.png")


def upload_file():
    """Upload file action."""
    filename = input("\nEnter filename to upload: ")
    print(f"\n✓ Uploading {filename}...")
    print("✓ Upload complete!")


def delete_file():
    """Delete file action."""
    filename = input("\nEnter filename to delete: ")
    confirm = input(f"Are you sure you want to delete '{filename}'? (y/n): ")
    
    if confirm.lower() == 'y':
        print(f"\n✓ File '{filename}' deleted successfully!")
    else:
        print("\n✗ Deletion cancelled.")


def show_stats():
    """Show statistics."""
    print("\n" + "=" * 50)
    print("SYSTEM STATISTICS")
    print("=" * 50)
    print("Total Users: 1,234")
    print("Active Sessions: 45")
    print("Storage Used: 2.3 GB")
    print("Uptime: 99.9%")


def export_data():
    """Export data action."""
    format_choice = input("\nExport format (csv/json/xml): ")
    print(f"\n✓ Exporting data as {format_choice}...")
    print("✓ Export complete! File saved to exports/data." + format_choice)


def generate_report():
    """Generate report action."""
    print("\nGenerating comprehensive report...")
    print("✓ Analyzing data...")
    print("✓ Creating charts...")
    print("✓ Compiling statistics...")
    print("\n✓ Report generated successfully!")


def main():
    """Create and run a nested menu structure."""
    
    # Create deeply nested file management menu
    file_operations = Menu("File Operations")
    file_operations.add_action("List Files", list_files)
    file_operations.add_action("Upload File", upload_file)
    file_operations.add_action("Delete File", delete_file)
    
    # Create reports submenu (level 3)
    reports_menu = Menu("Reports")
    reports_menu.add_action("Generate Report", generate_report)
    reports_menu.add_action("Export Data", export_data)
    reports_menu.add_action("View Statistics", show_stats)
    
    # Create data management menu (level 2) with nested reports
    data_menu = Menu("Data Management")
    data_menu.add_submenu("Reports & Analytics", reports_menu)
    data_menu.add_submenu("File Operations", file_operations)
    
    # Create security settings submenu (level 2)
    security_menu = Menu("Security Settings")
    security_menu.add_action("Change Password", change_password)
    security_menu.add_action("Update Email", update_email)
    
    # Create notifications submenu (level 2)
    notifications_menu = Menu("Notifications")
    notifications_menu.add_action("View Notifications", view_notifications)
    notifications_menu.add_action("Notification Settings", notification_settings)
    
    # Create account settings menu (level 1) with nested security
    account_menu = Menu("Account Settings")
    account_menu.add_action("View Profile", view_profile)
    account_menu.add_submenu("Security", security_menu)
    account_menu.add_submenu("Notifications", notifications_menu)
    
    # Create main menu (level 0)
    main_menu = Menu("Application Dashboard")
    main_menu.add_submenu("Account Settings", account_menu)
    main_menu.add_submenu("Data Management", data_menu)
    
    # Run the menu
    main_menu.run()


if __name__ == "__main__":
    main()
