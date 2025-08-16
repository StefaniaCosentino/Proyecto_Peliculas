import tkinter as tk
from tkinter import font, ttk, simpledialog, messagebox
import os
import random
import pygame


class Pelicula:
    """Clase para representar una película con sus atributos."""
    def __init__(self, nombre, anio):
        self.nombre = nombre
        self.__anio = anio  # Atributo privado

    def get_info(self):
        """Devuelve una cadena con la información de la película."""
        return f"{self.nombre} ({self.__anio})"

class CatalogoPelicula:
    """Clase para gestionar los catálogos de películas en archivos de texto."""
    def __init__(self, nombre_catalogo):
        self.nombre = nombre_catalogo
        self.ruta_archivo = f"{nombre_catalogo}.txt"

    def agregar(self):
        """Permite al usuario agregar una o más películas al catálogo."""
        peliculas = []
        try:
            with open(self.ruta_archivo, "r") as archivo:
                peliculas = [linea.strip() for linea in archivo.readlines()]
            messagebox.showinfo("Catálogo Cargado", f"Catálogo '{self.nombre}' cargado. Ahora puedes agregar más películas.")
        except FileNotFoundError:
            messagebox.showinfo("Catálogo Nuevo", f"El catálogo '{self.nombre}' no existe. Se creará uno nuevo.")

        while True:
            nueva_pelicula = simpledialog.askstring("Agregar Película", "Ingresa una película (o 'fin' para terminar):")
            if not nueva_pelicula or nueva_pelicula.lower() == 'fin':
                break
            # Aquí podríamos pedir el año para crear un objeto Pelicula
            peliculas.append(nueva_pelicula)
        
        with open(self.ruta_archivo, "w") as archivo:
            for p in peliculas:
                archivo.write(f"{p}\n")
        
        messagebox.showinfo("Éxito", f"¡Catálogo '{self.nombre}' actualizado con éxito!")

    def listar(self):
        """Muestra todas las películas del catálogo."""
        try:
            with open(self.ruta_archivo, "r") as archivo:
                peliculas = [linea.strip() for linea in archivo.readlines()]
                if not peliculas:
                    messagebox.showinfo("Catálogo Vacío", f"El catálogo '{self.nombre}' está vacío.")
                else:
                    lista_peliculas = "\n".join([f"- {p}" for p in peliculas])
                    messagebox.showinfo("Películas", f"Películas en '{self.nombre}':\n\n{lista_peliculas}")
        except FileNotFoundError:
            messagebox.showerror("Error", f"El catálogo '{self.nombre}' no existe.")

    def eliminar(self):
        """Elimina el archivo del catálogo."""
        if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que quieres eliminar el catálogo '{self.nombre}'?"):
            try:
                os.remove(self.ruta_archivo)
                messagebox.showinfo("Éxito", f"El catálogo '{self.nombre}' ha sido eliminado exitosamente.")
            except FileNotFoundError:
                messagebox.showerror("Error", f"El catálogo '{self.nombre}' no existe.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al intentar eliminar el archivo: {e}")

    def buscar(self, pelicula_buscada):
        """Busca una película en el catálogo y la agrega si no existe."""
        try:
            with open(self.ruta_archivo, "r") as archivo:
                peliculas = [linea.strip().lower() for linea in archivo.readlines()]
                
            if pelicula_buscada.lower() in peliculas:
                messagebox.showinfo("¡Encontrada!", "TU PELÍCULA SE ENCUENTRA DENTRO DEL CATÁLOGO.")
            else:
                respuesta = messagebox.askyesno("Película no encontrada", f"'{pelicula_buscada}' no se encuentra en el catálogo '{self.nombre}'. ¿Deseas agregarla?")
                if respuesta:
                    with open(self.ruta_archivo, "a") as archivo:
                        archivo.write(f"\n{pelicula_buscada}")
                    messagebox.showinfo("Éxito", f"'{pelicula_buscada}' ha sido agregada a la categoría '{self.nombre}'.")

        except FileNotFoundError:
            messagebox.showerror("Error", f"La categoría '{self.nombre}' no existe.")


def agregar_pelicula():
    nombre_catalogo = simpledialog.askstring("Agregar Película", "Ingresa el nombre del catálogo:")
    if nombre_catalogo:
        catalogo = CatalogoPelicula(nombre_catalogo)
        catalogo.agregar()

def listar_peliculas():
    nombre_catalogo = simpledialog.askstring("Listar Películas", "Ingresa el nombre del catálogo:")
    if nombre_catalogo:
        catalogo = CatalogoPelicula(nombre_catalogo)
        catalogo.listar()

def eliminar_catalogo():
    nombre_catalogo = simpledialog.askstring("Eliminar Catálogo", "Ingresa el nombre del catálogo que deseas eliminar:")
    if nombre_catalogo:
        catalogo = CatalogoPelicula(nombre_catalogo)
        catalogo.eliminar()

def buscar_pelicula_por_categoria():
    nombre_catalogo = simpledialog.askstring("Buscar Película", "Ingresa la categoría de la película:")
    if not nombre_catalogo:
        return
    pelicula_buscada = simpledialog.askstring("Buscar Película", "Ingresa el nombre de la película:")
    if pelicula_buscada:
        catalogo = CatalogoPelicula(nombre_catalogo)
        catalogo.buscar(pelicula_buscada)


def inicializar_catalogos():
    """Crea los archivos de catálogos si no existen con las películas predefinidas."""
    catalogos_base = {
        "Animada": ["Toy Story (1995)", "Coco (2017)", "Frozen (2013)"],
        "Romance": ["The Notebook (2004)", "Titanic (1997)", "La La Land (2016)"],
        "Drama": ["The Godfather (1972)", "The Shawshank Redemption (1994)", "Forrest Gump (1994)"],
        "Ciencia ficcion": ["Star Wars: Episode IV (1977)", "The Matrix (1999)", "Inception (2010)"]
    }

    for categoria, peliculas_lista in catalogos_base.items():
        nombre_archivo = f"{categoria}.txt"
        if not os.path.exists(nombre_archivo):
            with open(nombre_archivo, "w") as archivo:
                for pelicula in peliculas_lista:
                    archivo.write(f"{pelicula}\n")
            print(f"Catálogo '{categoria}' creado con éxito.")

def crear_fondo_personalizado(canvas):
    """Limpia y redibuja un Canvas con un fondo de color, nubes y flores, adaptándose al tamaño."""
    canvas.delete("all")
    ancho = canvas.winfo_width()
    alto = canvas.winfo_height()
    canvas.create_rectangle(0, 0, ancho, alto, fill="#FADADD")

    def dibujar_nube(x, y, color="white"):
        canvas.create_oval(x, y, x + 50, y + 30, fill=color, outline=color)
        canvas.create_oval(x + 20, y - 10, x + 70, y + 20, fill=color, outline=color)
        canvas.create_oval(x + 40, y, x + 90, y + 30, fill=color, outline=color)
        canvas.create_rectangle(x + 20, y + 10, x + 70, y + 30, fill=color, outline=color)
    
    for _ in range(8):
        x = random.randint(0, ancho - 100)
        y = random.randint(0, alto // 3)
        dibujar_nube(x, y)
    
    def dibujar_flor(x, y, color_petalo="#FFB6C1", color_centro="#FFFFE0"):
        canvas.create_oval(x - 10, y - 20, x + 10, y + 0, fill=color_petalo, outline=color_petalo)
        canvas.create_oval(x - 20, y - 10, x + 0, y + 10, fill=color_petalo, outline=color_petalo)
        canvas.create_oval(x + 0, y - 10, x + 20, y + 10, fill=color_petalo, outline=color_petalo)
        canvas.create_oval(x - 10, y + 0, x + 10, y + 20, fill=color_petalo, outline=color_petalo)
        canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color_centro, outline=color_centro)

    for _ in range(10):
        x = random.randint(0, ancho - 20)
        y = random.randint(alto // 2, alto - 20)
        dibujar_flor(x, y)

def mostrar_menu_principal():
    """Muestra la ventana con el menú de opciones."""
    menu_ventana = tk.Tk()
    menu_ventana.title("Menú Principal")
    menu_ventana.geometry("700x650")
    menu_ventana.configure(bg="#FADADD")
    
    menu_canvas = tk.Canvas(menu_ventana, bg="#FADADD", highlightthickness=0)
    menu_canvas.pack(fill="both", expand=True)
    menu_canvas.bind("<Configure>", lambda event: crear_fondo_personalizado(menu_canvas))

    frame_botones = tk.Frame(menu_ventana, bg="#FADADD")
    frame_botones.place(relx=0.5, rely=0.5, anchor="center")

    fuente_menu = font.Font(family="Times New Roman", size=24, slant="italic")
    color_celeste_oscuro = "#4682B4"
    
    label_menu = tk.Label(frame_botones, text="--- MENÚ ---", font=fuente_menu, bg="#FADADD", fg=color_celeste_oscuro)
    label_menu.pack(pady=5)
    
    estilo_boton_menu = ttk.Style()
    estilo_boton_menu.configure("TButton", background="white", foreground=color_celeste_oscuro, font=fuente_menu, padding=10)

    boton_agregar = ttk.Button(frame_botones, text="1. Agregar Película", style="TButton", command=agregar_pelicula)
    boton_agregar.pack(pady=5)
    
    boton_listar = ttk.Button(frame_botones, text="2. Listar Películas", style="TButton", command=listar_peliculas)
    boton_listar.pack(pady=5)
    
    boton_buscar = ttk.Button(frame_botones, text="3. Buscar en Categoría", style="TButton", command=buscar_pelicula_por_categoria)
    boton_buscar.pack(pady=5)

    boton_eliminar = ttk.Button(frame_botones, text="4. Eliminar Catálogo", style="TButton", command=eliminar_catalogo)
    boton_eliminar.pack(pady=5)
    
    boton_salir = ttk.Button(frame_botones, text="5. Salir", style="TButton", command=menu_ventana.quit)
    boton_salir.pack(pady=5)
    
    menu_ventana.mainloop()

def mostrar_ventana_bienvenida():
    ventana = tk.Tk()
    ventana.title("Repositorio de Películas")
    ventana.geometry("700x650")
    ventana.configure(bg="#FADADD")

    fuente_cursiva = font.Font(family="Times New Roman", size=24, slant="italic")
    color_celeste_oscuro = "#4682B4"
    
    mensaje = tk.Label(
        ventana,
        text="Bienvenidos al Repositorio de Stefi❤️, aca encontraras las peliculas que quieras💐!",
        bg="#FADADD",
        fg=color_celeste_oscuro,
        font=fuente_cursiva,
        wraplength=500
    )
    mensaje.pack(pady=80)

    def on_continuar_click():
        ventana.destroy()
        mostrar_menu_principal()
    
    estilo_boton = ttk.Style()
    estilo_boton.configure("TButton", 
                          background="white", 
                          foreground=color_celeste_oscuro, 
                          font=fuente_cursiva,
                          padding=10)

    boton_continuar = ttk.Button(
        ventana,
        text="Continuar",
        style="TButton",
        command=on_continuar_click
    )
    boton_continuar.pack(pady=20)
    
    ventana.mainloop()

if __name__ == "__main__":
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("Lavander Haze.mp3") 
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"No se pudo cargar o reproducir la música: {e}")

    inicializar_catalogos()
    mostrar_ventana_bienvenida()