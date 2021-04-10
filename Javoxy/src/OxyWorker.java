
import java.net.Socket;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Rathinn
 */
public class OxyWorker implements Runnable{
    Socket connection;
    
    public OxyWorker(Socket socket){
        connection = socket;
    }
    
    @Override
    public void run(){
        
    }
}
