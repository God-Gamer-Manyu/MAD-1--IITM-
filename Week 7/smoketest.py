from app import app

client = app.test_client()

def check(path):
    r = client.get(path)
    print(path, '->', r.status_code)
    text = r.get_data(as_text=True)
    # print a small snippet
    print(text[:400])
    print('---\n')

if __name__ == '__main__':
    check('/')
    # try students list
    check('/students')
    # pick first student if any
    resp = client.get('/students')
    body = resp.get_data(as_text=True)
    # naive find /student/ occurrence
    import re
    m = re.search(r'/student/(\d+)', body)
    if m:
        sid = m.group(1)
        check(f'/student/{sid}')
        # if student has any enrollments, try withdraw first course (we'll search for withdraw link)
        m2 = re.search(r'/student/{}/withdraw/(\d+)'.format(sid), body)
        if m2:
            cid = m2.group(1)
            check(f'/student/{sid}/withdraw/{cid}')
    # try a course
    resp2 = client.get('/courses')
    m3 = re.search(r'/course/(\d+)', resp2.get_data(as_text=True))
    if m3:
        cid = m3.group(1)
        check(f'/course/{cid}')
