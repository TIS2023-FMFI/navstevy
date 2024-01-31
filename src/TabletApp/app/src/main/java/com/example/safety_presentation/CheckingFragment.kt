package com.example.safety_presentation

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.navigation.Navigation
import com.example.safety_presentation.databinding.FragmentCheckingBinding

class CheckingFragment : Fragment() {
    lateinit var bind : FragmentCheckingBinding
    lateinit var mainActivity: MainActivity
    lateinit var en : Bitmap
    lateinit var sk : Bitmap

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        bind = FragmentCheckingBinding.inflate(inflater, container, false)

        bind.apply {
            textView2.text = "Prosím skontrolujte správnosť zadaných dát: \nmeno: "+
            mainActivity.visitor!!.name + "\npriezvisko: " + mainActivity.visitor!!.surname +
                    "\nfirma: " + mainActivity.visitor!!.company + "\nŠPZ: " +
                    mainActivity.visitor!!.cardId + "\npočet vo Vašej skupine: " +
                    mainActivity.visitor!!.count

            // yes_button
            button6.setOnClickListener {
                val action = CheckingFragmentDirections.actionCheckingFragmentToPresentationFragment()
                mainActivity.communication.send_progress(0)
                Navigation.findNavController(it).navigate(action)
            }
            imageButton.setOnClickListener {
                changeLanguage()
            }
            // no_button
            button7.setOnClickListener {
                val action = CheckingFragmentDirections.actionCheckingFragmentToTextFragment()
                action.message = "che"
                mainActivity.communication.send_wrong_data()
                Navigation.findNavController(it).navigate(action)
            }
        }

        bind.imageButton.setImageBitmap(sk)

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
            bind.imageButton.setImageBitmap(en)
            bind.button6.text = "Yes"
            bind.button7.text = "No"
            bind.textView2.text = "Please check, if the following data is correct: \nname: "+
                    mainActivity.visitor!!.name + "\nsurname: " + mainActivity.visitor!!.surname +
                    "\ncompany: " + mainActivity.visitor!!.company + "\nŠPZ: " +
                    mainActivity.visitor!!.cardId + "\namount in your party: " +
                    mainActivity.visitor!!.count
        }
        else{
            mainActivity.languageInUse = "sk"
            bind.imageButton.setImageBitmap(sk)
            bind.button6.text = "Áno"
            bind.button7.text = "Nie"
            bind.textView2.text = "Prosím skontrolujte správnosť zadaných dát: \nmeno: "+
                    mainActivity.visitor!!.name + "\npriezvisko: " + mainActivity.visitor!!.surname +
                    "\nfirma: " + mainActivity.visitor!!.company + "\nŠPZ: " +
                    mainActivity.visitor!!.cardId + "\npočet vo Vašej skupine: " +
                    mainActivity.visitor!!.count
        }

    }

}