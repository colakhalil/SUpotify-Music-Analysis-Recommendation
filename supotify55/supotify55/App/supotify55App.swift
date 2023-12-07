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
            //PlaylistView(playlistID: "3HAdIN8wtU2UBo94fznOTm")
            //AlbumView(albumID: "3HAdIN8wtU2UBo94fznOTm")
            //SongRegistrationView()
        }
    }
}


