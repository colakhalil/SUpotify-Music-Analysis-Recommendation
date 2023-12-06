//
//  ContentView.swift
//  SUpotify_Mobile
//
//  Created by Halil İbrahim Deniz on 31.10.2023.
//

import SwiftUI

struct LoginView: View {
    @State private var email: String = ""
    @State private var password: String = ""
    
    var body: some View {
        ZStack {
            let startColor = Color(red: 13/255, green: 35/255, blue: 22/255)
            let endColor = Color(red: 30/255, green: 16/255, blue: 37/255)

            LinearGradient(gradient: Gradient(colors: [startColor, endColor]), startPoint: .leading, endPoint: .trailing)
                .edgesIgnoringSafeArea(.all)

            Rectangle()
                .fill(Color(hex: "#363636").opacity(0.9))
                .frame(width: 370, height: 750)
                .cornerRadius(15)

            VStack(spacing: 20) {
                Text("Login")
                    .font(Font.custom("Avantgarde Gothic", size: 40))
                    .fontWeight(.bold)
                    .foregroundColor(.white)
                    .shadow(color: .black, radius: 1, x: 0, y: 1)
                    .padding(.top, 100)
                    .padding(.bottom, 70)
                
                
                Text("Please enter your email and password!")
                    .font(Font.custom("Avantgarde Gothic", size: 18))
                    .font(.headline)
                    .foregroundColor(.gray)

                TextField("Email", text: $email)
                    .padding()
                    .font(Font.custom("Avantgarde Gothic", size: 18))
                    .background(Color.white.opacity(0.9))
                    .cornerRadius(8)
                    .overlay(
                        RoundedRectangle(cornerRadius: 8)
                            .stroke(Color.gray, lineWidth: 2)
                    )
                    .padding(.horizontal)
                    .autocapitalization(.none) // prevent auto-capitalization

                SecureField("Password", text: $password)
                    .padding()
                    .font(Font.custom("Avantgarde Gothic", size: 18))
                    .background(Color.white.opacity(0.9))
                    .cornerRadius(8)
                    .overlay(
                        RoundedRectangle(cornerRadius: 8)
                            .stroke(Color.gray, lineWidth: 2)
                    )
                    .padding(.horizontal)

                Divider()
                    .background(Color.white)
                    .padding(.horizontal)
                    .padding(.vertical, 15)

                Button(action: {
                    apicaller.loginPostRequest(email: email, password: password) { success in
                        if success {
                            // Handle successful login
                            print("Login successful")
                            // Navigate to the main screen or perform necessary actions
                        } else {
                            // Handle login failure
                            print("Login failed")
                            // Show an error message or perform actions for failed login
                        }
                    }
                }) {
                    Text("Login")
                        .padding()
                        .font(Font.custom("Avantgarde Gothic", size: 18))
                        .frame(width: 330)
                        .foregroundColor(Color(hex: "#363636"))
                        .background(Color(hex: "#c1cdc1"))
                        .cornerRadius(8)
                }
                
                Spacer()

                HStack {
                    Text("Don't have an account?")
                        .foregroundColor(.white)
                        .font(Font.custom("Avantgarde Gothic", size: 18))
                    Button(action: {
                        navigator.LoginToSignup()
                    }) {
                        Text("Sign Up")
                            .foregroundColor(.green)
                            .font(Font.custom("Avantgarde Gothic", size: 18))
                    }

                }
            }
            .padding()

        }
    }
}

//struct SignInView_Previews: PreviewProvider {
//    static var previews: some View {
//        NavigationView {
//            LoginView()
//        }
//    }
//}
