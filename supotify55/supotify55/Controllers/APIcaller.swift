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
    
    func LoginPostRequest(email: String, password: String) {
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
                    return
                }
                
                // Check if there's a response
                guard let httpResponse = response as? HTTPURLResponse else {
                    // Handle the case where there's no valid HTTP response
                    print("Invalid or no HTTP response")
                    return
                }
                
                // Print the status code
                print("Status code: \(httpResponse.statusCode)")
                
                if let data = data {
                    // Process the response data
                    do {
                        let responseJSON = try JSONSerialization.jsonObject(with: data, options: [])
                        
                        if let jsonDictionary = responseJSON as? [String: Any],
                           let message = jsonDictionary["message"] as? String {
                            switch message {
                            case "Success":
                                // Başarılı durum: Ana sayfaya geçiş yapabilir
                                print("basarili")
                                navigator.LoginToMain()
                                
                            case "Wrong password":
                                // Hatalı şifre durumu: Hata mesajını göstermek için showAlert'ı true yapabilir
                                print("Wrong password")
                                //popup.showMessage("Wrong Password")
                            case "This user does not exist":
                                // Kullanıcı yok durumu: Hata mesajını göstermek için showAlert'ı true yapabilir
                                print("This user does not exist")
                                //popup.showMessage("This User Does Not Exist")
                            default:
                                // Bilinmeyen durum
                                print("Bilinmeyen mesaj")
                            }
                        }
                    } catch {
                        // Handle JSON parsing error
                        print("Error parsing JSON: \(error)")
                    }
                }
            }
            // Resume the task to execute the request
            task.resume()
        } catch {
            print("Error: \(error)")
        }
    }
    
    
    func SignupPostRequest(username: String, password: String, email: String) {
        let jsonObject: [String: Any] = [
            "user_id": username,
            "password": password,
            "email": email
        ]
        
        do {
            let jsonData = try JSONSerialization.data(withJSONObject: jsonObject, options: .prettyPrinted)
            let url = URL(string: "http://127.0.0.1:8008/sign_up")! // SignUp için uygun olan URL
            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            request.setValue("application/json", forHTTPHeaderField: "Content-Type")
            request.httpBody = jsonData
            
            let task = URLSession.shared.dataTask(with: request) { data, response, error in
                if let error = error {
                    print("Error: \(error)")
                    return
                }
                
                guard let httpResponse = response as? HTTPURLResponse else {
                    print("Invalid or no HTTP response")
                    return
                }
                
                print("Status code: \(httpResponse.statusCode)")
                
                if let data = data {
                    do {
                        let responseJSON = try JSONSerialization.jsonObject(with: data, options: [])
                        if let jsonDictionary = responseJSON as? [String: Any],
                           let message = jsonDictionary["message"] as? String {
                            switch message {
                            case "Success":
                                print("Kayıt başarılı!")
                                // Burada isterseniz otomatik olarak login sayfasına yönlendirebilirsiniz
                                navigator.SignupToWeb()
                                // Spotify Page e login
                                
                            case "User already exists":
                                print("Kullanıcı zaten mevcut!")
                                
                            default:
                                print("Bilinmeyen mesaj")
                            }
                        }
                    } catch {
                        print("Error parsing JSON: \(error)")
                    }
                }
            }
            task.resume()
        } catch {
            print("Error: \(error)")
        }
    }

}
