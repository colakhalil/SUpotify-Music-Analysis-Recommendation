import SwiftUI

struct DisplaySongView: View {
    var songTitle: String
    var songArtist: String
    
    var body: some View {
        HStack {
            /*AsyncImage(url: songThumbnailURL) { image in
                image.resizable()
                    .frame(width: 50, height: 50)
                    .cornerRadius(5)
            } placeholder: {
                Color.gray
                    .frame(width: 50, height: 50)
                    .cornerRadius(5)
            }*/

            VStack(alignment: .leading) {
                Text(songTitle)
                    .bold()
                    .foregroundColor(.white)
                    .onTapGesture {
                        print("\(songTitle) is clicked")
                    }

                Text(songArtist)
                    .foregroundColor(.white)
                    .onTapGesture {
                        print("\(songArtist) is clicked")
                    }
                // Add other song details as needed
            }
        }
    }
}



struct PlaylistView: View {
    @State var playlistID : String
    @State private var songs: [Song] = []
    @State private var playlistPhotoURL: URL? = URL(string: "https://example.com/playlist_cover.jpg")
    @State private var playlistName: String = "Default"
    @State private var jsonObject: [String: Any] = [:]
    let placeholderURL = URL(string: "https://example.com/placeholder_image.jpg")!
    var body: some View {
        NavigationView {
            VStack {
                // Playlist photo at the top with specified horizontal padding
                AsyncImage(url: playlistPhotoURL) { image in
                    image.resizable()
                        .frame(height: 150)
                        .cornerRadius(10)
                } placeholder: {
                    Color.gray
                        .frame(height: 150)
                        .cornerRadius(10)
                }
                .padding(.horizontal, 120)

                // Custom title
                Text(playlistName)
                    .font(.largeTitle)
                    .bold()
                    .foregroundColor(.white) // Text color set to white

                // List of songs
                List(songs, id: \.songID) { song in
                    DisplaySongView(songTitle: song.songName, songArtist: song.artist)
                        .listRowBackground(Color.black)
                }

                .listStyle(PlainListStyle()) // Set list style to plain without default separators
            }
            .background(Color.black) // Set the background color of the entire view
        }
        .navigationViewStyle(StackNavigationViewStyle()) // Use stack navigation style for smaller screens
        .statusBar(hidden: true) // Hide the status bar
        .onAppear {
            apicaller.getPlaylistInfo(playlistID: playlistID) { playlistInfo in
                if let playlistInfo = playlistInfo {
                    jsonObject = playlistInfo
                    if let playlistNameAny = playlistInfo["playlistName"] as? String {
                        playlistName = playlistNameAny
                    } else {
                        print("Value couldn't be converted to String")
                    }

                    if let playlistPictureAny = playlistInfo["playlistPicture"] as? String {
                        if let url = URL(string: playlistPictureAny) {
                            playlistPhotoURL = url
                        } else {
                            print("Invalid URL string for playlist picture")
                        }
                    } else {
                        print("Value is nil for playlist picture")
                    }

                    // Parsing songs from jsonObject["songs"]
                    if let songsData = jsonObject["songs"] as? [[String: Any]] {
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
                    } else {
                        print("No data for songs")
                    }

                } else {
                    print("Failed to fetch playlist info")
                }
            }
        }

    }
}

// Preview code (for testing purposes)
struct PlaylistView_Previews: PreviewProvider {
    static var previews: some View {
        PlaylistView(playlistID: "3HAdIN8wtU2UBo94fznOTm")
    }
}
