//
//  APIcaller.swift
//  supotify55
//
//  Created by Furkan Emre Güler on 16.11.2023.
//

import Foundation
import SwiftUI

let apicaller = APICaller.apicaller

struct APICaller {
    static let apicaller : APICaller = APICaller()
    
    func loginPostRequest(email: String, password: String, completion: @escaping (Bool) -> Void) {
        let jsonObject: [String: Any] = [
            "email": email,
            "password": password
        ]
        do {
            let jsonData = try JSONSerialization.data(withJSONObject: jsonObject, options: .prettyPrinted)
            let url = URL(string: "http://127.0.0.1:8008/login")!
            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            request.setValue("application/json", forHTTPHeaderField: "Content-Type")
            request.httpBody = jsonData
            let task = URLSession.shared.dataTask(with: request) { data, response, error in
                if let error = error {
                    // Handle the case where there's an error with the request
                    print("Error: \(error)")
                    completion(false) // Report login failure
                    return
                }
                
                // Check if there's a response
                guard let httpResponse = response as? HTTPURLResponse else {
                    // Handle the case where there's no valid HTTP response
                    print("Invalid or no HTTP response")
                    completion(false) // Report login failure
                    return
                }
                
                // Print the status code
                print(" xyz Status code: \(httpResponse.statusCode)")
                
                if let data = data {
                    // Process the response data
                    do {
                        let responseJSON = try JSONSerialization.jsonObject(with: data, options: [])
                        
                        if let jsonDictionary = responseJSON as? [String: Any],
                           let message = jsonDictionary["message"] as? Bool {
                            switch message {
                            case true:
                                // Successful login
                                print("Successful login")
                                completion(true) // Report login success
                                myUser.email = email
                                myUser.password = password
                                navigator.LoginToMain(email: email)
                            case false:
                                print("Wrong password")
                                completion(false) // Report login failure
                                
                            }
                        }
                    } catch {
                        // Handle JSON parsing error
                        print("Error parsing JSON: \(error)")
                        completion(false) // Report login failure due to JSON parsing error
                    }
                }
            }
            // Resume the task to execute the request
            task.resume()
        } catch {
            print("Error: \(error)")
            completion(false) // Report login failure due to error
        }
    }
    
    func signupPostRequest(username: String, password: String, email: String, completion: @escaping (Bool) -> Void) {
        let jsonObject: [String: Any] = [
            "user_id": username,
            "password": password,
            "email": email
        ]
        
        do {
            let jsonData = try JSONSerialization.data(withJSONObject: jsonObject, options: .prettyPrinted)
            let url = URL(string: "http://127.0.0.1:8008/sign_up")! // URL for SignUp
            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            request.setValue("application/json", forHTTPHeaderField: "Content-Type")
            request.httpBody = jsonData
            
            let task = URLSession.shared.dataTask(with: request) { data, response, error in
                if let error = error {
                    print("Error: \(error)")
                    completion(false) // Report signup failure
                    return
                }
                
                guard let httpResponse = response as? HTTPURLResponse else {
                    print("Invalid or no HTTP response")
                    completion(false) // Report signup failure
                    return
                }
                
                print("Status code: \(httpResponse.statusCode)")
                
                // Assuming success is indicated by a specific HTTP status code, like 200 for example
                let successCodes = 200..<300
                if successCodes.contains(httpResponse.statusCode) {
                    completion(true) // Report signup success
                } else {
                    completion(false) // Report signup failure
                }
            }
            task.resume()
        } catch {
            print("Error: \(error)")
            completion(false) // Report signup failure
        }
    }

    func getPlaylistInfo(playlistID: String, completion: @escaping ([String: Any]?) -> Void) {
        let urlString = "http://127.0.0.1:8008/get_playlist_info/\(myUser.username)/\(playlistID)"
        guard let url = URL(string: urlString) else {
            completion(nil)
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error: \(error)")
                completion(nil)
                return
            }
            
            guard let httpResponse = response as? HTTPURLResponse else {
                print("Invalid or no HTTP response")
                completion(nil)
                return
            }
            
            print("Status code: \(httpResponse.statusCode)")
            
            // Check if the response status is successful (status codes in 200-299 range)
            guard (200...299).contains(httpResponse.statusCode) else {
                print("Unsuccessful response: \(httpResponse.statusCode)")
                completion(nil)
                return
            }
            
            if let data = data {
                do {
                    let responseJSON = try JSONSerialization.jsonObject(with: data, options: [])
                    
                    if let playlistInfo = responseJSON as? [String: Any] {
                        // Successfully parsed JSON
                        completion(playlistInfo)
                    } else {
                        print("JSON does not match expected format")
                        completion(nil)
                    }
                } catch {
                    print("Error parsing JSON: \(error)")
                    // Print or log the response data to investigate further if needed
                    if let responseDataString = String(data: data, encoding: .utf8) {
                        print("Response data: \(responseDataString)")
                    }
                    completion(nil)
                }
            }
        }
        task.resume()
    }
    func getUserdata(email: String, completion: @escaping (Result<NSDictionary, Error>) -> Void) {
        let baseUrl = "http://127.0.0.1:8008/user_data/"
        let url = URL(string: baseUrl + email)!

        let task = URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }

            guard let data = data else {
                completion(.failure(NSError(domain: "", code: -1, userInfo: nil)))
                return
            }

            do {
                if let json = try JSONSerialization.jsonObject(with: data, options: []) as? NSDictionary {
                    completion(.success(json))
                } else {
                    completion(.failure(NSError(domain: "", code: -2, userInfo: nil)))
                }
            } catch {
                completion(.failure(error))
            }
        }

        task.resume()
    }
    func getUserPlaylists() {
            // The URL of your backend endpoint
            guard let url = URL(string: "http://127.0.0.1:8008/get_user_playlists") else {
                print("Invalid URL")
                return
            }
            
            var request = URLRequest(url: url)
            request.httpMethod = "GET"
            
            URLSession.shared.dataTask(with: request) { data, response, error in
                if let error = error {
                    print("Error: \(error.localizedDescription)")
                    return
                }
                
                guard let httpResponse = response as? HTTPURLResponse, (200...299).contains(httpResponse.statusCode) else {
                    print("Invalid response")
                    return
                }
                
                if let data = data {
                    do {
                        // Parse the received data
                        let json = try JSONSerialization.jsonObject(with: data, options: []) as? [[String: Any]]
                        
                        var playlists = [Playlist]() // Array to store Playlist objects
                        
                        if let jsonArray = json {
                            for playlistData in jsonArray {
                                let playlist = Playlist()
                                playlist.name = playlistData["name"] as? String ?? "default"
                                playlist.playlistID = playlistData["playlistID"] as? String ?? "default"
                                
                                if let picString = playlistData["playlistPic"] as? String, let picURL = URL(string: picString) {
                                    playlist.playlistPic = picURL
                                } else {
                                    playlist.playlistPic = nil // or set a default URL if needed
                                }
                                
                                playlist.songNumber = playlistData["songNumber"] as? Int ?? -1
                                
                                playlists.append(playlist)
                            }

                        }
                        myUser.playlists = playlists
                        // Use the 'playlists' array containing Playlist objects here
                        for playlist in playlists {
                            print("Playlist Name: \(playlist.name)")
                            print("Playlist ID: \(playlist.playlistID)")
                            // ... (Do whatever you need with each playlist object)
                        }
                        
                    } catch {
                        print("Error parsing JSON: \(error.localizedDescription)")
                    }
                }
            }.resume()
        }
    func getAlbumInfo(albumID: String, completion: @escaping ([String: Any]?) -> Void) {
        let urlString = "http://127.0.0.1:8008/get_playlist_info/\(albumID)"
        guard let url = URL(string: urlString) else {
            completion(nil)
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error: \(error)")
                completion(nil)
                return
            }
            
            guard let httpResponse = response as? HTTPURLResponse else {
                print("Invalid or no HTTP response")
                completion(nil)
                return
            }
            
            print("Status code: \(httpResponse.statusCode)")
            
            guard (200...299).contains(httpResponse.statusCode) else {
                print("Unsuccessful response: \(httpResponse.statusCode)")
                completion(nil)
                return
            }
            
            if let data = data {
                do {
                    let responseJSON = try JSONSerialization.jsonObject(with: data, options: [])
                    
                    if let albumInfo = responseJSON as? [String: Any] {
                        completion(albumInfo)
                    } else {
                        print("JSON does not match expected format")
                        completion(nil)
                    }
                } catch {
                    print("Error parsing JSON: \(error)")
                    if let responseDataString = String(data: data, encoding: .utf8) {
                        print("Response data: \(responseDataString)")
                    }
                    completion(nil)
                }
            }
        }
        task.resume()
    }
    func saveSongToBackend(songData: [String: Any], showMessage: Binding<Bool>, successMessage: Binding<Bool>) {
        // Define the URL of your backend endpoint
        guard let url = URL(string: "http://127.0.0.1:8008/save_song_with_form") else {
            print("Invalid URL")
            showMessage.wrappedValue = true // Notify failure due to invalid URL
            successMessage.wrappedValue = false
            return
        }

        // Create the request
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        // Set the Content-Type header to application/json
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        // Set the JSON data to be sent
        do {
            let jsonData = try JSONSerialization.data(withJSONObject: songData, options: [])
            request.httpBody = jsonData
        } catch {
            print("Error creating JSON data: \(error)")
            showMessage.wrappedValue = true // Notify failure due to JSON data creation error
            successMessage.wrappedValue = false
            return
        }

        // Create a URLSession task
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            // Check for errors
            if let error = error {
                print("Error: \(error)")
                showMessage.wrappedValue = true // Notify failure due to URLSession error
                successMessage.wrappedValue = false
                return
            }
            
            // Check if the response contains data
            if let data = data {
                // Handle the response data if needed
                print("Response data: \(String(data: data, encoding: .utf8) ?? "")")
                
                // Assuming the response contains a boolean value
                if let responseJSON = try? JSONSerialization.jsonObject(with: data, options: []) as? [String: Any],
                   let success = responseJSON["message"] as? Bool {
                    // Notify success or failure based on the boolean value received
                    showMessage.wrappedValue = true
                    successMessage.wrappedValue = success
                } else {
                    showMessage.wrappedValue = true // Notify failure if unable to parse response
                    successMessage.wrappedValue = false
                }
            }
        }
        task.resume()
    }
    
    func searchUsers(searchTerm: String, completion: @escaping (Result<[User], Error>) -> Void) {
            guard let encodedTerm = searchTerm.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed),
                  let url = URL(string: "http://127.0.0.1:8008/search_user/\(encodedTerm)") else {
                return
            }

            URLSession.shared.dataTask(with: url) { data, response, error in
                if let error = error {
                    DispatchQueue.main.async {
                        completion(.failure(error))
                    }
                    return
                }

                guard let data = data else { return }

                do {
                    let users = try JSONDecoder().decode([User].self, from: data)
                    DispatchQueue.main.async {
                        completion(.success(users))
                    }
                } catch {
                    DispatchQueue.main.async {
                        completion(.failure(error))
                    }
                }
            }.resume()
        }

        func searchItems(searchTerm: String, completion: @escaping (Result<SearchResult, Error>) -> Void) {
            guard let encodedTerm = searchTerm.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed),
                  let url = URL(string: "http://127.0.0.1:8008/search_item/\(encodedTerm)") else {
                return
            }

            URLSession.shared.dataTask(with: url) { data, response, error in
                if let error = error {
                    DispatchQueue.main.async {
                        completion(.failure(error))
                    }
                    return
                }

                guard let data = data else { return }

                do {
                    let items = try JSONDecoder().decode(SearchResult.self, from: data)
                    DispatchQueue.main.async {
                        completion(.success(items))
                    }
                } catch {
                    DispatchQueue.main.async {
                        completion(.failure(error))
                    }
                }
            }.resume()
        }
}
