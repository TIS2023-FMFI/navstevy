package com.example.safety_presentation

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import com.example.safety_presentation.databinding.FragmentPresentationBinding

class PresentationFragment : Fragment() {
    lateinit var bind : FragmentPresentationBinding
    lateinit var mainActivity: MainActivity
    var index = 0
    var dict : MutableMap<Int, Bitmap> = mutableMapOf()

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?,
                              savedInstanceState: Bundle?): View {
        bind = FragmentPresentationBinding.inflate(inflater, container, false)

        bind.apply {
            button.setOnClickListener{decrease() }
            button2.setOnClickListener{changeLanguage()}
            button3.setOnClickListener{increase()}
        }

        changeSlide()

        return bind.root
    }

    override fun onAttach(context: Context) {
        super.onAttach(context)
        mainActivity = context as MainActivity
        initRes(context)
    }

    fun initRes(context: Context){
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
            dict[i] = BitmapFactory.decodeResource(
                context.resources,
                resourceList[i])
        }

        dict[dict.size-1] = Bitmap.createScaledBitmap(dict[dict.size-1]!!,
            (dict[dict.size-1]!!.width/8),
            (dict[dict.size-1]!!.height/8),
            false)

        dict[dict.size-2] = Bitmap.createScaledBitmap(dict[dict.size-2]!!,
            (dict[dict.size-2]!!.width/8),
            (dict[dict.size-2]!!.height/8),
            false)
    }

    fun changeLanguage(){
        if (mainActivity.languageInUse == "sk"){
            mainActivity.languageInUse = "en"
        }
        else{
            mainActivity.languageInUse = "sk"
        }

        changeSlide()
    }

    fun increase(){
        if (index != 11){
            index += 1
        }

        changeSlide()
    }

    fun decrease(){
        if (index != 0){
            index -= 1
        }
        changeSlide()
    }

    fun changeSlide(){
        if (mainActivity.languageInUse == "en"){
            bind.presentation.setImageBitmap(dict[index])
            bind.button2.setImageBitmap(dict[dict.size-2])
        }

        else{
            bind.presentation.setImageBitmap(dict[index+12])
            bind.button2.setImageBitmap(dict[dict.size-1])
        }
    }
}