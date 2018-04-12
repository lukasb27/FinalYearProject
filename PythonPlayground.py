import requests
import sys


def main():

    programes = {'ccleaner':'https://download.ccleaner.com/ccsetup541.exe', 'other':'https://otherthingshere'}

    selection = 'ccleaner'

    for i in programes.keys():
            if selection == i:
                # print (programes[selection])
                link = programes[selection]
                file_name = selection +'.exe'
    # if selection == 'ccleaner':
    #     link = "https://download.ccleaner.com/ccsetup541.exe"
    #     file_name = "cCleaner.exe"
    # elif selection == 'another free program'
    #     link = "link to other programs download here"
    #     file_name = 'programe name'
    #
    download(link, file_name)
    # print(link, file_name)

def download(link, file_name):

    with open(file_name, "wb") as f:
            print ("Downloading %s" % file_name)
            response = requests.get(link, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None: # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )
                    sys.stdout.flush()



main()