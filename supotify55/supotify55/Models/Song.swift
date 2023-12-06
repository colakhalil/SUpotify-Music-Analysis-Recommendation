//
//  Song.swift
//  supotify55
//
//  Created by Furkan Emre Güler on 17.11.2023.
//

import Foundation

struct Song {
    let songID: String
    let songName: String
    let duration: Int
    let releaseYear: String
    let artist: String
    let songRating: Int
    var genre: String = "default"
    var mood: String = "default"
}
