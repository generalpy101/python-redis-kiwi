from deepdiff import DeepDiff


def test_post(app_client, test_data_1):
    response = app_client.post("/set", json=test_data_1)

    actual_response = {"test1": True, "test2": True, "test3": 2}

    data = response.json
    assert response.status_code == 200

    diff = DeepDiff(data, actual_response, ignore_order=True)
    assert diff == {}, diff.pretty()


def test_get_all(app_client, test_data_1):
    response = app_client.get("/all")

    data = response.json
    assert response.status_code == 200

    diff = DeepDiff(test_data_1, data, ignore_order=True)
    assert diff == {}, diff.pretty()


def test_get_one_key(app_client):
    response = app_client.get("/get?keys=test1")

    actual_response = {"test1": "value1"}

    data = response.json
    assert response.status_code == 200

    diff = DeepDiff(data, actual_response, ignore_order=True)
    assert diff == {}, diff.pretty()


def test_delete_key(app_client):
    response = app_client.post("/delete", json={"keys": ["test2"]})

    actual_response = {"test2": True}

    data = response.json
    assert response.status_code == 200

    diff = DeepDiff(data, actual_response, ignore_order=True)
    assert diff == {}, diff.pretty()


def test_get_all_keys_after_delete(app_client, test_data_2):
    response = app_client.get("/all")

    data = response.json
    assert response.status_code == 200

    diff = DeepDiff(test_data_2, data, ignore_order=True)
    assert diff == {}, diff.pretty()


def test_get_deleted_key(app_client):
    response = app_client.get("/get?keys=test2")

    actual_response = {"test2": None}

    data = response.json
    assert response.status_code == 200

    diff = DeepDiff(data, actual_response, ignore_order=True)
    assert diff == {}, diff.pretty()


def test_update_using_post(app_client, test_data_3):
    response_1 = app_client.post("/set", json={"test1": "value_new"})
    response_2 = app_client.get("/all")

    actual_response_1 = {"test1": True}

    response_1.status_code == 200
    response_2.status_code == 200

    data1 = response_1.json
    data_2 = response_2.json

    diff_1 = DeepDiff(data1, actual_response_1, ignore_order=True)
    diff2 = DeepDiff(data_2, test_data_3, ignore_order=True)

    assert diff_1 == {}, diff_1.pretty()
    assert diff2 == {}, diff2.pretty()


def test_delete_multiple_keys(app_client):
    response = app_client.post("/delete", json={"keys": ["test1", "test3"]})

    actual_response = {"test1": True, "test3": True}

    data = response.json
    assert response.status_code == 200

    diff = DeepDiff(data, actual_response, ignore_order=True)
    assert diff == {}, diff.pretty()


def test_get_all_keys_empty(app_client):
    response = app_client.get("/all")

    data = response.json
    assert response.status_code == 200

    diff = DeepDiff(data, {}, ignore_order=True)
    assert diff == {}, diff.pretty()
