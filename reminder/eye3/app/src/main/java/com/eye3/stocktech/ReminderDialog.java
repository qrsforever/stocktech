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
import android.webkit.WebChromeClient;
import android.webkit.WebViewClient;

import java.util.Map;

public class ReminderDialog extends Dialog implements View.OnClickListener {

    public static final String TAG = ReminderDialog.class.getSimpleName();

    private Context mContext;
    private String mBody = null;
    private String mUrl = null;
    private long mFirstClick = 0;
    private long mSecondClick = 0;

    public ReminderDialog(Context context, String body) {
        super(context, R.style.ReminderDialog);
        mContext = context;
        Log.d(TAG, body);
        if (body.startsWith("http://") || body.startsWith("https://")) {
            mUrl = body;
        } else {
            mBody = body;
        }
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
        lp.width = display.getWidth() * 9/10; /* Dialog占屏幕比例 */
        lp.height = display.getHeight() * 9/10;
        dialogWindow.setAttributes(lp);
        setCanceledOnTouchOutside(true); /* 点击外部Dialog消失 */

        WebView wv = (WebView)findViewById(R.id.body_wv);
        wv.getSettings().setDefaultTextEncodingName("UTF-8");
        wv.getSettings().setJavaScriptEnabled(true);
        // 缩放
        wv.getSettings().setSupportZoom(true);
        wv.getSettings().setBuiltInZoomControls(true);
        // 滚动条
        wv.setHorizontalScrollBarEnabled(true);
        wv.setVerticalScrollBarEnabled(true);
        wv.setScrollBarStyle(View.SCROLLBARS_INSIDE_OVERLAY);
        // 辅助
        wv.setWebChromeClient(new WebChromeClient());
        wv.setWebViewClient(new WebViewClient());
        if (null != mUrl) {
            wv.loadUrl(mUrl);
        } else {
            wv.loadData(mBody, "text/html; charset=UTF-8", null);
        }
        wv.setOnTouchListener(new OnTouchListener(){
            @Override
            public boolean onTouch(View v,MotionEvent event) {
                if (MotionEvent.ACTION_DOWN == event.getAction()) {
                    if (0 == mFirstClick) {
                        mFirstClick = System.currentTimeMillis();
                    } else {
                        mSecondClick = System.currentTimeMillis();
                        long diff = mSecondClick - mFirstClick;
                        Log.d(TAG, "diff = " + diff);
                        if ( diff > 100 && diff < 800 ) {
                            dismiss();
                        }
                        mFirstClick = mSecondClick;
                        mSecondClick = 0;
                    }
                }
                return false;
            }
        });
    }

    @Override
    public void onClick(View v) {
        Log.d(TAG, "ReminderDialog onClick");
    }
}
