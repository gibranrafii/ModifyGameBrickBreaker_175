import tkinter as tk  # Import tkinter untuk membuat GUI
import random  # Import library random untuk menghasilkan angka acak

# Kelas dasar untuk semua objek permainan
class GameObject(object):
    def __init__(self, canvas, item):
        self.canvas = canvas  # #command: Canvas tempat objek digambar
        self.item = item  # #command: Objek permainan yang dibuat di canvas

    def get_position(self):
        return self.canvas.coords(self.item)  # #command: Mengembalikan posisi objek di canvas

    def move(self, x, y):
        self.canvas.move(self.item, x, y)  # #command: Memindahkan objek ke posisi baru berdasarkan offset x dan y

    def delete(self):
        self.canvas.delete(self.item)  # #command: Menghapus objek dari canvas


# Kelas Ball (Bola)
class Ball(GameObject):
    def __init__(self, canvas, x, y):
        self.radius = 10  # #command: Radius bola
        self.direction = [random.choice([-1, 1]), -1]  # #command: Arah awal bola (acak untuk horizontal)
        self.speed = random.randint(4, 6)  # #command: Kecepatan bola (acak antara 4-6)
        item = canvas.create_oval(x - self.radius, y - self.radius,
                                  x + self.radius, y + self.radius,
                                  fill='white')  # #command: Menggambar bola di canvas
        super(Ball, self).__init__(canvas, item)  # #command: Memanggil konstruktor kelas induk

    def update(self):
        coords = self.get_position()  # #command: Mendapatkan posisi bola saat ini
        width = self.canvas.winfo_width()  # #command: Mendapatkan lebar canvas
        if coords[0] <= 0 or coords[2] >= width:  # #command: Jika bola menyentuh sisi kiri/kanan
            self.direction[0] *= -1  # #command: Membalik arah horizontal bola
        if coords[1] <= 0:  # #command: Jika bola menyentuh bagian atas
            self.direction[1] *= -1  # #command: Membalik arah vertikal bola
        x = self.direction[0] * self.speed  # #command: Menghitung pergeseran horizontal
        y = self.direction[1] * self.speed  # #command: Menghitung pergeseran vertikal
        self.move(x, y)  # #command: Memindahkan bola

    def collide(self, game_objects):
        coords = self.get_position()  # #command: Mendapatkan posisi bola
        x = (coords[0] + coords[2]) * 0.5  # #command: Menentukan posisi tengah horizontal bola
        if len(game_objects) > 1:  # #command: Jika bola bertabrakan dengan lebih dari satu objek
            self.direction[1] *= -1  # #command: Membalik arah vertikal bola
        elif len(game_objects) == 1:  # #command: Jika bola bertabrakan dengan satu objek
            game_object = game_objects[0]  # #command: Objek yang bertabrakan dengan bola
            coords = game_object.get_position()  # #command: Mendapatkan posisi objek
            if x > coords[2]:  # #command: Jika bola mengenai sisi kanan objek
                self.direction[0] = 1  # #command: Arah horizontal berubah ke kanan
            elif x < coords[0]:  # #command: Jika bola mengenai sisi kiri objek
                self.direction[0] = -1  # #command: Arah horizontal berubah ke kiri
            else:
                self.direction[1] *= -1  # #command: Membalik arah vertikal bola

        for game_object in game_objects:  # #command: Iterasi untuk setiap objek yang bertabrakan
            if isinstance(game_object, Brick):  # #command: Jika objek adalah brick
                game_object.hit()  # #command: Kurangi jumlah nyawa brick


# Kelas Paddle (Papan Pemantul)
class Paddle(GameObject):
    def __init__(self, canvas, x, y):
        self.width = 100  # #command: Lebar paddle
        self.height = 15  # #command: Tinggi paddle
        self.ball = None  # #command: Referensi ke bola yang menempel pada paddle
        self.color = '#FF5733'  # #command: Warna paddle
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill=self.color)  # #command: Membuat paddle di canvas
        super(Paddle, self).__init__(canvas, item)  # #command: Memanggil konstruktor kelas induk

    def set_ball(self, ball):
        self.ball = ball  # #command: Menetapkan bola yang menempel pada paddle

    def move(self, offset):
        coords = self.get_position()  # #command: Mendapatkan posisi paddle saat ini
        width = self.canvas.winfo_width()  # #command: Mendapatkan lebar canvas
        if coords[0] + offset >= 0 and coords[2] + offset <= width:  # #command: Memastikan paddle tidak keluar batas
            super(Paddle, self).move(offset, 0)  # #command: Memindahkan paddle
            if self.ball is not None:  # #command: Jika bola menempel pada paddle
                self.ball.move(offset, 0)  # #command: Bola ikut bergerak dengan paddle

    def change_color(self, color):
        self.color = color  # #command: Mengubah warna paddle
        self.canvas.itemconfig(self.item, fill=color)  # #command: Menerapkan warna baru pada paddle


# Kelas Brick (Balok)
class Brick(GameObject):
    COLORS = {1: '#1F618D', 2: '#FF0000', 3: '#F4D03F'}  # #command: Warna brick berdasarkan jumlah nyawa

    def __init__(self, canvas, x, y, hits):
        self.width = 60  # #command: Lebar brick
        self.height = 20  # #command: Tinggi brick
        self.hits = hits  # #command: Jumlah nyawa brick
        color = Brick.COLORS[hits]  # #command: Warna awal brick berdasarkan nyawa
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill=color, tags='brick')  # #command: Membuat brick di canvas
        super(Brick, self).__init__(canvas, item)  # #command: Memanggil konstruktor kelas induk

    def hit(self):
        self.hits -= 1  # #command: Kurangi jumlah nyawa brick
        if self.hits == 0:  # #command: Jika nyawa habis
            self.delete()  # #command: Hapus brick dari canvas
        else:
            self.canvas.itemconfig(self.item, fill=Brick.COLORS[self.hits])  # #command: Ubah warna brick

# Kelas utama untuk permainan
class Game(tk.Frame):
    def __init__(self, master):
        super(Game, self).__init__(master)  # #command: Memanggil konstruktor kelas induk
        self.lives = 3  # #command: Jumlah nyawa pemain
        self.width = 640  # #command: Lebar canvas
        self.height = 480  # #command: Tinggi canvas
        self.canvas = tk.Canvas(self, bg='#000e38',  # #command: Membuat canvas dengan warna latar
                                width=self.width,
                                height=self.height)
        self.canvas.pack()  # #command: Menambahkan canvas ke frame
        self.pack()  # #command: Menambahkan frame ke root Tkinter

        self.items = {}  # #command: Menyimpan semua objek permainan
        self.ball = None  # #command: Referensi ke bola
        self.paddle = Paddle(self.canvas, self.width / 2, 400)  # #command: Membuat paddle
        self.items[self.paddle.item] = self.paddle  # #command: Menambahkan paddle ke daftar objek

        for x in range(5, self.width - 5, 65):  # #command: Menambahkan brick secara horizontal
            self.add_brick(x + 32.5, 50, 3)  # #command: Baris pertama dengan nyawa 3
            self.add_brick(x + 32.5, 80, 2)  # #command: Baris kedua dengan nyawa 2
            self.add_brick(x + 32.5, 110, 1)  # #command: Baris ketiga dengan nyawa 1

        self.hud = None  # #command: Referensi untuk tampilan nyawa
        self.setup_game()  # #command: Mengatur permainan awal
        self.canvas.focus_set()  # #command: Mengatur fokus ke canvas untuk menangkap input
        self.canvas.bind('<Left>', lambda _: self.paddle.move(-15))  # #command: Gerakkan paddle ke kiri
        self.canvas.bind('<Right>', lambda _: self.paddle.move(15))  # #command: Gerakkan paddle ke kanan

    def setup_game(self):
        self.add_ball()  # #command: Menambahkan bola ke permainan
        self.update_lives_text()  # #command: Menampilkan jumlah nyawa di HUD
        self.text = self.draw_text(320, 240, 'Tekan Spasi untuk Mulai!', size='30')  # #command: Teks awal permainan
        
        self.canvas.bind('<space>', lambda _: self.start_game())  # #command: Tombol spasi untuk memulai permainan

    def add_ball(self):
        if self.ball is not None:  # #command: Jika bola sudah ada
            self.ball.delete()  # #command: Hapus bola sebelumnya
        paddle_coords = self.paddle.get_position()  # #command: Mendapatkan posisi paddle
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5  # #command: Menempatkan bola di tengah paddle
        self.ball = Ball(self.canvas, x, 380)  # #command: Membuat objek bola
        self.paddle.set_ball(self.ball)  # #command: Menempelkan bola ke paddle

    def add_brick(self, x, y, hits):
        brick = Brick(self.canvas, x, y, hits)  # #command: Membuat objek brick
        self.items[brick.item] = brick  # #command: Menambahkan brick ke daftar objek

    def draw_text(self, x, y, text, size='20', fill='white'):
        font = ('Arial', size)  # #command: Gaya font untuk teks
        return self.canvas.create_text(x, y, text=text, font=font, fill=fill)  # #command: Menambahkan teks ke canvas

    def update_lives_text(self):
        text = f'Nyawa: {self.lives}'  # #command: Format teks untuk nyawa
        if self.hud is None:  # #command: Jika HUD belum dibuat
            self.hud = self.draw_text(70, 20, text, 15,)  # #command: Menambahkan teks nyawa ke canvas
        else:
            self.canvas.itemconfig(self.hud, text=text)  # #command: Memperbarui teks nyawa di HUD

    def start_game(self):
        self.canvas.unbind('<space>')  # #command: Melepas binding tombol spasi
        self.canvas.delete(self.text)  # #command: Menghapus teks awal permainan
        self.paddle.ball = None  # #command: Melepaskan bola dari paddle
        self.game_loop()  # #command: Memulai loop permainan

    def game_loop(self):
        self.check_collisions()  # #command: Mengecek tabrakan bola dengan objek lain
        num_bricks = len(self.canvas.find_withtag('brick'))  # #command: Menghitung jumlah brick yang tersisa
        if num_bricks == 0:  # #command: Jika semua brick telah dihancurkan
            self.ball.speed = 0  # #command: Menghentikan bola
            self.draw_text(320, 240, 'Kamu Menang!')  # #command: Tampilkan pesan kemenangan
        elif self.ball.get_position()[3] >= self.height:  # #command: Jika bola jatuh ke bawah
            self.ball.speed = 0  # #command: Menghentikan bola
            self.lives -= 1  # #command: Kurangi nyawa pemain
            if self.lives < 0:  # #command: Jika nyawa habis
                self.draw_text(320, 240, 'Game Over!')  # #command: Tampilkan pesan game over
            else:
                self.after(1000, self.setup_game)  # #command: Reset permainan setelah 1 detik
        else:
            self.ball.update()  # #command: Memperbarui posisi bola
            self.after(50, self.game_loop)  # #command: Memanggil kembali loop permainan

    def check_collisions(self):
        ball_coords = self.ball.get_position()  # #command: Mendapatkan posisi bola
        items = self.canvas.find_overlapping(*ball_coords)  # #command: Mendapatkan semua objek yang bertabrakan
        objects = [self.items[x] for x in items if x in self.items]  # #command: Filter hanya objek permainan
        self.ball.collide(objects)  # #command: Menangani tabrakan bola


# Program utama untuk menjalankan permainan
if __name__ == '__main__':
    root = tk.Tk()  # #command: Membuat jendela utama
    root.title('Permainan Brick Breaker')  # #command: Menentukan judul jendela
    game = Game(root)  # #command: Membuat instance kelas Game
    game.mainloop()  # #command: Memulai loop Tkinter untuk menjalankan permainan


