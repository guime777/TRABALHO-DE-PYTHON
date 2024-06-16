import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Conectar ao banco de dados MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="dengue"
)
cursor = conn.cursor()

conn.commit()

class Aplicacao:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Diagnóstico de Dengue")
        self.root.geometry('600x400')

        # Labels e Entradas
        self.lbl_id = tk.Label(root, text="ID (para atualizar/excluir):")
        self.lbl_id.grid(row=0, column=0, padx=10, pady=10)
        self.txt_id = tk.Entry(root)
        self.txt_id.grid(row=0, column=1, padx=10, pady=10)

        self.lbl_nome = tk.Label(root, text="Nome:")
        self.lbl_nome.grid(row=1, column=0, padx=10, pady=10)
        self.txt_nome = tk.Entry(root)
        self.txt_nome.grid(row=1, column=1, padx=10, pady=10)

        self.lbl_idade = tk.Label(root, text="Idade:")
        self.lbl_idade.grid(row=2, column=0, padx=10, pady=10)
        self.txt_idade = tk.Entry(root)
        self.txt_idade.grid(row=2, column=1, padx=10, pady=10)

        self.lbl_regiao = tk.Label(root, text="Região:")
        self.lbl_regiao.grid(row=3, column=0, padx=10, pady=10)
        self.txt_regiao = tk.Entry(root)
        self.txt_regiao.grid(row=3, column=1, padx=10, pady=10)

        self.lbl_sintomas = tk.Label(root, text="Sintomas:")
        self.lbl_sintomas.grid(row=4, column=0, padx=10, pady=10)
        self.txt_sintomas = tk.Entry(root)
        self.txt_sintomas.grid(row=4, column=1, padx=10, pady=10)

        # Botões
        self.btn_adicionar = tk.Button(root, text="Adicionar Paciente", command=self.adicionar_paciente)
        self.btn_adicionar.grid(row=5, column=0, padx=10, pady=10)

        self.btn_visualizar = tk.Button(root, text="Visualizar Pacientes", command=self.visualizar_pacientes)
        self.btn_visualizar.grid(row=5, column=1, padx=10, pady=10)

        self.btn_atualizar = tk.Button(root, text="Atualizar Paciente", command=self.atualizar_paciente)
        self.btn_atualizar.grid(row=6, column=0, padx=10, pady=10)

        self.btn_excluir = tk.Button(root, text="Excluir Paciente", command=self.excluir_paciente)
        self.btn_excluir.grid(row=6, column=1, padx=10, pady=10)

        self.btn_voltar = tk.Button(root, text="Voltar", command=self.voltar_para_principal)
        self.btn_voltar.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        self.btn_voltar.grid_remove()  # Inicia oculto até necessário

        self.lbl_resultado = tk.Label(root, text="")
        self.lbl_resultado.grid(row=8, column=0, columnspan=2)

    def adicionar_paciente(self):
        nome = self.txt_nome.get()
        idade = self.txt_idade.get()
        regiao = self.txt_regiao.get()
        sintomas = self.txt_sintomas.get()

        if not self.validar_idade(idade):
            messagebox.showerror("Erro", "Idade deve ser um número inteiro.")
            return

        # Diagnóstico Simples baseado nos sintomas
        diagnostico = self.diagnosticar_dengue(sintomas)

        cursor.execute("INSERT INTO paciente (nome, idade, regiao, sintomas, diagnostico) VALUES (%s, %s, %s, %s, %s)",
                       (nome, int(idade), regiao, sintomas, diagnostico))
        conn.commit()
        messagebox.showinfo("Sucesso", "Paciente adicionado com sucesso!")
        self.limpar_campos()

    def diagnosticar_dengue(self, sintomas):
        sintomas_lower = sintomas.lower()
        sintomas_list = sintomas_lower.split(", ")
        sintomas_dengue = {"febre", "dor de cabeça", "dores musculares", "fadiga", "manchas vermelhas", "náuseas", "vômitos"}

        if any(sintoma in sintomas_dengue for sintoma in sintomas_list):
            return "Dengue"
        else:
            return "Sem Dengue"

    def visualizar_pacientes(self):
        cursor.execute("SELECT * FROM paciente")
        registros = cursor.fetchall()
        resultado = ""
        for registro in registros:
            resultado += f"ID: {registro[0]}, Nome: {registro[1]}, Idade: {registro[2]}, Região: {registro[3]}, Sintomas: {registro[4]}, Diagnóstico: {registro[5]}\n"
        self.lbl_resultado.config(text=resultado)
        self.btn_voltar.grid()  # Mostra o botão "Voltar"

    def atualizar_paciente(self):
        id_paciente = self.txt_id.get()
        nome = self.txt_nome.get()
        regiao = self.txt_regiao.get()
        sintomas = self.txt_sintomas.get()

        if not self.validar_id(id_paciente):
            messagebox.showerror("Erro", "ID deve ser um número inteiro válido.")
            return

        if nome.strip() == "" and regiao.strip() == "" and sintomas.strip() == "":
            messagebox.showerror("Erro", "Pelo menos um campo (Nome, Região ou Sintomas) deve ser preenchido.")
            return

        # Atualiza apenas os campos não vazios
        update_query = "UPDATE paciente SET "
        update_fields = []
        if nome.strip() != "":
            update_fields.append(f"nome = '{nome}'")
        if regiao.strip() != "":
            update_fields.append(f"regiao = '{regiao}'")
        if sintomas.strip() != "":
            update_fields.append(f"sintomas = '{sintomas}'")

        update_query += ", ".join(update_fields)
        update_query += f" WHERE id = {int(id_paciente)}"

        cursor.execute(update_query)
        conn.commit()

        if cursor.rowcount == 0:
            messagebox.showinfo("Nenhum campo foi alterado", "Nenhum campo foi alterado.")
        else:
            messagebox.showinfo("Sucesso", "Paciente atualizado com sucesso!")

        self.limpar_campos()

    def excluir_paciente(self):
        id_paciente = self.txt_id.get()

        if not self.validar_id(id_paciente):
            messagebox.showerror("Erro", "ID deve ser um número inteiro válido.")
            return

        cursor.execute("DELETE FROM paciente WHERE id=%s", (int(id_paciente),))
        conn.commit()
        messagebox.showinfo("Sucesso", "Paciente excluído com sucesso!")
        self.limpar_campos()

    def limpar_campos(self):
        self.txt_id.delete(0, tk.END)
        self.txt_nome.delete(0, tk.END)
        self.txt_idade.delete(0, tk.END)
        self.txt_regiao.delete(0, tk.END)
        self.txt_sintomas.delete(0, tk.END)
        self.btn_voltar.grid_remove()  # Esconde o botão "Voltar"

    def voltar_para_principal(self):
        self.lbl_resultado.config(text="")
        self.btn_voltar.grid_remove()  # Esconde o botão "Voltar"

    def validar_id(self, id_value):
        try:
            int(id_value)
            return True
        except ValueError:
            return False

    def validar_idade(self, idade):
        try:
            int(idade)
            return True
        except ValueError:
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacao(root)
    root.mainloop()
    conn.close()
