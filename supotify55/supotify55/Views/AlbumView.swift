//
//  AlbumView.swift
//  supotify55
//
//  Created by Furkan Emre Güler on 17.11.2023.
//

import SwiftUI

struct AlbumView: View {
    @State var albumID: String
    @State private var songs: [Song] = []
    @State private var albumPhotoURL: URL? = URL(string: "https://example.com/album_cover.jpg")
    @State private var albumName: String = "Default"
    @State private var artistName: String? = "Volkan Konak"
    @State private var albumRating: Int = 0 // Default rating
    @State private var jsonObject: [String: Any] = [:]

    var body: some View {
        NavigationView {
            VStack {
                AsyncImage(url: albumPhotoURL) { image in
                    image.resizable()
                        .frame(height: 150)
                        .cornerRadius(10)
                } placeholder: {
                    Color.gray
                        .frame(height: 150)
                        .cornerRadius(10)
                }
                .padding(.horizontal, 120)

                HStack {
                    VStack(alignment: .leading) {
                        Text(albumName)
                            .font(.largeTitle)
                            .bold()
                            .foregroundColor(.white)

                        if let artist = artistName {
                            Text(artist)
                                .font(.title2)
                                .foregroundColor(.white)
                        }
                    }
                    .padding(.leading, 20)

                    Spacer()

                    StarRatingView(albumID: albumID,rating: $albumRating)
                        .padding(.trailing, 20)
                }

                List(songs, id: \.songID) { song in
                    DisplaySongView(song: song)
                        .listRowBackground(Color.black)
                }
                .listStyle(PlainListStyle())
            }
            .background(Color.black)
        }
        .navigationViewStyle(StackNavigationViewStyle())
        .statusBar(hidden: true)
        .onAppear {
            apicaller.getAlbumInfo(albumID: albumID) { albumInfo in
                if let albumInfo = albumInfo {
                    jsonObject = albumInfo

                    albumName = albumInfo["albumName"] as? String ?? "Unknown Album"
                    artistName = albumInfo["artistName"] as? String ?? "Unknown Artist"
                    albumRating = albumInfo["albumRating"] as? Int ?? 3

                    albumPhotoURL = URL(string: albumInfo["albumPicture"] as? String ?? "")

                    if let songsData = albumInfo["songs"] as? [[String: Any]] {
                        songs = songsData.map { songData in
                            return Song(
                                songID: songData["song_id"] as? String ?? "",
                                songName: songData["song_name"] as? String ?? "",
                                duration: songData["duration"] as? Int ?? 0,
                                releaseYear: songData["release_year"] as? String ?? "",
                                artist: songData["artist"] as? String ?? "",
                                songRating: songData["song_rating"] as? Int ?? 0
                            )
                        }
                    }
                } else {
                    print("Failed to fetch album info")
                }
            }
        }
    }
}

struct StarRatingView: View {
    @State public var albumID :String
    @Binding var rating: Int // Two-way binding for the rating

    var body: some View {
        HStack {
            ForEach(1...5, id: \.self) { index in
                Image(systemName: index <= rating ? "star.fill" : "star")
                    .foregroundColor(index <= rating ? .yellow : .gray)
                    .onTapGesture {
                        rating = index // Update the rating when a star is tapped
                        apicaller.postAlbumRating(albumID: albumID, rating: index)
                    }
            }
        }
    }
}

struct AlbumView_Previews: PreviewProvider {
    static var previews: some View {
        AlbumView(albumID: "1234567890")
    }
}
