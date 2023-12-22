package com.example.safety_presentation

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View

class MainActivity : AppCompatActivity() {
    var languageInUse = "sk"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        if (savedInstanceState == null) {
            val fragmented = supportFragmentManager.beginTransaction()
            fragmented.apply {
                add(R.id.container, PresentationFragment(), "main")
                commit()
            }
        }
    }

}