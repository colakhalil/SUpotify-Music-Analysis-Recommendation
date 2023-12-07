import SwiftUI

struct SongStarRatingView: View {
    @Binding var rating : Int
    @State public var SongId : String
    var body: some View {
        HStack {
            ForEach(1...5, id: \.self) { index in
                Image(systemName: index <= rating ? "star.fill" : "star")
                    .foregroundColor(index <= rating ? .yellow : .gray)
                    .onTapGesture {
                        rating = index
                        
                    }
            }
        }
    }
}
struct DisplaySongView: View {
    var song : Song
    @State private var rating : Int
    init(song: Song) {
        self.song = song
        _rating = State(initialValue: song.songRating)
    }
    var body: some View {
        HStack {
            VStack(alignment: .leading) {
                Text("Song Title:")
                    .bold()
                    .foregroundColor(.white)
                Text(song.songName)
                    .foregroundColor(.white)
                
                Text("Artists:")
                    .bold()
                    .foregroundColor(.white)
                Text(song.artist)
                    .foregroundColor(.white)
                
                Text("Duration:")
                    .bold()
                    .foregroundColor(.white)
                Text("\(song.duration) seconds")
                    .foregroundColor(.white)
                
                Text("Release Year:")
                    .bold()
                    .foregroundColor(.white)
                Text(song.releaseYear)
                    .foregroundColor(.white)
                SongStarRatingView(rating: $rating, SongId: song.songID)
                .padding(.vertical)            }
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
                    DisplaySongView(song: song)
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
