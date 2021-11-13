import pandas as pd


KEY = "abcdefghijklmnopqrstuvwxyz-.0123456789~ABCDEFGHIJKLMNOPQRSTUVWXYZ_"


class BaseConverter:
    def __init__(self, KEY):
        self.hash = KEY

    def id_to_short(self, id):
        """
        Convert a positive number into Base X and return the string.
        """

        if id == 0:
            return self.hash[0]
        arrays = []
        arrays_append = arrays.append
        _divmod = divmod 
        base = len(self.hash)
        while id:
            id, rem = _divmod(id, base)
            arrays_append(self.hash[rem])
        arrays.reverse()
        return ''.join(arrays)

    def short_to_id(self, string):
        """
        Decode a Base X encoded string into the number
        """
        base = len(self.hash)
        strlen = len(string)
        id = 0

        idx = 0
        for char in string:
            power = (strlen - (idx + 1))
            id += self.hash.index(char) * (base ** power)
            idx += 1

        return id


class UrlShortener:
    def __init__(self, KEY):
        self.obj = BaseConverter(KEY)
        try:
            self.database = pd.read_csv('url.csv')

        except FileNotFoundError:
            self.database = pd.DataFrame(columns=['url'])

    def shorten(self, actual_url):
      """
      Shorten the original url and give back the shorten url
      """
        if actual_url not in list(self.database.url.values):
            self.database = self.database.append(pd.DataFrame({'url': [actual_url]})).reset_index(drop=True)
            id = self.database[self.database['url'] == actual_url].index.values[0]
            short_url = self.obj.id_to_short(id)

            print("\nShorten url for given url is ", short_url)
        else:
            id = self.database[self.database['url'] == actual_url].index.values[0]
            short_url = self.obj.id_to_short(id)
            print("\nGiven URL exist and short url of given url is ", short_url)

    def get_url(self, short_url):
      """
      Get original URL back from shorten url
      """
        try:
            get_id = self.obj.short_to_id(short_url)
            print(self.database.iloc[get_id].values[0])
        except IndexError:
            print('No URL found for given short url')

    def save_file(self):
        self.database.to_csv('url.csv', index=False)


shorten_obj = UrlShortener(KEY)
print("\n***************** Welcome to the URL shortener service.. What would you like to do? *************************")
command = 1
while command:
    print("""\nEnter 1 to get shorter URL of actual url\nEnter 2 to get actual url from shorter url\nEnter 0 to exit""")

    command = input("""\nWhat would you like to do?\n""")

    if command == '1':
        url = input("\nEnter URL to shortening\n")
        shorten_obj.shorten(url)
    elif command == '2':
        short_url = input("\nEnter short url\n")
        shorten_obj.get_url(short_url)
    elif command == '0':
        shorten_obj.save_file()
        print("\nThanks for playing. See you later.\n")
        break
    else:
        print("\nI don't understand that choice, please try again.\n")
