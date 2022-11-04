package edu.ufl.donegeon;

import android.app.Activity;
import android.content.Context;
import android.media.Image;
import android.net.wifi.WifiManager;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.GridLayout;


import java.math.BigInteger;
import java.net.*;
import java.util.ArrayList;
import java.util.BitSet;
import java.util.HashMap;

public class Peer extends Thread {
    boolean alive = true, shouldScan = true, canSend = false;
    int sendPort = 65432, prefix = 24;
    InetAddress thisAddr, sendTo, broadcast;
    byte[] ipBase, ipMax;
    String sendMsg;
    DatagramSocket s;
    TextView txt;
    EditText editTxt;
    Activity act;
    GridLayout healthGrid,bneCnt;

    View.OnClickListener listener = new View.OnClickListener() {
        @Override
        public void onClick(View view) {
            manualConnect(editTxt.getText().toString());
        }
    };

    public Peer(Activity act) {
        txt = act.findViewById(R.id.nfc_contents);
        this.act = act;
    }

    void changeText(String newText){
        act.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                txt.setText(newText);
            }
        });
    }

    void changeVisibility(int id, int visibility){
        act.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                act.findViewById(id).setVisibility(visibility);
            }
        });
    }

    void changeVisibilityGrid(int gridID, int bneCntID, int visibility){
        class visibilityChangerGrid implements Runnable {
            int gridID, lifeTxtID, bneCntID, bneTxtID,visibility;
            visibilityChangerGrid(int gridID, int bneCntID, int visibility){
                this.gridID = gridID;
                this.visibility = visibility;
                this.bneCntID = bneCntID;
            }
            @Override
            public void run() {
                healthGrid = act.findViewById(gridID);
                healthGrid.setVisibility(visibility);
                bneCnt = act.findViewById(bneCntID);
                bneCnt.setVisibility(visibility);
            }
        }
        visibilityChangerGrid vCG = new visibilityChangerGrid(gridID, bneCntID, visibility);
        act.runOnUiThread(vCG);
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
        changeVisibilityGrid(R.id.lifeGrid, R.id.boneCntPic, View.VISIBLE);
        changeText("Connected to: " + sendTo.getHostName() + "\n Scan NFC Tag");
        changeVisibility(R.id.submitIP, View.GONE);
        changeVisibility(R.id.manualIP,View.GONE);
    }

    void spawnManual(){
        try{
            sleep(5000);
            if(sendTo == null){
                changeText("Game device not found");
                editTxt = act.findViewById(R.id.manualIP);
                act.findViewById(R.id.submitIP).setOnClickListener(listener);
                changeVisibility(R.id.submitIP, View.VISIBLE);
                changeVisibility(R.id.manualIP,View.VISIBLE);
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
            WifiManager wm = (WifiManager) act.getApplicationContext().getSystemService(Context.WIFI_SERVICE);
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
        sendMsg("appClosed");
        alive = false;
    }
}

class Receiver extends Thread {
    TextView hpTxt, boneTxt;
    HashMap<String,Integer> powerups = new HashMap<>();
    int bones = 0, health = 0;
    InetAddress thisAddr;
    int port = 65433;
    Peer p;
    ArrayList<Button> btns = new ArrayList<>();
    LinearLayout ll;

    public Receiver(Peer p,InetAddress thisAddr) {
        this.p = p;
        this.thisAddr = thisAddr;
        ll = p.act.findViewById(R.id.layout);
    }

    void clearButtons(){
        powerups = new HashMap<>();
        for(Button b : btns){
            p.act.runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    ll.removeView(b);
                }
            });
        }
        btns = new ArrayList<>();
    }



    void parse(String msg){
        if(msg.equals("closedGame")){
            p.sendTo = null;
            p.changeText("Game disconnected.\n Waiting for new connection...");
            p.changeVisibilityGrid(R.id.lifeGrid, R.id.boneCntPic, View.GONE);
            clearButtons();
            p.shouldScan = true;
        }
        if(msg.equals("lose")){
            clearButtons();
        }
        char type = msg.charAt(0);
        String value = msg.substring(2);
        if(type == 'b'){
            bones = Integer.parseInt(value);
        }
        else if(type == 'h'){
            health = Integer.parseInt(value);
        }
        else if(type == 'u' && value.compareTo("empty") != 0){
            powerups.put(value, powerups.get(value) - 1 < 0 ? 0: powerups.get(value)-1);
        }
        else if(type == 'p'){
            boolean has = powerups.containsKey(value);
            int count = has ? powerups.get(value) : 0;
            powerups.put(value, count + 1);
            if(has == false){
                p.act.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        Button btn = new Button(p.act);
                        btn.setLayoutParams(new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT));
                        btns.add(btn);
                        ll.addView(btn);
                    }
                });
            }
        }
        changeText();
    }

    void updateHealthbar(int health){
        int[] healthBar = {R.id.healthPic1,R.id.healthPic2,R.id.healthPic3,R.id.healthPic4};
        for(int i = 0; i < 4;i++){
            if(i < health)
                p.changeVisibility(healthBar[i],View.VISIBLE);
            else
                p.changeVisibility(healthBar[i],View.GONE);
        }
    }

    void updateBones(int bones){
        int num = bones;
        boolean blank = true;
        int[] pos = {R.id.tenk,R.id.onek,R.id.hundred,R.id.ten,R.id.one};
        int[] size = {10000,1000,100,10,1};
        for(int i = 0; i < pos.length;i++){
            int[] images = {blank? R.drawable.blank:R.drawable.zero,R.drawable.one,R.drawable.two,R.drawable.three,R.drawable.four,
                    R.drawable.five,R.drawable.six,R.drawable.seven,R.drawable.eight,R.drawable.nine};
            ImageView img = p.act.findViewById(pos[i]);
            img.setImageResource(images[num/size[i]]);
            if(num/size[i] != 0 || size[i] == 1)
                blank = false;
            num = num % size[i];
        }

    }

    void changeText(){
        updateBones(bones);
        updateHealthbar(health);
        ArrayList<String> powerupNames = new ArrayList<>(powerups.keySet());
        ArrayList<Integer> powerupNums = new ArrayList<>(powerups.values());
        for(int i = 0; i < powerupNames.size(); i++){
            String value = powerupNames.get(i);
            btns.get(i).setText(powerupNames.get(i) + ": " + powerupNums.get(i));
            btns.get(i).setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    Log.e("","p " + value);
                    if(powerups.get(value) > 0){
                        p.sendMsg("p " + value);
                        powerups.put(value, powerups.get(value) - 1 < 0? 0: powerups.get(value) - 1);
                    }
                }
            });
        }
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
                    parse(msgRecvd);
                } catch (Exception e) {}
            }
        } catch (Exception e) {
            Log.e("",e.toString());
            this.run();
        }
    }
}