/// @file ReminderListActivity.java
/// @brief
/// @author QRS
/// @blog qrsforever.github.io
/// @version 1.0
/// @date 2019-05-15 18:39:14

package com.eye3.stocktech;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.BroadcastReceiver;
import android.media.RingtoneManager;
import android.media.AudioManager;
import android.media.Ringtone;
import android.net.Uri;
import android.os.Bundle;
import android.os.Vibrator;
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

    private Context mContext;
    private ArrayList<HashMap<String, Object>> mListItem = null;
    private SimpleAdapter mItemAdapter = null;
    private Intent mIntent = null;
    private MessageReceiver mMsgReceiver = null;

    private AudioManager mAudioManager = null;
    private Vibrator mVibrator = null;
    private Ringtone mRingtone = null;
    private long mLastNotifyTime = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        Log.d(TAG, "onCreate " + this.hashCode());
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        mContext = this;

        mAudioManager = (AudioManager)getSystemService(Context.AUDIO_SERVICE);
        mVibrator = (Vibrator)getSystemService(Context.VIBRATOR_SERVICE);

 		mMsgReceiver = new MessageReceiver();
		IntentFilter intentFilter = new IntentFilter();
		intentFilter.addAction(Constants.ACTIONS_RECV_MESSAGE);
		registerReceiver(mMsgReceiver, intentFilter);

        ListView listView = (ListView)this.findViewById(R.id.list_view);
        mListItem = new ArrayList<HashMap<String, Object>>();
        mItemAdapter = new SimpleAdapter(
                this,
                mListItem,
                R.layout.list_item,
                new String[] { "item_image", "item_title", "item_brief" },
                new int[] { R.id.item_image, R.id.item_title, R.id.item_brief } );

        listView.setAdapter(mItemAdapter);

        listView.setOnItemClickListener(new OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view,
                    int position, long id) {
                Log.d(TAG, "onItemClick[" +  position + "]");
                HashMap<String,String> listmap =(HashMap<String,String>)parent.getItemAtPosition(position);
                if (listmap != null) {
                    new ReminderDialog(mContext, listmap.get("item_body")).show();
                }
            }
        });

        mIntent = new Intent(this, ReminderMqttService.class);
        startService(mIntent);

    }

    public class MessageReceiver extends BroadcastReceiver {

        @Override
        public void onReceive(Context context, Intent intent) {
            String payload = intent.getStringExtra("payload");
            Log.d(TAG, "payload = " + payload);
            Map<String, Object> map = JSON.parseObject(intent.getStringExtra("payload"));
            HashMap<String, Object> listmap = new HashMap<String, Object>();
            switch ((int)map.get("predict")) {
                case 1:
                    listmap.put("item_image", R.drawable.ox);
                    break;
                case 0:
                    listmap.put("item_image", R.drawable.frog);
                    break;
                case -1:
                    listmap.put("item_image", R.drawable.bear);
                    break;
            }
            listmap.put("item_title", map.get("title"));
            listmap.put("item_brief", map.get("brief"));
            listmap.put("item_body", map.get("body"));
            mListItem.add(listmap);
            mItemAdapter.notifyDataSetChanged();
            ringNotify();
        }
    }

    public void ringNotify() {
        if (System.currentTimeMillis() - mLastNotifyTime < 1000)
            return;

        try {
            mLastNotifyTime = System.currentTimeMillis();

            if (mAudioManager.getRingerMode() == AudioManager.RINGER_MODE_SILENT) {
                Log.e("TAG", "Mute Setting");
                return;
            }
            long[] pattern = new long[] { 0, 180, 80, 120 };
            mVibrator.vibrate(pattern, -1);

            if (mRingtone == null) {
                Uri notificationUri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);
                mRingtone = RingtoneManager.getRingtone(mContext, notificationUri);
                if (mRingtone == null) {
                    Log.d(TAG, "Cant find ringtone at:" + notificationUri.getPath());
                    return;
                }
            }

            if (!mRingtone.isPlaying())
                mRingtone.play();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

	@Override
	protected void onDestroy() {
		stopService(mIntent);
		unregisterReceiver(mMsgReceiver);
		super.onDestroy();
	}
}
