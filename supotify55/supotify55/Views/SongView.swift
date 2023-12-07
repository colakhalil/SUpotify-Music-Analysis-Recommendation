import SwiftUI
import Combine

struct SongInfo: Codable {
    var song_id: String
    var artists: String
    var title: String
    var thumbnail: String
    var rateAvg: Double
    var playCount: Int
    var popularity: Double
    var valence: Double
    var duration: Int
    var genre: String
    var releaseYear: Int
    var dateAdded: String
    var userPrevRating: Int
}

struct RatingData: Codable {
    let song_id: String
    let user_id: String
    let rating: Int
}

// MARK: - View Model
class SongViewModel: ObservableObject {
    @Published var songInfo: SongInfo?
    @Published var lyrics: String?
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?

    private var cancellables = Set<AnyCancellable>()

    func changeRating(songId: String, userId: String, rating: Int, completion: @escaping (Bool) -> Void) {
        guard let url = URL(string: "http://127.0.0.1:8008/change_rating_song") else {
            completion(false)
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")

        let ratingData = RatingData(song_id: songId, user_id: userId, rating: rating)

        do {
            request.httpBody = try JSONEncoder().encode(ratingData)
        } catch {
            completion(false)
            return
        }

        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let data = data, error == nil else {
                completion(false)
                return
            }

            do {
                if let jsonResponse = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Bool], let message = jsonResponse["message"], message {
                    DispatchQueue.main.async {
                        completion(true)
                    }
                } else {
                    DispatchQueue.main.async {
                        completion(false)
                    }
                }
            } catch {
                DispatchQueue.main.async {
                    completion(false)
                }
            }
        }.resume()
    }

    func getSongInfo(userId: String, songId: String) {
        guard let url = URL(string: "http://127.0.0.1:8008/song_info/\(userId)/\(songId)") else {
            self.errorMessage = "Invalid URL"
            self.isLoading = false
            return
        }

        self.isLoading = true

        URLSession.shared.dataTaskPublisher(for: url)
            .map(\.data)
            .decode(type: SongInfo.self, decoder: JSONDecoder())
            .receive(on: DispatchQueue.main)
            .sink(receiveCompletion: { [weak self] completion in
                self?.isLoading = false
                if case let .failure(error) = completion {
                    self?.errorMessage = error.localizedDescription
                }
            }, receiveValue: { [weak self] songInfo in
                self?.songInfo = songInfo
            })
            .store(in: &cancellables)
    }

    func fetchLyrics(songId: String) {
        guard let url = URL(string: "http://127.0.0.1:8008/lyrics/\(songId)") else {
            self.errorMessage = "Invalid URL for lyrics"
            return
        }

        self.isLoading = true

        URLSession.shared.dataTaskPublisher(for: url)
            .map(\.data)
            .decode(type: String.self, decoder: JSONDecoder())
            .receive(on: DispatchQueue.main)
            .sink(receiveCompletion: { [weak self] completion in
                self?.isLoading = false
                if case let .failure(error) = completion {
                    self?.errorMessage = error.localizedDescription
                }
            }, receiveValue: { [weak self] fetchedLyrics in
                self?.lyrics = fetchedLyrics
            })
            .store(in: &cancellables)
    }
}

// MARK: - Main View
struct SongView: View {
    @StateObject private var viewModel = SongViewModel()
    @State private var rating: Int = 0

    var body: some View {
        ZStack {
            Color.black.edgesIgnoringSafeArea(.all)

            VStack {
                if viewModel.isLoading {
                    ProgressView("Loading...")
                        .progressViewStyle(CircularProgressViewStyle(tint: .white))
                } else if let songInfo = viewModel.songInfo {
                    SongInfoView(songInfo: songInfo, rating: $rating, viewModel: viewModel)
                } else if let errorMessage = viewModel.errorMessage {
                    Text("Error: \(errorMessage)").foregroundColor(.red)
                }
            }
        }
        .onAppear {
            viewModel.getSongInfo(userId: myUser.username, songId: "3VpxEo6vMpi4rQ6t2WVVkK")
        }
    }
}

// MARK: - Song Info Subview
struct SongInfoView: View {
    let songInfo: SongInfo
    @Binding var rating: Int
    @ObservedObject var viewModel: SongViewModel // Use ObservedObject to pass the view model

    var body: some View {
        VStack {
            AsyncImage(url: URL(string: songInfo.thumbnail)) { image in
                image.resizable()
            } placeholder: {
                Color.gray
            }
            .aspectRatio(contentMode: .fill)
            .frame(width: 150, height: 150)
            .cornerRadius(12)

            Text(songInfo.title)
                .font(.title2)
                .foregroundColor(.white)
                .padding(.top, 8)

            Text(songInfo.artists)
                .font(.headline)
                .foregroundColor(.gray)
                .padding(.bottom, 8)

            // Additional song details
            Group {
                Text("Average Rating: \(String(format: "%.2f", songInfo.rateAvg))")
                    .foregroundColor(.white)
                Text("Play Count: \(songInfo.playCount)")
                    .foregroundColor(.white)
                Text("Popularity: \(String(format: "%.2f", songInfo.popularity))")
                    .foregroundColor(.white)
                Text("Valence: \(String(format: "%.2f", songInfo.valence))")
                    .foregroundColor(.white)
                Text("Duration: \(songInfo.duration) seconds")
                    .foregroundColor(.white)
                Text("Genre: \(songInfo.genre)")
                    .foregroundColor(.white)
                Text("Release Year: \(songInfo.releaseYear)")
                    .foregroundColor(.white)
                Text("Date Added: \(songInfo.dateAdded)")
                    .foregroundColor(.white)
            }
            .padding(.vertical, 1)

            HStack {
                ForEach(1...5, id: \.self) { star in
                    Image(systemName: rating >= star ? "star.fill" : "star")
                        .foregroundColor(rating >= star ? .yellow : .gray)
                        .onTapGesture {
                            print("Star tapped: \(star)") // Debug print
                            rating = star
                            viewModel.changeRating(songId: songInfo.song_id, userId: myUser.username, rating: rating) { success in
                                if success {
                                    print("Rating sent successfully")
                                } else {
                                    print("Failed to send rating")
                                }
                            }
                        }
                }
            }
            .font(.title)
            .padding()
        }
    }
}



struct SongView_Previews: PreviewProvider {
    static var previews: some View {
        SongView()
    }
}
