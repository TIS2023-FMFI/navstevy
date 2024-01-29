import android.os.Build
import androidx.annotation.RequiresApi
import com.example.safety_presentation.MainActivity
import java.io.OutputStream
import java.lang.Thread.sleep
import java.net.ServerSocket
import java.net.Socket
import android.graphics.Bitmap
import android.graphics.Color
import android.os.AsyncTask
import androidx.core.graphics.toColor
import java.security.Signature


val IP_ADDRESS = "localhost"
val PORT_IN = 5555
val PORT_OUT = 5556

enum class MessageType(val message_code: Int) {
    // receiving message
    START(1),
    END(2),

    // sending message
    WRONG_DATA(3),
    PROGRESS(4),
    SIGNATURE(5),
    ERROR(6)
}

class Communication(val mainActivity: MainActivity) {

    fun send_wrong_data() {
        try {
            val socket = Socket(IP_ADDRESS, PORT_OUT)
            socket.reuseAddress = true

            // Get the output stream from the socket
            val outputStream: OutputStream = socket.getOutputStream()

            // Write raw bytes to the output stream
            outputStream.write(MessageType.WRONG_DATA.message_code)

            // Close the socket
            socket.close()
            println("Sending wrong data")
            sleep(100)
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    fun send_progress(percentage: Int) {
        try {
            val socket = Socket(IP_ADDRESS, PORT_OUT)
            socket.reuseAddress = true

            // Get the output stream from the socket
            val outputStream: OutputStream = socket.getOutputStream()

            // Write raw bytes to the output stream
            outputStream.write(MessageType.PROGRESS.message_code)
            outputStream.write(percentage)

            // Close the socket
            socket.close()
            println("Sending progress")
            sleep(100)
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    fun send_signature(signature: Bitmap) {
        try {
            val socket = Socket(IP_ADDRESS, PORT_OUT)
            socket.reuseAddress = true

            // Get the output stream from the socket
            val outputStream: OutputStream = socket.getOutputStream()

            // Write raw bytes to the output stream
            outputStream.write(MessageType.SIGNATURE.message_code)
            outputStream.write(signature.width)
            outputStream.write(signature.height)
            (0 until signature.height).forEach {y ->
                (0 until signature.width).forEach { x ->
                    val color = signature.getColor(x, y)
                    if (color == Color.BLACK.toColor()) {
                        outputStream.write(0)
                    }
                    else {
                        outputStream.write(1)
                    }
                }
            }

            // Close the socket
            socket.close()
            println("Sending signature")
            sleep(100)
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    fun send_error(message: String) {
        try {
            val socket = Socket(IP_ADDRESS, PORT_OUT)
            socket.reuseAddress = true

            // Get the output stream from the socket
            val outputStream: OutputStream = socket.getOutputStream()

            // Write raw bytes to the output stream
            outputStream.write(MessageType.ERROR.message_code)
            outputStream.write(message.length)
            outputStream.write(message.toByteArray())

            // Close the socket
            socket.close()
            println("Sending error")
            sleep(100)
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    fun recieve_message(): Visitor? {
        println("---- Waiting for some message ---- ")

        try {
            val serverSocket = ServerSocket(PORT_IN)
            val socket: Socket = serverSocket.accept()

            val input_stream = socket.getInputStream()
            val message_code = input_stream.read()

            // Start presentation
            if (message_code == MessageType.START.message_code) {
                val data_lenght = input_stream.read()
                val visitor_string = input_stream.readNBytes(data_lenght).decodeToString()
                val visitor = Visitor(visitor_string)
                return visitor
            }

            // End presentation
            else if (message_code == MessageType.END.message_code) {
                println("Ukonči prezentáciu")
                return null
            }
            socket.close()
            serverSocket.close()
        } catch (e: Exception) {
            println(e.toString())
        }
        return null
    }
}
