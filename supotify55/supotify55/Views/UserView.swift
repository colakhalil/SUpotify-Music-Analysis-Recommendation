import SwiftUI

struct UserView: View {
    @State private var playlists: [Playlist] = [] // Use Playlist model
    @ObservedObject var userData = UserData.sharedUser



    var body: some View {
        
        VStack {
            VStack(alignment: .center, spacing: 20) {
                AsyncImage(url: URL(string: userData.profilePicture)) { image in
                                    image.resizable()
                                } placeholder: {
                                    Image(systemName: "person.circle.fill")
                                        .resizable()
                                        .aspectRatio(contentMode: .fit)
                                        .frame(width: 120, height: 120)
                                        .foregroundColor(.gray) // Placeholder color
                                }
                                .frame(width: 120, height: 120)
                                .clipShape(Circle())
                                .overlay(Circle().stroke(Color.white, lineWidth: 4))
                
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
                    ForEach(playlists, id: \.playlistID) { playlist in // Iterate over playlists
                        Button(action: {
                            // Action for when playlist is clicked
                        }) {
                            HStack {
                                AsyncImage(url: playlist.playlistPic) { image in // Use playlistPic
                                    image.resizable()
                                } placeholder: {
                                    // Placeholder content
                                }
                                .frame(width: 50, height: 50)

                                Text(playlist.name) // Use playlist name
                                    .foregroundColor(.white)
                                Spacer()
                            }
                        }
                        .frame(maxWidth: .infinity)
                        .padding(.horizontal, 20)
                        .background(Color.gray.opacity(0.2))
                        .cornerRadius(8)
                    }
                }
                .padding(.horizontal, 20)
            }

            Spacer(minLength: 100)
        }
        .background(Color.black)
        .onAppear {
            apicaller.getUserPlaylists2 { fetchedPlaylists in
                self.playlists = fetchedPlaylists // Update state with fetched playlists
            }
        }
    }
}

struct UserProfileView_Previews: PreviewProvider {
    static var previews: some View {
        UserView()
    }
}
