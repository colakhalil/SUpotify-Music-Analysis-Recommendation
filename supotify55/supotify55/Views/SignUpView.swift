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
                    .autocapitalization(.none) // prevent auto-capitalization
                
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
                    .autocapitalization(.none) // prevent auto-capitalization
                
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
                        apicaller.signupPostRequest(username: username, password: password, email: email) { success in
                            if success {
                                // Handle successful signup
                                print("Signup successful")
                                
                                // Navigate to the web page after successful signup
                                navigator.SignupToWeb()
                                
                                // Proceed with other actions if needed
                            } else {
                                // Handle failed signup
                                print("Signup failed")
                                // Show an error message or perform actions for failed signup
                            }
                        }                    } else {
                        //popup.showMessage("Passwords do not match")
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
                        navigator.SignupToLogin()
                    }) {
                        Text("Login")
                            .foregroundColor(.green)
                            .font(Font.custom("Avantgarde Gothic", size: 18))
                    }
                }
            }
            .padding()
            
        }
        .navigationBarBackButtonHidden(true)
    }
    
}

//struct SignUpView_Previews: PreviewProvider {
//    static var previews: some View {
//        NavigationView {
//            SignUpView()
//        }
//    }
//}
