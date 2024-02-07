package com.example.safety_presentation

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.core.graphics.get
import androidx.core.graphics.toColor
import androidx.navigation.Navigation
import com.example.safety_presentation.databinding.FragmentConfirmationBinding



class ConfirmationFragment : Fragment() {
    lateinit var bind : FragmentConfirmationBinding
    lateinit var mainActivity: MainActivity

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        bind = FragmentConfirmationBinding.inflate(inflater, container, false)

        if (mainActivity.languageInUse == "sk"){
            bind.textView.text = "S podpisom potvrdzujem, že som pochopil bezpečnostnými pokynmy"
            bind.button4.text = "Prezentácia"
            bind.button5.text = "Súhlasím"
        }

        else{
            bind.textView.text = "With my signature I acknowledge that I have understood the safety instructions"
            bind.button4.text = "Presentation"
            bind.button5.text = "Agree"
        }

        bind.apply {
            button4.setOnClickListener {
                val action = ConfirmationFragmentDirections.actionConfirmationFragmentToPresentationFragment()
                mainActivity.communication.send_progress(0)
                Navigation.findNavController(it).navigate(action)
            }

            button5.setOnClickListener {
                val bitmap : Bitmap = Bitmap.createBitmap(view.width, view.height, Bitmap.Config.ARGB_8888)
                val canvas = Canvas(bitmap)
                view.draw(canvas)

                val signature = resizeBitmap(bitmap, 0.25f)
                if (!isBitmapEmpty(signature)) {
                    val action = ConfirmationFragmentDirections.actionConfirmationFragmentToTextFragment()
                    action.message = "con"
                    mainActivity.communication.send_signature(signature)
                    Navigation.findNavController(it).navigate(action)
                }
                else {
                    Toast.makeText(context,
                        if (mainActivity.languageInUse == "sk") "Prosím, najskôr sa podpíšte" else "Please, sign first",
                        Toast.LENGTH_SHORT).show();
                }
            }
        }

        return bind.root
    }



    override fun onAttach(context: Context) {
        super.onAttach(context)
        mainActivity = context as MainActivity

    }

    fun resizeBitmap(originalBitmap: Bitmap, k: Float): Bitmap {
        val originalWidth = originalBitmap.width
        val originalHeight = originalBitmap.height

        val newWidth = (originalWidth * k).toInt()
        val newHeight = (originalHeight * k).toInt()

        return Bitmap.createScaledBitmap(originalBitmap, newWidth, newHeight, true)
    }

    fun isBitmapEmpty(bitmap: Bitmap): Boolean {
        (0 until bitmap.height).forEach {y ->
            (0 until bitmap.width).forEach { x ->
                val color = Color.valueOf(bitmap.get(x, y))
                if (color == Color.BLACK.toColor()) {
                    return false
                }
            }
        }
        return true
    }
}