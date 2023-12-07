//
//  MainPageViews.swift
//  supotify55
//
//  Created by Furkan Emre Güler on 17.11.2023.
//

import SwiftUI

struct SideMenuView: View {
    @State var showSideMenu: Bool
    
    var body: some View {
        ZStack {
            // Dark overlay to disable the background view
            GeometryReader { _ in
                EmptyView()
            }
            .background(Color.black.opacity(0.5))
            .opacity(showSideMenu ? 1 : 0)
            .animation(Animation.easeIn.delay(0.25))
            .onTapGesture {
                withAnimation {
                    showSideMenu = false
                }
            }

            // Side menu content
            HStack {
                MenuContent()
                    .frame(width: 250)
                    .background(Color.black) // Set the side menu background to black
                    .offset(x: showSideMenu ? 0 : -250)
                    .transition(.move(edge: .trailing))
                Spacer()
            }
        }
        .edgesIgnoringSafeArea(.all)
    }

    @ViewBuilder
    private func MenuContent() -> some View {
        VStack(alignment: .leading) {
            Button(action: {
                withAnimation {
                    showSideMenu = false
                }
            }) {
                Image(systemName: "xmark")
                    .foregroundColor(.white)
                    .padding()
                    .padding(.top, 40) // To push down from the top edge
            }
            .frame(maxWidth: .infinity, alignment: .trailing)

            // Profile and other menu items
            Button("View Profile") {
                DispatchQueue.main.async {
                    if let window = UIApplication.shared.windows.first {
                        window.rootViewController = UIHostingController(rootView: UserView())
                        window.makeKeyAndVisible()
                    }
                }            }
            .foregroundColor(.white)
            .padding(.top, 20)
            Button("Search Item") {
                DispatchQueue.main.async {
                    if let window = UIApplication.shared.windows.first {
                        window.rootViewController = UIHostingController(rootView: SearchView())
                        window.makeKeyAndVisible()
                    }
                }            }
            .foregroundColor(.white)
            .padding(.top, 20)
            Button("Import/Export") {
                DispatchQueue.main.async {
                    if let window = UIApplication.shared.windows.first {
                        window.rootViewController = UIHostingController(rootView: ImportExportView())
                        window.makeKeyAndVisible()
                    }
                }            }
            .foregroundColor(.white)
            .padding(.top, 20)
            Button("Save Song") {
                DispatchQueue.main.async {
                    if let window = UIApplication.shared.windows.first {
                        window.rootViewController = UIHostingController(rootView: SongRegistrationView())
                        window.makeKeyAndVisible()
                    }
                }            }
            .foregroundColor(.white)
            .padding(.top, 20)
            Spacer()
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}

struct FriendRowView: View {
    var friend: Friend

    var body: some View {
        HStack {
            Image(friend.photo) // Replace with actual image loading logic
                .resizable()
                .frame(width: 50, height: 50)
                .clipShape(Circle())

            VStack(alignment: .leading) {
                Text(friend.name)
                    .font(.headline)
                    .foregroundColor(.white)

                Text(friend.lastSong)
                    .font(.subheadline)
                    .foregroundColor(.gray)
            }

            Spacer()
        }
        .padding()
    }
}

struct FriendsSideView: View {
    @State var showFriendSideView: Bool
    let friends: [Friend] // Assuming you have an array of `Friend` objects

    var body: some View {
        ZStack {
            // Dark overlay to disable the background view
            GeometryReader { _ in
                EmptyView()
            }
            .background(Color.black.opacity(0.5))
            .opacity(showFriendSideView ? 1 : 0)
            .animation(Animation.easeIn.delay(0.25))
            .onTapGesture {
                withAnimation {
                    showFriendSideView = false
                }
            }

            // Side view content
            HStack {
                Spacer()
                friendsMenuContent
                    .frame(width: 250)
                    .background(Color.black) // Set the side view background to black
                    .offset(x: showFriendSideView ? 0 : 250) // Adjust the offset to slide in from the right
                    .transition(.move(edge: .trailing)) // Use trailing edge for right-to-left appearance
            }
        }
        .edgesIgnoringSafeArea(.all)
    }

    // `friendsMenuContent` as a computed property
    private var friendsMenuContent: some View {
        VStack(alignment: .leading) {
            Button(action: {
                withAnimation {
                    showFriendSideView = false
                }
            }) {
                Image(systemName: "xmark")
                    .foregroundColor(.white)
                    .padding()
                    .padding(.top, 40)
            }
            .frame(maxWidth: .infinity, alignment: .trailing)

            ForEach(friends, id: \.name) { friend in
                FriendRowView(friend: friend)
            }

            Spacer()
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}


struct AlbumDisplayView : View {
    let album: Album // Assuming you have an Album instance to display
    var body: some View {
        Button(action:{
            print("hello ")
        })
        {
            HStack(spacing: 10) {
                // Cover Page on the left
                Image(uiImage: UIImage(contentsOfFile: album.CoverPage) ?? UIImage(systemName: "photo")!)
                    .resizable()
                    .frame(width: 100, height: 100)
                    .background(Color.gray.opacity(0.5))
                VStack(alignment: .leading) {
                    Text(album.AlbumName)
                        .font(Font.custom("Avantgarde Gothic", size: 18)).foregroundStyle(Color.cyan)
                    Text(album.ArtistOfAlbum).foregroundStyle(Color.gray)
                }
                .foregroundColor(.white)
            }
            .frame(height: 100)
        }
    }
}

let dummyAlbum = Album(AlbumName: "Fatih", ArtistOfAlbum: "Terim", CoverPage: "GS", id: UUID())

struct PlaylistDisplayView: View {
    let playlist: Playlist // Assuming you have a Playlist instance to display
    
    @State private var playlistImage: UIImage? // State variable to hold the image
    let placeholderImage = UIImage(systemName: "photo") // Placeholder image
    
    var body: some View {
        Button(action: {
            DispatchQueue.main.async {
                if let window = UIApplication.shared.windows.first {
                    window.rootViewController = UIHostingController(rootView: PlaylistView(playlistID: playlist.playlistID))
                    window.makeKeyAndVisible()
                }
            }
            print("go to playlist by using api call")
            print(playlist.name)
            print(playlist.playlistID)
        }) {
            HStack(spacing: 10) {
                // Cover Page on the left
                if let image = playlistImage {
                    Image(uiImage: image)
                        .resizable()
                        .frame(width: 100, height: 100)
                        .background(Color.gray.opacity(0.5))
                } else {
                    Image(uiImage: placeholderImage ?? UIImage(systemName: "photo")!)
                        .resizable()
                        .frame(width: 100, height: 100)
                        .background(Color.gray.opacity(0.5))
                }

                VStack(alignment: .leading) {
                    Text(playlist.name)
                        .font(Font.custom("Avantgarde Gothic", size: 18))
                        .foregroundStyle(Color.cyan)
                }
                .foregroundColor(.white)
            }
            .frame(height: 100)
        }
        .onAppear {
            // Load image asynchronously when the view appears
            loadImage(from: playlist.playlistPic)
        }
    }

    // Function to load image asynchronously from URL
    private func loadImage(from url: URL?) {
        guard let imageURL = url else {
            return
        }

        DispatchQueue.global().async {
            do {
                let imageData = try Data(contentsOf: imageURL)
                if let loadedImage = UIImage(data: imageData) {
                    DispatchQueue.main.async {
                        self.playlistImage = loadedImage
                    }
                }
            } catch {
                print("Error loading image: \(error)")
            }
        }
    }
}
