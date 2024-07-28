import subprocess
import os
import shutil

# 获取当前目录
current_dir = os.path.abspath(os.path.dirname(__file__))

# 文件路径
script_path = os.path.join(current_dir, "win_weather.py")
icon_path = os.path.join(current_dir, "weather_icon.ico")

# 自定义的可执行文件名称
exe_name = "weather4u"

# 输出路径
output_path = current_dir

# pyinstaller 打包命令
command = [
    "pyinstaller",
    "--onefile",
    "--windowed",
    "--name", exe_name,
    "--icon", icon_path,
    "--distpath", output_path,
    script_path
]

# 运行打包命令
try:
    subprocess.run(command, check=True)
    print(f"{exe_name}.exe created successfully in {output_path}.")
except subprocess.CalledProcessError as e:
    print(f"Failed to create {exe_name}.exe: {e}")

# 清理构建文件夹和规范化配置文件
for folder in ["build"]:
    folder_path = os.path.join(current_dir, folder)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

spec_file = os.path.join(current_dir, f"{exe_name}.spec")
if os.path.exists(spec_file):
    os.remove(spec_file)
