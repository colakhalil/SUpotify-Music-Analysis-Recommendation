//
//  SpotifyMainPageView.swift
//  SUpotify_Mobile
//
//  Created by Halil İbrahim Deniz on 6.11.2023.
//

import SwiftUI

struct MainPageView: View {
    @State private var rating: Int = 0
    @State public var DarkModeOn = true
    @State private var showSideMenu = false
    @State private var showFriendSideView = false
    @State private var email : String
    @State private var json_object: [String: Any] = [
        "username": "default",
        "profilePicture": "default",
        "lastListenedSong": "default",
        "friends": [],
        "friendsCount": 0]
    
    // Create instances of the Album class and add them to an array
    let albums: [Album] = [
        Album(AlbumName: "UTOPIA", ArtistOfAlbum: "Travis Scott", CoverPage: "/Users/furkanemre/Desktop/coverpages/utopia.jpeg"),
        Album(AlbumName: "MBDTF", ArtistOfAlbum: "Kanye West", CoverPage: "/Users/furkanemre/Desktop/coverpages/mbdtf.jpeg"),
        Album(AlbumName: "Savage Mode 2", ArtistOfAlbum: "21 Savage", CoverPage: "/Users/furkanemre/Desktop/coverpages/savagemode2.webp"),
        Album(AlbumName: "Her Loss", ArtistOfAlbum: "Drake", CoverPage: "/Users/furkanemre/Desktop/coverpages/herloss.png"),
        Album(AlbumName: "Heroes and Villians", ArtistOfAlbum: "Metro Boomin", CoverPage: "/Users/furkanemre/Desktop/coverpages/heroesandvillians.png"),
        Album(AlbumName: "Graduation", ArtistOfAlbum: "Kanye West", CoverPage: "/Users/furkanemre/Desktop/coverpages/graduation.jpeg")
    ]
    
    let friendsList = [
        Friend(name: "Alice", photo: "alicePhoto", lastSong: "GAZLLLLAAAAA"),
        Friend(name: "Bob", photo: "bobPhoto", lastSong: "HATUNLAYKEN DİNLEDİĞİM ŞARKILAR"),
        Friend(name: "Charlie", photo: "charliePhoto", lastSong: "EFKAAAAAARLIYKEN"),
        // Add more friends here...
    ]
    
    init(email: String) {
        self.email = email
        
        Color.self.hex = { hex in
            let scanner = Scanner(string: hex)
            var rgbValue: UInt64 = 0
            scanner.scanHexInt64(&rgbValue)
            
            let r = Double((rgbValue & 0xff0000) >> 16) / 255.0
            let g = Double((rgbValue & 0x00ff00) >> 8) / 255.0
            let b = Double(rgbValue & 0x0000ff) / 255.0
            
            return Color(red: r, green: g, blue: b)
        }
    }
    
    var body: some View {
        ZStack {
            let startColor = Color.hex("#0d2316")
            let endColor = Color.hex("#301629")
            
            LinearGradient(gradient: Gradient(colors: [startColor, endColor]), startPoint: .leading, endPoint: .trailing)
                .edgesIgnoringSafeArea(.all)
            
            Rectangle()
                .fill(.black)
                .frame(width: 370, height: 750)
                .cornerRadius(15)
            
            VStack {

                HStack {
                    Button(action: {
                        print(myUser.password)
                        print(myUser.friendsCount)
                        print(myUser.playlists.count)
                        print(myUser.friends)
                        print(myUser.username)
                        if myUser.playlists.count > 0
                        {
                            print(myUser.playlists[0].name)
                            print(myUser.playlists[0].playlistID)
                            print(myUser.playlists[0].playlistPic)
                            print(myUser.playlists[0].songNumber)
                        }
                        else
                        {
                            print("no  dataaaaa")
                        }


                        withAnimation {
                            showSideMenu.toggle()
                        }
                    }) {
                        Image(systemName: "ellipsis")
                            .resizable()
                            .frame(width: 20, height: 5)
                            .foregroundColor(.white)
                    }
                    
                    Spacer()
                    Text("Evening")
                        .font(Font.custom("Avantgarde Gothic", size: 28))
                        .foregroundColor(.white)
                    Spacer()
                    Button(action: {
                        DarkModeOn.toggle()
                    }){
                        Image(systemName: "moon")
                            .resizable()
                            .frame(width: 40, height: 40)
                            .foregroundColor(.white)
                    }
                    
                    Spacer()
                    Button(action: {
                        withAnimation {
                            showFriendSideView.toggle()
                        }
                    }) {
                        Image(systemName: "person.3.fill")
                            .resizable()
                            .frame(width: 40, height: 40)
                            .foregroundColor(.white)
                    }
                    .padding()
                }
                    ScrollView(.vertical, showsIndicators: false) {
                        VStack(alignment: .leading) {
                            Text("Your Playlists")
                                .font(Font.custom("Avantgarde Gothic", size: 24))
                                .foregroundColor(.white)
                                .padding(.bottom, 10)
                            ScrollView(.horizontal, showsIndicators: false) {
                                HStack {
//                                    ForEach(albums, id: \.AlbumName) { album in
//                                        AlbumDisplayView(album: album)
                                    ForEach(myUser.playlists, id: \.playlistID) { playlist in
                                        PlaylistDisplayView(playlist: playlist)
                                    }
                                }
                            }
                            Text("Recommended Playlists")
                                .font(Font.custom("Avantgarde Gothic", size: 24))
                                .foregroundColor(.white)
                                .padding(.vertical, 10)
                            
                            ForEach(albums, id: \.AlbumName) { album in
                                AlbumDisplayView(album: album)
                            }
                            .padding()
                        }
                    }
                    
                    
                    VStack {
                        Divider().background(Color.white)
                        HStack {
                            Image(systemName: "waveform")
                                .foregroundColor(.gray)
                            VStack(alignment: .leading) {
                                Text("Song Name")
                                    .foregroundColor(.white)
                                    .fontWeight(.bold)
                                    .font(Font.custom("Avantgarde Gothic", size: 18))
                                Text("Singer")
                                    .foregroundColor(.gray)
                                    .font(Font.custom("Avantgarde Gothic", size: 16))
                                
                                
                                HStack {
                                    ForEach(1...5, id: \.self) { star in
                                        Image(systemName: rating >= star ? "star.fill" : "star")
                                            .foregroundColor(rating >= star ? .yellow : .gray)
                                            .onTapGesture {
                                                rating = star
                                            }
                                    }
                                }
                                .font(Font.custom("Avantgarde Gothic", size: 16))
                            }
                            Spacer()
                            Image(systemName: "play.fill")
                                .foregroundColor(.white)
                            Image(systemName: "forward.fill")
                                .foregroundColor(.white)
                        }
                        .padding([.leading, .trailing, .top])
                    }
                    .background(Color.black.opacity(0.8))
                }
                .padding()
                if showSideMenu {
                    SideMenuView(showSideMenu: showSideMenu)
                }
            if showFriendSideView {
                FriendsSideView(showFriendSideView: showFriendSideView, friends: friendsList)
            }
                
            }.navigationBarBackButtonHidden(true)
            .onAppear {
                apicaller.getRecommendations(for: "pop")
                apicaller.getUserdata(email: email) { result in
                    switch result {
                    case .success(let userData):
                        DispatchQueue.main.async {
                            // Fetch playlists and set them in UserData shared instance
                            // Rest of your existing code to handle other user data
                            if let username = userData["username"] as? String {
                                myUser.username = username
                            }
                            if let profilePicture = userData["profilePicture"] as? String {
                                myUser.profilePicture = profilePicture
                            }
                            if let friends = userData["friends"] as? [String]{
                                myUser.friends = friends
                            }
                            if let friendsCount = userData["friendsCount"] as? Int{
                                myUser.friendsCount = friendsCount
                            }
                            if let lastListenedSong = userData["lastListenedSong"] as? String{
                                myUser.lastListenedSong = lastListenedSong
                            }
                        }
                    case .failure(let error):
                        print("Error fetching user data: \(error)")
                    }
                }
            }


        }
    }

//struct SpotifyMainPageView_Previews: PreviewProvider {
//    static var previews: some View {
//        MainPageView()
//    }
//}
