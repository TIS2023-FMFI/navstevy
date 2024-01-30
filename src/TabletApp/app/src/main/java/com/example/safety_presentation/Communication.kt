import android.os.Build
import androidx.annotation.RequiresApi
import com.example.safety_presentation.MainActivity
import java.io.OutputStream
import java.lang.Thread.sleep
import java.net.ServerSocket
import java.net.Socket
import android.graphics.Bitmap
import android.graphics.Color
import android.media.Rating
import android.os.AsyncTask
import androidx.core.graphics.toColor
import java.nio.ByteBuffer
import java.security.Signature
import kotlin.math.sign


var IP_ADDRESS = "localhost"
val PORT_IN = 5013
val PORT_OUT = 5014

enum class MessageType(val message_code: Int) {
    // receiving message
    PRESENTATION_START(1),
    PRESENTATION_END(2),
    RATING_START(3),

    // sending message
    WRONG_DATA(4),
    PROGRESS(5),
    SIGNATURE(6),
    RATING(7),
    ERROR(8)
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
        } catch (e: Exception) {
            println(e.toString())
        }
    }

    fun send_rating(rating: Int) {
        try {
            println("Trying send rating")
            val socket = Socket(IP_ADDRESS, PORT_OUT)
            socket.reuseAddress = true

            // Get the output stream from the socket
            val outputStream: OutputStream = socket.getOutputStream()

            // Write raw bytes to the output stream
            outputStream.write(MessageType.RATING.message_code)
            outputStream.write(rating)

            // Close the socket
            socket.close()
            println("Sending rating")
        } catch (e: Exception) {
            println(e.toString())
        }
    }



    fun send_signature(signature: Bitmap) {
        try {
            val socket = Socket(IP_ADDRESS, PORT_OUT)
            socket.reuseAddress = true

            // Get the output stream from the socket
            val outputStream: OutputStream = socket.getOutputStream()
            println("Posielam podpis")
            println(signature.width)
            println(signature.height)
            // Write raw bytes to the output stream
            outputStream.write(MessageType.SIGNATURE.message_code)

            outputStream.write(intToByteArray(signature.width))
            outputStream.write(intToByteArray(signature.height))
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

        } catch (e: Exception) {
            println(e.toString())
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
        } catch (e: Exception) {
            println(e.toString())
        }
    }



    fun recieve_message(): Visitor? {
        println("---- Waiting for some message ---- ")

        try {
            val serverSocket = ServerSocket(PORT_IN)
            val socket: Socket = serverSocket.accept()
            IP_ADDRESS = socket.inetAddress.toString().drop(1)


            val input_stream = socket.getInputStream()
            val message_code = input_stream.read()
            println("Message code: " + message_code)

            // Start presentation
            if (message_code == MessageType.PRESENTATION_START.message_code) {
                val data_lenght = input_stream.read()
                val visitor_string = input_stream.readNBytes(data_lenght).decodeToString()
                val visitor = Visitor("true;" + visitor_string)
                println("Visitor prišiel")
                return visitor
            }

            // Start rating
            if (message_code == MessageType.RATING_START.message_code) {
                println("Spustam review")
                val data_lenght = input_stream.read()
                val visitor_string = input_stream.readNBytes(data_lenght).decodeToString()
                println(visitor_string)
                val visitor = Visitor("false;" + visitor_string)
                println("Visitor odchadza")
                return visitor
            }

            // End presentation
            else if (message_code == MessageType.PRESENTATION_END.message_code) {
                println("Ukonči prezentáciu")
                return null
            }
            socket.close()
            serverSocket.close()
        } catch (e: Exception) {
            println(e.toString())
        }
        println("Tu returnujem")
        return null
    }

    private fun intToByteArray(value: Int): ByteArray {
        val buffer = ByteBuffer.allocate(4)
        buffer.putInt(value)
        return buffer.array()
    }
}
