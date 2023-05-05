class LonaHtml5QRCodeScannerWidget {
    constructor(lonaWindow, rootNode, widgetData) {
        this.lonaWindow = lonaWindow;
        this.rootNode = rootNode;
        this.widgetData = widgetData;

        this.html5QrcodeScanner = undefined;

        this.render(widgetData);
    }

    onDataUpdated(widgetData) {
        this.render(widgetData);
    }

    getConfig() {
        let config = JSON.parse(
            JSON.stringify(this.widgetData.data['scannerConfig']));

        config['supportedScanTypes'] = [Html5QrcodeScanType.SCAN_TYPE_CAMERA];

        return config;
    }

    stopScanning() {
        if(this.html5QrcodeScanner === undefined) {
            return;
        }

        this.html5QrcodeScanner.clear();
    }

    startScanning() {
        this.stopScanning();

        this.html5QrcodeScanner = new Html5QrcodeScanner(
            this.widgetData.data.scannerId,
            this.getConfig(),
            false,  // verbose
        );

        this.html5QrcodeScanner.render((decodedText, decodedResult) => {
            this.lonaWindow.fire_input_event(
                this.rootNode,
                'qrcode-scan-result',
                {
                    decodedText: decodedText,
                    decodedResult: decodedResult,
                },
            );
        });
    }

    render(widgetData) {
        if(widgetData.data.running) {
            this.startScanning();
        } else {
            this.stopScanning();
        }
    }
}


Lona.register_widget_class('LonaHtml5QRCodeScannerWidget', LonaHtml5QRCodeScannerWidget);
