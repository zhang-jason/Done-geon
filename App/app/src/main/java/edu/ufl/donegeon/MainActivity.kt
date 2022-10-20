package edu.ufl.donegeon

import android.app.Activity
import android.app.PendingIntent
import android.content.Intent
import android.content.IntentFilter
import android.nfc.*
import android.os.Bundle
import android.os.Parcelable
import android.widget.TextView
import edu.ufl.donegeon.databinding.ActivityMainBinding

class MainActivity : Activity() {

    lateinit var txtVw: TextView
    lateinit var nfcAdapter: NfcAdapter
    lateinit var pendingIntent: PendingIntent
    lateinit var myTag: Tag
    lateinit var server: Peer


    public override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        var binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        txtVw = findViewById(R.id.nfc_contents)
        server = Peer(applicationContext,txtVw)
        server.start()

        nfcAdapter = NfcAdapter.getDefaultAdapter(this)
        if (nfcAdapter == null) {
            finish()
        }

        pendingIntent = PendingIntent.getActivity(this, 0,
            Intent(this, javaClass).addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP), 0)
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
        if (msgs == null || msgs.isEmpty()|| server.checkConnection()) return
        val payload = msgs[0].records[0].payload
        try {
            var text = String(payload, 3, payload.size - 4)
            txtVw.text = "Message on tag:\n $text"
            server.setSendMsg(text)
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