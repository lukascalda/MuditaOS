# Copyright (c) 2017-2022, Mudita Sp. z.o.o. All rights reserved.
# For licensing, see https://github.com/mudita/MuditaOS/LICENSE.md
import pytest
from harness.request import TransactionError
from harness.api.messages import GetMessagesCount, GetMessagesWithOffsetAndLimit, GetMessageById, \
    GetMessagesByThreadIdWithOffsetAndLimit, AddMessage, DeleteMessageById


class MessagesTester:
    def __init__(self, harness):
        self.harness = harness

    def get_messages_count(self):
        try:
            count = GetMessagesCount().run(self.harness).count
        except TransactionError:
            return False
        else:
            return True, count

    def get_messages_with_offset_and_limit(self, offset, limit):
        try:
            result = GetMessagesWithOffsetAndLimit(offset, limit).run(self.harness)
        except TransactionError:
            return False
        else:
            return True, result

    def get_message_by_id(self, message_record_id):
        try:
            result = GetMessageById(message_record_id).run(self.harness)
        except TransactionError:
            return False
        else:
            return True, result.message

    def get_messages_by_thread_id(self, thread_record_id, offset, limit):
        try:
            result = GetMessagesByThreadIdWithOffsetAndLimit(thread_record_id, offset, limit).run(self.harness)
        except TransactionError:
            return False
        else:
            return True, result

    def add_message(self, message_number, message_body):
        try:
            message = AddMessage(message_number, message_body).run(self.harness).message
        except TransactionError:
            return False
        else:
            return True, message

    def delete_message_by_id(self, message_record_id):
        try:
            DeleteMessageById(message_record_id).run(self.harness)
        except TransactionError:
            return False
        else:
            return True


@pytest.mark.service_desktop_test
@pytest.mark.usefixtures("phone_unlocked")
def test_add_and_delete_message(harness):
    messages_tester = MessagesTester(harness)
    result, received_messages_records_count = messages_tester.get_messages_count()
    assert result, "Failed to get messages count!"
    initial_number_of_messages_records = received_messages_records_count

    message_number = "123456789"
    message_body = "Hello, how are you?"

    result, message_record = messages_tester.add_message(message_number, message_body)
    assert result, "Failed to add message!"
    assert message_record["messageBody"] == message_body, "Message body corrupted!"

    result, received_messages_records_count = messages_tester.get_messages_count()
    assert result, "Failed to get messages count!"
    assert received_messages_records_count == initial_number_of_messages_records + 1, "Wrong number of messages!"

    assert messages_tester.delete_message_by_id(message_record["messageID"]), "Failed to delete a message!"

    result, received_messages_records_count = messages_tester.get_messages_count()
    assert result, "Failed to get messages count!"
    assert received_messages_records_count == initial_number_of_messages_records, "Wrong number of messages!"


@pytest.mark.service_desktop_test
@pytest.mark.usefixtures("phone_unlocked")
def test_get_message_by_id(harness):
    messages_tester = MessagesTester(harness)
    result, received_messages_records_count = messages_tester.get_messages_count()
    assert result, "Failed to get messages count!"
    initial_number_of_messages_records = received_messages_records_count

    message_number = "123456789"
    message_body = "Hello, how are you?"

    result, message_record = messages_tester.add_message(message_number, message_body)
    assert result, "Failed to add message!"

    result, received_message_record = messages_tester.get_message_by_id(message_record["messageID"])
    assert result, "Failed to get message by id!"
    assert received_message_record["messageID"] == message_record["messageID"], "Wrong message id!"
    assert received_message_record["messageBody"] == message_body, "Wrong message body!"

    assert messages_tester.delete_message_by_id(message_record["messageID"]), "Failed to delete a message!"

    result, received_messages_records_count = messages_tester.get_messages_count()
    assert result, "Failed to get messages count!"
    assert received_messages_records_count == initial_number_of_messages_records, "Wrong number of messages!"


@pytest.mark.service_desktop_test
@pytest.mark.usefixtures("phone_unlocked")
def test_get_messages_by_thread_id(harness):
    messages_tester = MessagesTester(harness)
    result, received_messages_records_count = messages_tester.get_messages_count()
    assert result, "Failed to get messages count!"
    initial_number_of_messages_records = received_messages_records_count

    message_number = "123456789"
    message_1_body = "Hello, how are you?"
    message_2_body = "Are you there?"

    result, message_1_record = messages_tester.add_message(message_number, message_1_body)
    assert result, "Failed to add message!"
    result, message_2_record = messages_tester.add_message(message_number, message_2_body)
    assert result, "Failed to add message!"

    result, received_message_1_record = messages_tester.get_message_by_id(message_1_record["messageID"])
    assert result, "Failed to get message by id!"

    result, response = messages_tester.get_messages_by_thread_id(
        received_message_1_record["threadID"], 0, 0)
    assert result, "Failed to get messages by thread id!"
    found_message_1_id = False
    for record in response.messages:
        if message_1_record["messageID"] == record["messageID"]:
            found_message_1_id = True
            break
    found_message_2_id = False
    for record in response.messages:
        if message_2_record["messageID"] == record["messageID"]:
            found_message_2_id = True
            break
    assert found_message_1_id and found_message_2_id

    assert messages_tester.delete_message_by_id(message_1_record["messageID"]), "Failed to delete a message!"
    assert messages_tester.delete_message_by_id(message_2_record["messageID"]), "Failed to delete a message!"

    result, received_messages_records_count = messages_tester.get_messages_count()
    assert result, "Failed to get messages count!"
    assert received_messages_records_count == initial_number_of_messages_records, "Wrong number of messages!"


@pytest.mark.service_desktop_test
@pytest.mark.usefixtures("phone_unlocked")
def test_get_multiple_messages(harness):
    messages_tester = MessagesTester(harness)
    result, received_messages_records_count = messages_tester.get_messages_count()
    assert result, "Failed to get messages count!"
    initial_number_of_messages_records = received_messages_records_count

    message_number_1 = "123456789"
    message_1_body = "Hello, how are you?"
    message_2_body = "Are you there?"

    message_number_2 = "223456789"
    message_3_body = "What's up?"
    message_4_body = "Did you checked your email recently?"

    result, message_1_record = messages_tester.add_message(message_number_1, message_1_body)
    assert result, "Failed to add message!"
    result, message_2_record = messages_tester.add_message(message_number_1, message_2_body)
    assert result, "Failed to add message!"
    result, message_3_record = messages_tester.add_message(message_number_2, message_3_body)
    assert result, "Failed to add message!"
    result, message_4_record = messages_tester.add_message(message_number_2, message_4_body)
    assert result, "Failed to add message!"

    result, response = messages_tester.get_messages_with_offset_and_limit(
        initial_number_of_messages_records, 4)
    assert result, "Failed to get messages with offset and limit!"
    found_message_1_id = False
    for record in response.messages:
        if message_1_record["messageID"] == record["messageID"]:
            found_message_1_id = True
            break
    assert found_message_1_id

    found_message_2_id = False
    for record in response.messages:
        if message_2_record["messageID"] == record["messageID"]:
            found_message_2_id = True
            break
    assert found_message_2_id

    found_message_3_id = False
    for record in response.messages:
        if message_3_record["messageID"] == record["messageID"]:
            found_message_3_id = True
            break
    assert found_message_3_id

    found_message_4_id = False
    for record in response.messages:
        if message_4_record["messageID"] == record["messageID"]:
            found_message_4_id = True
            break
    assert found_message_4_id

    assert messages_tester.delete_message_by_id(message_1_record["messageID"]), "Failed to delete a message!"
    assert messages_tester.delete_message_by_id(message_2_record["messageID"]), "Failed to delete a message!"
    assert messages_tester.delete_message_by_id(message_3_record["messageID"]), "Failed to delete a message!"
    assert messages_tester.delete_message_by_id(message_4_record["messageID"]), "Failed to delete a message!"

    result, received_messages_records_count = messages_tester.get_messages_count()
    assert result, "Failed to get messages count!"
    assert received_messages_records_count == initial_number_of_messages_records, "Wrong number of messages!"


@pytest.mark.service_desktop_test
@pytest.mark.usefixtures("phone_unlocked")
def test_pagination(harness):
    messages_tester = MessagesTester(harness)
    result, received_messages_records_count = messages_tester.get_messages_count()
    assert result, "Failed to get messages count!"
    initial_number_of_messages_records = received_messages_records_count

    message_number = "123456789"
    message_1_body = "Test message nr 1"
    message_2_body = "Test message nr 2"
    message_3_body = "Test message nr 3"
    message_4_body = "Test message nr 4"
    message_5_body = "Test message nr 5"
    message_6_body = "Test message nr 6"

    result, message_1_record = messages_tester.add_message(message_number, message_1_body)
    assert result, "Failed to add message!"
    result, message_2_record = messages_tester.add_message(message_number, message_2_body)
    assert result, "Failed to add message!"
    result, message_3_record = messages_tester.add_message(message_number, message_3_body)
    assert result, "Failed to add message!"
    result, message_4_record = messages_tester.add_message(message_number, message_4_body)
    assert result, "Failed to add message!"
    result, message_5_record = messages_tester.add_message(message_number, message_5_body)
    assert result, "Failed to add message!"
    result, message_6_record = messages_tester.add_message(message_number, message_6_body)
    assert result, "Failed to add message!"

    result, response = messages_tester.get_messages_with_offset_and_limit(
        initial_number_of_messages_records, 6)
    assert result, "Failed to get messages with offset and limit!"
    MESSAGES_PAGE_SIZE = 4
    assert len(response.messages) == MESSAGES_PAGE_SIZE
    assert response.totalCount == initial_number_of_messages_records + 6
    assert response.nextPage["limit"] == 2
    assert response.nextPage["offset"] == initial_number_of_messages_records + 4
    received_messages = response.messages
    result, response = messages_tester.get_messages_with_offset_and_limit(
        response.nextPage["offset"], response.nextPage["limit"])
    assert result, "Failed to get messages with offset and limit!"
    assert len(response.messages) == 2
    received_messages += response.messages

    found_message_1_id = False
    for record in received_messages:
        if message_1_record["messageID"] == record["messageID"]:
            found_message_1_id = True
            break
    assert found_message_1_id

    found_message_2_id = False
    for record in received_messages:
        if message_2_record["messageID"] == record["messageID"]:
            found_message_2_id = True
            break
    assert found_message_2_id

    found_message_3_id = False
    for record in received_messages:
        if message_3_record["messageID"] == record["messageID"]:
            found_message_3_id = True
            break
    assert found_message_3_id

    found_message_4_id = False
    for record in received_messages:
        if message_4_record["messageID"] == record["messageID"]:
            found_message_4_id = True
            break
    assert found_message_4_id

    found_message_5_id = False
    for record in received_messages:
        if message_5_record["messageID"] == record["messageID"]:
            found_message_5_id = True
            break
    assert found_message_5_id

    found_message_6_id = False
    for record in received_messages:
        if message_6_record["messageID"] == record["messageID"]:
            found_message_6_id = True
            break
    assert found_message_6_id

    thread_id = received_messages[0]["threadID"]
    result, response = messages_tester.get_messages_by_thread_id(thread_id,
                                                                 initial_number_of_messages_records, 6)
    assert result, "Failed to get messages by thread id!"
    assert len(response.messages) == MESSAGES_PAGE_SIZE
    assert response.totalCount == initial_number_of_messages_records + 6
    assert response.nextPage["limit"] == 2
    assert response.nextPage["offset"] == initial_number_of_messages_records + 4
    received_messages = response.messages
    result, response = messages_tester.get_messages_by_thread_id(thread_id,
                                                                 response.nextPage["offset"],
                                                                 response.nextPage["limit"])
    assert result, "Failed to get messages with offset and limit!"
    assert len(response.messages) == 2
    received_messages += response.messages

    found_message_1_id = False
    for record in received_messages:
        if message_1_record["messageID"] == record["messageID"]:
            found_message_1_id = True
            break
    assert found_message_1_id

    found_message_2_id = False
    for record in received_messages:
        if message_2_record["messageID"] == record["messageID"]:
            found_message_2_id = True
            break
    assert found_message_2_id

    found_message_3_id = False
    for record in received_messages:
        if message_3_record["messageID"] == record["messageID"]:
            found_message_3_id = True
            break
    assert found_message_3_id

    found_message_4_id = False
    for record in received_messages:
        if message_4_record["messageID"] == record["messageID"]:
            found_message_4_id = True
            break
    assert found_message_4_id

    found_message_5_id = False
    for record in received_messages:
        if message_5_record["messageID"] == record["messageID"]:
            found_message_5_id = True
            break
    assert found_message_5_id

    found_message_6_id = False
    for record in received_messages:
        if message_6_record["messageID"] == record["messageID"]:
            found_message_6_id = True
            break
    assert found_message_6_id

    assert messages_tester.delete_message_by_id(message_1_record["messageID"]), "Failed to delete a message!"
    assert messages_tester.delete_message_by_id(message_2_record["messageID"]), "Failed to delete a message!"
    assert messages_tester.delete_message_by_id(message_3_record["messageID"]), "Failed to delete a message!"
    assert messages_tester.delete_message_by_id(message_4_record["messageID"]), "Failed to delete a message!"
    assert messages_tester.delete_message_by_id(message_5_record["messageID"]), "Failed to delete a message!"
    assert messages_tester.delete_message_by_id(message_6_record["messageID"]), "Failed to delete a message!"

    result, received_messages_records_count = messages_tester.get_messages_count()
    assert result, "Failed to get messages count!"
    assert received_messages_records_count == initial_number_of_messages_records, "Wrong number of messages!"
