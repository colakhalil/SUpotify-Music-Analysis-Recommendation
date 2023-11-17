//
//  PlaylistView.swift
//  SUpotify
//
//  Created by Furkan Emre Güler on 16.11.2023.
//

//
//  PlaylistView.swift
//  SUpotify
//
//  Created by Ayça Ataer on 13.11.2023.
//

import SwiftUI


struct Song: Identifiable, Decodable {
    let id = UUID()
    let title: String
    let artists: [String]
    let duration: String
    let lyrics: String
    let genre: [String]
    let rate: Int
    let mood: [String]
    let recordingType: String
    let instruments: [String]
    let playCount: Int
    let releaseYear: String
    let dateAdded: String
    let thumbnail: URL
}


struct DisplaySongView: View {
    var song: Song

    var body: some View {
        Button(action: {
                   
                }) {
                    HStack {
                        AsyncImage(url: song.thumbnail) { image in
                            image.resizable()
                        } placeholder: {
                            Color.gray
                        }
                        .frame(width: 50, height: 50)
                        .cornerRadius(5)
                        
                        VStack(alignment: .leading) {
                            Text(song.title).bold()
                            Text(song.artists.joined(separator: ", "))
                            HStack {
                                ForEach(song.genre, id: \.self) { genre in
                                    Text(genre)
                                        .padding(3)
                                        .background(Color.gray.opacity(0.2))
                                        .cornerRadius(5)
                                }
                            }
                        }
                    }
            Spacer()

            HStack {
                ForEach(0..<song.rate, id: \.self) { _ in
                    Image(systemName: "star.fill")
                        .foregroundColor(.yellow)
                }
            }
        }
        
    }
}

struct PlaylistView: View {
    var songs: [Song]
    let playlistPhotoURL: URL  // URL for the playlist photo

    var body: some View {
        NavigationView {
            VStack {
                // Playlist photo at the top with specified horizontal padding
                AsyncImage(url: playlistPhotoURL) { image in
                    image.resizable()
                } placeholder: {
                    Color.gray
                }
                .frame(height: 150)
                .cornerRadius(10)
                .padding(.horizontal, 120)
                // Custom title
                Text("Playlist")
                    .font(.largeTitle)
                    .bold()

                // List of songs
                List(songs) { song in
                    DisplaySongView(song: song)
                }
            }
        }
        .background(Color.black)
    }
}


struct PlaylistView_Previews: PreviewProvider {
    static var previews: some View {
        PlaylistView(songs: Array(repeating: Song(title: "Beni Böyle Hatırla", artists: ["Çetin Dilşiz"], duration: "2:48",
                                                  lyrics: "Here would be the lyrics of the song...",
                                                  genre: ["Pop", "Dance"],
                                                  rate: 5,
                                                  mood: ["Uplifting"],
                                                  recordingType: "Studio",
                                                  instruments: ["Guitar", "Piano", "Drums"],
                                                  playCount: 100,
                                                  releaseYear: "2021",
                                                  dateAdded: "2023-04-15",
                                                  thumbnail: URL(string: "https://example.com/image.jpg")!),
                        count: 10),
                 playlistPhotoURL: URL(string: "https://example.com/playlist_cover.jpg")!)
    }
}
extension Array {
    static func repeating(element: Element, times: Int) -> [Element] {
        return Array(repeating: element, count: times)
    }
}
