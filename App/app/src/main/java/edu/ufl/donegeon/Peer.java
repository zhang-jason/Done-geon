package edu.ufl.donegeon;

import android.content.Context;
import android.net.wifi.WifiManager;
import android.text.format.Formatter;
import android.util.Log;
import android.widget.TextView;

import java.io.*;
import java.net.*;

public class Peer extends Thread {
    public Sender sender;
    public Receiver receiver;
    Context context;
    TextView txt;

    public Peer(Context context, TextView txt) {
        this.context = context;
        this.txt = txt;
    }

    public void run() {
        WifiManager wm = (WifiManager) context.getSystemService(Context.WIFI_SERVICE);
        String ip = Formatter.formatIpAddress(wm.getConnectionInfo().getIpAddress());
        new Receiver(this).start();
        while (ip.charAt(ip.length() - 1) != '.') {
            ip = ip.substring(0, ip.length() - 1);
        }
        for (int i = 0; i < 256; i++) {
            new Sender(ip, i, this).start();
        }
    }

    public boolean checkConnection() {
        return sender == null;
    }

    public void setSendMsg(String msg) {
        sender.msg = msg;
        sender.msgCheck = true;
    }

    public void kill() {
        try {
            sender.s.close();
            sender.out.close();
            receiver.s.close();
            receiver.ss.close();
            receiver.in.close();
            Log.e("", "" + sender.s.isClosed());
        } catch (IOException e) {
            Log.e("", e.toString());
        }
    }
}

class Sender extends Thread {
    String msg = "";
    boolean msgCheck = false;
    Socket s;
    int ipNum;
    String ip;
    ObjectOutputStream out;
    Peer p;

    public Sender(String ip, int num, Peer p) {
        this.ip = ip + String.valueOf(num);
        ipNum = num;
        this.p = p;
    }

    public void run() {
        while (p.checkConnection()) {
            try {
                s = new Socket(this.ip, 65432);
                out = new ObjectOutputStream(s.getOutputStream());
                p.sender = this;
                p.txt.setText("Connected to: " + this.ip + "\nScan NFC tag");
                Log.e("", "connected" + this.ip);
                while (true) {
                    if (msgCheck) {
                        out.writeObject(msg);
                        out.flush();
                        msgCheck = false;
                    }
                }
            } catch (Exception e) {
            }
        }
    }
}

class Receiver extends Thread {
    int port = 65433;
    ServerSocket ss;
    Socket s;
    DataInputStream in;
    Peer p;

    public Receiver(Peer p) {
        this.p = p;
    }

    public void run() {
        try {
            while (ss == null) {
                ss = new ServerSocket(port);
                Log.e("", "Listening on port: " + port);
                s = ss.accept();
                p.receiver = this;
                Log.e("", "Connection received");
            }

            in = new DataInputStream(s.getInputStream());

            while (true) {
                String msg = in.readUTF();
                Log.e("", msg);
            }
        } catch (Exception e) {
        }
    }
}