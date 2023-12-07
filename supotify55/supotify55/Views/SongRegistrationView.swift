import SwiftUI

struct SongRegistrationView: View {

    @State private var songTitle = ""
    @State private var artistName = ""
    @State private var songGenre = ""
    @State private var songDurationText = ""
    @State private var songReleaseYearText = ""
    @State private var showMessage = false
    @State private var successMessage = false
    
    var body: some View {
        ZStack {
            Color.black.edgesIgnoringSafeArea(.all)
            
            ScrollView {
                VStack(alignment: .leading) {
                    Text("Enter the Details of the Song You Wish to Add")
                        .font(.title)
                        .foregroundColor(.white)
                        .padding([.top, .horizontal, .bottom])
                    
                    Group {
                        LabelTextField(label: "Title:", placeholder: "Title", text: $songTitle)
                            LabelTextField(label: "Artist Name:", placeholder: "Name", text: $artistName)
                            LabelTextField(label: "Song Genre:", placeholder: "Genre", text: $songGenre)
                            LabelTextField(label: "Song Duration:", placeholder: "Duration", text: $songDurationText)
                            LabelTextField(label: "Release Year:", placeholder: "Date", text: $songReleaseYearText)
          }
                    .background(Color.black)
                    .cornerRadius(5)
                    .padding(.horizontal)
                    
                    Button(action: {
                        var songDuration: Int {
                            return Int(songDurationText) ?? 0
                        }

                        var songReleaseYear: Int {
                            return Int(songReleaseYearText) ?? 0
                        }
                        let songData: [String: Any] =  [
                            "songTitle": songTitle,
                            "artistName": artistName,
                            "songGenre": songGenre,
                            "songDuration": songDuration,
                            "songReleaseYear": songReleaseYear
                        ]
                        apicaller.saveSongToBackend(songData: songData, showMessage: $showMessage , successMessage: $successMessage)

                    }) {
                        Text("Send")
                            .foregroundColor(.white)
                            .padding()
                            .frame(minWidth: 0, maxWidth: .infinity)
                            .background(Color.green)
                            .cornerRadius(8)
                    }
                    .padding([.horizontal, .bottom])
                }
            }
        }
        .alert(isPresented: $showMessage) {
            Alert(title: Text(successMessage ? "Success" : "Error"),
                  message: Text(successMessage ? "Song saved successfully" : "Failed to save song"),
                  dismissButton: .default(Text("OK")) {
                    if successMessage {
                        resetForm()
                    }
                  })
        }
    }
    
    func resetForm() {
        songTitle = ""
        artistName = ""
        songGenre = ""
        songDurationText = ""
        songReleaseYearText = ""
    }
}

struct LabelTextField: View {
    var label: String
    var placeholder: String
    @Binding var text: String
    
    var body: some View {
        VStack(alignment: .leading) {
            Text(label)
                .foregroundColor(.white)
            TextField(placeholder, text: $text)
                .textFieldStyle(.roundedBorder)
        }
    }
}

struct SongRegistrationView_Previews: PreviewProvider {
    static var previews: some View {
        SongRegistrationView()
    }
}
