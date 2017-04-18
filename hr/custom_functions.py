__author__ = 'Tusfiqur'

def populateMessage(message):

    form_message = ''
    if message == 'add':
        form_message = ''
    elif message == 'edited':
        form_message = 'Successfully Edited!!!'
    elif message == 'True':
        form_message = 'Successfully Added'
    elif message == 'False':
        form_message = ' Name already exists!! Not saved in database'

    return form_message