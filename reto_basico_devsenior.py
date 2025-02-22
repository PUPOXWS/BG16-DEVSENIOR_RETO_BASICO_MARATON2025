import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

class CarritoGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Carrito de Compras")
        self.master.geometry("800x500")  
        
        self.carrito = []
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botones del menú
        ttk.Button(main_frame, text="Agregar Producto", command=self.agregar_producto).grid(row=0, column=0, pady=5, padx=5, sticky=tk.W+tk.E)
        ttk.Button(main_frame, text="Ver Carrito", command=self.ver_carrito).grid(row=1, column=0, pady=5, padx=5, sticky=tk.W+tk.E)
        ttk.Button(main_frame, text="Eliminar Producto", command=self.eliminar_producto).grid(row=2, column=0, pady=5, padx=5, sticky=tk.W+tk.E)
        ttk.Button(main_frame, text="Finalizar Compra", command=self.finalizar_compra).grid(row=3, column=0, pady=5, padx=5, sticky=tk.W+tk.E)
        ttk.Button(main_frame, text="Salir", command=self.master.quit).grid(row=4, column=0, pady=5, padx=5, sticky=tk.W+tk.E)
        
        # Lista de productos
        self.tree = ttk.Treeview(main_frame, columns=("Nombre", "Cantidad", "Precio", "Subtotal", "Descuento", "Total"), show="headings")
        self.tree.grid(row=0, column=1, rowspan=5, padx=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar encabezados
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=2, rowspan=5, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Configurar expansión
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        
    def agregar_producto(self):
        # Crear una ventana de diálogo personalizada
        dialog = tk.Toplevel(self.master)
        dialog.title("Agregar Producto")
        dialog.geometry("300x200")
        dialog.transient(self.master)  
        dialog.grab_set()  
        
        # Centrar la ventana de diálogo
        self.center_window(dialog)
        
        # Variables para almacenar los valores ingresados
        nombre_var = tk.StringVar()
        cantidad_var = tk.IntVar()
        precio_var = tk.DoubleVar()
        
        # Crear y colocar los widgets en la ventana de diálogo
        ttk.Label(dialog, text="Nombre del producto:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(dialog, textvariable=nombre_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Cantidad:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(dialog, textvariable=cantidad_var).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Precio unitario:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(dialog, textvariable=precio_var).grid(row=2, column=1, padx=5, pady=5)
        
        def submit():
            nombre = nombre_var.get()
            try:
                cantidad = cantidad_var.get()
                precio = precio_var.get()
                if cantidad <= 0 or precio <= 0:
                    raise ValueError
            except tk.TclError:
                messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos para cantidad y precio.")
                return
            except ValueError:
                messagebox.showerror("Error", "La cantidad y el precio deben ser valores positivos.")
                return
            
            if not nombre:
                messagebox.showerror("Error", "Por favor, ingrese un nombre para el producto.")
                return
            
            self.agregar_producto_al_carrito(nombre, cantidad, precio)
            dialog.destroy()
        
        ttk.Button(dialog, text="Agregar", command=submit).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Esperar hasta que se cierre la ventana de diálogo
        self.master.wait_window(dialog)
    
    def agregar_producto_al_carrito(self, nombre, cantidad, precio):
        subtotal = cantidad * precio
        descuento = 0
        
        # Aplicar descuento si la cantidad es mayor a 5
        if cantidad > 5:
            descuento = subtotal * 0.1  # 10% de descuento
        
        total = subtotal - descuento
        
        producto = {
            "nombre": nombre,
            "cantidad": cantidad,
            "precio": precio,
            "subtotal": subtotal,
            "descuento": descuento,
            "total": total
        }
        
        self.carrito.append(producto)
        self.actualizar_lista()
        messagebox.showinfo("Éxito", "Producto agregado al carrito.")
    
    def ver_carrito(self):
        if not self.carrito:
            messagebox.showinfo("Carrito", "El carrito está vacío.")
            return
        
        # Crear una nueva ventana para ver el carrito
        carrito_window = tk.Toplevel(self.master)
        carrito_window.title("Ver Carrito")
        carrito_window.geometry("700x400")
        carrito_window.transient(self.master)
        self.center_window(carrito_window)
        
        # Crear un Treeview para mostrar los productos
        tree = ttk.Treeview(carrito_window, columns=("Nombre", "Cantidad", "Precio", "Subtotal", "Descuento", "Total"), show="headings")
        tree.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Configurar encabezados
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        # Insertar productos en el Treeview
        for producto in self.carrito:
            tree.insert("", "end", values=(
                producto['nombre'],
                producto['cantidad'],
                f"${producto['precio']:.2f}",
                f"${producto['subtotal']:.2f}",
                f"${producto['descuento']:.2f}",
                f"${producto['total']:.2f}"
            ))
        
        # Frame para botones y total
        bottom_frame = ttk.Frame(carrito_window)
        bottom_frame.pack(fill='x', padx=10, pady=10)
        
        # Botón para agregar más unidades
        ttk.Button(bottom_frame, text="Agregar Unidades", command=lambda: self.agregar_unidades(tree, carrito_window)).pack(side='left', padx=5)
        ttk.Button(bottom_frame, text="Disminuir Unidades", command=lambda: self.disminuir_unidades(tree, carrito_window)).pack(side='left', padx=5)
        
        # Mostrar total
        total_general = sum(producto['total'] for producto in self.carrito)
        ttk.Label(bottom_frame, text=f"Total a pagar: ${total_general:.2f}", font=('Arial', 12, 'bold')).pack(side='right', padx=5)
    
    def agregar_unidades(self, tree, window):
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Selección", "Por favor, seleccione un producto para agregar unidades.")
            return
        
        indice = tree.index(seleccion[0])
        producto = self.carrito[indice]
        
        # Pedir la cantidad a agregar
        cantidad = simpledialog.askinteger("Agregar Unidades", f"Cantidad actual: {producto['cantidad']}\nCantidad a agregar:", minvalue=1, parent=window)
        if cantidad is None:
            return
        
        # Actualizar la cantidad y recalcular
        producto['cantidad'] += cantidad
        producto['subtotal'] = producto['cantidad'] * producto['precio']
        
        # Recalcular descuento
        if producto['cantidad'] > 5:
            producto['descuento'] = producto['subtotal'] * 0.1
        else:
            producto['descuento'] = 0
        
        producto['total'] = producto['subtotal'] - producto['descuento']
        
        # Actualizar el Treeview
        tree.item(seleccion, values=(
            producto['nombre'],
            producto['cantidad'],
            f"${producto['precio']:.2f}",
            f"${producto['subtotal']:.2f}",
            f"${producto['descuento']:.2f}",
            f"${producto['total']:.2f}"
        ))
        
        # Actualizar el total general
        total_general = sum(p['total'] for p in self.carrito)
        for widget in window.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Label) and child.cget("text").startswith("Total a pagar:"):
                        child.config(text=f"Total a pagar: ${total_general:.2f}")
        
        # Actualizar la lista principal
        self.actualizar_lista()
        
        messagebox.showinfo("Éxito", f"Se han agregado {cantidad} unidades al producto {producto['nombre']}.")
    
    def disminuir_unidades(self, tree, window):
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Selección", "Por favor, seleccione un producto para disminuir unidades.")
            return
        
        indice = tree.index(seleccion[0])
        producto = self.carrito[indice]
        
        # Pedir la cantidad a disminuir
        cantidad = simpledialog.askinteger("Disminuir Unidades", f"Cantidad actual: {producto['cantidad']}\nCantidad a disminuir:", minvalue=1, maxvalue=producto['cantidad']-1, parent=window)
        if cantidad is None:
            return
        
        # Actualizar la cantidad y recalcular
        producto['cantidad'] -= cantidad
        producto['subtotal'] = producto['cantidad'] * producto['precio']
        
        # Recalcular descuento
        if producto['cantidad'] > 5:
            producto['descuento'] = producto['subtotal'] * 0.1
        else:
            producto['descuento'] = 0
        
        producto['total'] = producto['subtotal'] - producto['descuento']
        
        # Actualizar el Treeview
        tree.item(seleccion, values=(
            producto['nombre'],
            producto['cantidad'],
            f"${producto['precio']:.2f}",
            f"${producto['subtotal']:.2f}",
            f"${producto['descuento']:.2f}",
            f"${producto['total']:.2f}"
        ))
        
        # Actualizar el total general
        total_general = sum(p['total'] for p in self.carrito)
        for widget in window.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Label) and child.cget("text").startswith("Total a pagar:"):
                        child.config(text=f"Total a pagar: ${total_general:.2f}")
        
        # Actualizar la lista principal
        self.actualizar_lista()
        
        messagebox.showinfo("Éxito", f"Se han disminuido {cantidad} unidades del producto {producto['nombre']}.")
    
    def eliminar_producto(self):
        if not self.carrito:
            messagebox.showinfo("Carrito", "El carrito está vacío.")
            return
        
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Eliminar Producto", "Por favor, seleccione un producto para eliminar.")
            return
        
        indice = self.tree.index(seleccion[0])
        producto_eliminado = self.carrito.pop(indice)
        self.actualizar_lista()
        messagebox.showinfo("Éxito", f"Se ha eliminado {producto_eliminado['nombre']} del carrito.")
    
    def finalizar_compra(self):
        if not self.carrito:
            messagebox.showinfo("Carrito", "El carrito está vacío. No se puede finalizar la compra.")
            return
        
        # Crear una ventana nueva para el ticket
        ticket_window = tk.Toplevel(self.master)
        ticket_window.title("Ticket de Compra")
        ticket_window.geometry("600x600")
        ticket_window.transient(self.master)  # Hace que la ventana sea hija de la principal
        
        # Centrar la ventana del ticket
        self.center_window(ticket_window)
        
        # Crear un widget de texto para el ticket
        ticket_text = tk.Text(ticket_window, wrap=tk.WORD, font=("Courier", 10))
        ticket_text.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Generar el contenido del ticket
        ticket = "=" * 60 + "\n"
        ticket += "{:^60}\n".format("TICKET DE COMPRA")
        ticket += "=" * 60 + "\n"
        ticket += "Fecha: {}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        ticket += "-" * 60 + "\n"
        ticket += "{:<30} {:>7} {:>10} {:>10}\n".format("Producto", "Cant.", "Precio", "Total")
        ticket += "-" * 60 + "\n"
        
        total_general = 0
        for producto in self.carrito:
            ticket += "{:<30} {:>7} ${:>9.2f} ${:>9.2f}\n".format(
                producto['nombre'][:30],
                producto['cantidad'],
                producto['precio'],
                producto['total']
            )
            if producto['descuento'] > 0:
                ticket += "{:<30} {:>7} ${:>9.2f}\n".format(
                    "  Descuento", "", producto['descuento']
                )
            total_general += producto['total']
        
        ticket += "=" * 60 + "\n"
        ticket += "{:<40} ${:>17.2f}\n".format("TOTAL A PAGAR:", total_general)
        ticket += "=" * 60 + "\n\n"
        ticket += "{:^60}\n".format("¡Gracias por su compra!")
        ticket += "{:^60}\n".format("Vuelva pronto")
        
        # Insertar el ticket en el widget de texto
        ticket_text.insert(tk.END, ticket)
        ticket_text.config(state=tk.DISABLED)  # Hacer el texto de solo lectura
        
        # Botón para cerrar la ventana del ticket
        ttk.Button(ticket_window, text="Cerrar", command=ticket_window.destroy).pack(pady=10)
        
        # Limpiar el carrito y actualizar la lista
        self.carrito.clear()
        self.actualizar_lista()
        
        messagebox.showinfo("Compra Finalizada", "La compra ha sido finalizada. Gracias por su preferencia.")
        
    def actualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for producto in self.carrito:
            self.tree.insert("", "end", values=(
                producto['nombre'],
                producto['cantidad'],
                f"${producto['precio']:.2f}",
                f"${producto['subtotal']:.2f}",
                f"${producto['descuento']:.2f}",
                f"${producto['total']:.2f}"
            ))
    
    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

if __name__ == "__main__":
    root = tk.Tk()
    app = CarritoGUI(root)
    root.mainloop()

