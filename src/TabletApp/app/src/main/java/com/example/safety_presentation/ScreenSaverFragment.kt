package com.example.safety_presentation

import android.content.Context
import android.os.AsyncTask
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.lifecycle.lifecycleScope
import androidx.navigation.fragment.NavHostFragment
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.withContext


class ScreenSaverFragment : Fragment() {

    lateinit var mainActivity: MainActivity


    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        wait_for_signal()
        return inflater.inflate(R.layout.fragment_screen_saver, container, false)
    }

    override fun onAttach(context: Context) {
        super.onAttach(context)
        mainActivity = context as MainActivity
    }


    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

    }

    fun wait_for_signal() {
        CoroutineScope(Dispatchers.IO).launch {
            // Wait for presentation start on IO thread
            val visitor = mainActivity.communication.recieve_message()
            mainActivity.visitor = visitor
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
                val controller = NavHostFragment.findNavController(this@ScreenSaverFragment)
                controller.navigate(action)
            }
        }
    }

}
