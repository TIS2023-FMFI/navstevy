package com.example.safety_presentation

import Communication
import Visitor
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.StrictMode


class MainActivity : AppCompatActivity() {
    var languageInUse = "sk"
    var imagesDict : MutableMap<Int, Bitmap> = mutableMapOf()
    var ratingImages : MutableList<Bitmap> = mutableListOf()
    val communication: Communication = Communication(this)
    public var visitor: Visitor? = null;

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        StrictMode.setThreadPolicy(StrictMode.ThreadPolicy.Builder().permitNetwork().build())

    }

    fun imageCreation(){
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
    }

}