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
            VStack(spacing: 0) {
                HStack {
                    Button(action: {
                        navigator.WebToLogin()
                    }) {
                        Text("Login")
                            .foregroundColor(.green)
                            .font(Font.custom("Avantgarde Gothic", size: 18))
                            .padding(.top, 30)
                    }
                    .padding(.leading, 45)
                    Spacer()
                }
                .frame(height: 90)
                .background(Color.black)

                WebView(url: URL(string: url)!)
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            }
            .background(Color.white)
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
