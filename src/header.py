'''
Created on 28 de set. de 2015

@author: ari
'''


def get_header():
    return open('header.bin','rb').read()

if __name__ == '__main__':
    print(get_header()) 