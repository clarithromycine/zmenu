"""
Test script to verify the framework works with automated input.
"""

from unittest.mock import patch
from zmenu import Menu


def test_simple_menu():
    """Test a simple menu with automated input."""
    print("Testing simple menu...")
    
    executed = []
    
    def action1():
        executed.append("action1")
    
    def action2():
        executed.append("action2")
    
    menu = Menu("Test Menu")
    menu.add_action("Action 1", action1)
    menu.add_action("Action 2", action2)
    
    # Simulate: select action 1, then exit
    with patch('builtins.input', side_effect=['1', '', '0']):
        menu.run()
    
    assert "action1" in executed, "Action 1 should have been executed"
    print("✓ Simple menu test passed")


def test_nested_menu():
    """Test nested menus with automated input."""
    print("Testing nested menu...")
    
    executed = []
    
    def deep_action():
        executed.append("deep_action")
    
    # Create a 3-level nested structure
    level2 = Menu("Level 2")
    level2.add_action("Deep Action", deep_action)
    
    level1 = Menu("Level 1")
    level1.add_submenu("Go to Level 2", level2)
    
    main = Menu("Main Menu")
    main.add_submenu("Go to Level 1", level1)
    
    # Simulate: enter level1 -> enter level2 -> execute action -> back -> back -> exit
    with patch('builtins.input', side_effect=['1', '1', '1', '', '0', '0', '0']):
        main.run()
    
    assert "deep_action" in executed, "Deep action should have been executed"
    print("✓ Nested menu test passed")


def test_method_chaining():
    """Test method chaining."""
    print("Testing method chaining...")
    
    submenu = Menu("Submenu")
    
    menu = (Menu("Main")
            .add_action("Action 1", lambda: None)
            .add_action("Action 2", lambda: None)
            .add_submenu("Submenu", submenu))
    
    assert len(menu.items) == 3, "Should have 3 items"
    print("✓ Method chaining test passed")


if __name__ == "__main__":
    test_simple_menu()
    test_nested_menu()
    test_method_chaining()
    print("\n✅ All manual tests passed!")
