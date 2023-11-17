//
//  SpotifyWebView.swift
//  supotify55
//
//  Created by Furkan Emre Güler on 17.11.2023.
//

import SwiftUI
import WebKit

struct SpotifyWebView: View {
    private let url: String = "http://127.0.0.1:8008/sauth"
    
    var body: some View {
        GeometryReader { geometry in
            VStack(spacing: 0) { // Set spacing to 0 to eliminate any default spacing
                HStack {
                    Button(action: navigator.WebToLogin) {
                        Text("Login")
                            .foregroundColor(.white)
                            .frame(width: 60, height: 20)
                            .padding()
                            .background(Color.blue)
                            .cornerRadius(8)
                    }
                    .padding(.leading, 20)
                    Spacer()
                }
                .frame(height: 90)
                .background(Color.green) // Set the background color of the HStack containing the button

                WebView(url: URL(string: url)!)
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            }
            .background(Color.white) // Set the background color of the VStack
            .edgesIgnoringSafeArea(.all)
        }
    }
}




struct WebView: UIViewRepresentable {
    var url: URL

    func makeUIView(context: Context) -> WKWebView {
        return WKWebView()
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {
        let request = URLRequest(url: url)
        uiView.load(request)
    }
}


struct SpotifyWebView_Previews: PreviewProvider {
    static var previews: some View {
        SpotifyWebView()
    }
}
