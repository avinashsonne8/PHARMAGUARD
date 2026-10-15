
package com.pharmaguard.adr

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.animation.AnimationUtils
import android.widget.ImageView
import androidx.appcompat.app.AppCompatActivity

class SplashActivity : AppCompatActivity() {

    private val splashDuration = 2500L

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.activity_splash)

        // PHARMAGUARD splash pulse animation
        val splashImage = findViewById<ImageView>(R.id.splashImage)

        val pulseAnimation = AnimationUtils.loadAnimation(
            this,
            R.anim.pharmaguard_ecg_animation
        )

        splashImage.startAnimation(pulseAnimation)

        // Open the main app after 2.5 seconds
        Handler(Looper.getMainLooper()).postDelayed({

            startActivity(
                Intent(this, MainActivity::class.java)
            )

            finish()

        }, splashDuration)
    }
}
