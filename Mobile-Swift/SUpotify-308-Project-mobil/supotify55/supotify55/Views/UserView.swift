import SwiftUI

struct UserView: View {
    @State private var jsonObject : [String : Any] = [:]
    @ObservedObject var userData = UserData.sharedUser
    
    // Sample Playlists
    let playlists: [Album] = [
        Album(AlbumName: "Summer Vibes", ArtistOfAlbum: "Sunny Beats", CoverPage: "https://example.com/summer_vibes.jpg"),
        Album(AlbumName: "City Nights", ArtistOfAlbum: "Urban Sound", CoverPage: "https://example.com/city_nights.jpg"),
        Album(AlbumName: "Chill Acoustics", ArtistOfAlbum: "Guitar Groove", CoverPage: "https://example.com/chill_acoustics.jpg"),
        Album(AlbumName: "Summer Vibes", ArtistOfAlbum: "Sunny Beats", CoverPage: "https://example.com/summer_vibes.jpg"),
        Album(AlbumName: "City Nights", ArtistOfAlbum: "Urban Sound", CoverPage: "https://example.com/city_nights.jpg"),
        Album(AlbumName: "Chill Acoustics", ArtistOfAlbum: "Guitar Groove", CoverPage: "https://example.com/chill_acoustics.jpg")
    ]

    var body: some View {
        VStack {
            VStack(alignment: .center, spacing: 20) {
                Image(systemName: "person.circle.fill")
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .frame(width: 120, height: 120)
                    .foregroundColor(.white) // White color for user icon
                
                Text(myUser.username)
                    .font(.title2)
                    .foregroundColor(.white) // White color for username
                
                Button(action: {}) {
                    HStack {
                        Image(systemName: "person.3.fill") // Friends icon
                            .foregroundColor(.white)
                        Text("Friends")
                            .foregroundColor(.white) // White color
                    }
                }
                
                HStack(spacing: 15) {
                    Button(action: {}) {
                        Text("Düzenle")
                            .padding(.horizontal, 10)
                            .padding(.vertical, 5)
                            .background(Color.gray.opacity(0.2))
                            .cornerRadius(8)
                            .foregroundColor(.white) // White color
                    }
                    
                    Button(action: {}) {
                        Image(systemName: "square.and.arrow.up") // Share icon
                            .foregroundColor(.white) // White color
                    }
                    
                    Button(action: {}) {
                        Image(systemName: "gear") // Settings icon
                            .foregroundColor(.white) // White color
                    }
                }
                .padding(.horizontal)
            }
            .padding(.horizontal, 20)

            Text("Playlists")
                .font(.headline)
                .padding(.top, 20)
                .foregroundColor(.white) // White color for "Playlists" text

            // Vertical scroll view for playlists
            ScrollView(showsIndicators: false) {
                LazyVStack(spacing: 20) {
                    ForEach(playlists) { playlist in
                        Button(action: {
                            // Action for when playlist is clicked
                        }) {
                            HStack {
                                AsyncImage(url: URL(string: playlist.CoverPage)) { image in
                                    image.resizable()
                                } placeholder: {
                                    Image(systemName: "photo")
                                        .resizable()
                                        .scaledToFit()
                                        .frame(width: 50, height: 50)
                                        .foregroundColor(.white) // White color for placeholder
                                }
                                .frame(width: 50, height: 50)

                                Text(playlist.AlbumName)
                                    .foregroundColor(.white) // White color for text
                                Spacer()
                            }
                        }
                        .frame(maxWidth: .infinity) // Use the maximum width available
                        .padding(.horizontal, 20) // 20 points padding on both sides
                        .background(Color.gray.opacity(0.2))
                        .cornerRadius(8)
                    }
                }
                .padding(.horizontal, 20) // Padding for the LazyVStack
            }

            Spacer(minLength: 100) // Gives space before the bottom icons
        }
        .background(Color.black) // Black background for the entire view
        .foregroundColor(.white)
   }
}

struct UserProfileView_Previews: PreviewProvider {
    static var previews: some View {
        UserView()
    }
}
