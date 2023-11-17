//
//  SpotifyWebView.swift
//  supotify55
//
//  Created by Furkan Emre Güler on 17.11.2023.
//

import SwiftUI
import WebKit

struct SpotifyWebView: View {
    private let url : String = "http://127.0.0.1:8008/sauth"
    var body: some View {
        GeometryReader { geometry in
            VStack {
                HStack{
                    Button(action: navigator.WebToLogin, label: {
                        Text("Login")
                            .foregroundColor(/*@START_MENU_TOKEN@*/.blue/*@END_MENU_TOKEN@*/)
                            .frame(width: 100, height: 50)
                            .padding()
                            .background(Color.yellow)
                            .cornerRadius(8)

                    })
                    Spacer()
                }
                .frame(height: 90)
                .frame(width: geometry.size.width) // Set width to device's width
                VStack{
                    WebView(url: URL(string: url)!)
                }
            }
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
