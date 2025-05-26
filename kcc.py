#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012-2014 Ciro Mattia Gonano <ciromattia@gmail.com>
# Copyright (c) 2013-2019 Pawel Jastrzebski <pawelj@iosphe.re>
#
# Permission to use, copy, modify, and/or distribute this software for
# any purpose with or without fee is hereby granted, provided that the
# above copyright notice and this permission notice appear in all
# copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
# AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
# DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA
# OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

import os
import sys
import platform

from pathlib import Path

if sys.version_info < (3, 8, 0):
    print('ERROR: This is a Python 3.8+ script!')
    sys.exit(1)

def modify_path():
    # 首先尝试从设置中获取用户自定义路径
    from PySide6.QtCore import QSettings
    settings = QSettings('ciromattia', 'kcc')
    custom_path = settings.value('options').get('kindlePreviewerPath', '')

    if platform.system() == 'Darwin':
        mac_paths = [
            '/Applications/Kindle Comic Creator/Kindle Comic Creator.app/Contents/MacOS',
            '/Applications/Kindle Previewer 3.app/Contents/lib/fc/bin/',
        ]
        if getattr(sys, 'frozen', False):
            os.environ['PATH'] += os.pathsep + os.pathsep.join(mac_paths +
                [
                    '/opt/homebrew/bin',
                    '/usr/local/bin',
                    '/usr/bin',
                    '/bin',
                ]
            )
            os.chdir(os.path.dirname(os.path.abspath(sys.executable)))
        else:
            os.environ['PATH'] += os.pathsep + os.pathsep.join(mac_paths)
            os.chdir(os.path.dirname(os.path.abspath(__file__)))

    elif platform.system() == 'Linux':
        if getattr(sys, 'frozen', False):
            os.environ['PATH'] += os.pathsep + os.pathsep.join(
                [
                    str(Path.home() / ".local" / "bin"),
                    '/opt/homebrew/bin',
                    '/usr/local/bin',
                    '/usr/bin',
                    '/bin',
                ]
            )
            os.chdir(os.path.dirname(os.path.abspath(sys.executable)))
        else:
            os.chdir(os.path.dirname(os.path.abspath(__file__)))

    elif platform.system() == 'Windows':
        win_paths = [
            os.path.expandvars('%LOCALAPPDATA%\\Amazon\\KC2'),
            os.path.expandvars('%LOCALAPPDATA%\\Amazon\\Kindle Previewer 3\\lib\\fc\\bin\\'),
            os.path.expandvars('%UserProfile%\\Kindle Previewer 3\\lib\\fc\\bin\\'),
            'C:\\Apps\\Kindle Previewer 3\\lib\\fc\\bin',
            'D:\\Apps\\Kindle Previewer 3\\lib\\fc\\bin',
            'E:\\Apps\\Kindle Previewer 3\\lib\\fc\\bin',
            'C:\\Program Files\\7-Zip',
            'D:\\Program Files\\7-Zip',
            'E:\\Program Files\\7-Zip',
            # 'D:\\Program Files (x86)\\Kindle Previewer 3',
        ]
        # 如果用户设置了自定义路径，添加到环境变量中
        if custom_path and os.path.exists(custom_path):
            win_paths.append(custom_path)

        # 获取当前 PATH 中的路径
        current_paths = set(os.environ.get('PATH', '').split(os.pathsep))

        # 过滤出存在且不在当前 PATH 中的路径
        existing_paths = [t_path for t_path in win_paths
                          if os.path.exists(t_path) and t_path not in current_paths]



        if getattr(sys, 'frozen', False):
            if len(existing_paths):
                os.environ['PATH'] += os.pathsep + os.pathsep.join(existing_paths)
            os.chdir(os.path.dirname(os.path.abspath(sys.executable)))
        else:
            if len(existing_paths):
                os.environ['PATH'] += os.pathsep + os.pathsep.join(existing_paths)
            os.chdir(os.path.dirname(os.path.abspath(__file__)))


from multiprocessing import freeze_support, set_start_method
from kindlecomicconverter.startup import start

if __name__ == "__main__":
    modify_path()
    set_start_method('spawn')
    freeze_support()
    start()

