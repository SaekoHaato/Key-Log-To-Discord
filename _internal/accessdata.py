
def access_data(file_name):
    try:
        file = open(file_name,'r')
        data = file.read()
        file.close()
        return data
    except Exception as e:
        print(e)