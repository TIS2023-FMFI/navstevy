package com.example.safety_presentation

import Communication
import Visitor
import android.content.Context
import android.content.Intent
import android.content.pm.ActivityInfo
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.ConnectivityManager
import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.PowerManager
import android.os.StrictMode
import android.provider.Settings
import android.view.WindowManager
import androidx.core.content.ContextCompat.startActivity
import androidx.fragment.app.Fragment
import androidx.navigation.Navigation
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.cancel
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.lang.reflect.Method


class MainActivity : AppCompatActivity() {
    companion object {
        val imagesDict : MutableMap<Int, Bitmap> = mutableMapOf()
        val ratingImages : MutableList<Bitmap> = mutableListOf()
        var imagesInitialized = false;
    }

    var languageInUse = "sk"
    var visitor: Visitor? = null;
    var wakeLock: PowerManager.WakeLock? = null
    val communication: Communication = Communication(this);

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        imageCreation()
        setFullScreenMode()
        setAlwaysOnScreen()
        StrictMode.setThreadPolicy(StrictMode.ThreadPolicy.Builder().permitNetwork().build())
    }

    override fun onDestroy() {
        super.onDestroy()
        allowScreenToSleep()
        communication.send_error("Aplikácia bola vypnutá")
    }

    fun imageCreation(){
        if (imagesInitialized)
            return
        val resourceList : List<Int> = listOf(R.drawable.en1, R.drawable.en2, R.drawable.en3,
            R.drawable.en4, R.drawable.en5, R.drawable.en6,
            R.drawable.en7, R.drawable.en8, R.drawable.en9,
            R.drawable.en10, R.drawable.en11, R.drawable.en12,
            R.drawable.sk1, R.drawable.sk2, R.drawable.sk3,
            R.drawable.sk4, R.drawable.sk5, R.drawable.sk6,
            R.drawable.sk7, R.drawable.sk8, R.drawable.sk9,
            R.drawable.sk10, R.drawable.sk11, R.drawable.sk12,
            R.drawable.flagen, R.drawable.flagsk)

        for (i in resourceList.indices){
            imagesDict[i] = BitmapFactory.decodeResource(
                this.resources,
                resourceList[i])
        }

        imagesDict[imagesDict.size-1] = Bitmap.createScaledBitmap(imagesDict[imagesDict.size-1]!!,
            (imagesDict[imagesDict.size-1]!!.width/8),
            (imagesDict[imagesDict.size-1]!!.height/8),
            false)

        imagesDict[imagesDict.size-2] = Bitmap.createScaledBitmap(imagesDict[imagesDict.size-2]!!,
            (imagesDict[imagesDict.size-2]!!.width/8),
            (imagesDict[imagesDict.size-2]!!.height/8),
            false)


        val smiles : List<Int> = listOf(R.drawable.i, R.drawable.m, R.drawable.a, R.drawable.g,
            R.drawable.e)

        for (i in smiles){
            val curr = BitmapFactory.decodeResource(this.resources, i)
            ratingImages.add(Bitmap.createScaledBitmap(curr, (curr.width/4), (curr.height/4), false))
        }
        imagesInitialized = true;
    }

    fun setFullScreenMode() {
        getWindow().setFlags(
            WindowManager.LayoutParams.FLAG_FULLSCREEN,
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        );
    }

    fun setAlwaysOnScreen() {
        // Acquire a wake lock
        val powerManager = getSystemService(POWER_SERVICE) as PowerManager
        wakeLock = powerManager.newWakeLock(
            PowerManager.FULL_WAKE_LOCK or PowerManager.ACQUIRE_CAUSES_WAKEUP,
            "MyApp::MyWakelockTag"
        )
        wakeLock?.acquire()
        println(wakeLock?.isHeld)
    }

    fun allowScreenToSleep() {
        wakeLock?.let {
            if (it.isHeld) {
                it.release()
            }
        }
    }

    fun restart() {
        val navController = Navigation.findNavController(this, R.id.fragmentContainerView)
        // Call navigateToDestination() method when you want to switch to a specific fragment
        navController.navigate(R.id.screenSaverFragment)
    }

}