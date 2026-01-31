# ZMenu - Keyboard Controls Guide

## Overview

ZMenu provides comprehensive keyboard controls for efficient navigation and interaction. This guide explains all keyboard shortcuts and their behaviors across different components.

## Menu Navigation

### Basic Controls
- **↑ ↓ Arrow Keys**: Navigate between menu items
- **Number Keys (1-9)**: Jump directly to a numbered menu item
- **Enter**: Select the highlighted menu item
- **ESC**: Return to parent menu (or exit if at root)
- **Ctrl+C**: Force exit from any menu

### Advanced Behavior
- Arrow key sequences have a 0.5s timeout for proper detection
- Menu items update automatically as you navigate
- Descriptions appear inline when navigating to menu items

## Form Interaction

### Choice Fields (Single/Multi Selection)

#### Navigation Controls
- **↑ ↓ Arrow Keys**: Navigate between options
- **← → Arrow Keys**: Navigate between options (alternative to ↑ ↓)
- **Enter**: Confirm selection and proceed to next field
- **ESC**: Cancel selection and return to previous state

#### Selection Controls
- **Space**: Toggle selection (multi-choice only)
- **Other Keys**: Silently ignored (no interface refresh)

#### Important Behavior
- Invalid keys (letters, numbers, function keys) are completely ignored
- Pressing invalid keys does not cause interface refresh or redisplay
- This prevents visual flickering when users accidentally press wrong keys

### Text Input Fields
- **Standard typing**: Enter text as usual
- **Enter**: Submit text input and proceed
- **Backspace/Delete**: Edit text as standard terminal behavior
- **ESC**: Cancel input (where supported)

## Visual Feedback

### Active Elements
- **Highlighted Menu Item**: Arrow icon (▶) appears before the currently selected item
- **Selected Option**: Bullet icon (●) appears before the currently selected option
- **Checkbox States**: 
  - Unselected: ☐
  - Selected: ☑️
  - Currently focused: ► (appears before the checkbox)

### Navigation Indicators
- Current selection is clearly marked with visual indicators
- Options remain stable when invalid keys are pressed
- Interface only updates on valid navigation or selection actions

## Platform Compatibility

All keyboard controls work consistently across:
- **Windows**: Using MSVCRT for keyboard input
- **Unix/Linux/macOS**: Using termios for raw keyboard input

### Cross-Platform Features
- Arrow key detection works reliably on all platforms
- Special key sequences (Escape sequences) are properly handled
- Character input is normalized across platforms

## Performance Considerations

### Efficient Rendering
- Interface only refreshes when necessary (valid navigation keys)
- Invalid key presses do not trigger expensive redraw operations
- Smooth navigation with minimal latency

### Resource Usage
- Low CPU usage during keyboard monitoring
- Minimal memory footprint for key state tracking
- Optimized for long-running interactive sessions

## Troubleshooting

### Common Issues
- **Keys not responding**: Ensure terminal is in focus and accepting input
- **Delayed response**: May be experiencing terminal input buffering
- **Invalid keys showing**: Should be silently ignored (contact support if they aren't)

### Terminal Compatibility
- Best experience with modern terminal emulators
- Some older terminals may have limited arrow key support
- Color and emoji rendering depends on terminal font support

## Best Practices

### For Users
- Use arrow keys for navigation rather than number keys for better visual feedback
- Press ESC to cancel any operation safely
- Take advantage of pre-validation to speed up form completion

### For Developers
- Test keyboard controls in different terminal environments
- Consider providing visual cues for available keyboard shortcuts
- Implement graceful fallbacks for unsupported terminal features

---

**Happy interacting! 🎮**