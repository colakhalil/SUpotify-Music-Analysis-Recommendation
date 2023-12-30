import Foundation

struct User: Identifiable, Decodable {
    var id: String = "default"
    var profilePicture: String = "default"
    // Add other properties as per your JSON structure
}

struct SearchResult: Decodable {
    var songs: [searchSong]
    var albums: [searchAlbum]
    var artists: [searchArtist]
}

struct searchSong: Decodable {
    var song_id: String
    var song_name: String
    var artist_id: String
    var release_date: String
    var rate: Double
}

struct searchAlbum: Decodable {
    var album_id: String
    var album_name: String
    var artist_id: String
    // Add other properties as per your JSON structure
}

struct searchArtist: Decodable {
    var artist_id: String
    var artist_name: String
    // Add other properties as per your JSON structure
}
