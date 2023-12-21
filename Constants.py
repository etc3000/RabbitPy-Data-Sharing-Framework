class Constants:
    # Message Types
    ANNOUNCE_MESSAGE = "announce_data"
    CAN_TRANSLATE = "can_translate"
    REQUEST_DATA = "request_data"
    SENT_DATA = "sent_data"

    # Metadata Keys
    METADATA = "metadata"
    USER_ID = "user_id"
    MESSAGE_ID = "message_id"
    MESSAGE_TYPE = "message_type"
    METADATA_FILEDATA = "data"
    DATA_CONVERT_FORMATS = "data_convert_formats"
    DATA_REQUEST_FORMATS = "data_request_formats"
    ORIGIN_MESSAGE_ID = "origin_message_id"
    SOURCE_USER_ID = "source_user_id"
    TIMESTAMP = "time_stamp"
    ORIGINAL_FORMAT = "original_format"
    DESTINATION_FORMATS = "destination_formats"
    FILENAME = "filename"
    FILESIZE = "filesize"

    CONTENT = "content"

    # RabbitMQ Guest User Information
    # TODO: find more secure way of storing variables for distribution
    # RABBITMQ_URI = "amqps://xowvnltv:hwYeKNw5yGW6mg_7NoUx-QS7lDzGNael@woodpecker.rmq.cloudamqp.com/xowvnltv"
    RABBITMQ_URI = "amqps://crnulcjb:jTi5qkc_4BJQy-J4fmMk6CEJn1_phN3x@shark.rmq.cloudamqp.com/crnulcjb"

    def __init__(self):
        pass
