import glob
import fitz

PATH = '../input/vtb'
FILENAMES = glob.glob(PATH + '/*.pdf')

def get_data():
    for filename in FILENAMES:
        file = fitz.open(filename)
        for page in file:
            rows = page.get_text().split('\n')
            print(len(rows))
            print(rows)

if __name__ == '__main__':
    get_data()