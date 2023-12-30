//
//  Album.swift
//  supotify55
//
//  Created by Furkan Emre Güler on 17.11.2023.
//

import Foundation

struct Album: Identifiable {
    let id: UUID
    let AlbumName: String
    let ArtistOfAlbum: String
    let CoverPage: String

    init(AlbumName: String, ArtistOfAlbum: String, CoverPage: String, id: UUID = UUID()) {
        self.AlbumName = AlbumName
        self.ArtistOfAlbum = ArtistOfAlbum
        self.CoverPage = CoverPage
        self.id = id
    }
}
 
