class Name:
    def __init__(self, name, firstName, lastName, type):
        """
        Represents a name structure for a contact.

        This class stores name-related information for a contact, including a full name,
        first name, last name, and type.
        """
        self.name = name
        self.first_name = firstName
        self.last_name = lastName
        self.type = type

class Contact:
    def __init__(self, accountStatus = None, baseUrl = None, names = None, phone = None, description = None, options = None, photoId = None, updateTime = None, id = None, baseRawUrl = None):
        """
        Represents a contact with detailed profile information.

        This class encapsulates contact details, including status, URLs, names (as `Name` objects),
        phone number, description, and other metadata.
        """
        self.accountStatus = accountStatus
        self.base_url = baseUrl
        self.names = [Name(**n) for n in names]
        self.phone = phone
        self.description = description
        self.options = options
        self.photo_id = photoId
        self.update_time = updateTime
        self.id = id
        self.base_raw_url = baseRawUrl

class User:
    def __init__(self, profile):
        """
        Represents a user with a contact profile.

        This class wraps a `Contact` object created from a profile dictionary, typically
        received from the server.
        """
        self.contact = Contact(**profile)

class Chat:
    def __init__(self, client, chat_id):
        """
        Represents a chat in the messaging system.

        This class associates a chat with a client instance and its unique ID.
        """
        self._client = client

        self.id= chat_id

class Message:
    def __init__(self, client, chatId: str, sender: str, id, time, text, type, **kwargs):
        """
        Represents a message in a chat.

        This class encapsulates message details, including the sender, content, and metadata,
        and provides methods to interact with the message (e.g., reply, delete, edit).
        """
        self._client = client

        self.chat = Chat(client, chatId)
        self.sender = sender
        self.id = id
        self.time = time
        self.text = text
        self.type = type
        self.update_time = kwargs.get("updateTime")
        self.options = kwargs.get("options")
        self.cid = kwargs.get("cid")
        self.attaches = kwargs.get("attaches", [])
    
    def reply(self, text: str, **kwargs) -> "Message":
        """
        Replies to the current message in its chat.

        This method sends a new message in the same chat, linking it as a reply to the current message.

        Args:
            text (str): The text content of the reply.
            **kwargs: Additional arguments to pass to `send_message` (e.g., notify).

        Returns:
            Message: A `Message` object representing the sent reply.

        Usage:
            ```python
            reply_msg = message.reply("Thanks for your message!")
            ```
        """
        return self._client.send_message(self.chat.id, text, self.id, **kwargs)
    
    def answer(self, text: str, **kwargs) -> "Message":
        """
        Sends a new message in the same chat without linking it as a reply.

        This method sends a message to the same chat as the current message, without referencing it.

        Args:
            text (str): The text content of the message.
            **kwargs: Additional arguments to pass to `send_message` (e.g., notify).

        Returns:
            Message: A `Message` object representing the sent message.

        Usage:
            ```python
            new_msg = message.answer("Got it, sending a follow-up.")
            ```
        """
        return self._client.send_message(self.chat.id, text, **kwargs)

    def delete(self, for_me = False):
        """
        Deletes the current message from its chat.

        This method deletes the message, either for the current user only or for all chat participants.

        Args:
            for_me (bool, optional): If True, deletes the message only for the current user. Defaults to False.

        Usage:
            ```python
            # Delete message for all
            message.delete()
            
            # Delete message only for the current user
            message.delete(for_me=True)
            ```
        """
        return self._client.delete_message(self.chat.id, [self.id], for_me)
    
    def edit(self, text: str) -> "Message":
        """
        Edits the text content of the current message.

        This method updates the message's text and returns the updated `Message` object.

        Args:
            text (str): The new text content for the message.

        Returns:
            Message: A `Message` object representing the edited message.

        Usage:
            ```python
            updated_msg = message.edit("Updated message text!")
            print(updated_msg.text)  # Output: Updated message text!
            ```
        """
        return self._client.edit_message(self.chat.id, self.id, text)