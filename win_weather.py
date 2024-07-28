import os
import json
import requests
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import webbrowser
from datetime import datetime, timedelta
import threading
import winreg
import pystray
from PIL import Image, ImageDraw

# 配置
api_key = '3a85705575145b64044cd8b80575f93a'  # 替换为你的高德API密钥
config_file = os.path.join(os.path.expanduser("~"), 'weather_config.json')
icon_path = 'weather_icon.ico' 

def get_adcode(city_name):
    url = f"https://restapi.amap.com/v3/config/district?key={api_key}&keywords={city_name}&subdistrict=0"
    response = requests.get(url)
    data = response.json()
    if data['status'] == '1' and data['count'] != '0':
        return data['districts'][0]['adcode']
    else:
        raise Exception("获取城市编码失败")

def get_weather_forecast(adcode):
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={api_key}&city={adcode}&extensions=all"
    response = requests.get(url)
    weather_data = response.json()
    if weather_data['status'] == '1':
        forecasts = weather_data['forecasts'][0]['casts']
        today_weather = forecasts[0]
        tomorrow_weather = forecasts[1]
        return today_weather, tomorrow_weather
    else:
        raise Exception(f"获取天气数据失败: {weather_data['info']} (infocode: {weather_data['infocode']})")

def save_config(config):
    with open(config_file, 'w') as f:
        json.dump(config, f)

def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        return None

def add_to_startup(exe_path, name):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, name, 0, winreg.REG_SZ, exe_path)
    winreg.CloseKey(key)

def remove_from_startup(name):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
    try:
        winreg.DeleteValue(key, name)
    except FileNotFoundError:
        pass
    winreg.CloseKey(key)

def show_gui():
    def save_and_quit():
        city_name = city_entry.get()
        selected_info = [info_labels[i] for i, var in enumerate(info_vars) if var.get()]
        update_interval = update_interval_entry.get()
        auto_start = auto_start_var.get()
        
        if not selected_info:
            messagebox.showerror("错误", "请至少选择一个信息选项。")
            return
        if not update_interval.isdigit() or int(update_interval) <= 0:
            messagebox.showerror("错误", "请提供一个有效的更新间隔时间（分钟）。")
            return
        try:
            adcode = get_adcode(city_name)
            config = {
                "city_name": city_name,
                "adcode": adcode,
                "selected_info": selected_info,
                "update_interval": int(update_interval),
                "auto_start": auto_start
            }
            save_config(config)

            # 处理开机自启动
            exe_path = os.path.abspath(sys.argv[0])
            if auto_start:
                add_to_startup(exe_path, "weather4u")
            else:
                remove_from_startup("weather4u")

            root.destroy()
        except Exception as e:
            messagebox.showerror("错误", f"获取城市编码失败: {e}")

    root = tk.Tk()
    root.title("设置")

    tk.Label(root, text="请输入城市名称：").grid(row=0, column=0, padx=10, pady=5)
    city_entry = tk.Entry(root)
    city_entry.grid(row=0, column=1, padx=10, pady=5)

    info_labels = ["dayweather", "nightweather", "daytemp", "nighttemp", "daywind", "nightwind", "daypower", "nightpower", "humidity"]
    display_labels = ["白天天气现象", "晚上天气现象", "白天温度", "晚上温度", "白天风向", "晚上风向", "白天风力", "晚上风力", "空气湿度"]
    info_vars = [tk.BooleanVar() for _ in info_labels]
    for i, label in enumerate(display_labels):
        tk.Checkbutton(root, text=label, variable=info_vars[i]).grid(row=i+1, columnspan=2, padx=10, pady=5)

    tk.Label(root, text="自动更新间隔（分钟）：").grid(row=len(display_labels) + 1, column=0, padx=10, pady=5)
    update_interval_entry = tk.Entry(root)
    update_interval_entry.grid(row=len(display_labels) + 1, column=1, padx=10, pady=5)

    auto_start_var = tk.BooleanVar()
    auto_start_check = tk.Checkbutton(root, text="开机自启动", variable=auto_start_var)
    auto_start_check.grid(row=len(display_labels) + 2, columnspan=2, padx=10, pady=5)

    tk.Button(root, text="保存并退出", command=save_and_quit).grid(row=len(display_labels) + 3, columnspan=2, padx=10, pady=10)

    root.mainloop()

def fetch_and_notify(notifier, config):
    try:
        adcode = config['adcode']
        selected_info = config['selected_info']

        today_weather, tomorrow_weather = get_weather_forecast(adcode)

        today = datetime.now()
        tomorrow = datetime.now() + timedelta(days=1)

        today_str = f"{today.month}月{today.day}日"
        tomorrow_str = f"{tomorrow.month}月{tomorrow.day}日"

        def format_message(weather, day_str, day_label):
            message = f"{day_str}（{day_label}）："
            if "dayweather" in selected_info:
                message += f"白天天气：{weather['dayweather']}，"
            if "nightweather" in selected_info:
                message += f"晚上天气：{weather['nightweather']}，"
            if "daytemp" in selected_info:
                message += f"白天温度：{weather['daytemp']}°C，"
            if "nighttemp" in selected_info:
                message += f"晚上温度：{weather['nighttemp']}°C，"
            if "daywind" in selected_info:
                message += f"白天风向：{weather['daywind']}，"
            if "nightwind" in selected_info:
                message += f"晚上风向：{weather['nightwind']}，"
            if "daypower" in selected_info:
                message += f"白天风力：{weather['daypower']}级，"
            if "nightpower" in selected_info:
                message += f"晚上风力：{weather['nightpower']}级，"
            if "humidity" in selected_info:
                message += f"空气湿度：{weather['humidity']}%"
            return message.strip('，')

        today_message = format_message(today_weather, today_str, "今天")
        tomorrow_message = format_message(tomorrow_weather, tomorrow_str, "明天")

        notifier.notify(today_message, title="今天天气")
        time.sleep(5)  # 延长延迟时间
        notifier.notify(tomorrow_message, title="明天天气")
    except Exception as e:
        notifier.notify(f"错误: {str(e)}", title="天气")

def main():
    config = load_config()
    if config is None:
        show_gui()
        config = load_config()

    if 'selected_info' not in config:
        config['selected_info'] = ["dayweather", "nightweather", "daytemp", "nighttemp", "daywind", "nightwind", "daypower", "nightpower", "humidity"]

    if 'update_interval' not in config:
        config['update_interval'] = 60  # 默认每60分钟更新一次，这个好像没什么用，为了不修更多BUG我决定留着

    icon_image = Image.open(icon_path)
    
    def on_clicked(icon, item):
        if str(item) == "设置":
            show_gui()
        elif str(item) == "关于":
            webbrowser.open("https://github.com/rtlnut/weather4u")
        elif str(item) == "退出":
            icon.stop()

    menu = pystray.Menu(
        pystray.MenuItem("设置", on_clicked),
        pystray.MenuItem("关于", on_clicked),
        pystray.MenuItem("退出", on_clicked)
    )

    icon = pystray.Icon("weather4u", icon_image, "weather4u", menu)

    def update_weather_periodically():
        while True:
            fetch_and_notify(icon, config)
            time.sleep(config['update_interval'] * 60)

    weather_thread = threading.Thread(target=update_weather_periodically)
    weather_thread.daemon = True
    weather_thread.start()

    icon.run()

if __name__ == "__main__":
    main()
