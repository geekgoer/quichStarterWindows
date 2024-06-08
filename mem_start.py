import json
import subprocess

def load_programs(file_path='programs.json'):
    with open(file_path, 'r') as f:
        return json.load(f)

def start_programs(programs):
    for program in programs:
        try:
            # 直接启动程序
            subprocess.Popen(program['exe'])
        except Exception as e:
            print(f"Failed to start {program['name']}: {e}")

if __name__ == "__main__":
    programs = load_programs()
    start_programs(programs)
