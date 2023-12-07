//
//  User.swift
//  supotify55
//
//  Created by Furkan Emre Güler on 17.11.2023.
//

import Foundation

let myUser = UserData.sharedUser

class UserData: ObservableObject {
    static let sharedUser = UserData()
    
    @Published var email: String = "default"
    @Published var password: String = "default"
    @Published var username: String = "default"
    @Published var profilePicture: String = "default"
    @Published var lastListenedSong: String = "default"
    @Published var friends: [String] = ["default"]
    @Published var friendsCount: Int = -1
    @Published var playlists : [Playlist] = []
    
    private init() {
        apicaller.getUserPlaylists()
    }
}
