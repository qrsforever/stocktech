/// @file ReminderDialog.java
/// @brief
/// @author QRS
/// @blog qrsforever.github.io
/// @version 1.0
/// @date 2019-05-16 18:40:21

package com.eye3.stocktech;

import android.app.Activity;
import android.app.Dialog;
import android.content.Context;
import android.os.Bundle;
import android.view.Display;
import android.view.Gravity;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.view.View.OnTouchListener;
import android.view.MotionEvent;
import android.util.Log;
import android.webkit.WebView;

import java.util.Map;

public class ReminderDialog extends Dialog implements View.OnClickListener {

    public static final String TAG = ReminderDialog.class.getSimpleName();

    private Context mContext;
    private String mBody;

    public ReminderDialog(Context context, String body){
        super(context, R.style.ReminderDialog);
        mContext = context;
        mBody = body;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Window dialogWindow = getWindow();
        dialogWindow.setGravity(Gravity.CENTER);
        setContentView(R.layout.dialog_detail);

        WindowManager windowManager = ((Activity)mContext).getWindowManager();
        Display display = windowManager.getDefaultDisplay();
        WindowManager.LayoutParams lp = dialogWindow.getAttributes();
        lp.width = display.getWidth() * 4/5; /* Dialog占屏幕比例 */
        dialogWindow.setAttributes(lp);
        setCanceledOnTouchOutside(true); /* 点击外部Dialog消失 */

        WebView wv = (WebView)findViewById(R.id.body_wv);
        wv.getSettings().setDefaultTextEncodingName("UTF-8");
        wv.loadData(mBody, "text/html; charset=UTF-8", null);
        wv.setOnTouchListener(new OnTouchListener(){
            @Override
            public boolean onTouch(View v,MotionEvent event) {
                dismiss();
                return false;
            }
        });
    }

    @Override
    public void onClick(View v) {
        Log.d(TAG, "ReminderDialog onClick");
    }
}
