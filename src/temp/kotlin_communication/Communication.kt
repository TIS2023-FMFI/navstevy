import java.io.BufferedReader
import java.io.InputStreamReader
import java.lang.Thread.sleep
import java.net.ServerSocket
import java.net.Socket

val IP_ADDRESS = "localhost"
val PORT = 5555

enum class MessageType(val message_code: Int) {
    START(1),
    END(2),
    PROGRESS(3),
    SIGN(4)
}

class Communication(): Runnable {
    override fun run() {
        println("Communicator started")
        while (true) {
            recieve_message()
        }
    }

    private fun recieve_message() {
        println("---- Waiting for some message ---- ")

        try {
            val serverSocket = ServerSocket(PORT)
            val socket: Socket = serverSocket.accept()
            val input_stream = socket.getInputStream()
            val message_code = input_stream.read()
            if (message_code == MessageType.START.message_code) {
                val data_lenght = input_stream.read()
                val visitor_string = input_stream.readNBytes(data_lenght).decodeToString()
                val visitor = Visitor(visitor_string)
                println("Začínam prezentáciu pre $visitor")
            }
            else if (message_code == MessageType.END.message_code) {
                println("Ukonči prezentáciu")
            }
            socket.close()
            serverSocket.close()
        } catch (e: Exception) {
            println(e.toString())
        }
    }
}