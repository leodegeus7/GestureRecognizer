//
//  SerialViewController.swift
//  Gesture-Recognition
//
//  Created by Leonardo Geus on 18/06/2018.
//  Copyright © 2018 Emerging Interactions. All rights reserved.
//

import UIKit
import CoreBluetooth

class SerialViewController: UIViewController, BluetoothSerialDelegate{
    func serialDidChangeState() {
        reloadView()
    }
    
    func serialDidDisconnect(_ peripheral: CBPeripheral, error: NSError?) {
        reloadView()
    }
    
    func serialDidReceiveString(_ message: String) {
        print(message)
    }
    

    override func viewDidAppear(_ animated: Bool) {
        reloadView()
    }
    
    @IBOutlet weak var barButton: UIBarButtonItem!
    override func viewDidLoad() {
        super.viewDidLoad()
        serial = BluetoothSerial(delegate: self)
        
        reloadView()
        // Do any additional setup after loading the view.
    }
    
    func reloadView() {
        // in case we're the visible view again
        serial.delegate = self
        
        if serial.isReady {
            self.navigationItem.title = serial.connectedPeripheral!.name
            barButton.title = "Desconectar"
            barButton.tintColor = UIColor.red
            barButton.isEnabled = true
        } else if serial.centralManager.state == .poweredOn {
            self.navigationItem.title = "Bluetooth Serial"
            barButton.title = "Conectar"
            barButton.tintColor = view.tintColor
            barButton.isEnabled = true
        } else {
            self.navigationItem.title = "Bluetooth Serial"
            barButton.title = "Conectar"
            barButton.tintColor = view.tintColor
            barButton.isEnabled = false
        }
        
        

    }
    


    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func ButtonTap(_ sender: Any) {
        if serial.connectedPeripheral == nil {
            performSegue(withIdentifier: "ShowScanner", sender: self)
        } else {
            serial.disconnect()
            reloadView()
        }
    }
    
    
    

    

}
