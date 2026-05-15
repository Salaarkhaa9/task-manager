import os
import pytest
import sqlite3
from app import app, init_db, DB_FILE

@pytest.fixture
def client():
    app.config['TESTING'] = True
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    init_db()
    with app.test_client() as client:
        yield client

def test_index(client):
    rv = client.get('/')
    assert b'Item List' in rv.data

def test_add_item(client):
    rv = client.post('/add', data=dict(name='TestItem1'), follow_redirects=True)
    assert b'TestItem1' in rv.data
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT name FROM items WHERE name=?', ('TestItem1',))
    item = c.fetchone()
    conn.close()
    assert item is not None
