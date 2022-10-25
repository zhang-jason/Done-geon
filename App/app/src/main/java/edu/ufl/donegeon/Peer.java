package edu.ufl.donegeon;

import android.app.Activity;
import android.content.Context;
import android.net.wifi.WifiManager;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.math.BigInteger;
import java.net.*;
import java.util.BitSet;

public class Peer extends Thread {
    boolean alive = true, shouldScan = true, canSend = false;
    int sendPort = 65432, prefix = 24;
    InetAddress thisAddr, sendTo, broadcast;
    byte[] ipBase, ipMax;
    String sendMsg;
    DatagramSocket s;
    Context context;
    TextView txt;
    EditText editTxt;
    Activity act;


    View.OnClickListener listener = new View.OnClickListener() {
        @Override
        public void onClick(View view) {
            manualConnect(editTxt.getText().toString());
        }
    };

    public Peer(Context context, TextView txt, Activity act) {
        this.context = context;
        this.txt = txt;
        this.act = act;
    }

    void changeText(String newText){
        class textChanger implements Runnable {
            String text;
            textChanger(String s){
                text = s;
            }
            @Override
            public void run() {
                txt.setText(text);
            }
        }
        textChanger tC = new textChanger(newText);
        act.runOnUiThread(tC);
    }

    void changeVisibility(int btnID, int txtID, int visibility){
        class visibilityChanger implements Runnable {
            int btnID, txtID, visibility;
            visibilityChanger(int btnID, int txtID, int visibility){
                this.btnID = btnID;
                this.txtID = txtID;
                this.visibility = visibility;
            }
            @Override
            public void run() {
                Button btn = act.findViewById(btnID);
                btn.setVisibility(visibility);
                btn.setOnClickListener(listener);
                editTxt = act.findViewById(txtID);
                editTxt.setVisibility(visibility);
            }
        }
        visibilityChanger vC = new visibilityChanger(btnID,txtID,visibility);
        act.runOnUiThread(vC);
    }

    void scan(){
        shouldScan = false;
        byte[] buf = "init".getBytes();
        byte[] result = new byte[4];

        new Thread(){
            @Override
            public void run(){
                spawnManual();
            }
        }.start();

        while(sendTo == null){
            try{
                for(int i = Integer.reverseBytes(ipBase[3]<<24); i <= Integer.reverseBytes(ipMax[3]<<24);i++){
                    result[0] = (byte)i;
                    for(int j = Integer.reverseBytes(ipBase[2]<<24); j <= Integer.reverseBytes(ipMax[2]<<24);j++){
                        result[1] = (byte)j;
                        for(int k = Integer.reverseBytes(ipBase[1]<<24); k <= Integer.reverseBytes(ipMax[1]<<24);k++){
                            result[2] = (byte)k;
                            for(int l = Integer.reverseBytes(ipBase[0]<<24); l <= Integer.reverseBytes(ipMax[0]<<24);l++){
                                result[3] = (byte)l;
                                InetAddress addr = InetAddress.getByAddress(result);
                                s.send(new DatagramPacket(buf,buf.length,addr,sendPort));
                                if(sendTo != null)
                                    break;
                            }
                        }
                    }
                }
                sleep(500);
            }catch(Exception e){}
        }
        changeText("Connected to: " + sendTo.getHostName() + "\n Scan NFC Tag");
        changeVisibility(R.id.submitIP,R.id.manualIP,View.GONE);
    }

    void spawnManual(){
        try{
            sleep(5000);
            if(sendTo == null){
                changeText("Game device not found");
                changeVisibility(R.id.submitIP,R.id.manualIP,View.VISIBLE);
            }
        }catch (Exception e){}
    }

    void manualConnect(String ip){
        byte[] buf = "init".getBytes();
            new Thread(){
                @Override
                public void run(){
                    try{
                    s.send(new DatagramPacket(buf,buf.length,InetAddress.getByName(ip),sendPort));
                    }catch(Exception e){
                        changeText("Invalid IP");
                    }
                }
            }.start();
    }

    public void run() {
        try{
            byte[] buf;
            s = new DatagramSocket();
            WifiManager wm = (WifiManager) context.getSystemService(Context.WIFI_SERVICE);
            int ipNum = Integer.reverseBytes(wm.getConnectionInfo().getIpAddress());
            thisAddr = InetAddress.getByAddress(BigInteger.valueOf(ipNum).toByteArray());
            new Receiver(this,thisAddr).start();

            NetworkInterface networkInterface = NetworkInterface.getByInetAddress(thisAddr);
            InterfaceAddress[] interfaces = networkInterface.getInterfaceAddresses().toArray(new InterfaceAddress[0]);

            for(InterfaceAddress i : interfaces){
                if(i.getAddress() instanceof Inet4Address){
                    prefix = i.getNetworkPrefixLength();
                    broadcast = i.getBroadcast();
                }
            }

            BitSet bits = BitSet.valueOf(BigInteger.valueOf(Integer.reverseBytes(ipNum)).toByteArray());
            BitSet maxBits = BitSet.valueOf(BigInteger.valueOf(Integer.reverseBytes(ipNum)).toByteArray());
            for(int i = 0; i < 32- prefix; i++){
                bits.clear(i);
                maxBits.set(i);
            }
            ipBase = bits.toByteArray();
            ipMax = maxBits.toByteArray();

            scan();

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
                        p.changeText("Game disconnected.\n Waiting for new connection...");
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