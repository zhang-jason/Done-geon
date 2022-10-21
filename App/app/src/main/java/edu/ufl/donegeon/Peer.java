package edu.ufl.donegeon;

import android.app.Activity;
import android.content.Context;
import android.net.wifi.WifiManager;
import android.util.Log;
import android.widget.TextView;

import java.math.BigInteger;
import java.net.*;

public class Peer extends Thread {
    boolean alive = true, shouldScan = true, canSend = false;
    InetAddress thisAddr, sendTo;
    int sendPort = 65432;
    String sendMsg;
    DatagramSocket s;
    Context context;
    TextView txt;
    Activity act;
    InterfaceAddress[] interfaces;

    public Peer(Context context, TextView txt, Activity act) {
        this.context = context;
        this.txt = txt;
        this.act = act;
    }

    void scan(){
        shouldScan = false;
        byte[] buf = "init".getBytes();
        while(sendTo == null){
            try{
                for (InterfaceAddress address : interfaces) {
                    if(address.getBroadcast() != null){
                        s.send(new DatagramPacket(buf, buf.length, address.getBroadcast(),sendPort));
                    }
                }
                if(sendTo != null)
                    break;
                sleep(500);
            }catch(Exception e){}
        }
        String sendToString = sendTo.getHostName();
        act.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                txt.setText("Connected to: " + sendToString + "\nScan NFC Tag");
            }
        });
    }

    public void run() {
        try{
            s = new DatagramSocket();
            WifiManager wm = (WifiManager) context.getSystemService(Context.WIFI_SERVICE);
            int ipNum = Integer.reverseBytes(wm.getConnectionInfo().getIpAddress());
            thisAddr = InetAddress.getByAddress(BigInteger.valueOf(ipNum).toByteArray());

            NetworkInterface networkInterface = NetworkInterface.getByInetAddress(thisAddr);
            InetAddress broadcast = null;
            interfaces = networkInterface.getInterfaceAddresses().toArray(new InterfaceAddress[0]);
            new Receiver(this,thisAddr).start();

            this.scan();

            byte[] buf;
            while(alive){
                if(shouldScan){
                    this.scan();
                }
                if(canSend){
                    canSend = false;
                    buf = sendMsg.getBytes();
                    s.send(new DatagramPacket(buf, buf.length, sendTo,sendPort));
                }
            }
            s.close();
        }catch(Exception e){}
    }

    public void sendMsg(String msg) {
        sendMsg = msg;
        canSend = true;
    }

    public boolean checkConn(){
        return sendTo == null;
    }

    public void kill() {
        alive = false;
    }
}

class Receiver extends Thread {
    InetAddress thisAddr;
    int port = 65433;
    Peer p;

    public Receiver(Peer p,InetAddress thisAddr) {
        this.p = p;
        this.thisAddr = thisAddr;
    }

    public void run() {
        try {
            DatagramSocket s = new DatagramSocket(port,thisAddr);
            while(p.alive){
                byte[] buf = new byte[1024];
                DatagramPacket msg = new DatagramPacket(buf, buf.length);
                try {
                    s.receive(msg);
                    p.sendTo = msg.getAddress();
                    String msgRecvd = new String(msg.getData(),0, msg.getLength());
                    if(msgRecvd.equals("closedGame")){
                        p.sendTo = null;
                        p.act.runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                p.txt.setText("Game disconnected.\n Waiting for new connection...");
                            }
                        });
                        p.shouldScan = true;
                    }
                    Log.e("",msgRecvd);
                } catch (Exception e) {}
            }
        } catch (Exception e) {
            this.run();
        }
    }
}