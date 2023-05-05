import json

from lona.html import HTML, H1, Div
from lona import App, View

from lona_html5_qrcode.html import Html5QRCodeScanner
from lona_picocss.html import InlineButton, Modal
from lona_picocss import install_picocss

app = App(__file__)

install_picocss(app, debug=True)

app.settings.PICOCSS_BRAND = 'lona-html5-qrcode'
app.settings.PICOCSS_TITLE = 'lona-html5-qrcode'


@app.route('/')
class QRCodeView(View):
    def handle_scan_result(self, scanner, data):
        self.modal.close()
        scanner.stop()

        self.result.set_text(f'{json.dumps(data)}\n')

    def start_scanning(self, input_event):
        self.scanner.start()
        self.modal.open()

    def stop_scanning(self, input_event):
        self.modal.close()
        self.scanner.stop()

    def handle_request(self, request):
        self.result = Div()

        self.scanner = Html5QRCodeScanner(
            handle_scan_result=self.handle_scan_result,
            theme='picocss',
            autostart=False,
        )

        self.modal = Modal(closeable=False)

        self.modal.get_body().nodes = [
            self.scanner,
        ]

        self.modal.get_footer().nodes = [
            InlineButton('Stop Scanning', handle_click=self.stop_scanning)
        ]

        return HTML(
            H1('QRCodeScanner'),
            self.result,
            self.modal,
            InlineButton('Scan QR-Code', handle_click=self.start_scanning),
        )


app.run()
