//
//  MainPageViews.swift
//  supotify55
//
//  Created by Furkan Emre Güler on 17.11.2023.
//

import SwiftUI

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
#Preview {
    AlbumDisplayView(album: dummyAlbum )
}
