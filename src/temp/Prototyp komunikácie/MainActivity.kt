package com.example.communication_android

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import java.io.BufferedReader
import java.io.IOException
import java.io.InputStreamReader
import java.net.ServerSocket
import java.net.Socket
import com.example.communication_android.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    companion object {
        private const val SERVER_PORT = 5555
    }
    lateinit var binding: ActivityMainBinding;

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        binding = ActivityMainBinding.inflate(layoutInflater)
        Thread(ServerThread()).start()
    }


    class ServerThread(): Runnable {

        override fun run() {
            var socket: Socket
            try {
                val serverSocket = ServerSocket(SERVER_PORT)
                while (true) {
                    socket = serverSocket.accept()
                    val input = BufferedReader(InputStreamReader(socket.getInputStream()))
                    val message = input.readLine()
                    println(message)
                    socket.close()
                }
            } catch (e: IOException) {
                e.printStackTrace()
            }
        }
    }
}