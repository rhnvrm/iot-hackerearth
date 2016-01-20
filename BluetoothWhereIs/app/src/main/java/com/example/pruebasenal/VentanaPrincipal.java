package com.example.pruebasenal;

import android.app.Activity;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.RequestParams;

import org.apache.http.NameValuePair;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import cz.msebera.android.httpclient.Header;

public class VentanaPrincipal extends Activity {

    //Handler mHandler = new Handler();




    @Override
    protected void onDestroy() {
        unregisterReceiver(receiver);

        super.onDestroy();
    }

    private BluetoothAdapter bTAdapter ;


    TextView rssi_msg;

    int refresh_rate = 50;

    HashMap<String, Integer> BeaconMap;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.interfaz_ventana_principal);

        IntentFilter filter = new IntentFilter();

        filter.addAction(BluetoothDevice.ACTION_FOUND);
        filter.addAction(BluetoothAdapter.ACTION_DISCOVERY_FINISHED);


        registerReceiver(receiver, filter);

        bTAdapter = BluetoothAdapter.getDefaultAdapter();

        rssi_msg = (TextView) findViewById(R.id.textView);

        BeaconMap = new HashMap<String, Integer>();

        bTAdapter.startDiscovery();

        /*new Thread(new Runnable() {
            @Override
            public void run() {
                // TODO Auto-generated method stub
                while (true) {
                    try {
                        Thread.sleep(refresh_rate);
                        mHandler.post(new Runnable() {

                            @Override
                            public void run() {
                                // TODO Auto-generated method stub
                                // Write your code here to update the UI.


                            }
                        });
                    } catch (Exception e) {
                        // TODO: handle exception
                    }
                }
            }
        }).start();*/

    }

    public void postData(String bname, String uid, String rssi) throws IOException {


       RequestParams params = new RequestParams();

        params.put("beaconname", bname);
        params.put("buid", uid);
        params.put("rssi", rssi);

        AsyncHttpClient client = new AsyncHttpClient();
        client.post("http://10.6.5.124:8521/beacons", params, new AsyncHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] responseBody) {
               // Log.d(responseBody.);
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, byte[] responseBody, Throwable error) {

            }
        });

    }

    private String getQuery(List<NameValuePair> params) throws UnsupportedEncodingException
    {
        StringBuilder result = new StringBuilder();
        boolean first = true;

        for (NameValuePair pair : params)
        {
            if (first)
                first = false;
            else
                result.append("&");

            result.append(URLEncoder.encode(pair.getName(), "UTF-8"));
            result.append("=");
            result.append(URLEncoder.encode(pair.getValue(), "UTF-8"));
        }

        return result.toString();
    }

    public void refresh(View v){
        //rssi_msg.setText("");
        bTAdapter.startDiscovery();
        //refresh_rate = Integer.parseInt(((EditText)findViewById(R.id.editText2)).getText().toString());
    }

    public void clear(View v){
        rssi_msg.setText("");
        bTAdapter.startDiscovery();
    }


    private final BroadcastReceiver receiver = new BroadcastReceiver(){


        @Override
        public void onReceive(Context context, Intent intent) {

            String action = intent.getAction();


            if (BluetoothAdapter.ACTION_DISCOVERY_FINISHED.equals(action)) {
                //rssi_msg.setText("FUCK THIS"+ rssi_msg.getText() );
                for (Map.Entry<String, Integer> entry : BeaconMap.entrySet()) {
                    String key = entry.getKey();
                    Integer value = entry.getValue();

                    //rssi_msg.setText("");

                    rssi_msg.setText(rssi_msg.getText() + " :: " + "Bluetooth Device" + " :: " + key + " :: " + value + "dBm\n\n");




                    try {
                        postData("Bluetooth Device", key , String.valueOf(value));
                    } catch (IOException e) {
                        e.printStackTrace();
                    }


                }
                bTAdapter.startDiscovery();

            }
            else if(BluetoothDevice.ACTION_FOUND.equals(action)) {
               /* int rssi = intent.getShortExtra(BluetoothDevice.EXTRA_RSSI,Short.MIN_VALUE);
                String name = intent.getStringExtra(BluetoothDevice.EXTRA_NAME);
                rssi_msg.setText(rssi_msg.getText() +  + " => " + name + " => " + rssi + "dBm\n");*/

                rssi_msg.setText(rssi_msg.getText() + "." );
                BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
                int rssi = intent.getShortExtra(BluetoothDevice.EXTRA_RSSI,Short.MIN_VALUE);
                //rssi_msg.setText(rssi_msg.getText() + " :: " + device.getName() + " :: " + device.getAddress() + " :: " + rssi + "dBm\n\n");

                BeaconMap.put(device.getAddress(), rssi);
/*
                try {
                    postData("Bluetooth Device", device.getAddress() , String.valueOf(rssi));
                } catch (IOException e) {
                    e.printStackTrace();
                }*/
            }
        }
    };



}
