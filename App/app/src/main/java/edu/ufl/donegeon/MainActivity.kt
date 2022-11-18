package edu.ufl.donegeon

import android.app.Activity
import android.app.PendingIntent
import android.content.Intent
import android.content.IntentFilter
import android.nfc.*
import android.os.Bundle
import android.os.Parcelable
import android.view.View
import android.widget.ImageView
import android.widget.TextView
import edu.ufl.donegeon.databinding.ActivityMainBinding

class MainActivity : Activity() {

    lateinit var txtVw: TextView
    lateinit var nfcAdapter: NfcAdapter
    lateinit var pendingIntent: PendingIntent
    lateinit var myTag: Tag
    lateinit var server: Peer
    lateinit var plyPicN: ImageView
    lateinit var plyPicR: ImageView


    public override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        var binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        txtVw = findViewById(R.id.NFC_Txt)
        plyPicN = findViewById(R.id.PlayerPicNec)
        plyPicR = findViewById(R.id.PlayerPicRea)
        //plyPic = findViewById(R.id.PlayerPicNec)
        server = Peer(this)
        server.start()

        nfcAdapter = NfcAdapter.getDefaultAdapter(this)
        if (nfcAdapter == null) {
            finish()
        }

        pendingIntent = PendingIntent.getActivity(this, 0,
            Intent(this, javaClass).addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP), PendingIntent.FLAG_MUTABLE)
    }

    fun readTag(intent: Intent) {
        val action = intent.action
        val actions = arrayOf(NfcAdapter.ACTION_TAG_DISCOVERED,
            NfcAdapter.ACTION_TECH_DISCOVERED, NfcAdapter.ACTION_NDEF_DISCOVERED)
        for(a in actions){
            if (a == action) {
                myTag = intent.getParcelableExtra<Parcelable>(NfcAdapter.EXTRA_TAG) as Tag
                val rawMsgs = intent.getParcelableArrayExtra(NfcAdapter.EXTRA_NDEF_MESSAGES)
                var msgs = mutableListOf<NdefMessage>()
                if (rawMsgs != null) {
                    for (i in rawMsgs.indices) {
                        msgs.add(i, rawMsgs[i] as NdefMessage)
                    }
                    assembleTagMsg(msgs.toTypedArray())
                }
            }
        }
    }

    fun assembleTagMsg(msgs: Array<NdefMessage>) {
        if (msgs == null || msgs.isEmpty() || server.checkConn()) return
        val payload = msgs[0].records[0].payload
        try {
            var text = String(payload, 3, payload.size - 3)
            txtVw.text = "You have chosen: $text"
            server.sendMsg("n " + text)
            if (text == "Necromancer"){
                plyPicR.visibility = View.GONE
                plyPicN.visibility = View.VISIBLE
            }
            else if (text == "Reaper") {
                plyPicN.visibility = View.GONE
                plyPicR.visibility = View.VISIBLE
            }
        } catch (e: Exception) {
        }
    }

    override fun onNewIntent(intent: Intent) {
        setIntent(intent)
        readTag(intent)
        if (NfcAdapter.ACTION_TAG_DISCOVERED == intent.action) {
            myTag = intent.getParcelableExtra(NfcAdapter.EXTRA_TAG)!!
        }
    }

    override fun onPause() {
        super.onPause()
        nfcAdapter.disableForegroundDispatch(this)
    }

    override fun onResume() {
        super.onResume()
        nfcAdapter.enableForegroundDispatch(this, pendingIntent,
            arrayOf(IntentFilter(NfcAdapter.ACTION_TAG_DISCOVERED)), null)
    }

    override fun onDestroy() {
        super.onDestroy()
        server.kill()
    }
}