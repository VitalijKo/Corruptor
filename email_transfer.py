import win32com.client

target = ''


def outlook(subject, contents):
    outlook = win32com.client.Dispatch('Outlook.Application')

    message = outlook.CreateItem(0)
    message.DeleteAfterSubmit = True
    message.Subject = subject
    message.Body = contents.decode()
    message.To = target[0]
    message.Send()
