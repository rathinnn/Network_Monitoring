/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Rathinn
 */

import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.net.SocketTimeoutException;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;

public class OxyServer implements Runnable{
    
    volatile boolean isRunning;
    ServerSocket serverPort; 

    public boolean isRunning() {
        return isRunning;
    }

    public void signalstop() {
        this.isRunning = false;
    }
    
    private void startRunning(){
        this.isRunning = true;
    }
    @Override
    public void run(){
        Scanner in = new Scanner(System.in);
        
        while(isRunning()){
            System.out.println("Enter 'Exit' to stop the Server");
            if(in.nextLine().equals("Exit")){
                signalstop();
            }
        }
        
        
        
    }
    
    public void start(){
        startRunning();
        
        while(isRunning()){
            try {
                Socket connection = serverPort.accept();
            } catch (IOException ex) {
                Logger.getLogger(OxyServer.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }
    
    public OxyServer(int portNo){
        
        try {
            serverPort = new ServerSocket(portNo);
            startRunning();
        } catch (IOException ex) {
            Logger.getLogger(OxyServer.class.getName()).log(Level.SEVERE, null, ex);
        }
        
            
    }
}
