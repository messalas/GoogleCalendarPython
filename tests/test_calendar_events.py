import pytest
from calendar_events import *

test_username = "Enter a valid test_username"


def test_create_events():
    event = create_event(test_username, "test title", "2021-01-01", "2021-01-03", "test description", "busy")
    assert event["summary"] == "test title"
    assert event["start"]["date"] == "2021-01-01"
    assert event["end"]["date"] == "2021-01-03"
    assert event["description"] == "test description"
    delete_event(test_username, event['id'])


def test_update_events():
    event = create_event(test_username, "test title", "2021-01-01", "2021-01-03", "test description", "available")
    updated_event = update_event(test_username,
                                 event['id'],
                                 title="updated title",
                                 start="2021-10-10",
                                 end="2021-10-30",
                                 description="updated description",
                                 show_me_as="busy")
    assert updated_event["summary"] == "updated title"
    assert updated_event["start"]["date"] == "2021-10-10"
    assert updated_event["end"]["date"] == "2021-10-30"
    assert updated_event["description"] == "updated description"
    delete_event(test_username, updated_event['id'])


def test_wrong_dates():
    with pytest.raises(ValueError):
        create_event(test_username, title="test title", start="2022-01-01", end="2020-01-03")
    with pytest.raises(TypeError):
        create_event(test_username, title=123, start="2020-01-01", end="2021-01-03")
    with pytest.raises(TypeError):
        create_event(test_username, description=123, start="2020-01-01", end="2021-01-03")
    with pytest.raises(TypeError):
        create_event(test_username, title="valid", description=123, start="2020-01-01",end="2021-01-03")
    with pytest.raises(ValueError):
        create_event(test_username, title="valid", show_me_as="invalid", start="2020-01-01",end="2021-01-03")


try:
    test_create_events()
    test_update_events()
    test_wrong_dates()
    print("Tests passed!")
except Exception as e:
    print("Test failed! \n\n", e)
