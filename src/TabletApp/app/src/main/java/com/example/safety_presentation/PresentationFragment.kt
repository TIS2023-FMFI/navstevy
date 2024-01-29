package com.example.safety_presentation

import android.content.Context
import android.graphics.Bitmap
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.navigation.Navigation
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
            button3.setOnClickListener{
                if (index == 11) {
                    val action = PresentationFragmentDirections.actionPresentationFragmentToConfirmationFragment()
                    Navigation.findNavController(it).navigate(action)
                }

                else {
                    increase()
                }
            }
        }

        changeSlide()

        return bind.root
    }

    override fun onAttach(context: Context) {
        super.onAttach(context)
        mainActivity = context as MainActivity
        dict = mainActivity.imagesDict
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
        index += 1
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