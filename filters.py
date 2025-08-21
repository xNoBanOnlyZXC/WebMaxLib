class Filter:
    def __call__(self, client, message) -> bool:
        """
        Base class for message filters.

        This class defines the interface for filters that evaluate whether a message meets specific criteria.
        Subclasses implement the `__call__` method to provide filtering logic. Supports combining filters
        using logical AND (`&`), OR (`|`), and NOT (`~`) operators.

        Args:
            client (MaxClient): The client instance handling the message.
            message (Message): The message to evaluate.

        Returns:
            bool: True if the message passes the filter, False otherwise.

        Usage:
            ```python
            # Subclass Filter to create a custom filter
            class CustomFilter(Filter):
                def __call__(self, client, message):
                    return len(message.text) > 10

            custom_filter = CustomFilter()
            result = custom_filter(client, message)  # Returns True if message text is longer than 10 characters
            ```
        """
        return True

    def __and__(self, other: 'Filter') -> 'AndFilter':
        """
        Combines this filter with another using logical AND.

        Args:
            other (Filter): The filter to combine with.

        Returns:
            AndFilter: A new filter that requires both filters to pass.

        Usage:
            ```python
            combined_filter = filters.text("hello") & filters.user_id("123456")
            # Passes if message text is "hello" AND sender is "123456"
            ```
        """
        return AndFilter(self, other)

    def __or__(self, other: 'Filter') -> 'OrFilter':
        """
        Combines this filter with another using logical OR.

        Args:
            other (Filter): The filter to combine with.

        Returns:
            OrFilter: A new filter that passes if either filter passes.

        Usage:
            ```python
            combined_filter = filters.text("hello") | filters.text("world")
            # Passes if message text is "hello" OR "world"
            ```
        """
        return OrFilter(self, other)

    def __invert__(self) -> 'NotFilter':
        """
        Negates this filter using logical NOT.

        Returns:
            NotFilter: A new filter that passes if this filter fails.

        Usage:
            ```python
            not_me_filter = ~filters.me
            # Passes if the message sender is NOT the authenticated user
            ```
        """
        return NotFilter(self)

class AndFilter(Filter):
    def __init__(self, *filters: Filter):
        """
        A filter that requires all provided filters to pass (logical AND).

        Args:
            *filters (Filter): Variable number of filter instances to combine.

        Attributes:
            filters (tuple[Filter]): The filters to evaluate.

        Usage:
            ```python
            and_filter = AndFilter(filters.text("hello"), filters.user_id("123456"))
            result = and_filter(client, message)  # True if message text is "hello" AND sender is "123456"
            ```
        """
        self.filters = filters

    def __call__(self, client, message) -> bool:
        """
        Evaluates the message against all filters using logical AND.

        Args:
            client (MaxClient): The client instance handling the message.
            message (Message): The message to evaluate.

        Returns:
            bool: True if all filters pass, False otherwise.
        """
        return all(f(client, message) for f in self.filters)

class OrFilter(Filter):
    def __init__(self, *filters: Filter):
        """
        A filter that passes if any of the provided filters pass (logical OR).

        Args:
            *filters (Filter): Variable number of filter instances to combine.

        Attributes:
            filters (tuple[Filter]): The filters to evaluate.

        Usage:
            ```python
            or_filter = OrFilter(filters.text("hello"), filters.text("world"))
            result = or_filter(client, message)  # True if message text is "hello" OR "world"
            ```
        """
        self.filters = filters

    def __call__(self, client, message) -> bool:
        """
        Evaluates the message against all filters using logical OR.

        Args:
            client (MaxClient): The client instance handling the message.
            message (Message): The message to evaluate.

        Returns:
            bool: True if any filter passes, False otherwise.
        """
        return any(f(client, message) for f in self.filters)

class NotFilter(Filter):
    def __init__(self, filter: Filter):
        """
        A filter that negates the result of another filter (logical NOT).

        Args:
            filter (Filter): The filter to negate.

        Attributes:
            filter (Filter): The filter to negate.

        Usage:
            ```python
            not_me_filter = NotFilter(filters.me)
            result = not_me_filter(client, message)  # True if message sender is not the authenticated user
            ```
        """
        self.filter = filter

    def __call__(self, client, message) -> bool:
        """
        Evaluates the message by negating the result of the wrapped filter.

        Args:
            client (MaxClient): The client instance handling the message.
            message (Message): The message to evaluate.

        Returns:
            bool: True if the wrapped filter fails, False otherwise.
        """
        return not self.filter(client, message)

class text(Filter):
    def __init__(self, text: str):
        """
        A filter that matches messages with exact text (case-insensitive).

        Args:
            text (str): The text to match against the message's text.

        Attributes:
            text (str): The lowercase text to match.

        Usage:
            ```python
            text_filter = filters.text("hello")
            result = text_filter(client, message)  # True if message.text is "hello" (case-insensitive)
            ```
        """
        self.text = text.lower()

    def __call__(self, client, message) -> bool:
        """
        Checks if the message text matches the specified text.

        Args:
            client (MaxClient): The client instance handling the message.
            message (Message): The message to evaluate.

        Returns:
            bool: True if the message text matches (case-insensitive), False otherwise.
        """
        return message.text.lower() == self.text if message.text else False

class command(Filter):
    def __init__(self, command: str, prefix: str = "/"):
        """
        A filter that matches messages starting with a specific command (case-insensitive).

        Args:
            command (str): The command to match (without prefix).
            prefix (str, optional): The command prefix (e.g., "/"). Defaults to "/".

        Attributes:
            command (str): The full command string (prefix + command, lowercase).

        Usage:
            ```python
            cmd_filter = filters.command("start")
            result = cmd_filter(client, message)  # True if message.text starts with "/start" (case-insensitive)
            
            # Custom prefix
            cmd_filter = filters.command("help", prefix="!")  # Matches "!help"
            ```
        """
        self.command = (prefix + command).lower()

    def __call__(self, client, message) -> bool:
        """
        Checks if the message text starts with the specified command.

        Args:
            client (MaxClient): The client instance handling the message.
            message (Message): The message to evaluate.

        Returns:
            bool: True if the message text starts with the command (case-insensitive), False otherwise.
        """
        return message.text.lower().startswith(self.command) if message.text else False

class user_id(Filter):
    def __init__(self, user_id: str):
        """
        A filter that matches messages from a specific user ID.

        Args:
            user_id (str): The user ID to match against the message's sender.

        Attributes:
            user_id (str): The user ID to match.

        Usage:
            ```python
            user_filter = filters.user_id("123456")
            result = user_filter(client, message)  # True if message.sender is "123456"
            ```
        """
        self.user_id = user_id

    def __call__(self, client, message) -> bool:
        """
        Checks if the message sender matches the specified user ID.

        Args:
            client (MaxClient): The client instance handling the message.
            message (Message): The message to evaluate.

        Returns:
            bool: True if the message sender matches the user ID, False otherwise.
        """
        return message.sender == self.user_id

class me(Filter):
    def __init__(self):
        """
        A filter that matches messages sent by the authenticated user.

        This filter checks if the message sender matches the ID of the authenticated user (`client.me.contact.id`).

        Usage:
            ```python
            me_filter = filters.me
            result = me_filter(client, message)  # True if message.sender is the authenticated user
            not_me_filter = ~filters.me  # True if message.sender is NOT the authenticated user
            ```
        """
        pass

    def __call__(self, client, message) -> bool:
        """
        Checks if the message sender is the authenticated user.

        Args:
            client (MaxClient): The client instance handling the message.
            message (Message): The message to evaluate.

        Returns:
            bool: True if the message sender is the authenticated user, False otherwise.

        Raises:
            ValueError: If the client has no authenticated user (client.me is None).
        """
        if not client.me or not client.me.contact.id:
            raise ValueError("No authenticated user found. Please authenticate first.")
        return message.sender == client.me.contact.id

class _any(Filter):
    def __init__(self):
        """
        A filter that passes all messages.

        This filter always returns True, allowing any message to pass.

        Usage:
            ```python
            any_filter = filters.any
            result = any_filter(client, message)  # Always returns True
            ```
        """
        pass

    def __call__(self, client, message) -> bool:
        """
        Always passes the message.

        Args:
            client (MaxClient): The client instance handling the message.
            message (Message): The message to evaluate.

        Returns:
            bool: Always True.
        """
        return True
    
class user(Filter):
    def __init__(self):
        """
        A filter that matches messages sent by the authenticated user.

        This filter checks if the message sender matches the ID of the authenticated user (`client.me.contact.id`).

        Usage:
            ```python
            me_filter = filters.me
            result = me_filter(client, message)  # True if message.sender is the authenticated user
            not_me_filter = ~filters.me  # True if message.sender is NOT the authenticated user
            ```
        """
        pass

    def __call__(self, client, message) -> bool:
        """
        Checks if the message sender is the authenticated user.

        Args:
            client (MaxClient): The client instance handling the message.
            message (Message): The message to evaluate.

        Returns:
            bool: True if the message sender is the authenticated user, False otherwise.

        Raises:
            ValueError: If the client has no authenticated user (client.me is None).
        """
        if not client.me or not client.me.contact.id:
            raise ValueError("No authenticated user found. Please authenticate first.")
        return message.type == "USER"

class Filters:
    text = text
    command = command
    user_id = user_id
    me = me
    user = user
    any = _any

filters = Filters()