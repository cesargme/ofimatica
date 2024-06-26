import pyperclip
import pyautogui
import time

def get_clipboard_data():
    """Get data from the clipboard, split it by new lines, and remove empty lines."""
    clipboard_data = pyperclip.paste()
    lines = [line for line in clipboard_data.split('\n') if line.strip()]  # Remove empty lines
    return lines, clipboard_data


def send_lines(lines):
    """Send each line by pasting it and pressing the down arrow key, with Tab after the first line."""
    for i, line in enumerate(lines):
        pyperclip.copy(line)  # Copy the line to the clipboard
        pyautogui.hotkey('ctrl', 'v')  # Paste the line
        time.sleep(0.5)  # Small delay to allow for processing
        if i == len(lines)-1:
            continue
        # elif i == 0:
        #     pyautogui.press('tab')  # Press the Tab key after the first line
        else:
            pyautogui.press('down')  # Press the down arrow key for the rest
        time.sleep(0.5)  # Small delay to allow for processing

if __name__ == "__main__":
    time.sleep(1)
    lines, original_clipboard = get_clipboard_data()
    send_lines(lines)
    pyperclip.copy(original_clipboard)  # Restore the original clipboard content
