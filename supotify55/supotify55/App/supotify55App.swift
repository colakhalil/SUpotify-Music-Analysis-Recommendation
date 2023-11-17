//
//  supotify55App.swift
//  supotify55
//
//  Created by Furkan Emre Güler on 16.11.2023.
//

import SwiftUI

@main
struct supotify55App: App {
    static let apicaller : APICaller = APICaller()
    static let navigator : Navigator = Navigator()
    var body: some Scene {
        WindowGroup {
            LoginView()
        }
    }
}
