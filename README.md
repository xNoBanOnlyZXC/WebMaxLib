# WebMaxLib

WebMaxLib is a Python library for interacting with the Max messaging service via WebSocket. It provides a simple, Pyrogram-inspired API for sending messages, images, editing or deleting messages, and handling incoming messages with a flexible filter system. This library is designed for developers who want to automate interactions with the Max messenger, handling authentication, chats, and message processing.

## Features

- **WebSocket Communication**: Connects to the Max messaging service using WebSocket for real-time interaction.
- **Authentication**: Supports token-based and phone-based authentication.
- **Message Handling**: Send, reply, edit, and delete messages with ease.
- **Image Support**: Upload and send images to chats.
- **Filter System**: Flexible filters for processing incoming messages, including text, command, user ID, self-sent messages, and logical combinations (AND, OR, NOT).
- **Object-Oriented Design**: Classes like `User`, `Contact`, `Chat`, and `Message` for intuitive interaction with the service.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/xNoBanOnlyZXC/WebMaxLib.git
   cd maxclient
   ```

2. Install dependencies:
   ```bash
   pip install -y websockets requests
   ```

3. Set up your project:
   - Place your code in a Python environment.
   - Ensure you have a valid authentication token or phone number for the Max service.

## Usage

### Basic Example

The following example demonstrates how to set up a `MaxClient`, handle connection events, and respond to specific commands:

```python
from max import MaxClient as Client
from filters import filters
from classes import Message
import time

# Initialize client with a token
token = "your_auth_token"
client = Client(token)

# Handle connection event
@client.on_connect
def onconnect():
    print(f"Get User, full name: {client.me.contact.names[0].name}, number: {client.me.contact.phone} | {client.me.contact.id}")

# Example: bug with replymessage
@client.on_message(filters.command("wtf"))
def on_wtf(client: Client, message: Message):
    m = client.send_message(message.chat.id, "This message not exists")
    time.sleep(1)
    m2 = m.reply("Reply to removed message")
    time.sleep(1)
    m.delete()
    message.reply("Max - most bugged messenger.")

# Handle messages with "/z" command
@client.on_message(filters.command("z"))
def on_z(client: Client, message: Message):
    message.reply("I have Z!")

# Run the client
client.run()
```

### Authentication with Phone Number

If you don't have a token, you can authenticate using a phone number:

```python
client = Client()
client.auth("+7xxxxxxxxxx")  # Replace with your phone number
print(client.auth_token)  # Prints the obtained token
client.run()
```

### Using Filters

Filters allow you to process incoming messages based on specific criteria. Combine filters using logical operators (`&`, `|`, `~`):

```python
# Respond to messages from the authenticated user saying "hello"
@client.on_message(filters.me & filters.text("hello"))
def handle_my_hello(client: Client, message: Message):
    message.reply("I said hello!")

# Respond to messages NOT from the authenticated user with "/start"
@client.on_message(~filters.me & filters.command("start"))
def handle_non_me_start(client: Client, message: Message):
    message.reply("Someone else used /start!")
```

## Filter System

The library includes a powerful filter system inspired by Pyrogram, allowing you to handle messages based on various conditions:

- **`filters.text(text)`**: Matches messages with exact text (case-insensitive).
- **`filters.command(command, prefix="/")`**: Matches messages starting with a command (e.g., `/start`).
- **`filters.user_id(user_id)`**: Matches messages from a specific user ID.
- **`filters.me`**: Matches messages sent by the authenticated user.
- **`filters.any`**: Passes all messages.
- **Logical Operators**:
  - `&` (AND): Combine filters to require all to pass (e.g., `filters.text("hello") & filters.me`).
  - `|` (OR): Combine filters to pass if any succeed (e.g., `filters.text("hello") | filters.text("world")`).
  - `~` (NOT): Negate a filter (e.g., `~filters.me` for messages not from the authenticated user).

Example:
```python
@client.on_message(filters.me | filters.command("help"))
def handle_me_or_help(client: Client, message: Message):
    message.reply("Either I sent this or it's a /help command!")
```

## Classes

### `MaxClient`
The main class for interacting with the Max service.

- **Methods**:
  - `__init__(token=None, phone=None)`: Initializes the client with an optional token or phone number.
  - `connect()`: Establishes a WebSocket connection.
  - `disconnect()`: Closes the connection.
  - `set_token(token)`: Updates the authentication token.
  - `run()`: Starts the client and listener thread.
  - `stop()`: Stops the client and listener.
  - `auth(phone_number)`: Performs interactive authentication.
  - `send_message(chat_id, text, reply_id=None, notify=True)`: Sends a text message.
  - `delete_message(chat_id, message_ids, for_me=False)`: Deletes messages.
  - `edit_message(chat_id, message_id, text)`: Edits a message.
 
- **Decorators**:
  - `on_message(filter)`: Decorator for handling messages with a filter.
  - `on_connect(func)`: Decorator for handling connection events.

### `Name`
Stores name information for a contact.

- **Attributes**: `name`, `first_name`, `last_name`, `type`.

### `Contact`
Represents a contact's profile information.

- **Attributes**: `accountStatus`, `base_url`, `names` (list of `Name`), `phone`, `description`, `options`, `photo_id`, `update_time`, `id`, `base_raw_url`.

### `User`
Wraps a `Contact` to represent a user.

- **Attributes**: `contact`.

### `Chat`
Represents a chat in the messaging system.

- **Attributes**: `_client`, `id`.

### `Message`
Represents a message in a chat.

- **Attributes**: `_client`, `chat`, `sender`, `id`, `time`, `text`, `type`, `update_time`, `options`, `cid`, `attaches`.
- **Methods**:
  - `reply(text, **kwargs)`: Replies to the message.
  - `answer(text, **kwargs)`: Sends a new message in the same chat.
  - `delete(for_me=False)`: Deletes the message.
  - `edit(text)`: Edits the message's text.

### Filter Classes
- **`Filter`**: Base class for filters, supporting `&`, `|`, and `~` operators.
- **`AndFilter`**: Combines filters with logical AND.
- **`OrFilter`**: Combines filters with logical OR.
- **`NotFilter`**: Negates a filter.
- **`text`**: Matches exact message text.
- **`command`**: Matches commands with a prefix.
- **`user_id`**: Matches messages from a user ID.
- **`me`**: Matches messages from the authenticated user.
- **`any`**: Passes all messages.

### `Filters`
A container for filter factories and instances (`text`, `command`, `user_id`, `me`, `any`).

## Requirements

- Python 3.7+
- `websockets` library for WebSocket communication
- `requests` library for image uploads
- A valid Max service authentication token or phone number

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

## License

This project is licensed under the General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Disclaimer

This library is unofficial and not affiliated with the Max messaging service. Use it at your own risk, and ensure compliance with the service's terms of use.
