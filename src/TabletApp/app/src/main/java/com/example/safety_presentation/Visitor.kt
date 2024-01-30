class Visitor(val id: Int,
              val name: String,
              val surname: String,
              val cardId: Int,
              val carTag: String,
              val company: String,
              val count: Int,
              val reasonOfVisit: String) {

    constructor(message: String) : this(
        message.split(";")[0].toInt(),
        message.split(";")[1],
        message.split(";")[2],
        message.split(";")[3].toInt(),
        message.split(";")[4],
        message.split(";")[5],
        message.split(";")[6].toInt(),
        message.split(";")[7]
    )

    override fun toString(): String {
        return "$id: $name $surname"
    }


}