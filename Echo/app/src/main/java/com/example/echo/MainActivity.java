package com.example.echo;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.speech.tts.TextToSpeech;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.Serializable;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.WebSocket;
import okhttp3.WebSocketListener;

public class MainActivity extends AppCompatActivity implements TextToSpeech.OnInitListener, View.OnClickListener{
    Intent intent;
    public SpeechRecognizer mRecognizer = SpeechRecognizer.createSpeechRecognizer(this);
    public Button sttBtn;
    TextView textView;
    final int PERMISSION = 1;
    private TextToSpeech tts;
    ArrayList<String> matches;
    String ip_add="192.168.35.49";
    int port_num=8888;
    public static final int MY_UI = 1234;
    private WebSocket webSocket;
    private String SERVER_PATH = "ws://192.168.35.42:3000";
    //private String SERVER_PATH = "ws://192.168.35.203:3000";
    String msg="";
    Socket socket = null;
    public OkHttpClient client;
    Request request;
    private static final int NORMAL_CLOSURE_STATUS = 1000;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        tts = new TextToSpeech(this, this);

        if ( Build.VERSION.SDK_INT >= 23 ){
            // 퍼미션 체크
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.INTERNET,
                    Manifest.permission.RECORD_AUDIO},PERMISSION);
        }

        textView = (TextView)findViewById(R.id.sttResult);
        final Button sttBtn = (Button) findViewById(R.id.sttStart);

        intent=new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intent.putExtra(RecognizerIntent.EXTRA_CALLING_PACKAGE,getPackageName());
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE,"ko-KR");

        client = new OkHttpClient();
        request = new Request.Builder().url(SERVER_PATH).build();

        mRecognizer.setRecognitionListener(listener);
        mRecognizer.startListening(intent);
        /*sttBtn.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                Log.d("???","된거야??");
                mRecognizer.setRecognitionListener(listener);
                mRecognizer.startListening(intent);
                Log.d("test","wait~");
            }
        });*/
        sttBtn.setOnClickListener((View.OnClickListener) this);
    }

    @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
    public void speakOut(String tts_con) {
        Log.d("speak2",tts_con);
        CharSequence text = tts_con;
        //tts.setPitch((float) 0.6);
        tts.setSpeechRate((float) 1.0);
        tts.speak(text,TextToSpeech.QUEUE_FLUSH,null,"id1");
        while (tts.isSpeaking() ) {
        };
        Log.d("???",":<");
        sttBtn.performClick();
        //intent=new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        //intent.putExtra(RecognizerIntent.EXTRA_CALLING_PACKAGE,getPackageName());
        //intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE,"ko-KR");

        //mRecognizer.setRecognitionListener(listener);
        //mRecognizer.startListening(intent);
        //startActivityForResult(new Intent(getApplicationContext(), MainActivity.class), MY_UI);
        //finish();
    }

    @Override
    public void onClick(View v) {
        Log.d("???","된거야??");
        mRecognizer.setRecognitionListener(listener);
        mRecognizer.startListening(intent);
        Log.d("test","wait~");
    }

    @Override
    public void onDestroy() {
        if (tts != null)  {
            tts.stop();
            tts.shutdown();
            webSocket.close(NORMAL_CLOSURE_STATUS, null);
        }
        finish();
        super.onDestroy();
    }

    @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
    @Override
    public void onInit(int status) {
        if (status == TextToSpeech.SUCCESS)  {
            int result = tts.setLanguage(Locale.KOREA);

            if (result == TextToSpeech.LANG_MISSING_DATA
                    || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                Log.e("TTS", "This Language is not supported");
            } else {

            }

        } else {
            Log.e("TTS", "Initilization Failed!");
        }
    }

    private RecognitionListener listener = new RecognitionListener() {

        @Override
        public void onReadyForSpeech(Bundle params) {
            Toast.makeText(getApplicationContext(),"음성인식을 시작합니다.",Toast.LENGTH_SHORT).show();
        }

        @Override
        public void onBeginningOfSpeech() {}

        @Override
        public void onRmsChanged(float rmsdB) {}

        @Override
        public void onBufferReceived(byte[] buffer) {}

        @Override
        public void onEndOfSpeech() {}

        @Override
        public void onError(int error) {
            String message;

            switch (error) {
                case SpeechRecognizer.ERROR_AUDIO:
                    message = "오디오 에러";
                    break;
                case SpeechRecognizer.ERROR_CLIENT:
                    message = "클라이언트 에러";
                    break;
                case SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS:
                    message = "퍼미션 없음";
                    break;
                case SpeechRecognizer.ERROR_NETWORK:
                    message = "네트워크 에러";
                    break;
                case SpeechRecognizer.ERROR_NETWORK_TIMEOUT:
                    message = "네트웍 타임아웃";
                    break;
                case SpeechRecognizer.ERROR_NO_MATCH:
                    mRecognizer.setRecognitionListener(listener);
                    mRecognizer.startListening(intent);
                    message = "찾을 수 없음";
                    break;
                case SpeechRecognizer.ERROR_RECOGNIZER_BUSY:
                    mRecognizer.setRecognitionListener(listener);
                    mRecognizer.startListening(intent);
                    //startActivityForResult(new Intent(getApplicationContext(), MainActivity.class), MY_UI);
                    //finish();
                    message = "RECOGNIZER가 바쁨";
                    break;
                case SpeechRecognizer.ERROR_SERVER:
                    message = "서버가 이상함";
                    break;
                case SpeechRecognizer.ERROR_SPEECH_TIMEOUT:
                    message = "말하는 시간초과";
                    break;
                default:
                    message = "알 수 없는 오류임";
                    break;
            }

            Toast.makeText(getApplicationContext(), "에러가 발생하였습니다. : " + message,Toast.LENGTH_SHORT).show();
        }

        @Override
        public void onResults(Bundle results) {
            String tts_con="";
            // 말을 하면 ArrayList에 단어를 넣고 textView에 단어를 이어줍니다.
             matches = results.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);

            for(int i = 0; i < matches.size() ; i++){
                tts_con=tts_con+matches.get(i);
                textView.setText(matches.get(i));
            }
            msg=tts_con;
            /*runOnUiThread(() -> {
                webSocket = client.newWebSocket(request, new SocketListener());
            });*/
            webSocket = client.newWebSocket(request, new SocketListener());
            Log.d("...","nbb");
            /*MyClientTask myClientTask = new MyClientTask(ip_add, port_num, tts_con);
            Log.d("msg1",tts_con);
            myClientTask.execute();*/

        }

        @Override
        public void onPartialResults(Bundle partialResults) {}

        @Override
        public void onEvent(int eventType, Bundle params) {}
    };

    private void initiateSocketConnection(String tts_con) {
        OkHttpClient client = new OkHttpClient();
        Request request = new Request.Builder().url(SERVER_PATH).build();
        webSocket = client.newWebSocket(request, new SocketListener());
    }

    private  class SocketListener extends WebSocketListener {
        @Override
        public void onOpen(WebSocket webSocket, Response response) {
            super.onOpen(webSocket, response);

            JSONObject jsonObject = new JSONObject();
            try {
                jsonObject.put("name","dahee");
                jsonObject.put("message",msg);

                webSocket.send(jsonObject.toString());
                //webSocket.send(msg);
                jsonObject.put("isSent", true);


            } catch (JSONException e) {
                e.printStackTrace();
            }

        }

        @Override
        public void onMessage(WebSocket webSocket, String s_text) {
            super.onMessage(webSocket, s_text);
            JSONObject jsonObject = null;
            Log.d("speak",s_text);
            //textView.setText(s_text);

            speakOut(s_text);
            try {
                jsonObject = new JSONObject(s_text);

                //textView.setText(text);
                //speakOut(s_text);

                jsonObject.put("isSent", false);
            } catch (JSONException e) {
                e.printStackTrace();
                Log.d("bug","sibal");
            }
        }
    }

    /*@Override
    public void onBackPressed() {
        Toast.makeText(this, "Back button pressed.", Toast.LENGTH_SHORT).show();
        if (tts != null)  {
            tts.stop();
            tts.shutdown();
        }
        finish();
        super.onBackPressed();
    }*/

}