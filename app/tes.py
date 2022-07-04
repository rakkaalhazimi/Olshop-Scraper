class x:
    def __init__(self):
        self.nama = "tegar"

class c(x):
    def __init__(self, umur):
        super().__init__()
        self.umur = umur

    def kenal(self):
        return print(f'nama: {self.umur}, umur: {self.nama}')

a = c(21)

a.kenal()