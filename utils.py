import os
import sys
import platform
import random
import subprocess
import ctypes
import sys
import traceback

def is_admin():
    """
    检查当前进程是否具有管理员/root权限
    
    Returns:
        bool: 如果具有管理员权限则返回True，否则返回False
    """
    try:
        if platform.system() == "Windows":
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:  # Linux & macOS (Unix-like)
            return os.geteuid() == 0  # 0是root用户的ID
    except Exception as e:
        print(f"检查管理员权限时出错: {e}")
        # 如果无法检测，返回False以便程序尝试获取权限
        return False

def restart_as_admin():
    """
    以管理员/root权限重新启动当前程序
    
    Returns:
        bool: 如果成功启动了提权进程则返回True，否则返回False
    """
    try:
        # 获取当前脚本的完整路径
        script = sys.argv[0]
        args = sys.argv[1:]
        
        if platform.system() == "Windows":
            # Windows 系统使用 ShellExecute 以管理员身份运行
            ctypes.windll.shell32.ShellExecuteW(
                None,  # hwnd
                "runas",  # 操作 - "runas"表示以管理员身份运行
                sys.executable,  # 程序
                f'"{script}" {" ".join(args)}',  # 参数
                None,  # 默认目录
                1  # SW_SHOWNORMAL - 正常显示窗口
            )
            return True  # Windows下ShellExecuteW不会抛出异常，除非返回值<=32
            
        elif platform.system() == "Darwin":  # macOS
            # macOS 下使用 osascript 执行AppleScript以获取管理员权限
            cmd = [
                'osascript', '-e', 
                'do shell script "' + sys.executable + ' \\"' + script + '\\" ' + ' '.join(args) + '" with administrator privileges'
            ]
            subprocess.Popen(cmd)
            return True
            
        else:  # Linux
            # Linux下使用pkexec, sudo或gksu
            for tool in ["pkexec", "sudo", "gksudo", "kdesudo"]:
                try:
                    if subprocess.call(["which", tool], stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0:
                        # 工具存在，使用它
                        cmd = [tool, sys.executable, script] + args
                        subprocess.Popen(cmd)
                        return True
                except:
                    continue
                    
            # 如果没有找到任何提权工具，则尝试使用sudo（可能会在终端要求密码）
            try:
                cmd = ["sudo", sys.executable, script] + args
                subprocess.Popen(cmd)
                return True
            except:
                pass
                
        # 如果所有尝试都失败
        return False
        
    except Exception as e:
        print(f"尝试以管理员权限重启程序时出错: {e}")
        traceback.print_exc()
        return False
        
def ensure_admin():
    """
    确保程序以管理员权限运行，如果不是则尝试重启
    
    Returns:
        bool: 如果程序已经有管理员权限或成功重启则返回True，否则返回False
    """
    if is_admin():
        return True
    else:
        success = restart_as_admin()
        if success:
            # 退出当前非管理员实例
            sys.exit(0)
        return False

def get_user_documents_path():
    """Get user documents path"""
    if platform.system() == "Windows":
        return os.path.expanduser("~\\Documents")
    else:
        return os.path.expanduser("~/Documents")
    
def get_default_driver_path(browser_type='chrome'):
    """Get default driver path based on browser type"""
    browser_type = browser_type.lower()
    if browser_type == 'chrome':
        return get_default_chrome_driver_path()
    elif browser_type == 'edge':
        return get_default_edge_driver_path()
    elif browser_type == 'firefox':
        return get_default_firefox_driver_path()
    elif browser_type == 'brave':
        # Brave 使用 Chrome 的 driver
        return get_default_chrome_driver_path()
    else:
        # Default to Chrome if browser type is unknown
        return get_default_chrome_driver_path()

def get_default_chrome_driver_path():
    """Get default Chrome driver path"""
    if sys.platform == "win32":
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "drivers", "chromedriver.exe")
    elif sys.platform == "darwin":
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "drivers", "chromedriver")
    else:
        return "/usr/local/bin/chromedriver"

def get_default_edge_driver_path():
    """Get default Edge driver path"""
    if sys.platform == "win32":
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "drivers", "msedgedriver.exe")
    elif sys.platform == "darwin":
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "drivers", "msedgedriver")
    else:
        return "/usr/local/bin/msedgedriver"
        
def get_default_firefox_driver_path():
    """Get default Firefox driver path"""
    if sys.platform == "win32":
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "drivers", "geckodriver.exe")
    elif sys.platform == "darwin":
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "drivers", "geckodriver")
    else:
        return "/usr/local/bin/geckodriver"

def get_default_brave_driver_path():
    """Get default Brave driver path (uses Chrome driver)"""
    # Brave 浏览器基于 Chromium，所以使用相同的 chromedriver
    return get_default_chrome_driver_path()

def get_default_browser_path(browser_type='chrome'):
    """Get default browser executable path"""
    browser_type = browser_type.lower()
    
    if sys.platform == "win32":
        if browser_type == 'chrome':
            # 尝试在 PATH 中找到 Chrome
            try:
                import shutil
                chrome_in_path = shutil.which("chrome")
                if chrome_in_path:
                    return chrome_in_path
            except:
                pass
            # 使用默认路径
            return r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        elif browser_type == 'edge':
            return r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        elif browser_type == 'firefox':
            return r"C:\Program Files\Mozilla Firefox\firefox.exe"
        elif browser_type == 'opera':
            # 尝试多个可能的 Opera 路径
            opera_paths = [
                r"C:\Program Files\Opera\opera.exe",
                r"C:\Program Files (x86)\Opera\opera.exe",
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'Opera', 'launcher.exe'),
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'Opera', 'opera.exe')
            ]
            for path in opera_paths:
                if os.path.exists(path):
                    return path
            return opera_paths[0]  # 返回第一个路径，即使它不存在
        elif browser_type == 'operagx':
            # 尝试多个可能的 Opera GX 路径
            operagx_paths = [
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'Opera GX', 'launcher.exe'),
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'Opera GX', 'opera.exe'),
                r"C:\Program Files\Opera GX\opera.exe",
                r"C:\Program Files (x86)\Opera GX\opera.exe"
            ]
            for path in operagx_paths:
                if os.path.exists(path):
                    return path
            return operagx_paths[0]  # 返回第一个路径，即使它不存在
        elif browser_type == 'brave':
            # Brave 浏览器的默认安装路径
            paths = [
                os.path.join(os.environ.get('PROGRAMFILES', ''), 'BraveSoftware/Brave-Browser/Application/brave.exe'),
                os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'BraveSoftware/Brave-Browser/Application/brave.exe'),
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'BraveSoftware/Brave-Browser/Application/brave.exe')
            ]
            for path in paths:
                if os.path.exists(path):
                    return path
            return paths[0]  # 返回第一个路径，即使它不存在
    
    elif sys.platform == "darwin":
        if browser_type == 'chrome':
            return "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        elif browser_type == 'edge':
            return "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
        elif browser_type == 'firefox':
            return "/Applications/Firefox.app/Contents/MacOS/firefox"
        elif browser_type == 'brave':
            return "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
        elif browser_type == 'opera':
            return "/Applications/Opera.app/Contents/MacOS/Opera"
        elif browser_type == 'operagx':
            return "/Applications/Opera GX.app/Contents/MacOS/Opera"
        
    else:  # Linux
        if browser_type == 'chrome':
            # 尝试多种可能的名称
            chrome_names = ["google-chrome", "chrome", "chromium", "chromium-browser"]
            for name in chrome_names:
                try:
                    import shutil
                    path = shutil.which(name)
                    if path:
                        return path
                except:
                    pass
            return "/usr/bin/google-chrome"
        elif browser_type == 'edge':
            return "/usr/bin/microsoft-edge"
        elif browser_type == 'firefox':
            return "/usr/bin/firefox"
        elif browser_type == 'opera':
            return "/usr/bin/opera"
        elif browser_type == 'operagx':
            # 尝试常见的 Opera GX 路径
            operagx_names = ["opera-gx"]
            for name in operagx_names:
                try:
                    import shutil
                    path = shutil.which(name)
                    if path:
                        return path
                except:
                    pass
            return "/usr/bin/opera-gx"
        elif browser_type == 'brave':
            # 尝试常见的 Brave 路径
            brave_names = ["brave", "brave-browser"]
            for name in brave_names:
                try:
                    import shutil
                    path = shutil.which(name)
                    if path:
                        return path
                except:
                    pass
            return "/usr/bin/brave-browser"
    
    # 如果找不到指定的浏览器类型，则返回 Chrome 的路径
    return get_default_browser_path('chrome')

def get_linux_cursor_path():
    """Get Linux Cursor path"""
    possible_paths = [
        "/opt/Cursor/resources/app",
        "/usr/share/cursor/resources/app",
        "/opt/cursor-bin/resources/app",
        "/usr/lib/cursor/resources/app",
        os.path.expanduser("~/.local/share/cursor/resources/app")
    ]
    
    # return the first path that exists
    return next((path for path in possible_paths if os.path.exists(path)), possible_paths[0])

def get_random_wait_time(config, timing_key):
    """Get random wait time based on configuration timing settings
    
    Args:
        config (dict): Configuration dictionary containing timing settings
        timing_key (str): Key to look up in the timing settings
        
    Returns:
        float: Random wait time in seconds
    """
    try:
        # Get timing value from config
        timing = config.get('Timing', {}).get(timing_key)
        if not timing:
            # Default to 0.5-1.5 seconds if timing not found
            return random.uniform(0.5, 1.5)
            
        # Check if timing is a range (e.g., "0.5-1.5" or "0.5,1.5")
        if isinstance(timing, str):
            if '-' in timing:
                min_time, max_time = map(float, timing.split('-'))
            elif ',' in timing:
                min_time, max_time = map(float, timing.split(','))
            else:
                # Single value, use it as both min and max
                min_time = max_time = float(timing)
        else:
            # If timing is a number, use it as both min and max
            min_time = max_time = float(timing)
            
        return random.uniform(min_time, max_time)
        
    except (ValueError, TypeError, AttributeError):
        # Return default value if any error occurs
        return random.uniform(0.5, 1.5) 