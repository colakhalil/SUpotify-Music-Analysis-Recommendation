import SwiftUI

struct SearchView: View {
    @State private var searchText = ""
        @State private var searchOption = "User"
        let searchOptions = ["User", "Song/Artist/Album"]
        @State private var userResults: [User] = [] // For user search results
        @State private var itemResults: SearchResult? // For song/artist/album search results
    
    init() {
            // Customizing the appearance of UISegmentedControl
            UISegmentedControl.appearance().selectedSegmentTintColor = .white
            UISegmentedControl.appearance().setTitleTextAttributes([.foregroundColor: UIColor.lightGray], for: .normal)
            UISegmentedControl.appearance().setTitleTextAttributes([.foregroundColor: UIColor.black], for: .selected)
        }

    var body: some View {
        NavigationView {
            VStack {
                Picker("Search Type", selection: $searchOption) {
                    ForEach(searchOptions, id: \.self) {
                        Text($0)
                    }
                }
                .pickerStyle(SegmentedPickerStyle())
                .padding()

                TextField("Search...", text: $searchText)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding()
                    .foregroundColor(.black)
                    .background(Color.black)
                
                Button("Search") {
                    // Perform search based on selected option
                    if searchOption == "User" {
                        apicaller.searchUsers(searchTerm: searchText) { result in
                            switch result {
                            case .success(let users):
                                self.userResults = users
                            case .failure(let error):
                                print("Error fetching users: \(error)")
                                // Handle the error, maybe show an alert
                            }
                        }
                    } else {
                        apicaller.searchItems(searchTerm: searchText) { result in
                            switch result {
                            case .success(let items):
                                self.itemResults = items
                            case .failure(let error):
                                print("Error fetching items: \(error)")
                                // Handle the error, maybe show an alert
                            }
                        }
                    }
                }
                .padding()

                
                Spacer()
                
                List {
                    if searchOption == "User" {
                        ForEach(userResults, id: \.id) { user in
                            SearchResultRow(imageUrl: user.profilePicture, title: user.id)
                        }
                    } else if let items = itemResults {
                        Section(header: Text("Songs")) {
                            ForEach(items.songs, id: \.song_id) { song in
                                SearchResultRow(imageUrl: nil, title: song.song_name) // Assuming songs don't have images
                            }
                        }

                        Section(header: Text("Albums")) {
                            ForEach(items.albums, id: \.album_id) { album in
                                SearchResultRow(imageUrl: nil, title: album.album_name) // Assuming albums don't have images
                            }
                        }

                        Section(header: Text("Artists")) {
                            ForEach(items.artists, id: \.artist_id) { artist in
                                SearchResultRow(imageUrl: nil, title: artist.artist_name) // Assuming artists don't have images
                            }
                        }
                    }
                }
            }
            .background(Color.black)
            .navigationBarTitle("Search", displayMode: .inline)
            .navigationBarColor(.black, textColor: .white)
        }
        .navigationViewStyle(StackNavigationViewStyle())
    }
}

struct SearchResultRow: View {
    var imageUrl: String?
    var title: String

    var body: some View {
        HStack {
            if let imageUrl = imageUrl, !imageUrl.isEmpty {
                // Display the image, e.g., using AsyncImage (for iOS 15 and later)
                AsyncImage(url: URL(string: imageUrl)) { image in
                    image.resizable()
                } placeholder: {
                    ProgressView()
                }
                .frame(width: 50, height: 50)
                .clipShape(RoundedRectangle(cornerRadius: 8))
            }
            Text(title)
        }
    }
}

// Custom modifier to change navigation bar color and text color
extension View {
    func navigationBarColor(_ backgroundColor: UIColor, textColor: UIColor) -> some View {
        self.modifier(NavigationBarModifier(backgroundColor: backgroundColor, textColor: textColor))
    }
}

struct NavigationBarModifier: ViewModifier {
    var backgroundColor: UIColor
    var textColor: UIColor

    init(backgroundColor: UIColor, textColor: UIColor) {
        self.backgroundColor = backgroundColor
        self.textColor = textColor
        
        let coloredAppearance = UINavigationBarAppearance()
        coloredAppearance.configureWithOpaqueBackground()
        coloredAppearance.backgroundColor = backgroundColor
        coloredAppearance.titleTextAttributes = [.foregroundColor: textColor]
        coloredAppearance.largeTitleTextAttributes = [.foregroundColor: textColor]

        UINavigationBar.appearance().standardAppearance = coloredAppearance
        UINavigationBar.appearance().compactAppearance = coloredAppearance
        UINavigationBar.appearance().scrollEdgeAppearance = coloredAppearance
        UINavigationBar.appearance().tintColor = textColor
    }

    func body(content: Content) -> some View {
        content
    }
}

struct SearchView_Previews: PreviewProvider {
    static var previews: some View {
        SearchView()
    }
}
