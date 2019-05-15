package com.eye3.stocktech;

import java.util.ArrayList;
import java.util.HashMap;

import android.content.Context;
import android.content.Intent;
import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.Button;
import android.widget.ListView;
import android.widget.SimpleAdapter;


public class ReminderListActivity extends Activity {

    public static final String TAG = ReminderListActivity.class.getSimpleName();

    private ArrayList<HashMap<String, Object>> listItem = null;
    private SimpleAdapter itemAdapter = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        Log.d(TAG, "onCreate " + this.hashCode());
        super.onCreate(savedInstanceState);
        this.setContentView(R.layout.main);

        startService(new Intent(this, ReminderMqttService.class));

        // mbtn_add_item = (Button)this.findViewById(R.id.btn_add);
        // mbtn_add_item.setOnClickListener(new OnClickListener() {
        //     @Override
        //     public void onClick(View v) {
        //         HashMap<String, Object> map = new HashMap<String, Object>();
        //         map.put("item_image", R.drawable.checked);
        //         map.put("item_title", "Title-" + listItem.size());
        //         map.put("item_text", "New item!");
        //         listItem.add(map);
        //         itemAdapter.notifyDataSetChanged();
        //     }
        // });
        ListView list_view = (ListView)this.findViewById(R.id.list_view);
        listItem = new ArrayList<HashMap<String, Object>>();
        itemAdapter = new SimpleAdapter(
                this,
                listItem,
                R.layout.list_item,
                new String[] { "item_image", "item_title", "item_text" },
                new int[] { R.id.item_image, R.id.item_title, R.id.item_text } );

        list_view.setAdapter(itemAdapter);

        list_view.setOnItemClickListener(new OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view,
                    int position, long id) {
                Log.d(TAG, "onItemClick " + this.hashCode());
                // HashMap<String,String> map=(HashMap<String,String>)parent.getItemAtPosition(position);
                ReminderListActivity.this.setTitle("On click " + position + " item");
            }
        });

        // client = new ReminderMqttClient("127.0.0.1", 1883);
    }
}
