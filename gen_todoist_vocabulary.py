#!/usr/bin/env python3

import requests
import os


def get_tasks(filter):
    resp = requests.get(
        url="https://api.todoist.com/rest/v1/tasks",
        params={"filter": filter},
        headers={"Authorization": f'Bearer {os.environ["TODOIST_TOKEN"]}'},
    )
    resp.raise_for_status()
    return resp.json()


def close_task(id):
    requests.post(
        url=f'https://api.todoist.com/rest/v1/tasks/{id}/close',
        headers={"Authorization": f'Bearer {os.environ["TODOIST_TOKEN"]}'},
    ).raise_for_status()


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()
    with open("words.txt", "a") as of:
        for t in get_tasks('@anki'):
            print(t['content'], file=of)
            close_task(t['id'])