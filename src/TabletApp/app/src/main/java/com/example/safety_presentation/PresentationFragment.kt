package com.example.safety_presentation

import android.content.Context
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import com.example.safety_presentation.databinding.FragmentPresentationBinding

class PresentationFragment : Fragment() {
    lateinit var bind : FragmentPresentationBinding
    lateinit var mainActivity: MainActivity

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?,
                              savedInstanceState: Bundle?): View? {
        bind = FragmentPresentationBinding.inflate(inflater, container, false)
        return bind.root
    }

    override fun onAttach(context: Context) {
        super.onAttach(context)
        mainActivity = context as MainActivity
    }

//    companion object {
//        @JvmStatic
//        fun newInstance(param1: String, param2: String) =
//            PresentationFragment().apply {
//                arguments = Bundle().apply {
//                    putString(ARG_PARAM1, param1)
//                    putString(ARG_PARAM2, param2)
//                }
//            }
//    }
}