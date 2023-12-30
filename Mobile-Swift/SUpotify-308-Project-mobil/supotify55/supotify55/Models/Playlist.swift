//
//  Playlist.swift
//  supotify55
//
//  Created by Furkan Emre Güler on 17.11.2023.
//

 
import Foundation
import SwiftUI
import Combine

class Playlist: ObservableObject {
    @Published var name: String = "default"
    @Published var playlistID: String = "default"
    @Published var playlistPic: URL? // Changed to URL type
    @Published var songNumber: Int = -1
    @Published var songs : [Song] = []
}
