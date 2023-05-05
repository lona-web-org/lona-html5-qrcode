from uuid import uuid1

from lona.static_files import Script, StyleSheet, SORT_ORDER
from lona.html import Div


class Html5QRCodeScanner(Div):
    WIDGET = 'LonaHtml5QRCodeScannerWidget'

    STATIC_FILES = [
        Script(
            name='lona-html5-qrcode.js',
            path='../static/lona-html5-qrcode/dist/html5-qrcode.min.js',
            url='/lona-html5-qrcode/lona-html5-qrcode.js',
            sort_order=SORT_ORDER.FRAMEWORK,
        ),
        Script(
            name='lona-html5-qrcode/widgets.js',
            path='../static/lona-html5-qrcode/widgets.js',
            url='/lona-html5-qrcode/widgets.js',
            sort_order=SORT_ORDER.LIBRARY,
        ),
        StyleSheet(
            name='lona-html5-qrcode/themes.css',
            path='../static/lona-html5-qrcode/themes.css',
            url='/lona-html5-qrcode/themes.css',
            sort_order=SORT_ORDER.LIBRARY,
        ),
    ]

    def get_default_config(self):
        return {
            'fps': 10,
            'qrbox': {
                'width': 100,
                'height': 100,
            },
            'rememberLastUsedCamera': True,
        }

    def __init__(
            self,
            *args,
            handle_scan_result=None,
            theme='',
            config=None,
            autostart=True,
            **kwargs,
    ):

        super().__init__(*args, **kwargs)

        if handle_scan_result is not None:
            self.handle_scan_result = handle_scan_result

        # generate scanner id
        self.scanner_id = f'html5-qrcode-scanner-{uuid1().hex}'

        self.id_list.add(self.scanner_id)
        self.class_list.add('html5-qrcode-scanner')

        if theme:
            self.class_list.add(f'html5-qrcode-{theme}')

        # setup widget data
        self.widget_data = {
            'scannerId': self.scanner_id,
            'scannerConfig': config or self.get_default_config(),
            'running': False,
        }

        if autostart:
            self.start()

    # start / stop
    def is_running(self):
        return self.widget_data['running']

    def start(self):
        self.widget_data['running'] = True

    def stop(self):
        self.widget_data['running'] = False

    # scan results
    def handle_scan_result(self, scanner, data):
        pass

    def handle_input_event(self, input_event):
        if input_event.name != 'qrcode-scan-result':
            return input_event

        if not self.is_running():
            return

        return self.handle_scan_result(
            scanner=self,
            data=input_event.data,
        )
