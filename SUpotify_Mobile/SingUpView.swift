//
//  SingUpView.swift
//  SUpotify_Mobile
//
//  Created by Halil İbrahim Deniz on 31.10.2023.
//

import SwiftUI

struct SignUpView: View {
    @State private var username: String = ""
    @State private var email: String = ""
    @State private var password: String = ""
    @State private var confirmPassword: String = ""
    @State private var navigateToLogin: Bool = false
    @State private var showAlert: Bool = false
    @State private var alertTitle: String = ""
    @State private var alertMessage: String = ""

    var body: some View {
        ZStack {
            let startColor = Color(red: 13/255, green: 35/255, blue: 22/255) // RGB(13, 35, 22)
            let endColor = Color(red: 30/255, green: 16/255, blue: 37/255) // RGB(30, 16, 37)

            LinearGradient(gradient: Gradient(colors: [startColor, endColor]), startPoint: .leading, endPoint: .trailing)
                .edgesIgnoringSafeArea(.all)
            
            Rectangle()
                           .fill(Color(hex: "#363636").opacity(0.9))
                           .frame(width: 370, height: 750)
                           .cornerRadius(15)


               VStack(spacing: 20) {
                   
                   Text("Sign Up")
                       .font(Font.custom("Avantgarde Gothic", size: 40))
                       .fontWeight(.bold)
                       .foregroundColor(.white)
                       .shadow(color: .black, radius: 1, x: 0, y: 1) // Adds a slight shadow to the text
                       .padding(.top, 100)
                       .padding(.bottom, 70)


                   TextField("Username", text: $username)
                       .padding()
                       .font(Font.custom("Avantgarde Gothic", size: 18))
                       .background(Color.white.opacity(0.9))  // Adjusted opacity
                       .cornerRadius(8)
                       .overlay(
                           RoundedRectangle(cornerRadius: 8)
                               .stroke(Color.gray, lineWidth: 2)
                       )
                       .padding(.horizontal)  // Added horizontal padding

                   TextField("Email", text: $email)
                       .padding()
                       .font(Font.custom("Avantgarde Gothic", size: 18))
                       .background(Color.white.opacity(0.9))  // Adjusted opacity
                       .cornerRadius(8)
                       .overlay(
                           RoundedRectangle(cornerRadius: 8)
                               .stroke(Color.gray, lineWidth: 2)  // Added border
                       )
                       .padding(.horizontal)  // Added horizontal padding

                   SecureField("Password", text: $password)
                       .padding()
                       .font(Font.custom("Avantgarde Gothic", size: 18))
                       .background(Color.white.opacity(0.9))  // Adjusted opacity
                       .cornerRadius(8)
                       .overlay(
                           RoundedRectangle(cornerRadius: 8)
                               .stroke(Color.gray, lineWidth: 2)  // Added border
                       )
                       .padding(.horizontal)  // Added horizontal padding

                   SecureField("Confirm Password", text: $confirmPassword)
                       .padding()
                       .font(Font.custom("Avantgarde Gothic", size: 18))
                       .background(Color.white.opacity(0.9))
                       .cornerRadius(8)
                       .overlay(
                           RoundedRectangle(cornerRadius: 8)
                               .stroke(Color.gray, lineWidth: 2)
                       )
                       .padding(.horizontal)  // Added horizontal padding
                   
                   Divider()  // This adds the white line
                       .background(Color.white)
                       .padding(.horizontal)  // To match the padding of the fields above
                       .padding(.vertical, 15)  // Optional: adds some space above and below the line

                   Button(action: {
                       if password == confirmPassword {
                           signUpUser()
                       } else {
                           showAlert(with: "Error", message: "Passwords do not match!")
                       }
                   }) {
                       Text("Sign Up")
                           .padding()
                           .font(Font.custom("Avantgarde Gothic", size: 18))
                           .frame(width: 330)
                           .foregroundColor(Color(hex: "#363636"))
                           .background(Color(hex: "2e8b57"))
                           .cornerRadius(8)
                           
                   }


                   Spacer()

                   HStack {
                       Text("Already have an account?")
                           .foregroundColor(.white)
                           .font(Font.custom("Avantgarde Gothic", size: 18))
                       Button(action: {
                           self.navigateToLogin.toggle()
                       }) {
                           Text("Log in")
                               .foregroundColor(.green)
                               .font(Font.custom("Avantgarde Gothic", size: 18))
                       }
                       .background(
                           NavigationLink("", destination: LoginView(), isActive: $navigateToLogin)
                               .hidden()
                       )
                   }
               }
               .padding()

               .alert(isPresented: $showAlert) {
                   Alert(title: Text(alertTitle), message: Text(alertMessage), dismissButton: .default(Text("OK")))
               }
               }
           }

    func showAlert(with title: String, message: String) {
        alertTitle = title
        alertMessage = message
        showAlert = true
    }

    func signUpUser() {
        // Define the URL and the payload
        guard let url = URL(string: "https://jsonplaceholder.typicode.com/posts") else { return }

        let userData: [String: Any] = [
            "email": email,
            "username": username,
            "password": password
        ]

        do {
            let requestData = try JSONSerialization.data(withJSONObject: userData)
            
            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            request.setValue("application/json", forHTTPHeaderField: "Content-Type")
            request.httpBody = requestData

            URLSession.shared.dataTask(with: request) { (data, response, error) in
                if let error = error {
                    DispatchQueue.main.async {
                        showAlert(with: "Error", message: error.localizedDescription)
                    }
                    return
                }
                
                if let data = data {
                    do {
                        if let responseJSON = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any] {
                            DispatchQueue.main.async {
                                showAlert(with: "Response Received", message: "Data echoed back: \(responseJSON)")
                            }
                        }
                    } catch {
                        DispatchQueue.main.async {
                            showAlert(with: "Error", message: "Failed to parse JSON response")
                        }
                    }
                }
            }.resume()
        } catch {
            showAlert(with: "Error", message: "Failed to serialize JSON")
        }
    }
}

struct SignUpView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            SignUpView()
        }
    }
}

// Color extension to handle hex values
extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0

        Scanner(string: hex).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch hex.count {
        case 3: // RGB (12-bit)
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6: // RGB (24-bit)
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: // ARGB (32-bit)
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (255, 0, 0, 0)
        }

        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue:  Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
}
