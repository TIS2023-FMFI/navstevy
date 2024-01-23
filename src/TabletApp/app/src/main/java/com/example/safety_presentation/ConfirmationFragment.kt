package com.example.safety_presentation

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.navigation.Navigation
import com.example.safety_presentation.databinding.FragmentConfirmationBinding



class ConfirmationFragment : Fragment() {
    lateinit var bind : FragmentConfirmationBinding
    lateinit var mainActivity: MainActivity

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        bind = FragmentConfirmationBinding.inflate(inflater, container, false)
        bind.apply {
            button4.setOnClickListener {
                val action = ConfirmationFragmentDirections.actionConfirmationFragmentToPresentationFragment()
                Navigation.findNavController(it).navigate(action)
            }

            button5.setOnClickListener {
                val bitmap : Bitmap = Bitmap.createBitmap(view.width, view.height, Bitmap.Config.ARGB_8888)
                val canvas = Canvas(bitmap)
                view.draw(canvas)
                val action = ConfirmationFragmentDirections.actionConfirmationFragmentToTextFragment()
                Navigation.findNavController(it).navigate(action)
            }
        }

        return bind.root
    }



    override fun onAttach(context: Context) {
        super.onAttach(context)
        mainActivity = context as MainActivity

    }
}