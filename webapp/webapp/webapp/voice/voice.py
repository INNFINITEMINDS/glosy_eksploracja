import datetime


def handle_uploaded_file(f):
    with open('webapp/files/' + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")  + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
