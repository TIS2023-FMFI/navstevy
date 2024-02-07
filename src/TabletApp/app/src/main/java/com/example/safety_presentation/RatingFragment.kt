package com.example.safety_presentation

import android.content.Context
import android.graphics.Bitmap
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageButton
import androidx.navigation.Navigation
import androidx.navigation.fragment.NavHostFragment
import com.example.safety_presentation.databinding.FragmentConfirmationBinding
import com.example.safety_presentation.databinding.FragmentRatingBinding
import java.util.Timer
import kotlin.concurrent.schedule

class RatingFragment : Fragment() {
    lateinit var bind : FragmentRatingBinding
    lateinit var mainActivity: MainActivity
    lateinit var en : Bitmap
    lateinit var sk : Bitmap

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        bind = FragmentRatingBinding.inflate(inflater, container, false)
        val ratings : List<ImageButton> = listOf(bind.i1, bind.i2, bind.i3, bind.i4, bind.i5)

        val timer = Timer()

        timer.schedule(1000 * 15) {
            mainActivity.runOnUiThread(){
                val action = RatingFragmentDirections.actionRatingFragmentToScreenSaverFragment()
                mainActivity.communication.send_rating(0)
                val controller = NavHostFragment.findNavController(this@RatingFragment)
                controller.navigate(action)
            }
        }

        for (i in ratings.indices) {
            ratings[i].setImageBitmap(mainActivity.ratingImages[i])
        }

        bind.apply {
            imageButton2.setOnClickListener {changeLanguage()}
            for (i in ratings.indices){
                ratings[i].setOnClickListener {
                    val action = RatingFragmentDirections.actionRatingFragmentToScreenSaverFragment()
                    mainActivity.communication.send_rating(i+1)
                    timer.cancel()
                    Navigation.findNavController(it).navigate(action)
                }
            }
        }

        bind.imageButton2.setImageBitmap(sk)
        bind.textView3.text = "Prosím ohodnotte nás "+ mainActivity.visitor!!.name + " " +
                mainActivity.visitor!!.surname + "!"

        return bind.root
    }

    override fun onAttach(context: Context) {
        super.onAttach(context)
        mainActivity = context as MainActivity

        mainActivity.imageCreation()
        en = mainActivity.imagesDict[mainActivity.imagesDict.size - 2]!!
        sk = mainActivity.imagesDict[mainActivity.imagesDict.size - 1]!!
    }

    fun changeLanguage(){
        if (mainActivity.languageInUse == "sk"){
            mainActivity.languageInUse = "en"
            bind.imageButton2.setImageBitmap(en)
            bind.textView3.text = "Please rate your experience " + mainActivity.visitor!!.name +
            mainActivity.visitor!!.surname + "!"

        }
        else{
            mainActivity.languageInUse = "sk"
            bind.imageButton2.setImageBitmap(sk)
            bind.textView3.text = "Prosím ohodnotte nás"+ mainActivity.visitor!!.name +
                    mainActivity.visitor!!.surname + "!"

        }

    }
}

