package com.eye3.stocktech;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.BroadcastReceiver;
import android.os.Bundle;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.Button;
import android.widget.ListView;
import android.widget.SimpleAdapter;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.alibaba.fastjson.TypeReference;

public class ReminderListActivity extends Activity {

    public static final String TAG = ReminderListActivity.class.getSimpleName();

    private ArrayList<HashMap<String, Object>> mListItem = null;
    private SimpleAdapter mItemAdapter = null;
    private Intent mIntent = null;
    private MessageReceiver mMsgReceiver = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        Log.d(TAG, "onCreate " + this.hashCode());
        super.onCreate(savedInstanceState);
        this.setContentView(R.layout.main);

 		mMsgReceiver = new MessageReceiver();
		IntentFilter intentFilter = new IntentFilter();
		intentFilter.addAction(Constants.ACTIONS_RECV_MESSAGE);
		registerReceiver(mMsgReceiver, intentFilter);

        // mbtn_add_item = (Button)this.findViewById(R.id.btn_add);
        // mbtn_add_item.setOnClickListener(new OnClickListener() {
        //     @Override
        //     public void onClick(View v) {
        //         HashMap<String, Object> map = new HashMap<String, Object>();
        //         map.put("item_image", R.drawable.checked);
        //         map.put("item_title", "Title-" + mListItem.size());
        //         map.put("item_text", "New item!");
        //         mListItem.add(map);
        //         mItemAdapter.notifyDataSetChanged();
        //     }
        // });
        ListView listView = (ListView)this.findViewById(R.id.list_view);
        mListItem = new ArrayList<HashMap<String, Object>>();
        mItemAdapter = new SimpleAdapter(
                this,
                mListItem,
                R.layout.list_item,
                new String[] { "item_image", "item_title", "item_text" },
                new int[] { R.id.item_image, R.id.item_title, R.id.item_text } );

        listView.setAdapter(mItemAdapter);

        listView.setOnItemClickListener(new OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view,
                    int position, long id) {
                Log.d(TAG, "onItemClick " + this.hashCode());
                // HashMap<String,String> map=(HashMap<String,String>)parent.getItemAtPosition(position);
                ReminderListActivity.this.setTitle("On click " + position + " item");
            }
        });

        mIntent = new Intent(this, ReminderMqttService.class);
        startService(mIntent);

    }

    public class MessageReceiver extends BroadcastReceiver {

        @Override
        public void onReceive(Context context, Intent intent) {
            // Map<String, String> map = JSON.parseObject(payload,
            //         new TypeReference<Map<String, String>>(){});

            // for (Map.Entry<String, String> entry : map.entrySet()) {
            //     System.out.println("Key = " + entry.getKey() + ", Value = " + entry.getValue());
            // }
            Map<String, Object> o = JSON.parseObject(intent.getStringExtra("payload"));
            for (Map.Entry<String, Object> entry : o.entrySet()) {
                Log.d(TAG, "Key:" + entry.getKey() + ", Value: " + (String)entry.getValue());
            }
        }

    }

	@Override
	protected void onDestroy() {
		stopService(mIntent);
		unregisterReceiver(mMsgReceiver);
		super.onDestroy();
	}
}
