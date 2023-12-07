import SwiftUI
import UIKit

struct ImportExportView: View {
    @State private var importFileURL: URL?
    @State private var exportFileURL: URL?

    var body: some View {
        ZStack {
            Color.black.edgesIgnoringSafeArea(.all) // Set the background color to black

            VStack {
                Button("Import Data") {
                    let documentPicker = UIDocumentPickerViewController(documentTypes: ["public.json"], in: .import)
                    documentPicker.allowsMultipleSelection = false
                    documentPicker.delegate = DocumentPickerDelegate { selectedFileURL in
                        self.importFileURL = selectedFileURL
                        // Here you can use 'importFileURL' to process the selected JSON file
                    }
                    UIApplication.shared.windows.first?.rootViewController?.present(documentPicker, animated: true, completion: nil)
                }
                .padding()

                if let importFileURL = importFileURL {
                    Text("Selected File for Import: \(importFileURL.lastPathComponent)")
                        .foregroundColor(.white)
                }

                Button("Export Data") {
                    // Logic for exporting data
                    // Set 'exportFileURL' to the URL where you want to export the data
                }
                .padding()

                if let exportFileURL = exportFileURL {
                    Text("Selected File for Export: \(exportFileURL.lastPathComponent)")
                        .foregroundColor(.white)
                }
            }
        }
        .foregroundColor(.white) // Set the text color to white for better visibility
    }
}

class DocumentPickerDelegate: NSObject, UIDocumentPickerDelegate {
    let callback: (URL) -> Void

    init(callback: @escaping (URL) -> Void) {
        self.callback = callback
    }

    func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentsAt urls: [URL]) {
        guard let selectedFileURL = urls.first else { return }
        callback(selectedFileURL)
    }
}

struct ImportExportView_Previews: PreviewProvider {
    static var previews: some View {
        ImportExportView()
    }
}
