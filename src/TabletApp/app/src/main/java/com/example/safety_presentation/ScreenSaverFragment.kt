package com.example.safety_presentation

import android.content.Context
import android.os.AsyncTask
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.lifecycle.lifecycleScope
import androidx.navigation.findNavController
import androidx.navigation.fragment.NavHostFragment
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.cancel
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.withContext


class ScreenSaverFragment : Fragment() {
    companion object {
        lateinit var last_fragment: ScreenSaverFragment;
        lateinit var mainActivity: MainActivity
    }





    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        last_fragment = this;
        mainActivity = context as MainActivity
        wait_for_signal()
        return inflater.inflate(R.layout.fragment_screen_saver, container, false)
    }

    override fun onAttach(context: Context) {
        super.onAttach(context)
    }

    fun wait_for_signal() {

        CoroutineScope(Dispatchers.IO).launch {
            // Wait for presentation start on IO thread
            val visitor = mainActivity.communication.recieve_message()  // THIS LINE WAITS FOR TCP CONNECTION, SO THIS LINE IS BLOCKING
            mainActivity.visitor = visitor
            println("Nastavil som visitora na ${mainActivity.visitor}")

            if (visitor == null){
                return@launch
            }

            // update UI on main thread
            withContext(Dispatchers.Main) {

                val action =
                    if (visitor.is_new)
                        ScreenSaverFragmentDirections.actionScreenSaverFragmentToCheckingFragment()
                    else
                        ScreenSaverFragmentDirections.actionScreenSaverFragmentToRatingFragment()
                val controller = NavHostFragment.findNavController(last_fragment)
                controller.navigate(action)

            }
        }
    }

    fun switch_to_fragment(go_to_fragment: Fragment) {
        val fragmentManager = mainActivity.supportFragmentManager
        val transaction = fragmentManager.beginTransaction()

        transaction.replace(R.id.container, go_to_fragment) // Replace R.id.fragment_container with your actual container ID
        transaction.addToBackStack(null) // Add the transaction to the back stack
        transaction.commit()
    }
    //                val go_to_fragment: Fragment = if (visitor.is_new) CheckingFragment() else RatingFragment()
    //                switch_to_fragment(go_to_fragment)

}
