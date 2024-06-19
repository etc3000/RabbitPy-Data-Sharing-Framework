class Constants:
    """
    This class contains constant values that are used throughout the application.
    It should not be instantiated.
    """
    # Message Types
    ANNOUNCE_MESSAGE = "announce_data"  # Message type for announcing data
    CAN_TRANSLATE = "can_translate"  # Message type for indicating translation capability
    REQUEST_DATA = "request_data"  # Message type for requesting data
    SENT_DATA = "sent_data"  # Message type for indicating sent data

    # Metadata Keys
    METADATA = "metadata"  # Key for metadata
    USER_ID = "user_id"  # Key for user ID
    MESSAGE_ID = "message_id"  # Key for message ID
    MESSAGE_TYPE = "message_type"  # Key for message type
    METADATA_FILEDATA = "data"  # Key for file data within metadata
    DATA_CONVERT_FORMATS = "data_convert_formats"  # Key for data conversion formats
    DATA_REQUEST_FORMATS = "data_request_formats"  # Key for data request formats
    ORIGIN_MESSAGE_ID = "origin_message_id"  # Key for original message ID
    SOURCE_USER_ID = "source_user_id"  # Key for source user ID
    TIMESTAMP = "time_stamp"  # Key for timestamp
    ORIGINAL_FORMAT = "original_format"  # Key for original format
    DESTINATION_FORMATS = "destination_formats"  # Key for destination formats
    FILENAME = "filename"  # Key for filename
    FILESIZE = "filesize"  # Key for filesize
    CONTENT = "content"  # Key for content

    ALLOWED_FORMATS = ['.pdf', '.csv', '.txt', '.json',
                       '.jpg', '.png', '.jpeg', '.gif',
                       '.bmp', '.tiff', '.svg']

    FORMAT_CONVERSIONS = [
        'csv_to_pdf',
        'pdf_to_csv',
        'csv_to_json',
        'text_to_csv',
        'json_to_csv',
        'csv_to_text',
        'pdf_to_text',
        'text_to_pdf']

    # RabbitMQ Guest User Information
    # TODO: find more secure way of storing variables for distribution
    # RABBITMQ_URI = "amqps://xowvnltv:hwYeKNw5yGW6mg_7NoUx-QS7lDzGNael@woodpecker.rmq.cloudamqp.com/xowvnltv"
    RABBITMQ_URI = "amqps://crnulcjb:jTi5qkc_4BJQy-J4fmMk6CEJn1_phN3x@shark.rmq.cloudamqp.com/crnulcjb"

    # jTi5qkc_4BJQy-J4fmMk6CEJn1_phN3x
    def __init__(self):
        """
        Raises an error if an attempt is made to instantiate the Constants class.
        """
        raise ValueError("Constants class should not be instantiated.")
