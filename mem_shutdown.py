import psutil
import win32con
import win32gui
import win32process
import json

def enum_windows_callback(hwnd, results):
    if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
        tid, pid = win32process.GetWindowThreadProcessId(hwnd)
        results.append((hwnd, pid))


def get_running_programs():
    programs = []
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)

    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            if proc.info['exe'] and proc.info['name']:
                for hwnd, pid in windows:
                    if proc.info['pid'] == pid:
                        window_title = win32gui.GetWindowText(hwnd)
                        programs.append({'pid': proc.info['pid'], 'name': proc.info['name'], 'exe': proc.info['exe'],
                                         'title': window_title, 'hwnd': hwnd})
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return programs


def save_programs(programs, file_path='programs.json'):
    with open(file_path, 'w') as f:
        json.dump(programs, f)

def load_programs(file_path='programs.json'):
    with open(file_path, 'r') as f:
        return json.load(f)

def close_programs(programs):
    for program in programs:
        try:
            hwnd = program['hwnd']
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        except Exception as e:
            print(f"Failed to close {program['name']}: {e}")

if __name__ == "__main__":
    programs = get_running_programs()
    save_programs(programs)
    for program in programs:
        print(program)
    close_programs(programs)