# -*- mode: python ; coding: utf-8 -*-
import sys
import platform

block_cipher = None

# 根据平台调整参数
is_windows = platform.system() == 'Windows'
is_macos = platform.system() == 'Darwin'
is_linux = platform.system() == 'Linux'

a = Analysis(
    ['cursor_pro_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('turnstilePatch', 'turnstilePatch'),
        ('cursor_auth_manager.py', '.'),
        ('names-dataset.txt', '.'),
    ],
    hiddenimports=[
        'PyQt5.QtWidgets', 
        'PyQt5.QtCore', 
        'PyQt5.QtGui',
        'PyQt5.sip'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 平台特定参数
exe_args = {
    'name': 'CursorProGUI',
    'debug': False,
    'strip': False,
    'upx': True,
    'upx_exclude': [],
    'runtime_tmpdir': None,
    'console': False,  # 在所有平台上隐藏控制台
    'disable_windowed_traceback': False,
}

# Windows特定参数
if is_windows:
    try:
        # 确保在Windows上以管理员权限运行
        exe_args['uac_admin'] = True
        exe_args['manifest'] = '<requestedExecutionLevel level="requireAdministrator" uiAccess="false"/>'
    except Exception as e:
        print(f"警告: 设置Windows管理员权限时出错: {str(e)}")
    
# macOS特定参数
if is_macos:
    # macOS上，使用argv_emulation
    exe_args['argv_emulation'] = True
    # 添加Info.plist以配置应用程序特性
    exe_args['info_plist'] = {
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'CFBundleDisplayName': 'CursorProGUI',
        'CFBundleName': 'CursorProGUI',
        'CFBundleIdentifier': 'com.cursorpro.gui',
        'CFBundleVersion': '1.0.0',
        'CFBundlePackageType': 'APPL',
        'LSApplicationCategoryType': 'public.app-category.utilities',
        'NSHighResolutionCapable': True,
    }
else:
    exe_args['argv_emulation'] = False

# Linux特定参数
if is_linux:
    # Linux上不需要特殊配置
    pass

# 创建可执行文件
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    **exe_args,  # 使用平台特定参数
) 