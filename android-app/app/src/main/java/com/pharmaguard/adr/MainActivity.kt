package com.pharmaguard.adr

import android.annotation.SuppressLint
import android.app.DownloadManager
import android.content.Context
import android.net.Uri
import android.os.Bundle
import android.os.Environment
import android.webkit.CookieManager
import android.webkit.URLUtil
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView
    private var backPressedOnce = false

    private val pharmaguardUrl =
        "https://pharmaguard-qpfu9vclbstdjg3vmgm2vj.streamlit.app/"

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        webView = WebView(this)

        setContentView(webView)

        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            databaseEnabled = true

            builtInZoomControls = false
            displayZoomControls = false

            allowFileAccess = true
            allowContentAccess = true

            // Better mobile WebView behavior
            useWideViewPort = true
            loadWithOverviewMode = true
            setSupportZoom(false)

            // Require user interaction for media playback
            mediaPlaybackRequiresUserGesture = true
        }

        webView.webViewClient = WebViewClient()
        webView.webChromeClient = WebChromeClient()

        // CSV / PDF / TXT download handling
        webView.setDownloadListener {
                url,
                userAgent,
                contentDisposition,
                mimeType,
                _ ->

            val request =
                DownloadManager.Request(Uri.parse(url))

            val cookies =
                CookieManager
                    .getInstance()
                    .getCookie(url)

            if (!cookies.isNullOrEmpty()) {
                request.addRequestHeader(
                    "Cookie",
                    cookies
                )
            }

            request.addRequestHeader(
                "User-Agent",
                userAgent
            )

            val fileName =
                URLUtil.guessFileName(
                    url,
                    contentDisposition,
                    mimeType
                )

            request.setTitle(fileName)

            request.setDescription(
                "Downloading PHARMAGUARD report"
            )

            request.setMimeType(mimeType)

            request.setNotificationVisibility(
                DownloadManager.Request
                    .VISIBILITY_VISIBLE_NOTIFY_COMPLETED
            )

            request.setDestinationInExternalPublicDir(
                Environment.DIRECTORY_DOWNLOADS,
                fileName
            )

            val downloadManager =
                getSystemService(Context.DOWNLOAD_SERVICE)
                        as DownloadManager

            downloadManager.enqueue(request)
        }

        // Load PHARMAGUARD
        webView.loadUrl(pharmaguardUrl)

        // Professional Android back-button behavior
        onBackPressedDispatcher.addCallback(
            this,
            object : OnBackPressedCallback(true) {

                override fun handleOnBackPressed() {

                    if (webView.canGoBack()) {

                        webView.goBack()

                        backPressedOnce = false

                    } else {

                        if (backPressedOnce) {

                            finish()

                        } else {

                            backPressedOnce = true

                            android.widget.Toast.makeText(
                                this@MainActivity,
                                "Press back again to exit",
                                android.widget.Toast.LENGTH_SHORT
                            ).show()

                            android.os.Handler(
                                android.os.Looper.getMainLooper()
                            ).postDelayed({

                                backPressedOnce = false

                            }, 2000)
                        }
                    }
                }
            }
        )
    }

    override fun onDestroy() {

        webView.destroy()

        super.onDestroy()
    }
}
