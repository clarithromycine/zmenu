"""
Tests for the zmenu framework.
"""

import unittest
from unittest.mock import patch, MagicMock
from zmenu import Menu, MenuItem


class TestMenuItem(unittest.TestCase):
    """Test cases for MenuItem class."""
    
    def test_menuitem_creation_with_action(self):
        """Test creating a MenuItem with an action."""
        action = lambda: print("test")
        item = MenuItem("Test Item", action=action)
        
        self.assertEqual(item.title, "Test Item")
        self.assertEqual(item.action, action)
        self.assertIsNone(item.submenu)
        self.assertEqual(item.description, "")
    
    def test_menuitem_creation_with_submenu(self):
        """Test creating a MenuItem with a submenu."""
        submenu = Menu("Submenu")
        item = MenuItem("Test Item", submenu=submenu)
        
        self.assertEqual(item.title, "Test Item")
        self.assertIsNone(item.action)
        self.assertEqual(item.submenu, submenu)
    
    def test_menuitem_creation_with_description(self):
        """Test creating a MenuItem with a description."""
        item = MenuItem("Test Item", description="Test description")
        
        self.assertEqual(item.title, "Test Item")
        self.assertEqual(item.description, "Test description")
    
    def test_menuitem_cannot_have_both_action_and_submenu(self):
        """Test that MenuItem raises error when both action and submenu are provided."""
        submenu = Menu("Submenu")
        action = lambda: print("test")
        
        with self.assertRaises(ValueError):
            MenuItem("Test Item", action=action, submenu=submenu)
    
    def test_menuitem_execute_with_action(self):
        """Test executing a MenuItem with an action."""
        executed = []
        action = lambda: executed.append(True)
        item = MenuItem("Test Item", action=action)
        
        result = item.execute()
        
        self.assertTrue(executed)
        self.assertIsNone(result)
    
    def test_menuitem_execute_with_submenu(self):
        """Test executing a MenuItem with a submenu."""
        submenu = Menu("Submenu")
        item = MenuItem("Test Item", submenu=submenu)
        
        result = item.execute()
        
        self.assertEqual(result, submenu)


class TestMenu(unittest.TestCase):
    """Test cases for Menu class."""
    
    def test_menu_creation(self):
        """Test creating a Menu."""
        menu = Menu("Test Menu")
        
        self.assertEqual(menu.title, "Test Menu")
        self.assertEqual(menu.items, [])
        self.assertIsNone(menu.parent)
        self.assertFalse(menu._exit_requested)
    
    def test_menu_creation_with_items(self):
        """Test creating a Menu with items."""
        items = [MenuItem("Item 1"), MenuItem("Item 2")]
        menu = Menu("Test Menu", items=items)
        
        self.assertEqual(len(menu.items), 2)
    
    def test_menu_add_item(self):
        """Test adding an item to a menu."""
        menu = Menu("Test Menu")
        item = MenuItem("Test Item")
        
        result = menu.add_item(item)
        
        self.assertEqual(len(menu.items), 1)
        self.assertEqual(menu.items[0], item)
        self.assertEqual(result, menu)  # Check method chaining
    
    def test_menu_add_action(self):
        """Test adding an action to a menu."""
        menu = Menu("Test Menu")
        action = lambda: print("test")
        
        result = menu.add_action("Test Action", action, "Test description")
        
        self.assertEqual(len(menu.items), 1)
        self.assertEqual(menu.items[0].title, "Test Action")
        self.assertEqual(menu.items[0].action, action)
        self.assertEqual(menu.items[0].description, "Test description")
        self.assertEqual(result, menu)  # Check method chaining
    
    def test_menu_add_submenu(self):
        """Test adding a submenu to a menu."""
        menu = Menu("Main Menu")
        submenu = Menu("Submenu")
        
        result = menu.add_submenu("Go to Submenu", submenu, "Description")
        
        self.assertEqual(len(menu.items), 1)
        self.assertEqual(menu.items[0].title, "Go to Submenu")
        self.assertEqual(menu.items[0].submenu, submenu)
        self.assertEqual(submenu.parent, menu)
        self.assertEqual(result, menu)  # Check method chaining
    
    def test_menu_exit(self):
        """Test exiting from a menu."""
        menu = Menu("Test Menu")
        
        menu.exit()
        
        self.assertTrue(menu._exit_requested)
    
    def test_menu_exit_propagates_to_parent(self):
        """Test that exit propagates to parent menu."""
        parent = Menu("Parent Menu")
        child = Menu("Child Menu", parent=parent)
        
        child.exit()
        
        self.assertTrue(child._exit_requested)
        self.assertTrue(parent._exit_requested)
    
    @patch('builtins.input', return_value='1')
    def test_get_choice_valid(self, mock_input):
        """Test getting a valid choice from user."""
        menu = Menu("Test Menu")
        
        choice = menu.get_choice()
        
        self.assertEqual(choice, 1)
    
    @patch('builtins.input', return_value='invalid')
    def test_get_choice_invalid(self, mock_input):
        """Test getting an invalid choice from user."""
        menu = Menu("Test Menu")
        
        choice = menu.get_choice()
        
        self.assertIsNone(choice)
    
    @patch('builtins.input', side_effect=KeyboardInterrupt)
    def test_get_choice_keyboard_interrupt(self, mock_input):
        """Test handling keyboard interrupt."""
        menu = Menu("Test Menu")
        
        choice = menu.get_choice()
        
        self.assertIsNone(choice)


class TestMenuIntegration(unittest.TestCase):
    """Integration tests for menu navigation."""
    
    def test_nested_menu_structure(self):
        """Test creating a nested menu structure."""
        # Create a 3-level menu structure
        level2_menu = Menu("Level 2")
        level2_menu.add_action("Action L2", lambda: None)
        
        level1_menu = Menu("Level 1")
        level1_menu.add_submenu("Go to Level 2", level2_menu)
        
        main_menu = Menu("Main Menu")
        main_menu.add_submenu("Go to Level 1", level1_menu)
        
        # Verify structure
        self.assertEqual(len(main_menu.items), 1)
        self.assertEqual(main_menu.items[0].submenu, level1_menu)
        self.assertEqual(level1_menu.parent, main_menu)
        self.assertEqual(level1_menu.items[0].submenu, level2_menu)
        self.assertEqual(level2_menu.parent, level1_menu)
    
    def test_method_chaining(self):
        """Test method chaining for building menus."""
        menu = (Menu("Test Menu")
                .add_action("Action 1", lambda: None)
                .add_action("Action 2", lambda: None)
                .add_submenu("Submenu", Menu("Sub")))
        
        self.assertEqual(len(menu.items), 3)


if __name__ == '__main__':
    unittest.main()
