class Visitor(
    val is_new: Boolean,
    val id: Int,
    val name: String,
    val surname: String,
    val cardId: Int,
    val carTag: String,
    val company: String,
    val count: Int,
    val reasonOfVisit: String,
) {

    constructor(message: String) : this(
        message.split(";")[0].toBoolean(),
        message.split(";")[1].toInt(),
        message.split(";")[2],
        message.split(";")[3],
        message.split(";")[4].toInt(),
        message.split(";")[5],
        message.split(";")[6],
        message.split(";")[7].toInt(),
        message.split(";")[8],
    )

    init {
        println("Visitor: " + is_new)
    }

    override fun toString(): String {
        return "$id: $name $surname"
    }


}