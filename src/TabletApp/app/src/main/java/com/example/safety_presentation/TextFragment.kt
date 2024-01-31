package com.example.safety_presentation

import android.content.Context
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.navigation.fragment.NavHostFragment
import com.example.safety_presentation.databinding.FragmentConfirmationBinding
import com.example.safety_presentation.databinding.FragmentTextBinding
import java.util.Timer
import kotlin.concurrent.schedule

class TextFragment : Fragment() {
    lateinit var bind : FragmentTextBinding
    lateinit var msg : String
    lateinit var mainActivity: MainActivity

    override fun onStart() {
        super.onStart()
        arguments?.let{
            val args = TextFragmentArgs.fromBundle(it)
            msg = if (args.message == "con"){
                "con"
            } else{
                "che"
            }
        }

        if (msg == "con"){
            if (mainActivity.languageInUse == "en"){
                bind.tv.text = "Your signature has been sent, enjoy your stay"
            }
            else{
                bind.tv.text = "Váš podpis bol poslaný, užite si pobyt"
            }
        }

        else{
            if (mainActivity.languageInUse == "en"){
                bind.tv.text = "We have notified the employee of the wrongly inputed data"
            }
            else{
                bind.tv.text = "Informovali sme zamestnanca ohľadom zle zadaných dát"
            }
        }
        val timer = Timer()
        println("Prisiel som na text fragment")
        timer.schedule(1000 * 5) {

            mainActivity.runOnUiThread(){
                println("Vraciam saaaa")
                val action = TextFragmentDirections.actionTextFragmentToScreenSaverFragment()
                val controller = NavHostFragment.findNavController(this@TextFragment)
                controller.navigate(action)
            }
        }
    }


    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        bind = FragmentTextBinding.inflate(inflater, container, false)

        return bind.root
    }

    override fun onAttach(context: Context) {
        super.onAttach(context)
        mainActivity = context as MainActivity
    }

}