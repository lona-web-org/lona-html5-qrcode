# lona-html5-qrcode

![license MIT](https://img.shields.io/pypi/l/lona-html5-qrcode.svg)
![Python Version](https://img.shields.io/pypi/pyversions/lona-html5-qrcode.svg)
![Latest Version](https://img.shields.io/pypi/v/lona-html5-qrcode.svg)

lona-html5-qrcode provides [Html5-QRCode](https://www.npmjs.com/package/html5-qrcode) bindings for [Lona](https://lona-web.org)

[Demo](doc/screen-recording.gif)

(This demo is available in `test-script/test_script.py`)


## Installation

lona-html5-qrcode can be installed using pip

```
pip install lona lona-html5-qrcode
```


## Usage

```python
from lona.html import HTML, H1, Div
from lona import App, View

from lona_html5_qrcode.html import Html5QRCodeScanner

app = App(__file__)


@app.route('/')
class QRCodeView(View):
    def handle_scan_result(self, scanner, data):
        scanner.stop()
        self.result.set_text(f'{json.dumps(data)}\n')

    def handle_request(self, request):
        self.result = Div()

        return HTML(
            H1('QRCodeScanner'),
            self.result,
            Html5QRCodeScanner(
                handle_scan_result=self.handle_scan_result,
            ),
        )


app.run()

```


### Arguments

| Name | Type | Default | Description |
| - | - | - | - |
| handle_scan_result | Callable \| None | `None` | Callback that gets called on every scan result. Gets called with a reference to the scanner node, and the scan data |
| config | dict \| None | `None` | [html5-qrcode config](https://github.com/mebjas/html5-qrcode#extra-optional-configuration-in-start-method). Default is available using `Html5QRCodeScanner.get_default_config()` |
| theme | str | `''` | CSS theme name |
| autostart | bool | `False` | Start scanning on first render |


#### Default html5-qrcode config

```python
{
    'fps': 10,
    'qrbox': {
        'width': 100,
        'height': 100,
    },
    'rememberLastUsedCamera': True,
}
```


#### Themes

When `theme` is set, a CSS class named `f'html5-qrcode-{theme}'` gets added to `Html5QRCodeScanner`. This class then can be used for theming.

lona-html5-qrcode comes with a list of default themes builtin.

| Name | Description |
| - | - |
| picocss | Better integration into [lona-picocss](https://github.com/lona-web-org/lona-picocss) |


### Properties

| Name | Type | Description |
| - | - | - |
| handle_scan_result | Callable \| None | Callback that gets called on every result. Gets called with a reference to the scanner node, and the scan data |


### Methods

| Name | Return Type | Description |
| - | - | - |
| is_running() | bool | Check wether html5-qrcode is scanning |
| start() | None | Start html5-qrcode scanning |
| stop() | None | Stop html5-qrcode scanning |
| get_default_config() | dict | Returns the default config used for html5-qrcode |


## Troubleshooting

### Camera access is only supported in secure context like https or localhost

[Html5-QRCode](https://www.npmjs.com/package/html5-qrcode) uses the [browser media API](https://developer.mozilla.org/en-US/docs/Web/Media) scan QR-Codes. The browser grants access to this API only in [secure contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts). To get around this in development, use the Chrome flag `unsafely-treat-insecure-origin-as-secure`, like shown below.


![](doc/chrome-flags.png)