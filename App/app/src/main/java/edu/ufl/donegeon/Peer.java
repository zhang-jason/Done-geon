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
    TextView NFCtxt;
    EditText editTxt;
    Activity act;

    public Peer(Activity act) {
        txt = act.findViewById(R.id.nfc_contents);
        NFCtxt = act.findViewById(R.id.NFC_Txt);
        this.act = act;
        editTxt = act.findViewById(R.id.manualIP);
        act.findViewById(R.id.submitIP).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                manualConnect(editTxt.getText().toString());
            }
        });
    }

    void changeText(String newText){
        act.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                txt.setText(newText);
            }
        });
    }

    void changeTextNFC(String newText){
        act.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                NFCtxt.setText(newText);
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
        changeTextNFC("Scan NFC Tag");
        changeVisibility(R.id.NFC_Txt, View.VISIBLE);
        changeVisibility(R.id.nfc_contents,View.GONE);
        changeVisibility(R.id.manualIP,View.GONE);
        changeVisibility(R.id.submitIP,View.GONE);
        changeVisibility(R.id.connect,View.GONE);
        changeVisibility(R.id.game,View.VISIBLE);
    }

    void spawnManual(){
        try{
            sleep(5000);
            if(sendTo == null){
                changeText("Game device not found");
                changeVisibility(R.id.submitIP,View.VISIBLE);
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
    HashMap<String,Integer> powerups = new HashMap<>();
    int bones = 0, health = 4;
    InetAddress thisAddr;
    int port = 65433;
    Peer p;

    public Receiver(Peer p,InetAddress thisAddr) {
        this.p = p;
        this.thisAddr = thisAddr;
    }

    void parse(String msg){
        if(msg.equals("closedGame") || msg.equals("lose")) {
            setupBtns();
            health = 4;
            bones = 0;
            if (msg.equals("closedGame")) {
                p.sendTo = null;
                p.changeText("Game disconnected.\n Waiting for new connection...");
                p.changeVisibility(R.id.game, View.GONE);
                p.changeVisibility(R.id.connect, View.VISIBLE);
                p.shouldScan = true;
                p.changeTextNFC(".");
                p.changeVisibility(R.id.NFC_Txt, View.GONE);
                p.changeVisibility(R.id.PlayerPicNec, View.GONE);
                p.changeVisibility(R.id.PlayerPicRea, View.GONE);
                p.changeVisibility(R.id.nfc_contents, View.VISIBLE);
            }
        }
        char type = msg.charAt(0);
        String value = msg.substring(2);
        if (type == 'b') {
            bones = Integer.parseInt(value);
        } else if (type == 'h') {
            health = Integer.parseInt(value);
        } else if (type == 'u' && value.compareTo("empty") != 0) {
            powerups.put(value, powerups.get(value) - 1 < 0 ? 0 : powerups.get(value) - 1);
        } else if (type == 'p') {
            boolean has = powerups.containsKey(value);
            int count = has ? powerups.get(value) : 0;
            powerups.put(value, count + 1);
        }
        updateUI();
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
            if(num/size[i] != 0 || size[i] == 1)
                blank = false;
            int[] images = {blank? R.drawable.blank:R.drawable.zero,R.drawable.one,R.drawable.two,R.drawable.three,R.drawable.four,
                    R.drawable.five,R.drawable.six,R.drawable.seven,R.drawable.eight,R.drawable.nine};
            ImageView img = p.act.findViewById(pos[i]);
            img.setImageResource(images[num/size[i]]);
            num = num % size[i];
        }

    }

    void greyOut(Button btn, int image){
        btn.setCompoundDrawablesWithIntrinsicBounds(0, image, 0, 0);
    }

    String[] powerupNames = {"Heal","Shield","Speed"};
    int[] btnIds = {R.id.heal,R.id.shield,R.id.speed};
    int[] icons = {R.drawable.heal,R.drawable.shield,R.drawable.speed};
    int[] icons_empty = {R.drawable.heal_empty,R.drawable.shield_empty,R.drawable.speed_empty};

    String[] minionNames = {"Melee_Corpse_Zombie", "Melee_Sand_Zombie", "Melee_Skeleton_Knight",
            "Ranged_Sand_Archer", "Ranged_Witch", "Random"};
    int[] mnIds = {R.id.mone,R.id.mtwo,R.id.mthree,R.id.mfour,R.id.mfive,R.id.mrand};
    int[] mnIcons = {R.drawable.mone,R.drawable.mtwo,R.drawable.mthree,R.drawable.mfour,R.drawable.mfive,R.drawable.mrand};
    int[] mn_icons_empty = {R.drawable.mone_grey,R.drawable.mtwo_grey,R.drawable.mthree_grey,
            R.drawable.mfour_grey,R.drawable.mfive_grey,R.drawable.mrand_grey};

    void setupBtns(){
        for(int i = 0; i < powerupNames.length; i++){
            powerups.put(powerupNames[i],0);
            Button btn = p.act.findViewById(btnIds[i]);
            String value = powerupNames[i];
            btn.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    if(powerups.get(value) > 0){
                        p.sendMsg("p " + value);
                        powerups.put(value, powerups.get(value) - 1 < 0? 0: powerups.get(value) - 1);
                    }
                }
            });
        }
        for(int i = 0; i < minionNames.length; i++){
            Button btn = p.act.findViewById(mnIds[i]);
            String value = minionNames[i];
            btn.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    p.sendMsg("m " + value);
                    for(int i = 0; i < minionNames.length;i++){
                        Button btn = p.act.findViewById(mnIds[i]);
                        greyOut(btn,minionNames[i].equals(value)?mnIcons[i]:mn_icons_empty[i]);
                    }
                }
            });
        }
    }

    void updateBtns(){
        for(int i = 0; i < powerupNames.length; i++){
            Button btn = p.act.findViewById(btnIds[i]);
            int count = powerups.get(powerupNames[i]);
            btn.setText(powerupNames[i] + ": " + count);
            greyOut(btn,count > 0? icons[i] : icons_empty[i]);
        }
    }

    void updateUI(){
        updateBones(bones);
        updateHealthbar(health);
        updateBtns();
    }

    public void run() {
        setupBtns();
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