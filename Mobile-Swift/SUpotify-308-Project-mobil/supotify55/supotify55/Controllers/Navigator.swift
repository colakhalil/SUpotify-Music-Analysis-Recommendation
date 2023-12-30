//
//  Navigator.swift
//  supotify55
//
//  Created by Furkan Emre Güler on 17.11.2023.
//

import Foundation
import SwiftUI

let navigator = Navigator.navigator

class Navigator {
    static let navigator = Navigator()
    func LoginToMain(email: String) {
        DispatchQueue.main.async {
            if let window = UIApplication.shared.windows.first {
                let mainPageView = MainPageView(email: email) // Pass the email parameter here
                window.rootViewController = UIHostingController(rootView: mainPageView)
                window.makeKeyAndVisible()
            }
        }
    }
    func LoginToSignup() {
        DispatchQueue.main.async {
            if let window = UIApplication.shared.windows.first {
                window.rootViewController = UIHostingController(rootView: SignUpView())
                window.makeKeyAndVisible()
            }
        }
    }
    func SignupToLogin() {
        DispatchQueue.main.async {
            if let window = UIApplication.shared.windows.first {
                window.rootViewController = UIHostingController(rootView: LoginView())
                window.makeKeyAndVisible()
            }
        }
    }
    func WebToLogin() {
        DispatchQueue.main.async {
            if let window = UIApplication.shared.windows.first {
                window.rootViewController = UIHostingController(rootView: LoginView())
                window.makeKeyAndVisible()
            }
        }
    }
    func SignupToWeb() {
        DispatchQueue.main.async {
            if let window = UIApplication.shared.windows.first {
                window.rootViewController = UIHostingController(rootView: SpotifyWebView())
                window.makeKeyAndVisible()
            }
        }
    }
}
