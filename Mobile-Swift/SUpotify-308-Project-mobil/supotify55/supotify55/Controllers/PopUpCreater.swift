//
//  PopUpCreater.swift
//  supotify55
//
//  Created by Furkan Emre Güler on 17.11.2023.
//

import Foundation
import UIKit

let popup = PopupGenerator.popupgenerator


class PopupGenerator {
    static let popupgenerator = PopupGenerator ()
    func showMessage(_ message: String, on viewController: UIViewController) {
        let alert = UIAlertController(title: "Popup", message: message, preferredStyle: .alert)
        let okayAction = UIAlertAction(title: "OK", style: .default, handler: nil)
        alert.addAction(okayAction)
        
        viewController.present(alert, animated: true, completion: nil)
    }
}
